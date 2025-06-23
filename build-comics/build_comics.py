import concurrent.futures
import logging
import os
import shutil
import sys
import traceback
from datetime import datetime
from typing import List, Union, Tuple

from PIL import Image

from additional_file_writing import (
    write_readme_file,
    write_metadata_file,
    write_json_metadata,
    write_srce_dest_map,
    write_dest_panels_bboxes,
)
from barks_fantagraphics.barks_titles import get_safe_title
from barks_fantagraphics.comic_book import (
    ComicBook,
    ComicDimensions,
    RequiredDimensions,
)
from barks_fantagraphics.comics_consts import (
    PageType,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
    DEST_TARGET_ASPECT_RATIO,
)
from barks_fantagraphics.comics_utils import (
    get_clean_path,
    get_abbrev_path,
    delete_all_files_in_directory,
)
from barks_fantagraphics.page_classes import CleanPage, SrceAndDestPages
from barks_fantagraphics.pages import (
    get_max_timestamp,
    get_page_num_str,
    get_sorted_srce_and_dest_pages_with_dimensions,
)
from barks_fantagraphics.pil_image_utils import METADATA_PROPERTY_GROUP
from build_comic_images import ComicBookImageBuilder
from consts import (
    MIN_HD_SRCE_HEIGHT,
    DEST_JPG_COMPRESS_LEVEL,
    DEST_JPG_QUALITY,
)
from image_io import open_image_for_reading
from zipping import zip_comic_book, create_symlinks_to_comic_zip

_process_page_error = False


