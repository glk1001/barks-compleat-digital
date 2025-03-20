import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union, Callable

from .comics_consts import (
    PageType,
    IMAGES_SUBDIR,
    BOUNDED_SUBDIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_COMICS_DIR,
    THE_YEARS_COMICS_DIR,
    INSET_FILE_EXT,
    RESTORABLE_PAGE_TYPES,
    STORY_PAGE_TYPES,
    STORY_PAGE_TYPES_STR_LIST,
)
from .comics_info import (
    JPG_FILE_EXT,
    PNG_FILE_EXT,
    SVG_FILE_EXT,
    JSON_FILE_EXT,
    ISSUE_NAME_AS_TITLE,
    MONTH_AS_LONG_STR,
    CENSORED_TITLES,
    THE_MILKMAN,
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
class ComicDimensions:
    min_panels_bbox_width: int = -1
    max_panels_bbox_width: int = -1
    min_panels_bbox_height: int = -1
    max_panels_bbox_height: int = -1
    av_panels_bbox_width: int = -1
    av_panels_bbox_height: int = -1


@dataclass
class ComicBookDirs:
    srce_dir: str
    srce_upscayled_dir: str
    srce_restored_dir: str
    srce_restored_upscayled_dir: str
    srce_restored_svg_dir: str
    srce_restored_ocr_dir: str
    srce_fixes_dir: str
    srce_upscayled_fixes_dir: str
    panel_segments_dir: str


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

    srce_dim: ComicDimensions
    required_dim: RequiredDimensions

    fanta_info: SourceBook
    srce_dir_num_page_files: int
    dirs: ComicBookDirs

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

    @staticmethod
    def __get_image_subdir(dirpath: str) -> str:
        return os.path.join(dirpath, IMAGES_SUBDIR)

    def get_srce_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_dir)

    def get_srce_upscayled_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_upscayled_dir)

    def get_srce_restored_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_restored_dir)

    def get_srce_restored_upscayled_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_restored_upscayled_dir)

    def get_srce_restored_svg_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_restored_svg_dir)

    def get_srce_restored_ocr_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_restored_ocr_dir)

    def get_srce_original_fixes_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_fixes_dir)

    def get_srce_upscayled_fixes_image_dir(self) -> str:
        return self.__get_image_subdir(self.dirs.srce_upscayled_fixes_dir)

    def get_srce_original_fixes_bounded_dir(self) -> str:
        return os.path.join(self.get_srce_original_fixes_image_dir(), BOUNDED_SUBDIR)

    def get_srce_original_story_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.__get_srce_original_story_file)

    def get_srce_upscayled_story_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.get_srce_upscayled_story_file)

    def get_srce_restored_story_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.__get_srce_restored_story_file)

    def get_srce_restored_upscayled_story_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.get_srce_restored_upscayled_story_file)

    def get_srce_restored_svg_story_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.get_srce_restored_svg_story_file)

    def get_srce_restored_ocr_story_files(
        self, page_types: List[PageType]
    ) -> List[Tuple[str, str]]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(self.__get_srce_restored_ocr_story_file(page.page_filenames))

        return all_files

    def get_srce_panel_segments_files(self, page_types: List[PageType]) -> List[str]:
        return self.__get_story_files(page_types, self.get_srce_panel_segments_file)

    def get_final_srce_original_story_files(
        self, page_types: List[PageType]
    ) -> List[Tuple[str, bool]]:
        return self.__get_story_files_with_mods(page_types, self.get_final_srce_original_story_file)

    def get_final_srce_upscayled_story_files(
        self, page_types: List[PageType]
    ) -> List[Tuple[str, bool]]:
        return self.__get_story_files_with_mods(
            page_types, self.get_final_srce_upscayled_story_file
        )

    def get_final_srce_story_files(
        self, page_types: Union[None, List[PageType]]
    ) -> List[Tuple[str, bool]]:
        return self.__get_story_files_with_mods(page_types, self.get_final_srce_story_file)

    def __get_story_files(
        self,
        page_types: List[PageType],
        get_story_file: Callable[[str], str],
    ) -> List[str]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(get_story_file(page.page_filenames))

        return all_files

    def __get_story_files_with_mods(
        self,
        page_types: List[PageType],
        get_story_file: Callable[[str, PageType], Tuple[str, bool]],
    ) -> List[Tuple[str, bool]]:
        all_files = []
        for page in self.page_images_in_order:
            if page.page_type in page_types:
                all_files.append(get_story_file(page.page_filenames, page.page_type))

        return all_files

    def __get_srce_original_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_image_dir(), page_num + JPG_FILE_EXT)

    def get_srce_upscayled_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_upscayled_image_dir(), page_num + PNG_FILE_EXT)

    def __get_srce_restored_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_restored_image_dir(), page_num + PNG_FILE_EXT)

    def get_srce_restored_upscayled_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_restored_upscayled_image_dir(), page_num + PNG_FILE_EXT)

    def get_srce_restored_svg_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_restored_svg_image_dir(), page_num + SVG_FILE_EXT)

    def __get_srce_restored_ocr_story_file(self, page_num: str) -> Tuple[str, str]:
        return (
            os.path.join(
                self.dirs.srce_restored_ocr_dir,
                page_num + ".easyocr" + JSON_FILE_EXT,
            ),
            os.path.join(
                self.dirs.srce_restored_ocr_dir,
                page_num + ".paddleocr" + JSON_FILE_EXT,
            ),
        )

    def get_srce_panel_segments_file(self, page_num: str) -> str:
        return os.path.join(self.dirs.panel_segments_dir, page_num + JSON_FILE_EXT)

    def get_srce_original_fixes_story_file(self, page_num: str) -> str:
        jpg_fixes_file = os.path.join(
            self.get_srce_original_fixes_image_dir(), page_num + JPG_FILE_EXT
        )
        png_fixes_file = os.path.join(
            self.get_srce_original_fixes_image_dir(), page_num + PNG_FILE_EXT
        )
        if os.path.isfile(jpg_fixes_file) and os.path.isfile(png_fixes_file):
            raise Exception(f'Cannot have both .jpg and .png fixes file "{jpg_fixes_file}"')

        if os.path.isfile(jpg_fixes_file):
            return jpg_fixes_file

        return png_fixes_file

    def get_srce_upscayled_fixes_story_file(self, page_num: str) -> str:
        return os.path.join(self.get_srce_upscayled_fixes_image_dir(), page_num + PNG_FILE_EXT)

    def get_final_srce_original_story_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_file = self.__get_srce_original_story_file(page_num)
        srce_fixes_file = self.get_srce_original_fixes_story_file(page_num)

        return self.__get_final_story_file(
            "original", page_num, page_type, srce_file, srce_fixes_file
        )

    def get_final_srce_upscayled_story_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_upscayled_file = self.get_srce_upscayled_story_file(page_num)
        srce_upscayled_fixes_file = os.path.join(
            self.get_srce_upscayled_fixes_image_dir(), page_num + JPG_FILE_EXT
        )
        if os.path.isfile(srce_upscayled_fixes_file):
            raise Exception(
                f'Upscayled fixes file must be .png not .jpg: "{srce_upscayled_fixes_file}".'
            )
        srce_upscayled_fixes_file = self.get_srce_upscayled_fixes_story_file(page_num)

        return self.__get_final_story_file(
            "upscayled", page_num, page_type, srce_upscayled_file, srce_upscayled_fixes_file
        )

    def get_final_srce_story_file(self, page_num: str, page_type: PageType) -> Tuple[str, bool]:
        if page_type == PageType.TITLE:
            return "TITLE PAGE", False
        if page_type == PageType.BLANK_PAGE:
            return "EMPTY PAGE", False

        if page_type in RESTORABLE_PAGE_TYPES:
            srce_restored_file = os.path.join(
                self.get_srce_restored_image_dir(), page_num + JPG_FILE_EXT
            )
            if os.path.isfile(srce_restored_file):
                raise Exception(f'Restored files should be png not jpg: "{srce_restored_file}".')

            srce_restored_file = self.__get_srce_restored_story_file(page_num)
            if os.path.isfile(srce_restored_file):
                return srce_restored_file, False

            raise Exception(
                f'Could not find restored source file "{srce_restored_file}"'
                f' of type "{page_type.name}"'
            )

        srce_file, is_modified = self.get_final_srce_original_story_file(page_num, page_type)
        if os.path.isfile(srce_file):
            return srce_file, is_modified

        raise Exception(f'Could not find source file "{srce_file}" of type "{page_type.name}"')

    def __get_final_srce_restored_file(
        self, page_num: str, page_type: PageType
    ) -> Tuple[str, bool]:
        srce_restored_file = os.path.join(
            self.get_srce_restored_image_dir(), page_num + JPG_FILE_EXT
        )
        if os.path.isfile(srce_restored_file):
            raise Exception(f'Restored files should be png not jpg: "{srce_restored_file}".')

        return self.__get_srce_restored_story_file(page_num), False

    def __get_final_story_file(
        self, file_type: str, page_num: str, page_type: PageType, primary_file: str, fixes_file: str
    ) -> Tuple[str, bool]:
        if not os.path.isfile(fixes_file):
            return primary_file, False

        # Fixes file exists - use it unless a special case.
        if os.path.isfile(primary_file):
            # Fixes file is an EDITED file.
            if self.__is_edited_fixes_special_case(page_num):
                logging.info(
                    f"NOTE: Special case - using EDITED {page_type.name} {file_type} fixes file:"
                    f' "{get_abbrev_path(fixes_file)}".'
                )
            else:
                logging.info(
                    f'NOTE: Using EDITED {file_type} fixes file: "{get_abbrev_path(fixes_file)}".'
                )
                if page_type not in STORY_PAGE_TYPES:
                    raise Exception(
                        f"EDITED {file_type} fixes page '{page_num}',"
                        f" must be in \"{', '.join(STORY_PAGE_TYPES_STR_LIST)}\""
                    )
        elif self._is_added_fixes_special_case(page_num, page_type):
            # Fixes file is a special case ADDED file.
            logging.info(
                f"NOTE: Special case - using ADDED {file_type} fixes file"
                f' for {page_type.name} page: "{get_abbrev_path(fixes_file)}".'
            )
        else:
            # Fixes file is an ADDED file - must not be a COVER or BODY page.
            logging.info(
                f"NOTE: Using ADDED {file_type} fixes file of type {page_type.name}:"
                f' "{get_abbrev_path(fixes_file)}".'
            )
            if page_type in STORY_PAGE_TYPES:
                raise Exception(
                    f"ADDED {file_type} page '{page_num}',"
                    f" must NOT be in \"{', '.join(STORY_PAGE_TYPES_STR_LIST)}\""
                )

        is_modified_file = page_type in STORY_PAGE_TYPES

        return fixes_file, is_modified_file

    @staticmethod
    def is_fixes_special_case(volume: int, page_num: str) -> bool:
        if volume == 16 and page_num == "209":
            return True
        if volume == 4 and page_num == "227":  # Bill collectors
            return True

        return False

    @staticmethod
    def is_fixes_special_case_added(volume: int, page_num: str) -> bool:
        if volume == 4 and page_num == "227":  # Restored Bill Collectors
            return True
        if volume == 7 and page_num == "240":  # Copied from volume 8, jpeg 31
            return True
        if volume == 7 and page_num == "241":  # Copied from volume 8, jpeg 32
            return True
        if volume == 16 and page_num == "235":  # Copied from volume 14, jpeg 145
            return True

        return False

    def __is_edited_fixes_special_case(self, page_num: str) -> bool:
        if self.fanta_info.volume == 16 and page_num == "209":
            return True

        return False

    def _is_added_fixes_special_case(self, page_num: str, page_type: PageType) -> bool:
        if self.is_fixes_special_case_added(self.fanta_info.volume, page_num):
            return True
        if self.get_ini_title() in CENSORED_TITLES:
            return page_type == PageType.BODY

        return False

    def get_story_file_sources(self, page_num: str) -> List[str]:
        srce_restored_file = self.__get_srce_restored_story_file(page_num)
        srce_upscayled_file = self.get_srce_upscayled_story_file(page_num)
        srce_upscayled_fixes_file = self.get_srce_upscayled_fixes_story_file(page_num)
        srce_original_file = self.__get_srce_original_story_file(page_num)
        srce_original_fixes_file = self.get_srce_original_fixes_story_file(page_num)

        sources = []

        if os.path.isfile(srce_restored_file):
            sources.append(srce_restored_file)

        if os.path.isfile(srce_upscayled_fixes_file):
            sources.append(srce_upscayled_fixes_file)
        elif os.path.isfile(srce_upscayled_file):
            sources.append(srce_upscayled_file)

        if os.path.isfile(srce_original_fixes_file):
            sources.append(srce_original_fixes_file)
        elif os.path.isfile(srce_original_file):
            sources.append(srce_original_file)

        return sources

    def get_final_fixes_panel_bounds_file(self, page_num: int) -> str:
        panels_bounds_file = os.path.join(
            self.get_srce_original_fixes_bounded_dir(), get_page_str(page_num) + JPG_FILE_EXT
        )

        if os.path.isfile(panels_bounds_file):
            return panels_bounds_file

        return ""

    # TODO: Should dest stuff be elsewhere??
    @staticmethod
    def get_dest_root_dir() -> str:
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

    @staticmethod
    def get_dest_zip_root_dir() -> str:
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
    if file_title == THE_MILKMAN:
        # Originally intended for WDCS 215
        publication_text = (
            f"(*) Rejected by Western editors in 1957, this story was originally\n"
            f" intended for publication in {get_formatted_first_published_str(cb_info)}\n"
            + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
            + f"\n"
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

    return os.path.join(ini_file_dir, inset_filename)


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


def get_total_num_pages(comic: ComicBook) -> int:
    return len(comic.page_images_in_order)
