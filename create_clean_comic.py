import argparse
import configparser
import datetime
import inspect
import json
import logging
import os
import shlex
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import numpy as np
from PIL import Image, ImageFont, ImageDraw

from comics_info import (
    ComicBookInfo,
    ComicBookInfoDict,
    get_all_comic_book_info,
    MONTH_AS_LONG_STR,
    SOURCE_COMICS,
    CS,
    ISSUE_NAME_AS_TITLE,
    SHORT_ISSUE_NAME,
)
from consts import (
    THIS_DIR,
    PUBLICATION_INFO_DIRNAME,
    BARKS,
    BARKS_ROOT_DIR,
    THE_COMICS_DIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    CONFIGS_SUBDIR,
    IMAGES_SUBDIR,
    INSET_FILE_EXT,
    DEST_FILE_EXT,
    SRCE_FILE_EXT,
    DEST_JPG_QUALITY,
    DEST_JPG_COMPRESS_LEVEL,
    EMPTY_FILENAME,
    TITLE_EMPTY_FILENAME,
    DRY_RUN_STR,
    BIG_NUM,
    ROMAN_NUMERALS,
    DEST_SRCE_MAP_FILENAME,
    DEST_PANELS_BBOXES_FILENAME,
    PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN,
    PageType,
    FRONT_MATTER_PAGES,
    PAGES_WITHOUT_PANELS,
    PAINTING_PAGES,
    SPLASH_PAGES,
    CACHEABLE_PAGES,
    MEDIAN_FILTERABLE_PAGES,
    MIN_HD_SRCE_HEIGHT,
)
from panel_bounding_boxes import BoundingBox, BoundingBoxProcessor
from remove_alias_artifacts import (
    get_median_filter,
    get_thickened_black_lines,
    SMALL_FLOAT,
)

THIS_SCRIPT_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

README_FILENAME = "readme.txt"
DOUBLE_PAGES_SECTION = "double_pages"
PAGE_NUMBERS_SECTION = "page_numbers"
METADATA_FILENAME = "metadata.txt"
JSON_METADATA_FILENAME = "comic-metadata.json"
STORIES_INFO_FILENAME = "the-stories.csv"

DEST_TARGET_WIDTH = 2120
DEST_TARGET_HEIGHT = 3200
DEST_TARGET_X_MARGIN = 100
DEST_TARGET_ASPECT_RATIO = float(DEST_TARGET_HEIGHT) / float(DEST_TARGET_WIDTH)

FONT_DIR = os.path.join(str(Path.home()), "Prj", "fonts")
INTRO_TITLE_DEFAULT_FONT_FILE = os.path.join(FONT_DIR, "Carl Barks Script.ttf")
INTRO_TEXT_FONT_FILE = "Verdana Italic.ttf"
PAGE_NUM_FONT_FILE = "verdana.ttf"
PAGE_NUM_COLOR = (10, 10, 10)

INTRO_TOP = 350
INTRO_BOTTOM_MARGIN = INTRO_TOP
INTRO_TITLE_SPACING = 50
INTRO_TITLE_DEFAULT_FONT_SIZE = 155
INTRO_TITLE_COLOR = (0, 0, 0)
INTRO_TITLE_AUTHOR_GAP = 130
INTRO_TITLE_AUTHOR_BY_GAP = INTRO_TITLE_AUTHOR_GAP
INTRO_AUTHOR_DEFAULT_FONT_SIZE = 90
INTRO_AUTHOR_COLOR = (0, 0, 0)
INTRO_AUTHOR_INSET_GAP = 8
INTRO_MAX_WIDTH_INSET_MARGIN_FRAC = 0.05
INTRO_MAX_HEIGHT_INSET_MARGIN_FRAC = 0.18
INTRO_PUB_TEXT_FONT_SIZE = 35
INTRO_PUB_TEXT_COLOR = (0, 0, 0)
INTRO_PUB_TEXT_SPACING = 20

PAGE_NUM_X_OFFSET_FROM_CENTRE = 150
PAGE_NUM_X_BLANK_PIXEL_OFFSET = 250
PAGE_NUM_HEIGHT = 40
PAGE_NUM_FONT_SIZE = 30

EMPTY_IMAGE_FILEPATH = os.path.join(THIS_SCRIPT_DIR, "empty_page.png")
TITLE_EMPTY_IMAGE_FILEPATH = EMPTY_IMAGE_FILEPATH
EMPTY_IMAGE_FILES = {
    EMPTY_IMAGE_FILEPATH,
    TITLE_EMPTY_IMAGE_FILEPATH,
}

SPLASH_BORDER_COLOR = (128, 0, 0)
SPLASH_BORDER_WIDTH = 10


@dataclass
class Timing:
    start_time: datetime = None
    end_time: datetime = None

    def get_elapsed_time_in_seconds(self) -> int:
        elapsed_time = self.end_time - self.start_time
        elapsed_time = int(round(elapsed_time.total_seconds(), 1))
        return elapsed_time


@dataclass
class OriginalPage:
    filenames: str
    page_type: PageType


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


class CleanPage:
    def __init__(
        self,
        filename: str,
        page_type: PageType,
        page_num: int = -1,
        page_thicken_lines_alpha=0.0,
    ):
        self.filename = filename
        self.page_type = page_type
        self.page_num: int = page_num
        self.page_thicken_lines_alpha = page_thicken_lines_alpha
        self.panels_bbox: BoundingBox = BoundingBox()


@dataclass
class SrceAndDestPages:
    srce_pages: List[CleanPage]
    dest_pages: List[CleanPage]


@dataclass
class ComicBook:
    config_file: str
    title: str
    title_font_file: str
    title_font_size: int
    issue_title: str
    file_title: str
    author_font_size: int
    srce_min_panels_bbox_width: int
    srce_max_panels_bbox_width: int
    srce_min_panels_bbox_height: int
    srce_max_panels_bbox_height: int
    srce_av_panels_bbox_width: int
    srce_av_panels_bbox_height: int
    required_dim: RequiredDimensions
    srce_root_dir: str
    srce_dir: str
    srce_fixes_dir: str
    panel_segments_dir: str
    series_name: str
    number_in_series: int
    chronological_number: int
    intro_inset_file: str
    publication_date: str
    submitted_date: str
    publication_text: str
    comic_book_info: ComicBookInfo
    images_in_order: List[OriginalPage]
    thicken_line_alphas: Dict[int, float]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0

    def get_srce_fixes_root_dir(self) -> str:
        return os.path.dirname(self.srce_fixes_dir)

    def get_srce_image_dir(self) -> str:
        return os.path.join(self.srce_dir, IMAGES_SUBDIR)

    def get_srce_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_fixes_dir, IMAGES_SUBDIR)

    def get_srce_segments_root_dir(self) -> str:
        return os.path.dirname(self.panel_segments_dir)

    def get_dest_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIRS_DIR

    def get_dest_dir(self) -> str:
        return os.path.join(
            self.get_dest_root_dir(),
            self.get_dest_rel_dirname(),
        )

    def get_dest_rel_dirname(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        return f"{self.chronological_number:03d} {file_title}"

    def get_series_comic_title(self) -> str:
        return f"{self.series_name} {self.number_in_series}"

    def get_dest_image_dir(self) -> str:
        return os.path.join(self.get_dest_dir(), IMAGES_SUBDIR)

    def get_dest_zip_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIR

    def get_dest_series_zip_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            self.series_name,
        )

    def get_dest_zip_dir(self) -> str:
        title = f"{self.get_dest_rel_dirname()} [{self.get_comic_issue_title()}]"
        return os.path.join(self.get_dest_zip_root_dir(), title)

    def get_dest_comic_zip(self) -> str:
        return self.get_dest_zip_dir() + ".cbz"

    def get_dest_series_comic_zip_symlink(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        full_title = f"{file_title} [{self.get_comic_issue_title()}]"
        return (
            os.path.join(
                f"{self.get_dest_series_zip_dir()}",
                f"{self.number_in_series:03d} {full_title}",
            )
            + ".cbz"
        )

    def get_comic_title(self) -> str:
        if self.title != "":
            return self.title
        if self.issue_title != "":
            return self.issue_title

        return self.__get_comic_title_from_issue_name()

    def __get_comic_title_from_issue_name(self) -> str:
        issue_name = self.comic_book_info.issue_name
        if issue_name not in ISSUE_NAME_AS_TITLE:
            issue_name += "\n"
        else:
            issue_name = ISSUE_NAME_AS_TITLE[issue_name] + " #"

        return f"{issue_name}{self.comic_book_info.issue_number}"

    def get_comic_issue_title(self) -> str:
        issue_name = SHORT_ISSUE_NAME[self.comic_book_info.issue_name]
        return f"{issue_name} {self.comic_book_info.issue_number}"


def open_image_for_reading(filename: str) -> Image:
    current_log_level = logging.getLogger().level
    try:
        logging.getLogger().setLevel(logging.INFO)
        image = Image.open(filename, "r")

        if filename in EMPTY_IMAGE_FILES:
            image = image.resize(
                size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
                resample=Image.Resampling.NEAREST,
            )
    finally:
        logging.getLogger().setLevel(current_log_level)

    return image


def get_safe_title(title: str) -> str:
    safe_title = title.replace("\n", " ")
    safe_title = safe_title.replace("- ", "-")
    safe_title = safe_title.replace('"', "")
    return safe_title


def get_lookup_title(title: str, file_title: str) -> str:
    if title != "":
        return get_safe_title(title)

    assert file_title != ""
    return file_title


def get_inset_filename(ini_file: str, file_title: str) -> str:
    if file_title:
        return file_title + " Inset" + INSET_FILE_EXT

    ini_filename = os.path.splitext(os.path.basename(ini_file))[0]

    return ini_filename + " Inset" + INSET_FILE_EXT


def zip_comic_book(dry_run: bool, comic: ComicBook):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Zipping directory "{comic.get_dest_dir()}"'
            f' to "{comic.get_dest_comic_zip()}".'
        )
    else:
        logging.info(
            f'Zipping directory "{comic.get_dest_dir()}" to "{comic.get_dest_comic_zip()}".'
        )

        os.makedirs(comic.get_dest_zip_root_dir(), exist_ok=True)
        temp_zip_file = comic.get_dest_dir() + ".zip"

        shutil.make_archive(comic.get_dest_dir(), "zip", comic.get_dest_dir())
        if not os.path.isfile(temp_zip_file):
            raise Exception(f'Could not create temporary zip file "{temp_zip_file}".')

        os.replace(temp_zip_file, comic.get_dest_comic_zip())
        if not os.path.isfile(comic.get_dest_comic_zip()):
            raise Exception(
                f'Could not create final comic zip "{comic.get_dest_comic_zip()}".'
            )


def symlink_comic_book_zip(dry_run: bool, comic: ComicBook):
    if not os.path.exists(comic.get_dest_comic_zip()):
        raise Exception(f'Could not find zip file "{comic.get_dest_comic_zip()}".')

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Symlinking (relative) zip file "{comic.get_dest_comic_zip()}"'
            f' to "{comic.get_dest_series_comic_zip_symlink()}".'
        )
    else:
        logging.info(
            f'Symlinking (relative) the zip file "{comic.get_dest_comic_zip()}"'
            f' to "{comic.get_dest_series_comic_zip_symlink()}".'
        )

        if not os.path.exists(comic.get_dest_series_zip_dir()):
            os.makedirs(comic.get_dest_series_zip_dir())
        if os.path.islink(comic.get_dest_series_comic_zip_symlink()):
            os.remove(comic.get_dest_series_comic_zip_symlink())

        relative_symlink(
            comic.get_dest_comic_zip(), comic.get_dest_series_comic_zip_symlink()
        )
        if not os.path.islink(comic.get_dest_series_comic_zip_symlink()):
            raise Exception(
                f'Could not create symlink "{comic.get_dest_series_comic_zip_symlink()}".'
            )


