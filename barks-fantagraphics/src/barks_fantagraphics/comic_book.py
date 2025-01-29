import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union

from .comics_consts import (
    PageType,
    IMAGES_SUBDIR,
    BOUNDED_SUBDIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_COMICS_DIR,
    THE_YEARS_COMICS_DIR,
    INSET_FILE_EXT,
    STORY_PAGE_TYPES,
)
from .comics_info import (
    JPG_FILE_EXT,
    PNG_FILE_EXT,
    SVG_FILE_EXT,
    JSON_FILE_EXT,
    ISSUE_NAME_AS_TITLE,
    MONTH_AS_LONG_STR,
    CENSORED_TITLES,
    SILENT_NIGHT,
    SILENT_NIGHT_PUBLICATION_ISSUE,
    ComicBookInfo,
    SourceBook,
    get_formatted_day,
)
from .comics_utils import get_abbrev_path

INTRO_TITLE_DEFAULT_FONT_SIZE = 155
INTRO_AUTHOR_DEFAULT_FONT_SIZE = 90


@dataclass
class OriginalPage:
    page_filenames: str
    page_type: PageType


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


@dataclass
class ComicBook:
    ini_file: str
    title: str
    title_font_file: str
    title_font_size: int
    # NOTE: Need 'issue_title' to force a series title that has
    #       changed from another title. E.g., FC 495 == Uncle Scrooge #3
    issue_title: str
    author_font_size: int
    srce_min_panels_bbox_width: int
    srce_max_panels_bbox_width: int
    srce_min_panels_bbox_height: int
    srce_max_panels_bbox_height: int
    srce_av_panels_bbox_width: int
    srce_av_panels_bbox_height: int
    required_dim: RequiredDimensions
    fanta_info: SourceBook
    srce_dir: str
    srce_dir_num_page_files: int
    srce_upscayled_dir: str
    srce_restored_dir: str
    srce_restored_upscayled_dir: str
    srce_restored_svg_dir: str
    srce_restored_ocr_dir: str
    srce_fixes_dir: str
    srce_upscayled_fixes_dir: str
    srce_restored_fixes_dir: str  # TODO: Get rid of this????
    panel_segments_dir: str
    series_name: str
    number_in_series: int
    chronological_number: int
    intro_inset_file: str
    publication_date: str
    submitted_date: str
    submitted_year: int
    publication_text: str
    comic_book_info: ComicBookInfo
    config_page_images: List[OriginalPage]
    page_images_in_order: List[OriginalPage]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0
        assert self.title or not self.is_barks_title()

    def is_barks_title(self) -> bool:
        return self.comic_book_info.is_barks_title

    def get_srce_image_dir(self) -> str:
        return os.path.join(self.srce_dir, IMAGES_SUBDIR)

    def get_srce_upscayled_image_dir(self) -> str:
        return os.path.join(self.srce_upscayled_dir, IMAGES_SUBDIR)

    def get_srce_restored_image_dir(self) -> str:
        return os.path.join(self.srce_restored_dir, IMAGES_SUBDIR)

    def get_srce_restored_upscayled_image_dir(self) -> str:
        return os.path.join(self.srce_restored_upscayled_dir, IMAGES_SUBDIR)

    def get_srce_restored_svg_image_dir(self) -> str:
        return os.path.join(self.srce_restored_svg_dir, IMAGES_SUBDIR)

    def get_srce_restored_ocr_image_dir(self) -> str:
        return os.path.join(self.srce_restored_ocr_dir, IMAGES_SUBDIR)

    def get_srce_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_fixes_dir, IMAGES_SUBDIR)

    def get_srce_upscayled_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_upscayled_fixes_dir, IMAGES_SUBDIR)

    def get_srce_fixes_bounded_dir(self) -> str:
        return os.path.join(self.get_srce_fixes_image_dir(), BOUNDED_SUBDIR)

    def get_srce_restored_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_restored_fixes_dir, IMAGES_SUBDIR)

    def get_srce_restored_fixes_bounded_dir(self) -> str:
        return os.path.join(self.get_srce_restored_fixes_image_dir(), BOUNDED_SUBDIR)

    def get_srce_upscayled_story_files(self, page_types: List[PageType]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_upscayled_story_file(page.page_filenames))

        return all_files

    def get_final_srce_upscayled_story_files(
        self, page_types: List[PageType]
    ) -> List[Tuple[str, bool]]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                file, modified = self.get_srce_upscayled_with_fixes_story_file(
                    page.page_filenames, page.page_type
                )
                all_files.append((file, modified))

        return all_files

    # TODO: Simplify these duplications
    # TODO: Not needed once everything is restored??????
    def get_srce_restored_story_files(self, page_types: List[PageType]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_restored_story_file(page.page_filenames))

        return all_files

    def get_srce_restored_upscayled_story_files(self, page_types: List[PageType]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_restored_upscayled_story_file(page.page_filenames))

        return all_files

    def get_srce_restored_svg_story_files(self, page_types: List[PageType]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_restored_svg_story_file(page.page_filenames))

        return all_files

    def get_srce_restored_ocr_story_files(
        self, page_types: List[PageType]
    ) -> List[Tuple[str, str]]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_restored_ocr_story_file(page.page_filenames))

        return all_files

    def get_original_srce_story_files(self, page_types: Union[None, List[PageType]]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if not page_types or page.page_type in page_types:
                file = self.get_original_srce_story_file(page.page_filenames, page.page_type)
                all_files.append(file)

        return all_files

    def get_final_srce_story_files(
        self, page_types: Union[None, List[PageType]]
    ) -> List[Tuple[str, bool]]:
        all_files = []
        for page in self.page_images_in_order:
            if not page_types or page.page_type in page_types:
                file, modified = self.get_final_srce_story_file(page.page_filenames, page.page_type)
                all_files.append((file, modified))

        return all_files

    def get_srce_with_fixes_story_files(self, page_types: List[PageType]) -> List[Tuple[str, bool]]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                file, modified = self.get_srce_with_fixes_story_file(
                    page.page_filenames, page.page_type
                )
                all_files.append((file, modified))

        return all_files

    def get_srce_panel_segments_files(self, page_types: List[PageType]) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.get_srce_panel_segments_file(page.page_filenames))

        return all_files

    def get_srce_upscayled_story_file(self, page_num: str) -> str:
        return str(os.path.join(self.get_srce_upscayled_image_dir(), page_num + PNG_FILE_EXT))

    def get_srce_restored_story_file(self, page_num: str) -> str:
        return str(os.path.join(self.get_srce_restored_image_dir(), page_num + PNG_FILE_EXT))

    def get_srce_restored_upscayled_story_file(self, page_num: str) -> str:
        return str(
            os.path.join(self.get_srce_restored_upscayled_image_dir(), page_num + PNG_FILE_EXT)
        )

    def get_srce_restored_svg_story_file(self, page_num: str) -> str:
        return str(os.path.join(self.get_srce_restored_svg_image_dir(), page_num + SVG_FILE_EXT))

    def get_srce_restored_ocr_story_file(self, page_num: str) -> Tuple[str, str]:
        return (
            str(os.path.join(self.srce_restored_ocr_dir, page_num + ".easyocr" + JSON_FILE_EXT)),
            str(os.path.join(self.srce_restored_ocr_dir, page_num + ".paddleocr" + JSON_FILE_EXT)),
        )

    def get_srce_panel_segments_file(self, page_num: str) -> str:
        return str(os.path.join(self.panel_segments_dir, page_num + JSON_FILE_EXT))

    def get_srce_upscayled_with_fixes_story_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_upscayled_file = self.get_srce_upscayled_story_file(page_num)

        srce_upscayled_fixes_file = str(
            os.path.join(self.get_srce_upscayled_fixes_image_dir(), page_num + JPG_FILE_EXT)
        )
        if os.path.isfile(srce_upscayled_fixes_file):
            raise Exception(
                f'Upscayled fixes file must be .png not .jpg: "{srce_upscayled_fixes_file}".'
            )
        srce_upscayled_fixes_file = str(
            os.path.join(self.get_srce_upscayled_fixes_image_dir(), page_num + PNG_FILE_EXT)
        )

        if not os.path.isfile(srce_upscayled_fixes_file):
            return srce_upscayled_file, False

        if os.path.isfile(srce_upscayled_file):
            logging.info(
                f"NOTE: Using upscayled fixes srce file:"
                f' "{get_abbrev_path(srce_upscayled_fixes_file)}".'
            )
            if page_type not in [PageType.COVER, PageType.BODY]:
                raise Exception(f"Expected upscayled fixes page to be COVER or BODY: '{page_num}'.")
        else:
            logging.info(
                f"NOTE: Using added srce upscayled file of type {page_type.name}:"
                f' "{get_abbrev_path(srce_upscayled_fixes_file)}".'
            )
            if page_type in [PageType.COVER, PageType.BODY]:
                raise Exception(f"Expected added page to be NOT COVER OR BODY: '{page_num}'.")

        is_modified_file = page_type in [PageType.COVER, PageType.BODY]

        return srce_upscayled_fixes_file, is_modified_file

    def get_original_srce_story_file(self, page_num: str, page_type: PageType) -> str:
        if page_type == PageType.TITLE:
            return "TITLE PAGE"

        return str(os.path.join(self.get_srce_image_dir(), page_num + JPG_FILE_EXT))

    def get_final_srce_story_file(self, page_num: str, page_type: PageType) -> Tuple[str, bool]:
        if page_type == PageType.TITLE:
            srce_file, is_modified = "TITLE PAGE", False
            return srce_file, is_modified
        elif page_type in [
            PageType.FRONT,
            PageType.COVER,
            PageType.PAINTING,
            PageType.BACK_NO_PANELS,
        ]:
            srce_file, is_modified = self.get_srce_with_fixes_story_file(page_num, page_type)
            if os.path.isfile(srce_file):
                return srce_file, is_modified

        srce_restored_file, is_modified = self.get_srce_restored_with_fixes_file(
            page_num, page_type
        )
        if os.path.isfile(srce_restored_file):
            return srce_restored_file, is_modified

        raise Exception(f'Could not find restored source file "{srce_restored_file}".')

    def get_srce_with_fixes_story_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_file = str(os.path.join(self.get_srce_image_dir(), page_num + JPG_FILE_EXT))
        srce_fixes_file = str(
            os.path.join(self.get_srce_fixes_image_dir(), page_num + JPG_FILE_EXT)
        )
        if not os.path.isfile(srce_fixes_file):
            return srce_file, False

        if os.path.isfile(srce_file):
            if self._is_fixes_special_case(page_num, page_type):
                logging.info(
                    f"NOTE: Special case - using {page_type.name} fixes srce file:"
                    f' "{get_abbrev_path(srce_fixes_file)}".'
                )
            else:
                logging.info(f'NOTE: Using fixes srce file: "{get_abbrev_path(srce_fixes_file)}".')
                if page_type not in [PageType.COVER, PageType.BODY]:
                    raise Exception(f"Expected fixes page to be COVER or BODY: '{page_num}'.")
        elif self._is_fixes_special_case(page_num, page_type):
            logging.info(
                f"NOTE: Special case - using ADDED fixes srce file for {page_type.name} page:"
                f' "{get_abbrev_path(srce_fixes_file)}".'
            )
        else:
            logging.info(
                f"NOTE: Using added srce file of type {page_type.name}:"
                f' "{get_abbrev_path(srce_fixes_file)}".'
            )
            if page_type in [PageType.COVER, PageType.BODY]:
                raise Exception(f"Expected added page to be NOT COVER OR BODY: '{page_num}'.")

        is_modified_file = page_type in [PageType.COVER, PageType.BODY]

        return srce_fixes_file, is_modified_file

    def get_srce_restored_with_fixes_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_restored_file = str(
            os.path.join(self.get_srce_restored_image_dir(), page_num + JPG_FILE_EXT)
        )
        if os.path.isfile(srce_restored_file):
            raise Exception(f'Restored files should be png not jpg: "{srce_restored_file}".')
        srce_restored_fixes_file = str(
            os.path.join(self.get_srce_restored_fixes_image_dir(), page_num + JPG_FILE_EXT)
        )
        if os.path.isfile(srce_restored_fixes_file):
            raise Exception(
                f'Restored fixes files should be png not jpg: "{srce_restored_fixes_file}".'
            )

        srce_restored_file = str(
            os.path.join(self.get_srce_restored_image_dir(), page_num + PNG_FILE_EXT)
        )
        srce_restored_fixes_file = str(
            os.path.join(self.get_srce_restored_fixes_image_dir(), page_num + PNG_FILE_EXT)
        )

        if not os.path.isfile(srce_restored_fixes_file):
            return srce_restored_file, False

        if os.path.isfile(srce_restored_file):
            if self._is_fixes_special_case(page_num, page_type):
                logging.info(
                    f"NOTE: Special case - using {page_type.name} restored fixes srce file:"
                    f' "{get_abbrev_path(srce_restored_fixes_file)}".'
                )
            else:
                logging.info(
                    f"NOTE: Using restored fixes srce file:"
                    f' "{get_abbrev_path(srce_restored_fixes_file)}".'
                )
                if page_type not in [PageType.COVER, PageType.BODY]:
                    raise Exception(
                        f"Expected restored fixes page to be COVER or BODY:" f' "{page_num}".'
                    )
        elif self._is_fixes_special_case(page_num, page_type):
            logging.info(
                f"NOTE: Special case - using ADDED restored fixes srce file for"
                f' {page_type.name} page: "{get_abbrev_path(srce_restored_fixes_file)}".'
            )
        else:
            logging.info(
                f"NOTE: Using added srce restored file of type {page_type.name}:"
                f' "{get_abbrev_path(srce_restored_fixes_file)}".'
            )
            if page_type in [PageType.COVER, PageType.BODY]:
                raise Exception(f"Expected added page to be NOT COVER OR BODY: '{page_num}'.")

        is_modified_file = page_type in [PageType.COVER, PageType.BODY]

        return srce_restored_fixes_file, is_modified_file

    def _is_fixes_special_case(self, page_num: str, page_type: PageType) -> bool:
        if get_safe_title(self.title) == "Back to Long Ago!" and page_num == "209":
            return page_type == PageType.BACK_NO_PANELS
        if self.get_ini_title() == "The Bill Collectors" and page_num == "227":
            return page_type == PageType.BODY
        if self.get_ini_title() in CENSORED_TITLES:
            return page_type == PageType.BODY

        return False

    def get_fixes_panel_bounds_file(self, page_num: int) -> str:
        panels_bounds_file = os.path.join(
            self.get_srce_fixes_bounded_dir(), get_page_str(page_num) + JPG_FILE_EXT
        )
        panels_bounds_restored_file = os.path.join(
            self.get_srce_restored_fixes_bounded_dir(), get_page_str(page_num) + PNG_FILE_EXT
        )

        if os.path.isfile(panels_bounds_file):
            if os.path.isfile(panels_bounds_restored_file):
                raise Exception(
                    f"Cannot have fixes and restored fixes bounds files: "
                    f'"{panels_bounds_file}" and'
                    f'"{panels_bounds_restored_file}".'
                )
            return panels_bounds_file

        if os.path.isfile(panels_bounds_restored_file):
            return panels_bounds_restored_file

        return ""

    # TODO: Should dest stuff be elsewhere??
    def get_dest_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIRS_DIR

    def get_dest_dir(self) -> str:
        return os.path.join(
            self.get_dest_root_dir(),
            self.get_dest_rel_dirname(),
        )

    def get_dest_rel_dirname(self) -> str:
        dir_title = _get_lookup_title(self.title, self.get_ini_title())
        return f"{self.chronological_number:03d} {dir_title}"

    def get_series_comic_title(self) -> str:
        return f"{self.series_name} {self.number_in_series}"

    def get_dest_image_dir(self) -> str:
        return os.path.join(self.get_dest_dir(), IMAGES_SUBDIR)

    def get_dest_zip_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIR

    def get_dest_series_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            self.series_name,
        )

    def get_dest_year_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_YEARS_COMICS_DIR,
            str(self.submitted_year),
        )

    def get_dest_comic_zip_filename(self) -> str:
        return f"{self.get_title_with_issue_num()}.cbz"

    def get_dest_comic_zip(self) -> str:
        return os.path.join(self.get_dest_zip_root_dir(), self.get_dest_comic_zip_filename())

    def get_dest_series_comic_zip_symlink_filename(self) -> str:
        file_title = _get_lookup_title(self.title, self.get_ini_title())
        full_title = f"{file_title} [{self.get_comic_issue_title()}]"
        return f"{self.number_in_series:03d} {full_title}.cbz"

    def get_dest_series_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_series_zip_symlink_dir()}",
            f"{self.get_dest_series_comic_zip_symlink_filename()}",
        )

    def get_dest_year_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_year_zip_symlink_dir()}",
            f"{self.get_dest_comic_zip_filename()}",
        )

    def get_ini_title(self) -> str:
        return Path(self.ini_file).stem

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
        return self.comic_book_info.get_issue_title()

    def get_title_with_issue_num(self) -> str:
        return f"{self.get_dest_rel_dirname()} [{self.get_comic_issue_title()}]"


