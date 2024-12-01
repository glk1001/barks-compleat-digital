import inspect
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Dict, Union

from barks_fantagraphics.comic_book import OriginalPage, ComicBook
from barks_fantagraphics.comics_consts import PageType
from consts import (
    ROMAN_NUMERALS,
    TITLE_EMPTY_FILENAME,
    EMPTY_FILENAME,
    DEST_FILE_EXT,
    FRONT_MATTER_PAGES,
)
from panel_bounding_boxes import BoundingBox

THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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
        page_is_modified: bool = False,
    ):
        self.page_filename = page_filename
        self.page_type = page_type
        self.page_num: int = page_num
        self.page_is_modified = page_is_modified
        self.panels_bbox: BoundingBox = BoundingBox()


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


def get_srce_and_dest_pages_in_order(comic: ComicBook) -> SrceAndDestPages:
    required_pages = get_required_pages_in_order(comic.page_images_in_order)

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
        dest_file = os.path.join(comic.get_dest_image_dir(), file_num_str + DEST_FILE_EXT)

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


def get_required_pages_in_order(page_images_in_book: List[OriginalPage]) -> List[CleanPage]:
    req_pages = []

    for page_image in page_images_in_book:
        filename = page_image.page_filenames

        if filename == TITLE_EMPTY_FILENAME:
            assert page_image.page_type == PageType.TITLE
            req_pages.append(CleanPage(filename, page_image.page_type))
        elif filename == EMPTY_FILENAME:
            assert page_image.page_type == PageType.BLANK_PAGE
            req_pages.append(CleanPage(filename, page_image.page_type))
        else:
            file_num = int(filename)
            req_pages.append(CleanPage(filename, page_image.page_type, file_num))

    return req_pages


def get_checked_srce_file(comic: ComicBook, page: CleanPage) -> Tuple[str, bool]:
    if page.page_filename == TITLE_EMPTY_FILENAME:
        srce_file = TITLE_EMPTY_IMAGE_FILEPATH
        is_modified_file = False
    elif page.page_filename == EMPTY_FILENAME:
        srce_file = EMPTY_IMAGE_FILEPATH
        is_modified_file = False
    else:
        srce_file, is_modified_file = comic.get_final_srce_story_file(
            page.page_filename, page.page_type
        )

    return srce_file, is_modified_file


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