def relative_symlink(target: Union[Path, str], destination: Union[Path, str]):
    """Create a symlink pointing to ``target`` from ``location``.
    Args:
        target: The target of the symlink (the file/directory that is pointed to)
        destination: The location of the symlink itself.
    """
    target = Path(target)
    destination = Path(destination)

    target_dir = destination.parent
    target_dir.mkdir(exist_ok=True, parents=True)

    relative_source = os.path.relpath(target, target_dir)

    logging.debug(f"{relative_source} -> {destination.name} in {target_dir}")
    target_dir_fd = os.open(str(target_dir.absolute()), os.O_RDONLY)
    try:
        os.symlink(relative_source, destination.name, dir_fd=target_dir_fd)
    finally:
        os.close(target_dir_fd)


def write_summary(
    comic: ComicBook,
    pages: SrceAndDestPages,
    timing: Timing,
    caching: bool,
):
    summary_file = os.path.join(comic.get_dest_dir(), "clean_summary.txt")

    calc_panels_bbox_height = int(
        round(
            (comic.srce_av_panels_bbox_height * comic.required_dim.panels_bbox_width)
            / comic.srce_av_panels_bbox_width
        )
    )

    with open(summary_file, "w") as f:
        f.write("Run Summary:\n")
        f.write(f"Time of run              = {timing.start_time}\n")
        f.write(
            f"Time taken               = {timing.get_elapsed_time_in_seconds()} seconds\n"
        )
        f.write(f'title                    = "{comic.title}"\n')
        f.write(f'file_title               = "{comic.file_title}"\n')
        f.write(f'issue_title              = "{comic.issue_title}"\n')
        f.write(f'comic title              = "{comic.get_comic_title()}"\n')
        f.write(f'srce_dir                 = "{comic.srce_dir}"\n')
        f.write(f'srce_fixes_dir           = "{comic.srce_fixes_dir}"\n')
        f.write(f'dest_dir                 = "{comic.get_dest_dir()}"\n')
        f.write(f'dest_zip_dir             = "{comic.get_dest_zip_dir()}"\n')
        f.write(
            f'dest_series_zip_symlink  = "{comic.get_dest_series_comic_zip_symlink()}"\n'
        )
        f.write(
            f'title_font_file          = "{get_font_path(comic.title_font_file)}"\n'
        )
        f.write(f"title_font_size          = {comic.title_font_size}\n")
        f.write(f"author_font_size         = {comic.author_font_size}\n")
        f.write(f"chronological_number     = {comic.chronological_number}\n")
        f.write(f'series                   = "{comic.series_name}"\n')
        f.write(f"series_book_num          = {comic.number_in_series}\n")
        f.write(f"Caching                  = {caching}\n")
        f.write(f"DEST_TARGET_X_MARGIN     = {DEST_TARGET_X_MARGIN}\n")
        f.write(f"DEST_TARGET_WIDTH        = {DEST_TARGET_WIDTH}\n")
        f.write(f"DEST_TARGET_HEIGHT       = {DEST_TARGET_HEIGHT}\n")
        f.write(f"DEST_TARGET_ASPECT_RATIO = {DEST_TARGET_ASPECT_RATIO:.2f}\n")
        f.write(f"DEST_JPG_QUALITY         = {DEST_JPG_QUALITY}\n")
        f.write(f"DEST_JPG_COMPRESS_LEVEL  = {DEST_JPG_COMPRESS_LEVEL}\n")
        f.write(f"Thicken line alpha       = {len(comic.thicken_line_alphas) > 0}\n")
        f.write(f"srce_min_panels_bbox_wid = {comic.srce_min_panels_bbox_width}\n")
        f.write(f"srce_max_panels_bbox_wid = {comic.srce_max_panels_bbox_width}\n")
        f.write(f"srce_av_panels_bbox_wid  = {comic.srce_av_panels_bbox_width}\n")
        f.write(f"srce_min_panels_bbox_hgt = {comic.srce_min_panels_bbox_height}\n")
        f.write(f"srce_max_panels_bbox_hgt = {comic.srce_max_panels_bbox_height}\n")
        f.write(f"srce_av_panels_bbox_hgt  = {comic.srce_av_panels_bbox_height}\n")
        f.write(f"req_panels_bbox_width    = {comic.required_dim.panels_bbox_width}\n")
        f.write(f"req_panels_bbox_height   = {comic.required_dim.panels_bbox_height}\n")
        f.write(f"calc_panels_bbox_height  = {calc_panels_bbox_height}\n")
        f.write(f"page_num_y_bottom        = {comic.required_dim.page_num_y_bottom}\n")
        f.write(f'intro_inset_file         = "{comic.intro_inset_file}"\n')
        f.write(f"publication_text         = \n{comic.publication_text}\n")
        f.write("\n")

        f.write("Pages Config Summary:\n")
        for pg in comic.images_in_order:
            f.write(
                f"pages = {pg.filenames:11}," f" page_type = {pg.page_type.name:12}\n"
            )
        f.write("\n")

        f.write("Page List Summary:\n")
        for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
            srce_filename = f'"{os.path.basename(srce_page.filename)}"'
            dest_filename = f'"{os.path.basename(dest_page.filename)}"'
            dest_page_type = f'"{dest_page.page_type.name}"'
            f.write(
                f"Added srce {srce_filename:17}"
                f" as dest {dest_filename:6},"
                f" type {dest_page_type:14}, "
                f" page {dest_page.page_num:2} ({get_page_num_str(dest_page):>3}),"
                f" bbox ({dest_page.panels_bbox.x_min:3}, {dest_page.panels_bbox.y_min:3},"
                f" {dest_page.panels_bbox.x_max:3}, {dest_page.panels_bbox.y_max:3}).\n"
            )
        f.write("\n")


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)


def get_required_pages_in_order(
    page_images_in_book: List[OriginalPage],
) -> List[CleanPage]:
    req_pages = []

    for page_image in page_images_in_book:
        if page_image.filenames == TITLE_EMPTY_FILENAME:
            assert page_image.page_type == PageType.TITLE
            req_pages.append(CleanPage(page_image.filenames, page_image.page_type))
            continue
        if page_image.filenames == EMPTY_FILENAME:
            assert page_image.page_type == PageType.BLANK_PAGE
            req_pages.append(CleanPage(page_image.filenames, page_image.page_type))
            continue

        if "-" not in page_image.filenames:
            filename = page_image.filenames
            file_num = int(filename)
            req_pages.append(CleanPage(filename, page_image.page_type, file_num))
        else:
            start, end = page_image.filenames.split("-")
            start_num = int(start)
            end_num = int(end)
            for file_num in range(start_num, end_num + 1):
                filename = f"{file_num:03d}"
                req_pages.append(CleanPage(filename, page_image.page_type, file_num))

    return req_pages


def get_srce_and_dest_pages_in_order(
    comic: ComicBook,
) -> SrceAndDestPages:
    required_pages = get_required_pages_in_order(comic.images_in_order)

    srce_page_list = []
    dest_page_list = []

    file_section_num = 1
    file_page_num = 0
    start_front_matter = True
    start_body = False
    page_num = 0
    for page in required_pages:
        if start_front_matter and page.page_type == PageType.BODY:
            start_front_matter = False
            start_body = True
            file_section_num += 1
            file_page_num = 1
            page_num = 1
        elif start_body and page.page_type != PageType.BODY:
            start_body = False
            file_section_num += 1
            file_page_num = 1
            page_num += 1
        elif page.page_type != PageType.FRONT:
            file_page_num += 1
            page_num += 1

        srce_file = get_checked_srce_file(comic, page)
        file_num_str = f"{file_section_num}-{file_page_num:02d}"
        dest_file = os.path.join(
            comic.get_dest_image_dir(), file_num_str + DEST_FILE_EXT
        )
        dest_thicken_line_alpha = comic.thicken_line_alphas.get(page.page_num, 0.0)

        srce_page_list.append(CleanPage(srce_file, page.page_type, page.page_num))
        dest_page_list.append(
            CleanPage(dest_file, page.page_type, page_num, dest_thicken_line_alpha)
        )

    return SrceAndDestPages(srce_page_list, dest_page_list)


def get_checked_srce_file(comic: ComicBook, page: CleanPage) -> str:
    if page.filename == TITLE_EMPTY_FILENAME:
        srce_file = TITLE_EMPTY_IMAGE_FILEPATH
    elif page.filename == EMPTY_FILENAME:
        srce_file = EMPTY_IMAGE_FILEPATH
    else:
        srce_file = get_srce_file(comic, page)

    if not os.path.isfile(srce_file):
        raise Exception(f'Could not find source file "{srce_file}".')

    return srce_file


def get_srce_file(comic: ComicBook, page: CleanPage) -> str:
    srce_file = os.path.join(comic.get_srce_image_dir(), page.filename + SRCE_FILE_EXT)
    srce_fixes_file = os.path.join(
        comic.get_srce_fixes_image_dir(), page.filename + SRCE_FILE_EXT
    )
    if not os.path.isfile(srce_fixes_file):
        return srce_file

    if os.path.isfile(srce_file):
        if is_fixes_special_case(comic, page):
            logging.info(
                f"NOTE: Special case - using {page.page_type.name} fixes srce file:"
                f' "{srce_fixes_file}".'
            )
        else:
            logging.info(f'NOTE: Using fixes srce file: "{srce_fixes_file}".')
            if page.page_type not in [PageType.COVER, PageType.BODY]:
                raise Exception(
                    f"Expected fixes page to be COVER or BODY: '{page.filename}'."
                )
    elif is_fixes_special_case(comic, page):
        logging.info(
            f"NOTE: Special case - using ADDED fixes srce file for {page.page_type.name} page:"
            f' "{srce_fixes_file}".'
        )
    else:
        logging.info(
            f"NOTE: Using added srce file of type {page.page_type.name}:"
            f' "{srce_fixes_file}".'
        )
        if page.page_type in [PageType.COVER, PageType.BODY]:
            raise Exception(
                f"Expected added page to be NOT COVER OR BODY: '{page.filename}'."
            )

    return srce_fixes_file


def is_fixes_special_case(comic: ComicBook, page: CleanPage) -> bool:
    if get_safe_title(comic.title) == "Back to Long Ago!" and page.filename == "209":
        return page.page_type == PageType.BACK_NO_PANELS
    if comic.file_title == "The Bill Collectors" and page.filename == "227":
        return page.page_type == PageType.BODY

    return False


def process_pages(
    dry_run: bool,
    cache_pages: bool,
    comic: ComicBook,
    pages: SrceAndDestPages,
):
    delete_all_files_in_directory(dry_run, comic.get_dest_dir())
    if cache_pages:
        logging.debug(
            f"Caching on - not deleting cached files"
            f' in images directory "{comic.get_dest_image_dir()}".'
        )
    else:
        delete_all_files_in_directory(dry_run, comic.get_dest_image_dir())

    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        process_page(dry_run, cache_pages, comic, srce_page, dest_page)


def delete_all_files_in_directory(dry_run: bool, directory_path: str):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Deleting all files in directory "{directory_path}".'
        )
        return

    logging.debug(f'Deleting all files in directory "{directory_path}".')

    with os.scandir(directory_path) as files:
        for file in files:
            if file.is_file():
                os.unlink(file.path)


