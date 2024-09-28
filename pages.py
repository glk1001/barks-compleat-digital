import inspect
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Dict, Union

from comic_book import OriginalPage, ComicBook, get_safe_title
from comics_info import CENSORED_TITLES
from consts import (
    PageType,
    TITLE_EMPTY_FILENAME,
    EMPTY_FILENAME,
    DEST_FILE_EXT,
    SRCE_FILE_EXT,
    FRONT_MATTER_PAGES,
    ROMAN_NUMERALS,
)
from panel_bounding_boxes import BoundingBox

THIS_SCRIPT_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

EMPTY_IMAGE_FILEPATH = os.path.join(THIS_SCRIPT_DIR, "empty_page.png")
TITLE_EMPTY_IMAGE_FILEPATH = EMPTY_IMAGE_FILEPATH
EMPTY_IMAGE_FILES = {
    EMPTY_IMAGE_FILEPATH,
    TITLE_EMPTY_IMAGE_FILEPATH,
}


class CleanPage:
    def __init__(
        self,
        page_filename: str,
        page_type: PageType,
        page_num: int = -1,
        page_is_modified: bool = False
    ):
        self.page_filename = page_filename
        self.page_type = page_type
        self.page_num: int = page_num
        self.page_is_modified = page_is_modified
        self.panels_bbox: BoundingBox = BoundingBox()


def is_fixes_special_case(comic: ComicBook, page: CleanPage) -> bool:
    if (
        get_safe_title(comic.title) == "Back to Long Ago!"
        and page.page_filename == "209"
    ):
        return page.page_type == PageType.BACK_NO_PANELS
    if comic.file_title == "The Bill Collectors" and page.page_filename == "227":
        return page.page_type == PageType.BODY
    if comic.file_title in CENSORED_TITLES:
        return page.page_type == PageType.BODY

    return False


@dataclass
class SrceAndDestPages:
    srce_pages: List[CleanPage]
    dest_pages: List[CleanPage]


def get_max_timestamp(pages: List[CleanPage]) -> float:
    return max(get_timestamp(p.page_filename) for p in pages)


def get_timestamp(file: str) -> float:
    if os.path.islink(file):
        return os.lstat(file).st_mtime

    return os.path.getmtime(file)


def get_timestamp_str(file: str) -> str:
    return get_timestamp_as_str(get_timestamp(file))


def get_timestamp_as_str(timestamp: float) -> str:
    timestamp_as_date = datetime.fromtimestamp(timestamp)
    return timestamp_as_date.strftime("%Y_%m_%d-%H_%M_%S.%f")


def get_page_num_str(page: CleanPage) -> str:
    return get_page_number_str(page, page.page_num)


def get_page_number_str(page: CleanPage, page_number: int) -> str:
    if page.page_type not in FRONT_MATTER_PAGES:
        return str(page_number)
    if page.page_type == PageType.FRONT:
        assert page_number == 0
        return ""

    return ROMAN_NUMERALS[page_number]


def get_required_pages_in_order(
    page_images_in_book: List[OriginalPage],
) -> List[CleanPage]:
    req_pages = []

    for page_image in page_images_in_book:
        if page_image.page_filenames == TITLE_EMPTY_FILENAME:
            assert page_image.page_type == PageType.TITLE
            req_pages.append(CleanPage(page_image.page_filenames, page_image.page_type))
            continue
        if page_image.page_filenames == EMPTY_FILENAME:
            assert page_image.page_type == PageType.BLANK_PAGE
            req_pages.append(CleanPage(page_image.page_filenames, page_image.page_type))
            continue

        if "-" not in page_image.page_filenames:
            filename = page_image.page_filenames
            file_num = int(filename)
            req_pages.append(CleanPage(filename, page_image.page_type, file_num))
        else:
            start, end = page_image.page_filenames.split("-")
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

        srce_file, is_modified_srce_file = get_checked_srce_file(comic, page)
        file_num_str = f"{file_section_num}-{file_page_num:02d}"
        dest_file = os.path.join(
            comic.get_dest_image_dir(), file_num_str + DEST_FILE_EXT
        )

        srce_page_list.append(
            CleanPage(srce_file, page.page_type, page.page_num, is_modified_srce_file)
        )
        dest_page_list.append(
            CleanPage(
                dest_file,
                page.page_type,
                page_num,
                is_modified_srce_file,
            )
        )

    return SrceAndDestPages(srce_page_list, dest_page_list)


def get_checked_srce_file(comic: ComicBook, page: CleanPage) -> Tuple[str, bool]:
    if page.page_filename == TITLE_EMPTY_FILENAME:
        srce_file = TITLE_EMPTY_IMAGE_FILEPATH
        is_modified_file = False
    elif page.page_filename == EMPTY_FILENAME:
        srce_file = EMPTY_IMAGE_FILEPATH
        is_modified_file = False
    else:
        srce_file, is_modified_file = get_srce_file(comic, page)

    if not os.path.isfile(srce_file):
        raise Exception(f'Could not find source file "{srce_file}".')

    return srce_file, is_modified_file


def get_srce_file(comic: ComicBook, page: CleanPage) -> Tuple[str, bool]:
    srce_file = os.path.join(
        comic.get_srce_image_dir(), page.page_filename + SRCE_FILE_EXT
    )
    srce_fixes_file = os.path.join(
        comic.get_srce_fixes_image_dir(), page.page_filename + SRCE_FILE_EXT
    )
    if not os.path.isfile(srce_fixes_file):
        return srce_file, False

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
                    f"Expected fixes page to be COVER or BODY: '{page.page_filename}'."
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
                f"Expected added page to be NOT COVER OR BODY: '{page.page_filename}'."
            )

    is_modified_file = page.page_type in [PageType.COVER, PageType.BODY]

    return srce_fixes_file, is_modified_file


def get_srce_dest_map(
    comic: ComicBook,
    pages: SrceAndDestPages,
) -> Dict[str, Union[str, int, Dict[str, str]]]:
    srce_dest_map = dict()
    srce_dest_map["srce_dirname"] = os.path.basename(comic.srce_dir)
    srce_dest_map["dest_dirname"] = comic.get_dest_rel_dirname()

    srce_dest_map["srce_min_panels_bbox_width"] = comic.srce_min_panels_bbox_width
    srce_dest_map["srce_max_panels_bbox_width"] = comic.srce_max_panels_bbox_width
    srce_dest_map["srce_min_panels_bbox_height"] = comic.srce_min_panels_bbox_height
    srce_dest_map["srce_max_panels_bbox_height"] = comic.srce_max_panels_bbox_height
    srce_dest_map["dest_required_bbox_width"] = comic.required_dim.panels_bbox_width
    srce_dest_map["dest_required_bbox_height"] = comic.required_dim.panels_bbox_height

    dest_page_map = dict()
    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        srce_page = {
            "file": os.path.basename(srce_page.page_filename),
            "type": dest_page.page_type.name,
        }
        dest_page_map[os.path.basename(dest_page.page_filename)] = srce_page
    srce_dest_map["pages"] = dest_page_map

    return srce_dest_map