def _get_lookup_title(title: str, file_title: str) -> str:
    if title != "":
        return get_safe_title(title)

    assert file_title != ""
    return file_title


def get_safe_title(title: str) -> str:
    safe_title = title.replace("\n", " ")
    safe_title = safe_title.replace("- ", "-")
    safe_title = safe_title.replace('"', "")
    return safe_title


def get_main_publication_info(
    file_title: str, cb_info: ComicBookInfo, fanta_info: SourceBook
) -> str:
    if file_title == SILENT_NIGHT:
        # Originally intended for WDCS 64
        publication_text = (
            f"(*) Rejected by Western editors in 1945, this story was originally\n"
            f" intended for publication in {get_formatted_first_published_str(cb_info)}\n"
            + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
            + f"\n"
            + f"The story was also not published in the Fantagraphics CBDL but\n"
            + f"fortunately did appear in {SILENT_NIGHT_PUBLICATION_ISSUE}\n"
            + f"Color restoration by {cb_info.colorist}"
        )
        return publication_text

    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published in {fanta_info.pub} CBDL,"
        + f" Volume {fanta_info.volume}, {fanta_info.year}\n"
        + f"Color restoration by {cb_info.colorist}"
    )

    return publication_text


def _get_pages_in_order(config_pages: List[OriginalPage]) -> List[OriginalPage]:
    page_images = []
    for config_page in config_pages:
        if "-" not in config_page.page_filenames:
            page_images.append(config_page)
        else:
            start, end = config_page.page_filenames.split("-")
            start_num = int(start)
            end_num = int(end)
            for file_num in range(start_num, end_num + 1):
                filename = get_page_str(file_num)
                page_images.append(OriginalPage(filename, config_page.page_type))

    return page_images