def set_required_dimensions(
    comic: ComicBook,
    srce_pages: List[CleanPage],
):
    (
        required_panels_bbox_width,
        required_panels_bbox_height,
        comic.srce_min_panels_bbox_width,
        comic.srce_max_panels_bbox_width,
        comic.srce_min_panels_bbox_height,
        comic.srce_max_panels_bbox_height,
        comic.srce_av_panels_bbox_width,
        comic.srce_av_panels_bbox_height,
    ) = get_required_panels_bbox_width_height(srce_pages)

    assert required_panels_bbox_width == int(
        round((DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN)))
    )

    comic.required_dim.panels_bbox_width = required_panels_bbox_width
    comic.required_dim.panels_bbox_height = required_panels_bbox_height

    page_num_y_centre = int(
        round(0.5 * (0.5 * (DEST_TARGET_HEIGHT - required_panels_bbox_height)))
    )
    comic.required_dim.page_num_y_bottom = int(
        page_num_y_centre - (PAGE_NUM_HEIGHT / 2)
    )

    logging.debug(
        f"Set srce average panels bbox width to {comic.srce_av_panels_bbox_width}."
    )
    logging.debug(
        f"Set srce average panels bbox height to {comic.srce_av_panels_bbox_height}."
    )
    logging.debug(
        f"Set required panels bbox width to {comic.required_dim.panels_bbox_width}."
    )
    logging.debug(
        f"Set required panels bbox height to {comic.required_dim.panels_bbox_height}."
    )
    logging.debug(f"Set page num y bottom to {comic.required_dim.page_num_y_bottom}.")
    logging.debug("")


def get_required_panels_bbox_width_height(
    srce_pages: List[CleanPage],
) -> Tuple[int, int, int, int, int, int, int, int]:
    (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    ) = get_min_max_panels_bbox_width_height(srce_pages)

    av_panels_bbox_width, av_panels_bbox_height = get_average_panels_bbox_width_height(
        max_panels_bbox_height, srce_pages
    )
    assert av_panels_bbox_width > 0
    assert av_panels_bbox_height > 0

    required_panels_bbox_width = DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN)
    required_panels_bbox_height = get_scaled_panels_bbox_height(
        required_panels_bbox_width, av_panels_bbox_width, av_panels_bbox_height
    )

    return (
        required_panels_bbox_width,
        required_panels_bbox_height,
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
        av_panels_bbox_width,
        av_panels_bbox_height,
    )


def get_scaled_panels_bbox_height(
    scaled_panels_bbox_width: int, panels_bbox_width, panels_bbox_height: int
) -> int:
    return int(
        round((panels_bbox_height * scaled_panels_bbox_width) / panels_bbox_width)
    )


def get_average_panels_bbox_width_height(
    max_panels_bbox_height: int, srce_pages: List[CleanPage]
) -> Tuple[int, int]:
    sum_panels_bbox_width = 0
    sum_panels_bbox_height = 0
    num_pages = 0
    for srce_page in srce_pages:
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue

        panels_height = srce_page.panels_bbox.get_height()
        if panels_height < (
            max_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
        ):
            continue

        panels_width = srce_page.panels_bbox.get_width()

        sum_panels_bbox_width += panels_width
        sum_panels_bbox_height += panels_height
        num_pages += 1

    assert num_pages > 0
    return int(round(float(sum_panels_bbox_width) / float(num_pages))), int(
        round(float(sum_panels_bbox_height) / float(num_pages))
    )


def get_min_max_panels_bbox_width_height(
    srce_pages: List[CleanPage],
) -> Tuple[int, int, int, int]:
    min_panels_bbox_width = BIG_NUM
    max_panels_bbox_width = 0
    min_panels_bbox_height = BIG_NUM
    max_panels_bbox_height = 0
    for srce_page in srce_pages:
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue

        panels_bbox_width = srce_page.panels_bbox.get_width()
        panels_bbox_height = srce_page.panels_bbox.get_height()
        if min_panels_bbox_width > panels_bbox_width:
            min_panels_bbox_width = panels_bbox_width
        if min_panels_bbox_height > panels_bbox_height:
            min_panels_bbox_height = panels_bbox_height
        if max_panels_bbox_width < panels_bbox_width:
            max_panels_bbox_width = panels_bbox_width
        if max_panels_bbox_height < panels_bbox_height:
            max_panels_bbox_height = panels_bbox_height

    return (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    )


def set_srce_panel_bounding_boxes(
    dry_run: bool,
    use_cached_bboxes: bool,
    comic: ComicBook,
    srce_pages: List[CleanPage],
):
    logging.debug("Setting srce panel bounding boxes.")

    for srce_page in srce_pages:
        srce_page_image = open_image_for_reading(srce_page.filename)
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            srce_page.panels_bbox = BoundingBox(
                0, 0, srce_page_image.width - 1, srce_page_image.height - 1
            )
        else:
            srce_page_image = srce_page_image.convert("RGB")
            srce_page.panels_bbox = get_panels_bounding_box(
                dry_run, use_cached_bboxes, comic, srce_page_image, srce_page
            )

    logging.debug("")


def get_panels_bounding_box(
    dry_run: bool,
    use_cached_bboxes: bool,
    comic: ComicBook,
    srce_page_image: Image,
    srce_page: CleanPage,
) -> BoundingBox:
    assert srce_page.page_type not in PAGES_WITHOUT_PANELS

    srce_page_bounding_box_filename = str(
        os.path.join(
            comic.panel_segments_dir,
            os.path.splitext(os.path.basename(srce_page.filename))[0]
            + "_panel_bounds.txt",
        )
    )

    if not use_cached_bboxes and os.path.isfile(srce_page_bounding_box_filename):
        if dry_run:
            logging.info(
                f"{DRY_RUN_STR}: "
                f'Caching off - deleting panel bbox file "{srce_page_bounding_box_filename}".'
            )
        else:
            logging.debug(
                f'Caching off - deleting panel bbox file "{srce_page_bounding_box_filename}".'
            )
            os.remove(srce_page_bounding_box_filename)
            assert not os.path.isfile(srce_page_bounding_box_filename)

    if os.path.isfile(srce_page_bounding_box_filename):
        return bounding_box_processor.get_panels_bounding_box_from_file(
            srce_page_bounding_box_filename
        )

    logging.info(
        f'Getting Kumiko panel segment info for srce file "{os.path.basename(srce_page.filename)}".'
    )

    if not os.path.isdir(comic.panel_segments_dir):
        if dry_run:
            logging.info(
                f'{DRY_RUN_STR}: Making panel segments directory "{comic.panel_segments_dir}".'
            )
        else:
            os.makedirs(comic.panel_segments_dir, exist_ok=True)

    srce_bounded_dir = os.path.join(comic.get_srce_fixes_image_dir(), "bounded")

    bounding_box = bounding_box_processor.get_panels_bounding_box_from_kumiko(
        dry_run,
        comic.panel_segments_dir,
        srce_page_image,
        srce_page.filename,
        srce_bounded_dir,
    )

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Saving panel bounding box to "{srce_page_bounding_box_filename}".'
        )
    else:
        bounding_box_processor.save_panels_bounding_box(
            srce_page_bounding_box_filename, bounding_box
        )

    return bounding_box


def set_dest_panel_bounding_boxes(
    comic: ComicBook,
    pages: SrceAndDestPages,
):
    logging.debug("Setting dest panel bounding boxes.")

    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        dest_page.panels_bbox = get_dest_panel_bounding_box(comic, srce_page)

    logging.debug("")


def get_dest_panel_bounding_box(comic: ComicBook, srce_page: CleanPage) -> BoundingBox:
    if srce_page.page_type in PAGES_WITHOUT_PANELS:
        return BoundingBox(0, 0, DEST_TARGET_WIDTH - 1, DEST_TARGET_HEIGHT - 1)

    required_panels_width = int(DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN))
    srce_panels_bbox_width = srce_page.panels_bbox.get_width()
    srce_panels_bbox_height = srce_page.panels_bbox.get_height()

    if srce_panels_bbox_height >= (
        comic.srce_av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    ):
        required_panels_height = comic.required_dim.panels_bbox_height
    else:
        required_panels_height = get_scaled_panels_bbox_height(
            required_panels_width, srce_panels_bbox_width, srce_panels_bbox_height
        )
        logging.warning(
            f'For "{os.path.basename(srce_page.filename)}",'
            f" panels bbox height {srce_panels_bbox_height}"
            f" < {comic.srce_av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN}"
            f" (average height {comic.srce_av_panels_bbox_height}"
            f" - error {PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN})."
            f" So setting required bbox height to {required_panels_height},"
            f" not {comic.required_dim.panels_bbox_height}."
        )

    # Centre the dest panels image on an empty page.
    dest_panels_x_min = DEST_TARGET_X_MARGIN
    dest_panels_y_min = int(0.5 * (DEST_TARGET_HEIGHT - required_panels_height))
    dest_panels_x_max = dest_panels_x_min + (required_panels_width - 1)
    dest_panels_y_max = dest_panels_y_min + (required_panels_height - 1)

    return BoundingBox(
        dest_panels_x_min, dest_panels_y_min, dest_panels_x_max, dest_panels_y_max
    )


def process_page(
    dry_run: bool,
    cache_pages: bool,
    comic: ComicBook,
    srce_page: CleanPage,
    dest_page: CleanPage,
):
    logging.info(
        f'Convert "{os.path.basename(srce_page.filename)}" (page-type {srce_page.page_type.name})'
        f' to "{os.path.basename(dest_page.filename)}"'
        f" (page number = {get_page_num_str(dest_page)},"
        f" cache pages = {cache_pages})..."
    )

    srce_page_image = open_image_for_reading(srce_page.filename)
    if (
        srce_page.page_type == PageType.BODY
        and srce_page_image.height < MIN_HD_SRCE_HEIGHT
    ):
        raise Exception(
            f"Srce image error: min required height {MIN_HD_SRCE_HEIGHT}."
            f' Poor srce file resolution for "{srce_page.filename}":'
            f" {srce_page_image.width} x {srce_page_image.height}."
        )

    if (
        srce_page.page_type in CACHEABLE_PAGES
        and cache_pages
        and os.path.exists(dest_page.filename)
        and not is_dest_file_out_of_date(srce_page.filename, dest_page.filename)
    ):
        logging.debug(f'Caching on - using existing page file "{dest_page.filename}".')
        return

    dest_page_image = get_dest_page_image(comic, srce_page_image, srce_page, dest_page)

    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Save changes to image "{dest_page.filename}".')
    else:
        dest_page_image.save(
            dest_page.filename,
            optimize=True,
            compress_level=DEST_JPG_COMPRESS_LEVEL,
            quality=DEST_JPG_QUALITY,
            comment="\n".join(get_dest_jpg_comments(srce_page, dest_page)),
        )
        logging.info(f'Saved changes to image "{dest_page.filename}".')

    logging.info("")


def is_dest_file_out_of_date(srce_file: str, dest_file: str) -> bool:
    srce_timestamp = os.path.getmtime(srce_file)
    dest_timestamp = os.path.getmtime(dest_file)

    if srce_timestamp > dest_timestamp:
        logging.debug(get_out_of_date_file_msg(srce_file, dest_file))
        return True

    return False


def get_out_of_date_file_msg(srce_file: str, dest_file: str) -> str:
    srce_timestamp = os.path.getmtime(srce_file)
    dest_timestamp = os.path.getmtime(dest_file)
    assert srce_timestamp > dest_timestamp

    srce_date = datetime.fromtimestamp(srce_timestamp)
    dest_date = datetime.fromtimestamp(dest_timestamp)

    return (
        f'Dest file "{dest_file}" ({dest_date.strftime("%Y_%m_%d-%H_%M_%S.%f")})'
        f" is out of date WRT"
        f' srce file "{srce_file}" ({srce_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}).'
    )