class ComicBookBuilder:
    def __init__(self, comic: ComicBook):
        self.__comic = comic
        self.__image_builder = ComicBookImageBuilder(comic)

        self.__srce_dim: Union[ComicDimensions, None] = None
        self.__required_dim: Union[RequiredDimensions, None] = None

        self.__srce_and_dest_pages: Union[SrceAndDestPages, None] = None
        self.__max_dest_page_timestamp = None

    def get_srce_dim(self) -> ComicDimensions:
        return self.__srce_dim

    def get_required_dim(self) -> RequiredDimensions:
        return self.__required_dim

    def get_srce_and_dest_pages(self) -> SrceAndDestPages:
        return self.__srce_and_dest_pages

    def get_max_dest_page_timestamp(self) -> float:
        return self.__max_dest_page_timestamp

    def build(self) -> None:
        self._init_pages()

        self._create_comic_book()

        self._log_comic_book_params()

        self._zip_and_symlink_comic_book()

    def _init_pages(self):
        self.__srce_and_dest_pages, self.__srce_dim, self.__required_dim = (
            self._get_srce_and_dest_pages_and_dimensions(self.__comic)
        )
        self.__image_builder.set_required_dim(self.__required_dim)
        self.__max_dest_page_timestamp = get_max_timestamp(self.__srce_and_dest_pages.dest_pages)

    @staticmethod
    def _get_srce_and_dest_pages_and_dimensions(
        comic: ComicBook,
    ) -> Tuple[SrceAndDestPages, ComicDimensions, RequiredDimensions]:
        srce_and_dest_pages, srce_dim, required_dim = (
            get_sorted_srce_and_dest_pages_with_dimensions(comic, get_full_paths=True)
        )

        assert srce_dim.max_panels_bbox_width >= srce_dim.min_panels_bbox_width > 0
        assert srce_dim.max_panels_bbox_height >= srce_dim.min_panels_bbox_height > 0
        assert srce_dim.max_panels_bbox_width >= srce_dim.av_panels_bbox_width > 0
        assert srce_dim.max_panels_bbox_height >= srce_dim.av_panels_bbox_height > 0
        assert required_dim.panels_bbox_width == int(
            round((DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN)))
        )

        logging.debug(f"Srce average panels bbox width: {srce_dim.av_panels_bbox_width}.")
        logging.debug(f"Srce average panels bbox height: {srce_dim.av_panels_bbox_height}.")
        logging.debug(f"Required panels bbox width: {required_dim.panels_bbox_width}.")
        logging.debug(f"Required panels bbox height: {required_dim.panels_bbox_height}.")
        logging.debug(f"Required page num y bottom: {required_dim.page_num_y_bottom}.")
        logging.debug("")

        return srce_and_dest_pages, srce_dim, required_dim

    def _create_comic_book(self) -> None:
        self._create_dest_dirs()
        self._process_pages()
        self._process_additional_files()

    def _process_pages(self):
        delete_all_files_in_directory(self.__comic.get_dest_dir())
        delete_all_files_in_directory(self.__comic.get_dest_image_dir())

        global _process_page_error
        _process_page_error = False

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for srce_page, dest_page in zip(
                self.__srce_and_dest_pages.srce_pages, self.__srce_and_dest_pages.dest_pages
            ):
                executor.submit(self._process_page, srce_page, dest_page)

        # for srce_page, dest_page in zip(
        #     srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages
        # ):
        #     self._process_page(srce_page, dest_page)

        if _process_page_error:
            raise Exception("There were errors while processing pages.")

    def _process_page(
        self,
        srce_page: CleanPage,
        dest_page: CleanPage,
    ) -> None:
        # noinspection PyBroadException
        try:
            srce_page_image = open_image_for_reading(srce_page.page_filename)
            if srce_page.page_type == PageType.BODY and srce_page_image.height < MIN_HD_SRCE_HEIGHT:
                raise Exception(
                    f"Srce image error: min required height {MIN_HD_SRCE_HEIGHT}."
                    f' Poor srce file resolution for "{srce_page.page_filename}":'
                    f" {srce_page_image.width} x {srce_page_image.height}."
                )

            logging.info(
                f'Convert "{get_abbrev_path(srce_page.page_filename)}"'
                f" (page-type {srce_page.page_type.name})"
                f' to "{get_abbrev_path(dest_page.page_filename)}"'
                f" (page {get_page_num_str(dest_page):>2}."
            )

            logging.info(
                f'Creating dest image "{get_abbrev_path(dest_page.page_filename)}"'
                f' from srce file "{get_abbrev_path(srce_page.page_filename)}".'
            )
            dest_page_image = self.__image_builder.get_dest_page_image(
                srce_page_image, srce_page, dest_page
            )

            self._save_dest_image(dest_page, dest_page_image, srce_page)
            logging.info(f'Saved changes to image "{get_abbrev_path(dest_page.page_filename)}".')

            logging.info("")
        except Exception:
            _, _, tb = sys.exc_info()
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            err_msg = f'Error in process page at "{filename}:{line}" for statement "{text}".'
            logging.error(err_msg)
            global _process_page_error
            _process_page_error = True

    def _save_dest_image(
        self, dest_page: CleanPage, dest_page_image: Image, srce_page: CleanPage
    ) -> None:
        dest_page_image.save(
            dest_page.page_filename,
            optimize=True,
            compress_level=DEST_JPG_COMPRESS_LEVEL,
            quality=DEST_JPG_QUALITY,
            comment="\n".join(self._get_dest_jpg_comments(srce_page, dest_page)),
        )

    @staticmethod
    def _get_dest_jpg_comments(srce_page: CleanPage, dest_page: CleanPage) -> List[str]:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        prefix = METADATA_PROPERTY_GROUP
        indent = "      "
        comments = [
            indent,
            f'{indent}{prefix}:Srce file: "{get_clean_path(srce_page.page_filename)}"',
            f'{indent}{prefix}:Dest file: "{get_clean_path(dest_page.page_filename)}"',
            f"{indent}{prefix}:Dest created: {now_str}",
            f"{indent}{prefix}:Srce page num: {srce_page.page_num}",
            f"{indent}{prefix}:Srce page type: {srce_page.page_type.name}",
            f"{indent}{prefix}:Srce panels bbox:"
            f" {dest_page.panels_bbox.x_min}, {dest_page.panels_bbox.y_min},"
            f" {dest_page.panels_bbox.x_max}, {dest_page.panels_bbox.y_max}",
            f"{indent}{prefix}:Dest page num: {dest_page.page_num}",
        ]

        return comments

    def _process_additional_files(self) -> None:
        shutil.copy2(self.__comic.ini_file, self.__comic.get_dest_dir())

        write_readme_file(self.__comic)
        write_metadata_file(self.__comic, self.__srce_and_dest_pages.dest_pages)
        write_json_metadata(
            self.__comic,
            self.__srce_dim,
            self.__required_dim,
            self.__srce_and_dest_pages.dest_pages,
        )
        write_srce_dest_map(
            self.__comic, self.__srce_dim, self.__required_dim, self.__srce_and_dest_pages
        )
        write_dest_panels_bboxes(self.__comic, self.__srce_and_dest_pages.dest_pages)

    def _create_dest_dirs(self) -> None:
        if not os.path.isdir(self.__comic.get_dest_image_dir()):
            os.makedirs(self.__comic.get_dest_image_dir())

        if not os.path.isdir(self.__comic.get_dest_image_dir()):
            raise Exception(f'Could not make directory "{self.__comic.get_dest_image_dir()}".')

    def _zip_and_symlink_comic_book(self):
        zip_comic_book(self.__comic)
        create_symlinks_to_comic_zip(self.__comic)

    # noinspection LongLine
    def _log_comic_book_params(self) -> None:
        logging.info("")

        calc_panels_bbox_height = int(
            round(
                (self.__srce_dim.av_panels_bbox_height * self.__required_dim.panels_bbox_width)
                / self.__srce_dim.av_panels_bbox_width
            )
        )

        # fmt: off
        logging.info(f'Comic book series:    "{self.__comic.series_name}".')
        logging.info(f'Comic book title:     "{get_safe_title(self.__comic.get_comic_title())}".')
        logging.info(f'Comic issue title:    "{self.__comic.get_comic_issue_title()}".')
        logging.info(f"Number in series:     {self.__comic.number_in_series}.")
        logging.info(f"Chronological number  {self.__comic.chronological_number}.")
        logging.info(f"Dest x margin:        {DEST_TARGET_X_MARGIN}.")
        logging.info(f"Dest width:           {DEST_TARGET_WIDTH}.")
        logging.info(f"Dest height:          {DEST_TARGET_HEIGHT}.")
        logging.info(f"Dest aspect ratio:    {DEST_TARGET_ASPECT_RATIO :.2f}.")
        logging.info(f"Dest jpeg quality:    {DEST_JPG_QUALITY}.")
        logging.info(f"Dest compress level:  {DEST_JPG_COMPRESS_LEVEL}.")
        logging.info(f"Srce min bbox wid:    {self.__srce_dim.min_panels_bbox_width}.")
        logging.info(f"Srce max bbox wid:    {self.__srce_dim.max_panels_bbox_width}.")
        logging.info(f"Srce min bbox hgt:    {self.__srce_dim.min_panels_bbox_height}.")
        logging.info(f"Srce max bbox hgt:    {self.__srce_dim.max_panels_bbox_height}.")
        logging.info(f"Srce av bbox wid:     {self.__srce_dim.av_panels_bbox_width}.")
        logging.info(f"Srce av bbox hgt:     {self.__srce_dim.av_panels_bbox_height}.")
        logging.info(f"Req panels bbox wid:  {self.__required_dim.panels_bbox_width}.")
        logging.info(f"Req panels bbox hgt:  {self.__required_dim.panels_bbox_height}.")
        logging.info(f"Calc panels bbox ht:  {calc_panels_bbox_height}.")
        logging.info(f"Page num y bottom:    {self.__required_dim.page_num_y_bottom}.")
        logging.info(f'Ini file:             "{get_clean_path(self.__comic.ini_file)}".')
        logging.info(f'Srce dir:             "{get_abbrev_path(self.__comic.dirs.srce_dir)}".')
        logging.info(f'Srce upscayled dir:   "{get_abbrev_path(self.__comic.dirs.srce_upscayled_dir)}".')
        logging.info(f'Srce restored dir:    "{get_abbrev_path(self.__comic.dirs.srce_restored_dir)}".')
        logging.info(f'Srce fixes dir:       "{get_abbrev_path(self.__comic.dirs.srce_fixes_dir)}".')
        logging.info(f'Srce upscayled fixes: "{get_abbrev_path(self.__comic.dirs.srce_upscayled_fixes_dir)}".')
        logging.info(f'Srce segments dir:    "{get_abbrev_path(self.__comic.dirs.panel_segments_dir)}".')
        logging.info(f'Dest dir:             "{get_abbrev_path(self.__comic.get_dest_dir())}".')
        logging.info(f'Dest comic zip:       "{get_abbrev_path(self.__comic.get_dest_comic_zip())}".')
        logging.info(f'Dest series symlink:  "{get_abbrev_path(self.__comic.get_dest_series_comic_zip_symlink())}".')
        logging.info(f'Dest year symlink:    "{get_abbrev_path(self.__comic.get_dest_year_comic_zip_symlink())}".')
        logging.info("")
        # fmt: on