def get_page_str(page_num: int) -> str:
    return f"{page_num:03d}"


def get_page_num_str(filename: str) -> str:
    return Path(filename).stem


def get_inset_file(ini_file: str) -> str:
    prefix = Path(ini_file).stem
    inset_filename = prefix + " Inset" + INSET_FILE_EXT
    ini_file_dir = os.path.dirname(ini_file)

    return str(os.path.join(ini_file_dir, inset_filename))


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


def get_story_files(image_dir: str, comic: ComicBook, file_ext: str) -> List[str]:
    return get_story_files_of_page_type(image_dir, comic, file_ext, STORY_PAGE_TYPES)


def get_story_files_of_page_type(
    image_dir: str, comic: ComicBook, file_ext: str, page_types: List[PageType]
) -> List[str]:
    srce_pages = comic.page_images_in_order
    all_files = []
    for page in srce_pages:
        if page.page_type in page_types:
            all_files.append(os.path.join(image_dir, page.page_filenames + file_ext))

    return all_files


def get_abbrev_jpg_page_list(comic: ComicBook) -> List[str]:
    return get_abbrev_jpg_page_of_type_list(comic, STORY_PAGE_TYPES)


def get_abbrev_jpg_page_of_type_list(comic: ComicBook, page_types: List[PageType]) -> List[str]:
    all_pages = []
    for page in comic.config_page_images:
        if page.page_type in page_types:
            all_pages.append(page.page_filenames)

    return all_pages


def get_jpg_page_list(comic: ComicBook) -> List[str]:
    return get_jpg_page_of_type_list(comic, STORY_PAGE_TYPES)


def get_jpg_page_of_type_list(comic: ComicBook, page_types: List[PageType]) -> List[str]:
    all_pages = []
    for page in comic.page_images_in_order:
        if page.page_type in page_types:
            all_pages.append(page.page_filenames)

    return all_pages