def get_dest_jpg_comments(srce_page: CleanPage, dest_page: CleanPage) -> List[str]:
    indent = "      "
    comments = [
        indent,
        f"{indent}Srce page num: {srce_page.page_num}",
        f"{indent}Srce page type: {srce_page.page_type.name}",
        f"{indent}Srce panels bbox: {dest_page.panels_bbox.x_min}, {dest_page.panels_bbox.y_min},"
        + f" {dest_page.panels_bbox.x_max}, {dest_page.panels_bbox.y_max}",
        f"{indent}Dest page num: {dest_page.page_num}",
        f"{indent}Dest thicken alpha: {dest_page.page_thicken_lines_alpha}",
    ]

    return comments


def get_dest_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    log_page_info("Srce", srce_page_image, srce_page)
    log_page_info("Dest", None, dest_page)

    if dest_page.page_type in PAGES_WITHOUT_PANELS:
        dest_page_image = get_dest_non_body_page_image(
            comic, srce_page_image, srce_page, dest_page
        )
    else:
        dest_page_image = get_dest_main_page_image(
            comic, srce_page_image, srce_page, dest_page
        )

    rgb_dest_page_image = dest_page_image.convert("RGB")

    if dest_page.page_type in MEDIAN_FILTERABLE_PAGES:
        logging.debug(f'Starting median filter of "{dest_page.filename}"...')
        rgb_dest_page_image = get_improved_image(
            rgb_dest_page_image, dest_page.page_thicken_lines_alpha
        )

    log_page_info("Dest", rgb_dest_page_image, dest_page)

    return rgb_dest_page_image


def get_improved_image(image: Image, thicken_lines_alpha: float) -> Image:
    current_log_level = logging.getLogger().level
    try:
        logging.getLogger().setLevel(logging.INFO)

        image = get_median_filter(np.asarray(image))
        if thicken_lines_alpha < SMALL_FLOAT:
            return Image.fromarray(image)

        logging.info(f"Doing black line thickening with alpha = {thicken_lines_alpha}.")
        image = get_thickened_black_lines(image, thicken_lines_alpha)
        return Image.fromarray(image)

    finally:
        logging.getLogger().setLevel(current_log_level)


def log_page_info(prefix: str, image: Image, page: CleanPage):
    width = image.width if image else 0
    height = image.height if image else 0
    logging.debug(
        f"{prefix}: width = {width:4}, height = {height:4},"
        f" page_type = {page.page_type.name:13},"
        f" panels bbox = {page.panels_bbox.x_min:4}, {page.panels_bbox.y_min:4},"
        f" {page.panels_bbox.x_max:4}, {page.panels_bbox.y_max:4}."
    )


def get_dest_non_body_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    if dest_page.page_type == PageType.FRONT:
        return get_dest_front_page_image(srce_page_image, srce_page)
    if dest_page.page_type == PageType.COVER:
        return get_dest_cover_page_image(srce_page_image, srce_page)
    if dest_page.page_type in PAINTING_PAGES:
        return get_dest_painting_page_image(srce_page_image, srce_page)
    if dest_page.page_type in SPLASH_PAGES:
        return get_dest_splash_page_image(srce_page_image, srce_page)
    if dest_page.page_type == PageType.BACK_NO_PANELS:
        return get_dest_no_panels_page_image(
            comic, srce_page_image, srce_page, dest_page
        )
    if dest_page.page_type == PageType.BLANK_PAGE:
        return get_dest_blank_page_image(srce_page_image)
    if dest_page.page_type == PageType.TITLE:
        return get_dest_title_page_image(comic, srce_page_image)
    assert False


def get_dest_title_page_image(comic: ComicBook, srce_page_image: Image) -> Image:
    dest_page_image = srce_page_image.resize(
        size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
        resample=Image.Resampling.BICUBIC,
    )

    write_introduction(comic, dest_page_image)

    return dest_page_image


def get_dest_front_page_image(srce_page_image: Image, srce_page: CleanPage) -> Image:
    return get_dest_black_bars_page_image(srce_page_image, srce_page)


def get_dest_cover_page_image(srce_page_image: Image, srce_page: CleanPage) -> Image:
    return get_dest_black_bars_page_image(srce_page_image, srce_page)


def get_dest_painting_page_image(painting_image: Image, srce_page: CleanPage) -> Image:
    if srce_page.page_type == PageType.PAINTING:
        draw_border_around_image(painting_image)

    dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

    return get_dest_centred_page_image(painting_image, srce_page, dest_page_image)


def get_dest_splash_page_image(splash_image: Image, srce_page: CleanPage) -> Image:
    if srce_page.page_type == PageType.SPLASH:
        draw_border_around_image(splash_image)

    dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

    return get_dest_centred_page_image(splash_image, srce_page, dest_page_image)


def draw_border_around_image(image: Image):
    x_max = image.width - 1
    y_max = image.height - 1
    border = [
        (0, 0),
        (x_max, 0),
        (x_max, y_max),
        (0, y_max),
        (0, 0),
    ]
    draw = ImageDraw.Draw(image)
    draw.line(border, fill=SPLASH_BORDER_COLOR, width=SPLASH_BORDER_WIDTH)


def get_dest_no_panels_page_image(
    comic: ComicBook, no_panels_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

    dest_page_image = get_dest_centred_page_image(
        no_panels_image, srce_page, dest_page_image
    )

    write_page_number(comic, dest_page_image, dest_page, PAGE_NUM_COLOR)

    return dest_page_image


def get_dest_black_bars_page_image(
    srce_page_image: Image, srce_page: CleanPage
) -> Image:
    dest_page_image = Image.new(
        "RGB", (DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT), (0, 0, 0)
    )
    return get_dest_centred_page_image(srce_page_image, srce_page, dest_page_image)


def get_dest_centred_page_image(
    srce_page_image: Image, srce_page: CleanPage, dest_page_image: Image
) -> Image:
    srce_aspect_ratio = float(srce_page_image.height) / float(srce_page_image.width)
    if abs(srce_aspect_ratio - DEST_TARGET_ASPECT_RATIO) > 0.01:
        logging.debug(
            f"Wrong aspect ratio for page '{srce_page.filename}':"
            f" {srce_aspect_ratio:.2f} != {DEST_TARGET_ASPECT_RATIO:.2f}."
            f" Using black bars."
        )

    required_height = get_scaled_panels_bbox_height(
        DEST_TARGET_WIDTH, srce_page_image.width, srce_page_image.height
    )

    no_margins_image = srce_page_image.resize(
        size=(DEST_TARGET_WIDTH, required_height),
        resample=Image.Resampling.BICUBIC,
    )
    no_margins_aspect_ratio = float(no_margins_image.height) / float(
        no_margins_image.width
    )
    assert abs(srce_aspect_ratio - no_margins_aspect_ratio) <= 0.01

    if required_height == DEST_TARGET_HEIGHT:
        return no_margins_image

    cover_top = int(round(0.5 * (DEST_TARGET_HEIGHT - required_height)))
    dest_page_image.paste(no_margins_image, (0, cover_top))

    return dest_page_image


def get_dest_blank_page_image(srce_page_image: Image) -> Image:
    dest_page_image = srce_page_image.resize(
        size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
        resample=Image.Resampling.BICUBIC,
    )

    return dest_page_image


def get_dest_main_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    dest_panels_image = srce_page_image.crop(srce_page.panels_bbox.get_box())
    dest_page_image = get_centred_dest_page_image(dest_page, dest_panels_image)

    if dest_page_image.width != DEST_TARGET_WIDTH:
        raise Exception(
            f'Width mismatch for page "{srce_page.filename}":'
            f"{dest_page_image.width} != {DEST_TARGET_WIDTH}"
        )
    if dest_page_image.height != DEST_TARGET_HEIGHT:
        raise Exception(
            f'Height mismatch for page "{srce_page.filename}":'
            f"{dest_page_image.height} != {DEST_TARGET_HEIGHT}"
        )

    write_page_number(comic, dest_page_image, dest_page, PAGE_NUM_COLOR)

    return dest_page_image


def get_centred_dest_page_image(
    dest_page: CleanPage, dest_panels_image: Image
) -> Image:
    dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

    dest_panels_image = dest_panels_image.resize(
        size=(dest_page.panels_bbox.get_width(), dest_page.panels_bbox.get_height()),
        resample=Image.Resampling.BICUBIC,
    )

    dest_panels_pos = (dest_page.panels_bbox.x_min, dest_page.panels_bbox.y_min)
    dest_page_image.paste(dest_panels_image, dest_panels_pos)

    return dest_page_image


def write_introduction(comic: ComicBook, dest_page_image: Image):
    logging.info(f'Writing introduction - using inset file "{comic.intro_inset_file}".')

    draw = ImageDraw.Draw(dest_page_image)

    top = INTRO_TOP

    title, title_fonts, text_height = get_title_and_fonts(
        draw, comic.get_comic_title(), comic.title_font_file, comic.title_font_size
    )

    draw_centered_multiline_multi_font_text(
        title,
        dest_page_image,
        draw,
        title_fonts,
        INTRO_TITLE_COLOR,
        top,
        spacing=INTRO_TITLE_SPACING,
    )
    top += text_height + INTRO_TITLE_SPACING

    top += INTRO_TITLE_AUTHOR_GAP
    text = "by"
    author_font = ImageFont.truetype(
        comic.title_font_file, int(0.6 * comic.author_font_size)
    )
    text_height = get_intro_text_height(draw, text, author_font)
    draw_centered_text(
        text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top
    )
    top += text_height

    top += INTRO_TITLE_AUTHOR_BY_GAP
    text = f"{BARKS}"
    author_font = ImageFont.truetype(comic.title_font_file, comic.author_font_size)
    text_height = get_intro_text_height(draw, text, author_font)
    draw_centered_text(
        text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top
    )
    top += text_height + INTRO_AUTHOR_INSET_GAP

    pub_text_font = ImageFont.truetype(
        get_font_path(INTRO_TEXT_FONT_FILE), INTRO_PUB_TEXT_FONT_SIZE
    )
    text_height = get_intro_text_height(draw, comic.publication_text, pub_text_font)
    pub_text_top = dest_page_image.height - INTRO_BOTTOM_MARGIN - text_height

    inset_pos, new_inset = get_resized_inset(
        comic.intro_inset_file,
        top,
        pub_text_top,
        dest_page_image.width,
    )
    dest_page_image.paste(new_inset, inset_pos)

    draw_centered_multiline_text(
        comic.publication_text,
        dest_page_image,
        draw,
        pub_text_font,
        INTRO_PUB_TEXT_COLOR,
        pub_text_top,
        INTRO_PUB_TEXT_SPACING,
    )


def get_resized_inset(
    inset_file: str, top: int, bottom: int, page_width: int
) -> Tuple[Tuple[int, int], Image]:
    inset = open_image_for_reading(inset_file)
    inset_width, inset_height = inset.size

    usable_width = page_width - (2 * DEST_TARGET_X_MARGIN)
    usable_height = bottom - top

    width_margin = int(INTRO_MAX_WIDTH_INSET_MARGIN_FRAC * usable_width)
    height_margin = int(INTRO_MAX_HEIGHT_INSET_MARGIN_FRAC * usable_height)

    new_inset_width = usable_width - (2 * width_margin)
    new_inset_height = int((inset_height / inset_width) * new_inset_width)

    max_inset_height = usable_height - (2 * height_margin)
    if new_inset_height > max_inset_height:
        new_inset_height = max_inset_height
        new_inset_width = int((inset_width / inset_height) * new_inset_height)

    new_inset = inset.resize(
        size=(new_inset_width, new_inset_height), resample=Image.Resampling.BICUBIC
    )

    inset_left = int((page_width - new_inset_width) / 2)
    inset_top = top + int(((bottom - top) - new_inset_height) / 2)

    return (inset_left, inset_top), new_inset


def get_intro_text_height(draw: ImageDraw.Draw, text: str, font: ImageFont) -> int:
    text_bbox = draw.multiline_textbbox(
        (0, 0), text, font=font, spacing=INTRO_TITLE_SPACING
    )
    return text_bbox[3] - text_bbox[1]


def get_intro_text_width(draw: ImageDraw.Draw, text: str, font: ImageFont) -> int:
    text_bbox = draw.multiline_textbbox(
        (0, 0), text, font=font, spacing=INTRO_TITLE_SPACING
    )
    return text_bbox[2] - text_bbox[0]


def get_title_and_fonts(
    draw: ImageDraw.Draw, title: str, font_file: str, font_size: int
) -> Tuple[List[str], List[ImageFont.truetype], int]:
    if title.startswith(CS):
        return get_comics_and_stories_title_and_fonts(draw, title, font_file, font_size)

    title_font = ImageFont.truetype(font_file, font_size)
    text_height = get_intro_text_height(draw, title, title_font)
    return [title], [title_font], text_height


def get_comics_and_stories_title_and_fonts(
    draw: ImageDraw.Draw, title: str, font_file: str, font_size: int
) -> Tuple[List[str], List[ImageFont.truetype], int]:
    assert title.startswith(CS)

    comic_num = title[len(CS) :]

    title_split = ["Comics", "and Stories", comic_num]
    title_fonts = [
        ImageFont.truetype(font_file, font_size),
        ImageFont.truetype(font_file, int(0.5 * font_size)),
        ImageFont.truetype(font_file, font_size),
    ]

    text_height = get_intro_text_height(draw, title, title_fonts[0])

    return title_split, title_fonts, text_height


def draw_centered_text(
    text: str, image: Image, draw: ImageDraw, font: ImageFont, color, top: int
):
    w = draw.textlength(text, font)
    # h = font.getbbox(text)[3]
    left = (image.width - w) / 2
    draw.text((left, top), text, fill=color, font=font, align="center")


def draw_centered_multiline_text(
    text: str,
    image: Image,
    draw: ImageDraw,
    font: ImageFont,
    color,
    top: int,
    spacing: int,
):
    text_width = get_intro_text_width(draw, text, font)
    left = (image.width - text_width) / 2
    draw.multiline_text(
        (left, top), text, fill=color, font=font, align="center", spacing=spacing
    )


def draw_centered_multiline_multi_font_text(
    text_vals: List[str],
    image: Image,
    draw: ImageDraw,
    fonts: List[ImageFont],
    color,
    top: int,
    spacing: int,
):
    lines = []
    line = []
    for text, font in zip(text_vals, fonts):
        if not text.startswith("\n"):
            line.append((text, font))
        else:
            lines.append(line)
            line = [(text[1:], font)]
    lines.append(line)

    line_widths = []
    text_lines = []
    for line in lines:
        line_width = 0
        text_line = []
        for text, font in line:
            text_width = get_intro_text_width(draw, text, font)
            line_width += text_width
            text_line.append((text, font, text_width))
        line_widths.append(line_width)
        text_lines.append(text_line)

    max_font_height = get_intro_text_height(draw, text_vals[0], fonts[0])
    line_top = top
    for text_line, line_width in zip(text_lines, line_widths):
        left = (image.width - line_width) / 2
        line_start = True
        for text, font, text_width in text_line:
            font_height = get_intro_text_height(draw, text, font)
            assert font_height <= max_font_height

            if line_start or font_height == max_font_height:
                line_top_extra = 0
                width_spacing = 0
            else:
                line_top_extra = 10
                width_spacing = int(1.1 * ((font_height * spacing) / max_font_height))
            left += width_spacing

            draw.multiline_text(
                (left, line_top + line_top_extra),
                text,
                fill=color,
                font=font,
                align="center",
                spacing=spacing,
            )
            left += text_width
            line_start = False
        line_top += int(1.5 * max_font_height)


def write_page_number(
    comic: ComicBook, dest_page_image: Image, dest_page: CleanPage, color
):
    draw = ImageDraw.Draw(dest_page_image)

    dest_page_centre = int(dest_page_image.width / 2)
    page_num_x_start = dest_page_centre - PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_x_end = dest_page_centre + PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_y_start = (
        dest_page_image.height - comic.required_dim.page_num_y_bottom
    ) - PAGE_NUM_HEIGHT
    page_num_y_end = page_num_y_start + PAGE_NUM_HEIGHT

    # Get the color of a blank part of the page
    page_blank_color = dest_page_image.getpixel(
        (
            page_num_x_start + PAGE_NUM_X_BLANK_PIXEL_OFFSET,
            page_num_y_end,
        )
    )

    # Remove the existing page number
    shape = (
        (
            page_num_x_start - 1,
            page_num_y_start - 1,
        ),
        (
            page_num_x_end + 1,
            page_num_y_end + 1,
        ),
    )
    draw.rectangle(shape, fill=page_blank_color)

    font = ImageFont.truetype(get_font_path(PAGE_NUM_FONT_FILE), PAGE_NUM_FONT_SIZE)
    text = get_page_num_str(dest_page)
    draw_centered_text(
        text,
        dest_page_image,
        draw,
        font,
        color,
        page_num_y_start,
    )


def get_page_num_str(page: CleanPage) -> str:
    return get_page_number_str(page, page.page_num)


def get_page_number_str(page: CleanPage, page_number: int) -> str:
    if page.page_type not in FRONT_MATTER_PAGES:
        return str(page_number)
    if page.page_type == PageType.FRONT:
        assert page_number == 0
        return ""

    return ROMAN_NUMERALS[page_number]


def process_additional_files(
    dry_run: bool, cfg_file: str, comic: ComicBook, pages: SrceAndDestPages
):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: shutil.copy2("{cfg_file}", "{comic.get_dest_dir()}")'
        )
    else:
        shutil.copy2(cfg_file, comic.get_dest_dir())

    write_readme_file(dry_run, cfg_file, comic)
    write_metadata_file(dry_run, comic, pages.dest_pages)
    write_json_metadata(dry_run, comic, pages.dest_pages)
    write_srce_dest_map(dry_run, comic, pages)
    write_dest_panels_bboxes(dry_run, comic, pages.dest_pages)


def write_readme_file(dry_run: bool, cfg_file: str, comic: ComicBook):
    readme_file = os.path.join(comic.get_dest_dir(), README_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write info to "{readme_file}".')
    else:
        with open(readme_file, "w") as f:
            title = get_safe_title(comic.title)
            f.write(f"{title}\n")
            f.write("".ljust(len(title), "-") + "\n")
            f.write("\n")
            now_str = datetime.now().strftime("%b %d %Y %H:%M:%S")
            f.write(f"Created:           {now_str}\n")
            f.write(f'Archived ini file: "{os.path.basename(cfg_file)}"\n')


def write_metadata_file(dry_run: bool, comic: ComicBook, dest_pages: List[CleanPage]):
    metadata_file = os.path.join(comic.get_dest_dir(), METADATA_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write metadata to "{metadata_file}".')
    else:
        with open(metadata_file, "w") as f:
            f.write(f"[{DOUBLE_PAGES_SECTION}]\n")
            orig_page_num = 0
            for page in dest_pages:
                orig_page_num += 1
                if page.page_type not in FRONT_MATTER_PAGES:
                    break
                f.write(f"{orig_page_num} = False" + "\n")
            f.write("\n")

            body_start_page_num = orig_page_num
            f.write(f"[{PAGE_NUMBERS_SECTION}]\n")
            f.write(f"body_start = {body_start_page_num}\n")


def write_json_metadata(dry_run: bool, comic: ComicBook, dest_pages: List[CleanPage]):
    metadata_file = os.path.join(comic.get_dest_dir(), JSON_METADATA_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write json metadata to "{metadata_file}".')
    else:
        metadata = dict()
        metadata["title"] = get_safe_title(comic.title)
        metadata["file_title"] = comic.file_title
        metadata["issue_title"] = get_safe_title(comic.issue_title)
        metadata["comic_title"] = get_safe_title(comic.get_comic_title())
        metadata["series_name"] = comic.series_name
        metadata["number_in_series"] = comic.number_in_series
        metadata["srce_file"] = comic.srce_dir
        metadata["dest_file"] = comic.get_dest_dir()
        metadata["publication_date"] = comic.publication_date
        metadata["submitted_date"] = comic.submitted_date
        metadata["srce_min_panels_bbox_width"] = comic.srce_min_panels_bbox_width
        metadata["srce_max_panels_bbox_width"] = comic.srce_max_panels_bbox_width
        metadata["srce_av_panels_bbox_width"] = comic.srce_av_panels_bbox_width
        metadata["srce_min_panels_bbox_height"] = comic.srce_min_panels_bbox_height
        metadata["srce_max_panels_bbox_height"] = comic.srce_max_panels_bbox_height
        metadata["srce_av_panels_bbox_height"] = comic.srce_av_panels_bbox_height
        metadata["required_dim"] = [
            comic.required_dim.panels_bbox_width,
            comic.required_dim.panels_bbox_height,
            comic.required_dim.page_num_y_bottom,
        ]
        metadata["page_counts"] = get_page_counts(comic, dest_pages)
        with open(metadata_file, "w") as f:
            json.dump(metadata, f)


def get_page_counts(comic: ComicBook, dest_pages: List[CleanPage]) -> Dict[str, int]:
    page_counts = dict()

    front_page_count = len([p for p in dest_pages if p.page_type == PageType.FRONT])
    assert front_page_count <= 1

    title_page_count = len([p for p in dest_pages if p.page_type == PageType.TITLE])
    assert title_page_count == 1

    cover_page_count = len([p for p in dest_pages if p.page_type == PageType.COVER])
    assert cover_page_count <= 1

    painting_page_count = len([p for p in dest_pages if p.page_type in PAINTING_PAGES])

    splash_page_count = len([p for p in dest_pages if p.page_type in SPLASH_PAGES])

    front_matter_page_count = len(
        [p for p in dest_pages if p.page_type == PageType.FRONT_MATTER]
    )

    story_page_count = len([p for p in dest_pages if p.page_type == PageType.BODY])

    back_matter_page_count = len(
        [
            p
            for p in dest_pages
            if p.page_type in [PageType.BACK_MATTER, PageType.BACK_NO_PANELS]
        ]
    )

    blank_page_count = len(
        [p for p in dest_pages if p.page_type == PageType.BLANK_PAGE]
    )

    total_page_count = len(dest_pages)
    assert total_page_count == (
        front_page_count
        + title_page_count
        + cover_page_count
        + painting_page_count
        + splash_page_count
        + front_matter_page_count
        + story_page_count
        + back_matter_page_count
        + blank_page_count
    )

    page_counts["painting"] = painting_page_count
    page_counts["title"] = title_page_count
    page_counts["cover"] = cover_page_count
    page_counts["splash"] = splash_page_count
    page_counts["front_matter"] = front_matter_page_count
    page_counts["story"] = story_page_count
    page_counts["back_matter"] = back_matter_page_count
    page_counts["blank"] = blank_page_count

    page_counts["total"] = total_page_count

    return page_counts


def write_srce_dest_map(
    dry_run: bool,
    comic: ComicBook,
    pages: SrceAndDestPages,
):
    src_dst_map_file = os.path.join(comic.get_dest_dir(), DEST_SRCE_MAP_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write srce dest map to "{src_dst_map_file}".')
    else:
        srce_dest_map = dict()
        srce_dest_map["srce_dirname"] = os.path.basename(comic.srce_dir)
        srce_dest_map["dest_dirname"] = comic.get_dest_rel_dirname()

        srce_dest_map["srce_min_panels_bbox_width"] = comic.srce_min_panels_bbox_width
        srce_dest_map["srce_max_panels_bbox_width"] = comic.srce_max_panels_bbox_width
        srce_dest_map["srce_min_panels_bbox_height"] = comic.srce_min_panels_bbox_height
        srce_dest_map["srce_max_panels_bbox_height"] = comic.srce_max_panels_bbox_height
        srce_dest_map["dest_required_bbox_width"] = comic.required_dim.panels_bbox_width
        srce_dest_map["dest_required_bbox_height"] = (
            comic.required_dim.panels_bbox_height
        )

        dest_page_map = dict()
        for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
            srce_page = {
                "file": os.path.basename(srce_page.filename),
                "type": dest_page.page_type.name,
            }
            dest_page_map[os.path.basename(dest_page.filename)] = srce_page
        srce_dest_map["pages"] = dest_page_map

        with open(src_dst_map_file, "w") as f:
            json.dump(srce_dest_map, f)


def write_dest_panels_bboxes(
    dry_run: bool,
    comic: ComicBook,
    dest_pages: List[CleanPage],
):
    dst_bboxes_file = os.path.join(comic.get_dest_dir(), DEST_PANELS_BBOXES_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write dest panels bboxes to "{dst_bboxes_file}".')
    else:
        bboxes_dict = dict()
        for dest_page in dest_pages:
            bbox_key = os.path.basename(dest_page.filename)
            bboxes_dict[bbox_key] = dest_page.panels_bbox.get_box()

        with open(dst_bboxes_file, "w") as f:
            json.dump(bboxes_dict, f)


def create_dest_dirs(dry_run: bool, comic: ComicBook):
    if not os.path.isdir(comic.get_dest_image_dir()):
        if dry_run:
            logging.info(
                f'{DRY_RUN_STR} Would have made directory "{comic.get_dest_image_dir()}".'
            )
            return
        os.makedirs(comic.get_dest_image_dir())

    if not os.path.isdir(comic.get_dest_image_dir()):
        raise Exception(f'Could not make directory "{comic.get_dest_image_dir()}".')


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]


def get_key_number(ordered_dict: ComicBookInfoDict, key: str) -> int:
    n = 1
    for k in ordered_dict:
        if k == key:
            return n
        n += 1
    return -1


def get_formatted_day(day: int) -> str:
    if day == 1 or day == 31:
        day_str = str(day) + "st"
    elif day == 2 or day == 22:
        day_str = str(day) + "nd"
    elif day == 3 or day == 23:
        day_str = str(day) + "rd"
    else:
        day_str = str(day) + "th"

    return day_str


def get_formatted_first_published_str(info: ComicBookInfo) -> str:
    issue = f"{info.issue_name} #{info.issue_number}"

    if info.issue_month == -1:
        issue_date = info.issue_year
    else:
        issue_date = f"{MONTH_AS_LONG_STR[info.issue_month]} {info.issue_year}"

    return f"{issue}, {issue_date}"


def get_formatted_submitted_date(info: ComicBookInfo) -> str:
    if info.submitted_day == -1:
        return f", {MONTH_AS_LONG_STR[info.submitted_month]} {info.submitted_year}"

    return (
        f" on {MONTH_AS_LONG_STR[info.submitted_month]}"
        f" {get_formatted_day(info.submitted_day)}, {info.submitted_year}"
    )


def get_comic_book(stories: ComicBookInfoDict, ini_file: str) -> ComicBook:
    logging.info(f'Getting comic book info from config file "{ini_file}".')

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    config.read(ini_file)

    title = config["info"]["title"]
    issue_title = (
        "" if "issue_title" not in config["info"] else config["info"]["issue_title"]
    )
    file_title = config["info"]["file_title"]
    lookup_title = get_lookup_title(title, file_title)
    intro_inset_file = str(
        os.path.join(CONFIGS_SUBDIR, get_inset_filename(ini_file, file_title))
    )

    cb_info: ComicBookInfo = stories[lookup_title]
    srce_info = SOURCE_COMICS[config["info"]["source_comic"]]
    srce_root_dir = str(os.path.join(BARKS_ROOT_DIR, srce_info.pub))
    srce_dir = os.path.join(srce_root_dir, srce_info.title)
    srce_fixup_dir = os.path.join(
        srce_root_dir + "-fixes-and-additions", srce_info.title
    )
    panel_segments_dir = str(
        os.path.join(BARKS_ROOT_DIR, srce_info.pub + "-panel-segments", srce_info.title)
    )

    publication_date = get_formatted_first_published_str(cb_info)
    submitted_date = get_formatted_submitted_date(cb_info)
    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published in {srce_info.pub} CBDL,"
        + f" Volume {srce_info.volume}, {srce_info.year}\n"
        + f"Color restoration by {cb_info.colorist}"
    )

    if "extra_pub_info" in config["info"]:
        publication_text += "\n" + config["info"]["extra_pub_info"]

    thicken_line_alphas: Dict[int, float] = {}
    if "black_line_thickening" in config:
        thicken_line_alphas = get_thicken_line_alphas(
            config._sections["black_line_thickening"]
        )

    comic = ComicBook(
        config_file=ini_file,
        title=title,
        title_font_file=get_font_path(
            config["info"].get("title_font_file", INTRO_TITLE_DEFAULT_FONT_FILE)
        ),
        title_font_size=config["info"].getint(
            "title_font_size", INTRO_TITLE_DEFAULT_FONT_SIZE
        ),
        file_title=file_title,
        issue_title=issue_title,
        author_font_size=config["info"].getint(
            "author_font_size", INTRO_AUTHOR_DEFAULT_FONT_SIZE
        ),
        srce_min_panels_bbox_width=-1,
        srce_max_panels_bbox_width=-1,
        srce_min_panels_bbox_height=-1,
        srce_max_panels_bbox_height=-1,
        srce_av_panels_bbox_width=-1,
        srce_av_panels_bbox_height=-1,
        required_dim=RequiredDimensions(),
        srce_root_dir=srce_root_dir,
        srce_dir=srce_dir,
        srce_fixes_dir=srce_fixup_dir,
        panel_segments_dir=panel_segments_dir,
        series_name=cb_info.series_name,
        number_in_series=cb_info.number_in_series,
        chronological_number=cb_info.chronological_number,
        intro_inset_file=intro_inset_file,
        publication_date=publication_date,
        submitted_date=submitted_date,
        publication_text=publication_text,
        comic_book_info=cb_info,
        images_in_order=[
            OriginalPage(key, PageType[config["pages"][key]]) for key in config["pages"]
        ],
        thicken_line_alphas=thicken_line_alphas,
    )

    if not os.path.isdir(comic.srce_dir):
        raise Exception(f'Could not find srce directory "{comic.srce_dir}".')
    if not os.path.isdir(comic.get_srce_image_dir()):
        raise Exception(
            f'Could not find srce image directory "{comic.get_srce_image_dir()}".'
        )
    if not os.path.isdir(comic.srce_fixes_dir):
        raise Exception(
            f'Could not find srce fixup directory "{comic.srce_fixes_dir}".'
        )
    if not os.path.isdir(comic.get_srce_fixes_image_dir()):
        raise Exception(
            f'Could not find srce fixup image directory "{comic.get_srce_fixes_image_dir()}".'
        )

    return comic


def get_thicken_line_alphas(page_alphas: Dict[str, str]) -> Dict[int, float]:
    thicken_line_alphas: Dict[int, float] = {}

    for key in page_alphas:
        alpha = float(page_alphas[key])
        if "-" not in key:
            page_num = int(key)
            thicken_line_alphas[page_num] = alpha
        else:
            start, end = key.split("-")
            start_num = int(start)
            end_num = int(end)
            for page_num in range(start_num, end_num + 1):
                thicken_line_alphas[page_num] = alpha

    return thicken_line_alphas


def log_comic_book_params(comic: ComicBook, caching: bool):
    logging.info("")

    calc_panels_bbox_height = int(
        round(
            (comic.srce_av_panels_bbox_height * comic.required_dim.panels_bbox_width)
            / comic.srce_av_panels_bbox_width
        )
    )

    fixes_basename = os.path.basename(comic.srce_fixes_dir)
    panel_segments_basename = os.path.basename(comic.panel_segments_dir)
    dest_basename = os.path.basename(comic.get_dest_dir())
    dest_comic_zip_basename = os.path.basename(comic.get_dest_comic_zip())

    logging.info(f'Comic book series:   "{comic.series_name}".')
    logging.info(f'Comic book title:    "{get_safe_title(comic.get_comic_title())}".')
    logging.info(f'Comic issue title:   "{comic.get_comic_issue_title()}".')
    logging.info(f"Number in series:    {comic.number_in_series}.")
    logging.info(f"Chronological number {comic.chronological_number}.")
    logging.info(f"Caching:             {caching}.")
    logging.info(f"Dest x margin:       {DEST_TARGET_X_MARGIN}.")
    logging.info(f"Dest width:          {DEST_TARGET_WIDTH}.")
    logging.info(f"Dest height:         {DEST_TARGET_HEIGHT}.")
    logging.info(f"Dest aspect ratio:   {DEST_TARGET_ASPECT_RATIO:.2f}.")
    logging.info(f"Dest jpeg quality:   {DEST_JPG_QUALITY}.")
    logging.info(f"Dest compress level: {DEST_JPG_COMPRESS_LEVEL}.")
    logging.info(f"Thicken line alpha:  {len(comic.thicken_line_alphas) > 0}.")
    logging.info(f"Srce min bbox wid:   {comic.srce_min_panels_bbox_width}.")
    logging.info(f"Srce max bbox wid:   {comic.srce_max_panels_bbox_width}.")
    logging.info(f"Srce min bbox hgt:   {comic.srce_min_panels_bbox_height}.")
    logging.info(f"Srce max bbox hgt:   {comic.srce_max_panels_bbox_height}.")
    logging.info(f"Srce av bbox wid:    {comic.srce_av_panels_bbox_width}.")
    logging.info(f"Srce av bbox hgt:    {comic.srce_av_panels_bbox_height}.")
    logging.info(f"Req panels bbox wid: {comic.required_dim.panels_bbox_width}.")
    logging.info(f"Req panels bbox hgt: {comic.required_dim.panels_bbox_height}.")
    logging.info(f"Calc panels bbox ht: {calc_panels_bbox_height}.")
    logging.info(f"Page num y bottom:   {comic.required_dim.page_num_y_bottom}.")
    logging.info(f'Srce root:           "{comic.srce_root_dir}".')
    logging.info(
        f'Srce comic dir:      "SRCE ROOT/{os.path.basename(comic.srce_dir)}".'
    )
    logging.info(f'Srce fixes root:     "{comic.get_srce_fixes_root_dir()}".')
    logging.info(f'Srce fixes dir:      "FIXES ROOT/{fixes_basename}".')
    logging.info(f'Srce segments root:  "{comic.get_srce_segments_root_dir()}".')
    logging.info(f'Srce segments dir:   "SEGMENTS ROOT/{panel_segments_basename}".')
    logging.info(f'Dest root:           "{comic.get_dest_root_dir()}".')
    logging.info(f'Dest comic dir:      "DEST ROOT/{dest_basename}".')
    logging.info(f'Dest zip root:       "{comic.get_dest_zip_root_dir()}".')
    logging.info(f'Dest comic zip:      "ZIP ROOT/{dest_comic_zip_basename}".')
    logging.info(f'Dest zip symlink:    "{comic.get_dest_series_comic_zip_symlink()}".')
    logging.info(f'Work directory:      "{work_dir}".')
    logging.info("")


def create_comic_book(
    dry_run: bool, cfg_file: str, comic: ComicBook, caching: bool
) -> SrceAndDestPages:
    pages = get_srce_and_dest_pages_in_order(comic)

    set_srce_panel_bounding_boxes(dry_run, caching, comic, pages.srce_pages)
    set_required_dimensions(comic, pages.srce_pages)
    set_dest_panel_bounding_boxes(comic, pages)

    log_comic_book_params(comic, caching)

    create_dest_dirs(dry_run, comic)
    process_pages(dry_run, caching, comic, pages)
    process_additional_files(dry_run, cfg_file, comic, pages)

    return pages


def setup_logging(log_level) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=log_level,
    )


def get_config_dir(config_dir_arg: str) -> str:
    config_dir = os.path.realpath(config_dir_arg)

    if not os.path.isdir(config_dir):
        raise Exception(f'Could not find config directory "{config_dir}".')

    return config_dir


def get_config_file(ini_file: str) -> str:
    cfg_file = ini_file
    real_cfg_file = os.path.realpath(cfg_file)

    if os.path.islink(cfg_file):
        logging.debug(f'Converted config symlink "{cfg_file}" to "{real_cfg_file}".')

    if not os.path.isfile(real_cfg_file):
        raise Exception(f'Could not find ini file "{real_cfg_file}".')

    return real_cfg_file


def get_work_dir(wrk_dir_root: str) -> str:
    if not os.path.isdir(wrk_dir_root):
        raise Exception(f'Could not find work root directory "{wrk_dir_root}".')

    wrk_dir = os.path.join(
        wrk_dir_root, datetime.now().strftime("%Y_%m_%d-%H_%M_%S.%f")
    )
    os.makedirs(wrk_dir)

    return wrk_dir


@dataclass
class CmdOptions:
    dry_run: bool = False
    just_symlinks: bool = False
    no_cache: bool = False
    list_cmds: bool = False
    check_integrity: bool = False


def process_all_comic_books(
    options: CmdOptions,
    cfg_dir: str,
    comic_book_info: ComicBookInfoDict,
) -> int:
    ini_files = get_ini_files(cfg_dir)

    if options.check_integrity:
        ret_code = check_comics_integrity(options, ini_files, comic_book_info)
    elif options.list_cmds:
        ret_code = print_all_cmds(options, ini_files)
    else:
        ret_code = process_comic_books(options, cfg_dir, ini_files, comic_book_info)

    return ret_code


def process_comic_books(
    options: CmdOptions,
    cfg_dir: str,
    ini_files: List[str],
    comic_book_info: ComicBookInfoDict,
) -> int:
    logging.info(f'Processing all ini files in "{cfg_dir}".')

    ret_code = 0
    for ini_file in ini_files:
        comic = get_comic_book(comic_book_info, ini_file)
        if 0 != process_comic_book(options, ini_file, comic):
            ret_code = 1

    return ret_code


def print_all_cmds(options: CmdOptions, ini_files: List[str]) -> int:
    assert options.list_cmds

    for ini_file in ini_files:
        if 0 != print_cmd(options, ini_file):
            return 1

    return 0


def get_ini_files(cfg_dir: str) -> List[str]:
    possible_ini_files = [f for f in os.listdir(cfg_dir) if f.endswith(".ini")]

    ini_files = []
    for file in possible_ini_files:
        ini_file = os.path.join(cfg_dir, file)
        if os.path.islink(ini_file):
            logging.debug(f'Skipping ini file symlink in "{ini_file}".')
            continue
        ini_files.append(ini_file)

    return sorted(ini_files)


def process_single_comic_book(
    options: CmdOptions,
    ini_file: str,
    comic_book_info: ComicBookInfoDict,
) -> int:
    comic = get_comic_book(comic_book_info, ini_file)
    return process_comic_book(options, ini_file, comic)


def process_comic_book(
    options: CmdOptions,
    ini_file: str,
    comic: ComicBook,
) -> int:
    process_timing = Timing(datetime.now())

    if options.just_symlinks:
        symlink_comic_book_zip(options.dry_run, comic)
        return 0

    srce_and_dest_pages = build_comic_book(
        options.dry_run, ini_file, options.no_cache, comic
    )

    process_timing.end_time = datetime.now()
    logging.info(
        f"Time taken to complete comic: {process_timing.get_elapsed_time_in_seconds()} seconds"
    )

    write_summary(comic, srce_and_dest_pages, process_timing, not options.no_cache)

    return 0


def check_comics_integrity(
    options: CmdOptions,
    ini_files: List[str],
    comic_book_info: ComicBookInfoDict,
) -> int:
    assert options.check_integrity

    print()

    dest_dirs = []
    zip_files = []
    zip_symlink_dirs = set()
    zip_symlinks = []
    ret_code = 0
    for ini_file in ini_files:
        comic = get_comic_book(comic_book_info, ini_file)

        dest_dirs.append((ini_file, comic.get_dest_dir()))
        zip_files.append(comic.get_dest_comic_zip())
        zip_symlink_dirs.add(comic.get_dest_series_zip_dir())
        zip_symlinks.append(comic.get_dest_series_comic_zip_symlink())

        if 0 != check_out_of_date_files(options, ini_file, comic):
            ret_code = 1

    if 0 != check_unexpected_files(
        dest_dirs, zip_files, zip_symlink_dirs, zip_symlinks
    ):
        ret_code = 1

    return ret_code


@dataclass
class OutOfDateErrors:
    srce_and_dest_files_missing: List[Tuple[str, str]]
    srce_and_dest_files_out_of_date: List[Tuple[str, str]]
    unexpected_dest_files: List[str]
    unexpected_zip_files: List[str]
    unexpected_zip_symlinks: List[str]
    ini_file: str = ""
    is_error: bool = False
    max_srce_timestamp: float = 0.0
    max_dest_timestamp: float = 0.0
    ini_timestamp: float = 0.0
    zip_missing: bool = False
    zip_file: str = ""
    zip_out_of_date_wrt_ini: bool = False
    zip_out_of_date_wrt_srce: bool = False
    zip_out_of_date_wrt_dest: bool = False
    zip_timestamp: float = 0.0
    zip_symlink: str = ""
    zip_symlink_missing: bool = False
    zip_symlink_out_of_date_wrt_ini: bool = False
    zip_symlink_out_of_date_wrt_zip: bool = False
    zip_symlink_timestamp: float = 0.0


def check_out_of_date_files(
    options: CmdOptions,
    ini_file: str,
    comic: ComicBook,
) -> int:
    out_of_date_errors = OutOfDateErrors(
        ini_file=ini_file,
        srce_and_dest_files_out_of_date=[],
        srce_and_dest_files_missing=[],
        unexpected_dest_files=[],
        unexpected_zip_files=[],
        unexpected_zip_symlinks=[],
    )

    check_srce_and_dest_files(comic, out_of_date_errors)
    check_zip_files(comic, out_of_date_errors)

    out_of_date_errors.is_error = (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        or len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
        or len(out_of_date_errors.unexpected_dest_files) > 0
        or len(out_of_date_errors.unexpected_zip_files) > 0
        or len(out_of_date_errors.unexpected_zip_symlinks) > 0
        or out_of_date_errors.zip_missing
        or out_of_date_errors.zip_symlink_missing
        or out_of_date_errors.zip_out_of_date_wrt_srce
        or out_of_date_errors.zip_out_of_date_wrt_dest
        or out_of_date_errors.zip_symlink_out_of_date_wrt_zip
    )

    print_check_errors(out_of_date_errors)

    return 1 if out_of_date_errors.is_error else 0


def check_srce_and_dest_files(
    comic: ComicBook, out_of_date_errors: OutOfDateErrors
) -> None:
    out_of_date_errors.max_srce_timestamp = 0.0
    out_of_date_errors.max_dest_timestamp = 0.0
    out_of_date_errors.num_missing_dest_files = 0
    out_of_date_errors.num_out_of_date_dest_files = 0
    out_of_date_errors.srce_and_dest_files_missing = []
    out_of_date_errors.srce_and_dest_files_out_of_date = []

    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    check_missing_or_out_of_date_dest_files(srce_and_dest_pages, out_of_date_errors)
    check_unexpected_dest_files(comic, srce_and_dest_pages, out_of_date_errors)


def check_missing_or_out_of_date_dest_files(
    srce_and_dest_pages: SrceAndDestPages,
    out_of_date_errors: OutOfDateErrors,
) -> None:
    for pages in zip(srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages):
        srce_page = pages[0]
        dest_page = pages[1]
        if not os.path.isfile(dest_page.filename):
            out_of_date_errors.srce_and_dest_files_missing.append(
                (srce_page.filename, dest_page.filename)
            )
        else:
            srce_timestamp = os.path.getmtime(srce_page.filename)
            if out_of_date_errors.max_srce_timestamp < srce_timestamp:
                out_of_date_errors.max_srce_timestamp = srce_timestamp

            dest_timestamp = os.path.getmtime(dest_page.filename)
            if out_of_date_errors.max_dest_timestamp < dest_timestamp:
                out_of_date_errors.max_dest_timestamp = dest_timestamp

            if srce_timestamp > dest_timestamp:
                out_of_date_errors.srce_and_dest_files_out_of_date.append(
                    (srce_page.filename, dest_page.filename)
                )


def check_unexpected_dest_files(
    comic: ComicBook,
    srce_and_dest_pages: SrceAndDestPages,
    out_of_date_errors: OutOfDateErrors,
) -> None:
    allowed_dest_files = [f.filename for f in srce_and_dest_pages.dest_pages]
    dest_dir = comic.get_dest_image_dir()
    for file in os.listdir(dest_dir):
        dest_file = os.path.join(dest_dir, file)
        if dest_file not in allowed_dest_files:
            out_of_date_errors.unexpected_dest_files.append(dest_file)


def check_unexpected_files(
    dest_dirs_info_list: List[Tuple[str, str]],
    zip_files: List[str],
    zip_symlink_dirs: Set[str],
    zip_symlinks: List[str],
) -> int:
    ret_code = 0

    print()

    allowed_dest_non_image_files = {
        "clean_summary.txt",
        "comic-metadata.json",
        "dest-panels-bboxes.json",
        "metadata.txt",
        "readme.txt",
        "srce-dest-map.json",
    }
    for dest_dir_info in dest_dirs_info_list:
        ini_file = os.path.basename(dest_dir_info[0])
        dest_dir = dest_dir_info[1]

        for file in os.listdir(dest_dir):
            if file in ["images", ini_file]:
                continue
            if file not in allowed_dest_non_image_files:
                print(f'ERROR: The dest file "{file}" was unexpected.')
                ret_code = 1

    if dest_dirs_info_list:
        dest_dirs = [d[1] for d in dest_dirs_info_list]
        dest_dir = os.path.dirname(dest_dirs[0])
        for file in os.listdir(dest_dir):
            dest_file = os.path.join(dest_dir, file)
            if dest_file not in dest_dirs:
                print(f'ERROR: The dest file "{dest_file}" was unexpected.')
                ret_code = 1

    if zip_files:
        dest_dir = os.path.dirname(zip_files[0])
        for file in os.listdir(dest_dir):
            dest_file = os.path.join(dest_dir, file)
            if dest_file not in zip_files:
                print(f'ERROR: The zip file "{dest_file}" was unexpected.')
                ret_code = 1

    if zip_symlinks:
        for dest_dir in zip_symlink_dirs:
            for file in os.listdir(dest_dir):
                dest_file = os.path.join(dest_dir, file)
                if dest_file not in zip_symlinks:
                    print(f'ERROR: The zip symlink "{dest_file}" was unexpected.')
                    ret_code = 1

    if ret_code != 0:
        print()

    return ret_code


def check_zip_files(comic: ComicBook, out_of_date_errors: OutOfDateErrors) -> None:
    if not os.path.exists(comic.get_dest_comic_zip()):
        out_of_date_errors.zip_missing = True
        out_of_date_errors.zip_file = comic.get_dest_comic_zip()
        return

    zip_timestamp = os.path.getmtime(comic.get_dest_comic_zip())
    if zip_timestamp < out_of_date_errors.max_srce_timestamp:
        out_of_date_errors.zip_out_of_date_wrt_srce = True
        out_of_date_errors.zip_timestamp = zip_timestamp
        out_of_date_errors.zip_file = comic.get_dest_comic_zip()

    if zip_timestamp < out_of_date_errors.max_dest_timestamp:
        out_of_date_errors.zip_out_of_date_wrt_dest = True
        out_of_date_errors.zip_timestamp = zip_timestamp
        out_of_date_errors.zip_file = comic.get_dest_comic_zip()

    ini_timestamp = os.path.getmtime(out_of_date_errors.ini_file)
    if zip_timestamp < ini_timestamp:
        out_of_date_errors.zip_out_of_date_wrt_ini = True
        out_of_date_errors.zip_timestamp = zip_timestamp
        out_of_date_errors.zip_file = comic.get_dest_comic_zip()
        out_of_date_errors.ini_timestamp = ini_timestamp

    if not os.path.exists(comic.get_dest_series_comic_zip_symlink()):
        out_of_date_errors.zip_symlink_missing = True
        out_of_date_errors.zip_symlink = comic.get_dest_series_comic_zip_symlink()
        return

    zip_symlink_timestamp = os.lstat(comic.get_dest_series_comic_zip_symlink()).st_mtime
    if zip_symlink_timestamp < zip_timestamp:
        out_of_date_errors.zip_symlink_out_of_date_wrt_zip = True
        out_of_date_errors.zip_symlink_timestamp = zip_symlink_timestamp
        out_of_date_errors.zip_symlink = comic.get_dest_series_comic_zip_symlink()
        out_of_date_errors.zip_timestamp = zip_timestamp
        out_of_date_errors.zip_file = comic.get_dest_comic_zip()

    if zip_symlink_timestamp < ini_timestamp:
        out_of_date_errors.zip_symlink_out_of_date_wrt_ini = True
        out_of_date_errors.zip_symlink_timestamp = zip_symlink_timestamp
        out_of_date_errors.zip_symlink = comic.get_dest_series_comic_zip_symlink()
        out_of_date_errors.ini_timestamp = ini_timestamp


def print_check_errors(out_of_date_errors: OutOfDateErrors) -> None:
    if (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        or len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
    ):
        print_out_of_date_or_missing_errors(out_of_date_errors)

    if out_of_date_errors.zip_missing:
        print(
            f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip file "{out_of_date_errors.zip_file}" is missing.'
        )

    if out_of_date_errors.zip_symlink_missing:
        print(
            f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip symlink "{out_of_date_errors.zip_symlink}" is missing.'
        )

    if out_of_date_errors.zip_out_of_date_wrt_srce:
        max_srce_date = datetime.fromtimestamp(out_of_date_errors.max_srce_timestamp)
        file_date = datetime.fromtimestamp(out_of_date_errors.zip_timestamp)
        print(
            f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip file "{out_of_date_errors.zip_file}" timestamp'
            f' {file_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}, is less than the max srce'
            f' file timestamp {max_srce_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}.'
        )

    if out_of_date_errors.zip_out_of_date_wrt_dest:
        max_dest_date = datetime.fromtimestamp(out_of_date_errors.max_dest_timestamp)
        file_date = datetime.fromtimestamp(out_of_date_errors.zip_timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip file "{out_of_date_errors.zip_file}" timestamp'
            f' {file_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}, is less than the max dest'
            f' file timestamp {max_dest_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}.'
        )

    if out_of_date_errors.zip_out_of_date_wrt_ini:
        ini_date = datetime.fromtimestamp(out_of_date_errors.ini_timestamp)
        file_date = datetime.fromtimestamp(out_of_date_errors.zip_timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip file "{out_of_date_errors.zip_file}" timestamp'
            f' {file_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}, is less than the ini'
            f' file timestamp {ini_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}.'
        )

    if out_of_date_errors.zip_symlink_out_of_date_wrt_zip:
        symlink_date = datetime.fromtimestamp(out_of_date_errors.zip_symlink_timestamp)
        zip_date = datetime.fromtimestamp(out_of_date_errors.zip_timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip symlink "{out_of_date_errors.zip_symlink}" timestamp'
            f' {symlink_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}, is less than the zip'
            f' file "{out_of_date_errors.zip_file}" timestamp'
            f' {zip_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}.'
        )

    if out_of_date_errors.zip_symlink_out_of_date_wrt_ini:
        ini_date = datetime.fromtimestamp(out_of_date_errors.ini_timestamp)
        symlink_date = datetime.fromtimestamp(out_of_date_errors.zip_symlink_timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f' the zip symlink "{out_of_date_errors.zip_symlink}" timestamp'
            f' {symlink_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}, is less than the ini'
            f' file timestamp {ini_date.strftime("%Y_%m_%d-%H_%M_%S.%f")}.'
        )

    if (
        len(out_of_date_errors.unexpected_dest_files) > 0
        or len(out_of_date_errors.unexpected_zip_files) > 0
        or len(out_of_date_errors.unexpected_zip_symlinks) > 0
    ):
        print_unexpected_dest_files_errors(out_of_date_errors)


def print_unexpected_dest_files_errors(out_of_date_errors: OutOfDateErrors) -> None:
    for file in out_of_date_errors.unexpected_dest_files:
        print(f'ERROR: The dest file "{file}" was unexpected.')
    for file in out_of_date_errors.unexpected_zip_files:
        print(f'ERROR: The zip file "{file}" was unexpected.')
    for file in out_of_date_errors.unexpected_zip_symlinks:
        print(f'ERROR: The zip symlink "{file}" was unexpected.')


def print_out_of_date_or_missing_errors(out_of_date_errors: OutOfDateErrors) -> None:
    for srce_dest in out_of_date_errors.srce_and_dest_files_missing:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(
            f'ERROR: There is no dest file "{dest_file}"'
            f' matching srce file "{srce_file}".'
        )
    for srce_dest in out_of_date_errors.srce_and_dest_files_out_of_date:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(f"ERROR: {get_out_of_date_file_msg(srce_file, dest_file)}")

    if (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        or len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
    ):
        print()

    if (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        and len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
    ):
        print(
            f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
            f" there are {len(out_of_date_errors.srce_and_dest_files_missing)} missing dest files"
            f" and {len(out_of_date_errors.srce_and_dest_files_out_of_date)} out of date"
            f" dest files.\n"
        )
    else:
        if len(out_of_date_errors.srce_and_dest_files_missing) > 0:
            print(
                f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
                f" there are {len(out_of_date_errors.srce_and_dest_files_missing)} missing"
                f" dest files.\n"
            )

        if len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0:
            print(
                f'ERROR: For "{get_shorter_ini_filename(out_of_date_errors.ini_file)}",'
                f" there are {len(out_of_date_errors.srce_and_dest_files_out_of_date)} out of"
                f" date dest files.\n"
            )


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def print_cmd(options: CmdOptions, ini_file: str) -> int:
    dry_run_arg = "" if not options.dry_run else f" {DRY_RUN_ARG}"
    just_symlinks_arg = "" if not options.just_symlinks else f" {JUST_SYMLINKS_ARG}"
    no_cache_arg = "" if not options.no_cache else f" {NO_CACHE_ARG}"
    print(
        f"python3 {__file__}{dry_run_arg}{just_symlinks_arg}{no_cache_arg}"
        f' {WORK_DIR_ARG} "{work_dir_root}" {INI_FILE_ARG} {shlex.quote(ini_file)}'
    )

    return 0


def build_comic_book(
    dry_run: bool, cfg_file: str, no_cache: bool, comic: ComicBook
) -> SrceAndDestPages:
    srce_and_dest_pages = create_comic_book(dry_run, cfg_file, comic, not no_cache)

    zip_comic_book(dry_run, comic)
    symlink_comic_book_zip(dry_run, comic)

    return srce_and_dest_pages


CONFIG_DIR_ARG = "--config-dir"
INI_FILE_ARG = "--ini-file"
LOG_LEVEL_ARG = "--log-level"
DRY_RUN_ARG = "--dry-run"
JUST_SYMLINKS_ARG = "--just-symlinks"
WORK_DIR_ARG = "--work-dir"
NO_CACHE_ARG = "--no-cache"
LIST_CMDS_ARG = "--list-cmds"
CHECK_INTEGRITY = "--check-integrity"


def get_args():
    parser = argparse.ArgumentParser(
        description="Create a clean Barks comic from Fantagraphics source."
    )
    parser.add_argument(CONFIG_DIR_ARG, action="store", type=str, required=False)
    parser.add_argument(INI_FILE_ARG, action="store", type=str, required=False)
    parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    parser.add_argument(DRY_RUN_ARG, action="store_true", required=False, default=False)
    parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    parser.add_argument(WORK_DIR_ARG, type=str, required=True)
    parser.add_argument(
        NO_CACHE_ARG, action="store_true", required=False, default=False
    )
    parser.add_argument(
        LIST_CMDS_ARG, action="store_true", required=False, default=False
    )
    parser.add_argument(
        CHECK_INTEGRITY, action="store_true", required=False, default=False
    )

    args = parser.parse_args()

    if args.config_dir and args.ini_file:
        print(
            f"Argument error: Cannot have both '{CONFIG_DIR_ARG}' and '{INI_FILE_ARG}'."
        )
        return None
    if not args.config_dir and not args.ini_file:
        print(
            f"Argument error: You need to specify one of '{CONFIG_DIR_ARG}' or '{INI_FILE_ARG}'."
        )
        return None

    return args


if __name__ == "__main__":
    cmd_args = get_args()
    if not cmd_args:
        sys.exit(1)

    setup_logging(cmd_args.log_level)

    work_dir_root = cmd_args.work_dir
    work_dir = get_work_dir(work_dir_root)
    bounding_box_processor = BoundingBoxProcessor(work_dir)
    all_comic_book_info = get_all_comic_book_info(
        str(os.path.join(THIS_DIR, PUBLICATION_INFO_DIRNAME, STORIES_INFO_FILENAME))
    )

    cmd_options = CmdOptions(
        dry_run=cmd_args.dry_run,
        just_symlinks=cmd_args.just_symlinks,
        no_cache=cmd_args.no_cache,
        list_cmds=cmd_args.list_cmds,
        check_integrity=cmd_args.check_integrity,
    )

    if cmd_args.config_dir:
        exit_code = process_all_comic_books(
            cmd_options,
            get_config_dir(cmd_args.config_dir),
            all_comic_book_info,
        )
    else:
        exit_code = process_single_comic_book(
            cmd_options,
            get_config_file(cmd_args.ini_file),
            all_comic_book_info,
        )

    if exit_code != 0:
        print(f"\nThere were errors: exit code = {exit_code}.")
        sys.exit(exit_code)
