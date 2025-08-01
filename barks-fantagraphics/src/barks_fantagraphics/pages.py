import inspect
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Union, Tuple, Callable

from .comic_book import (
    ComicBook,
    ModifiedType,
    get_page_str,
)
from .comics_consts import (
    PageType,
    ROMAN_NUMERALS,
    JPG_FILE_EXT,
    DEST_TARGET_HEIGHT,
    PAGE_NUM_HEIGHT,
    RESTORABLE_PAGE_TYPES,
    FRONT_MATTER_PAGES,
    BACK_MATTER_PAGES,
)
from .comics_utils import get_timestamp
from .page_classes import (
    CleanPage,
    SrceAndDestPages,
    OriginalPage,
    RequiredDimensions,
    ComicDimensions,
)
from .panel_bounding import (
    set_srce_panel_bounding_boxes,
    set_dest_panel_bounding_boxes,
    get_required_panels_bbox_width_height,
)

THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

TITLE_EMPTY_FILENAME = "title_empty"
EMPTY_FILENAME = "empty"
DEST_FILE_EXT = ".jpg"

EMPTY_IMAGE_FILEPATH = os.path.join(THIS_SCRIPT_DIR, "empty_page.png")
TITLE_EMPTY_IMAGE_FILEPATH = EMPTY_IMAGE_FILEPATH
EMPTY_IMAGE_FILES = {
    EMPTY_IMAGE_FILEPATH,
    TITLE_EMPTY_IMAGE_FILEPATH,
}


def get_max_timestamp(pages: List[CleanPage]) -> float:
    return max(get_timestamp(p.page_filename) for p in pages)


def get_page_num_str(page: CleanPage) -> str:
    return get_page_number_str(page, page.page_num)


def get_page_number_str(page: CleanPage, page_number: int) -> str:
    if page.page_type in [PageType.PAINTING_NO_BORDER, PageType.BACK_PAINTING_NO_BORDER]:
        return ""
    if page.page_type == PageType.FRONT:
        assert page_number == 0
        return ""
    if page.page_type not in FRONT_MATTER_PAGES:
        return str(page_number)

    assert page_number in ROMAN_NUMERALS
    return ROMAN_NUMERALS[page_number]


def get_sorted_srce_and_dest_pages(
    comic: ComicBook,
    get_full_paths: bool,
    get_srce_panel_segments_file: Callable[[str], str] = None,
    check_srce_page_timestamps: bool = True,
) -> SrceAndDestPages:
    return get_sorted_srce_and_dest_pages_with_dimensions(
        comic, get_full_paths, get_srce_panel_segments_file, check_srce_page_timestamps
    )[0]


def get_sorted_srce_and_dest_pages_with_dimensions(
    comic: ComicBook,
    get_full_paths: bool,
    get_srce_panel_segments_file: Callable[[str], str] = None,
    check_srce_page_timestamps: bool = True,
) -> Tuple[SrceAndDestPages, ComicDimensions, RequiredDimensions]:
    if get_srce_panel_segments_file is None:
        get_srce_panel_segments_file = comic.get_srce_panel_segments_file

    srce_and_dest_pages = _get_srce_and_dest_pages_in_order(comic, get_full_paths)

    srce_panels_segment_info_files = [
        get_srce_panel_segments_file(get_page_str(srce_page.page_num))
        for srce_page in srce_and_dest_pages.srce_pages
    ]
    set_srce_panel_bounding_boxes(
        srce_and_dest_pages.srce_pages, srce_panels_segment_info_files, check_srce_page_timestamps
    )

    srce_dim, required_dim = get_required_panels_bbox_width_height(
        srce_and_dest_pages.srce_pages, DEST_TARGET_HEIGHT, PAGE_NUM_HEIGHT
    )

    set_dest_panel_bounding_boxes(srce_dim, required_dim, srce_and_dest_pages)

    return srce_and_dest_pages, srce_dim, required_dim


def _get_srce_and_dest_pages_in_order(comic: ComicBook, get_full_paths: bool) -> SrceAndDestPages:
    required_pages = get_required_pages_in_order(comic.page_images_in_order)

    srce_page_list = []
    dest_page_list = []

    file_section_num = 1
    file_page_num = 0
    in_front_matter = True
    in_body = False
    in_back_matter = False
    page_num = 0
    for page in required_pages:
        if in_front_matter and page.page_type == PageType.BODY:
            in_front_matter = False
            in_body = True
            file_section_num += 1
            file_page_num = 1
            page_num = 1
        elif in_body and page.page_type != PageType.BODY:
            in_body = False
            in_back_matter = True
            file_section_num += 1
            file_page_num = 1
            page_num += 1
        elif page.page_type != PageType.FRONT:
            if in_front_matter and page.page_type not in FRONT_MATTER_PAGES:
                raise Exception(
                    f"Processing front matter but page type is incorrect:"
                    f' "{page.page_type}" - "{page.page_filename}"'
                )
            if in_back_matter and page.page_type not in BACK_MATTER_PAGES:
                raise Exception(
                    f"Processing back matter but page type is incorrect:"
                    f' "{page.page_type}" - "{page.page_filename}"'
                )
            file_page_num += 1
            page_num += 1

        file_num_str = f"{file_section_num}-{file_page_num:02d}"
        if get_full_paths:
            srce_file = get_full_srce_filepath(comic, page)
            dest_file = os.path.join(comic.get_dest_image_dir(), file_num_str + DEST_FILE_EXT)
        else:
            srce_file = get_relative_srce_filepath(page)
            dest_file = file_num_str + DEST_FILE_EXT

        srce_page_list.append(CleanPage(srce_file, page.page_type, page.page_num))
        dest_page_list.append(
            CleanPage(
                dest_file,
                page.page_type,
                page_num,
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


def get_full_srce_filepath(comic: ComicBook, page: CleanPage) -> str:
    if page.page_filename == TITLE_EMPTY_FILENAME:
        return TITLE_EMPTY_IMAGE_FILEPATH
    elif page.page_filename == EMPTY_FILENAME:
        return EMPTY_IMAGE_FILEPATH

    return comic.get_final_srce_story_file(page.page_filename, page.page_type)[0]


def get_relative_srce_filepath(page: CleanPage) -> str:
    if page.page_filename == TITLE_EMPTY_FILENAME:
        rel_srce_file = os.path.basename(TITLE_EMPTY_IMAGE_FILEPATH)
    elif page.page_filename == EMPTY_FILENAME:
        rel_srce_file = os.path.basename(EMPTY_IMAGE_FILEPATH)
    else:
        rel_srce_file = page.page_filename + JPG_FILE_EXT

    return rel_srce_file


def get_page_mod_type(comic: ComicBook, page: CleanPage) -> ModifiedType:
    if page.page_filename == TITLE_EMPTY_FILENAME:
        mod_type = ModifiedType.ORIGINAL
    elif page.page_filename == EMPTY_FILENAME:
        mod_type = ModifiedType.ORIGINAL
    else:
        page_num_str = Path(page.page_filename).stem
        _, mod_type = comic.get_final_srce_story_file(page_num_str, page.page_type)
        if mod_type == ModifiedType.ORIGINAL:
            _, mod_type = comic.get_final_srce_upscayled_story_file(page_num_str, page.page_type)
        if mod_type == ModifiedType.ORIGINAL:
            _, mod_type = comic.get_final_srce_original_story_file(page_num_str, page.page_type)

    return mod_type


def get_srce_dest_map(
    comic: ComicBook,
    srce_dim: ComicDimensions,
    required_dim: RequiredDimensions,
    pages: SrceAndDestPages,
) -> Dict[str, Union[str, int, Dict[str, str]]]:
    srce_dest_map = dict()
    srce_dest_map["srce_dirname"] = os.path.basename(comic.dirs.srce_dir)
    srce_dest_map["dest_dirname"] = comic.get_dest_rel_dirname()

    srce_dest_map["srce_min_panels_bbox_width"] = srce_dim.min_panels_bbox_width
    srce_dest_map["srce_max_panels_bbox_width"] = srce_dim.max_panels_bbox_width
    srce_dest_map["srce_min_panels_bbox_height"] = srce_dim.min_panels_bbox_height
    srce_dest_map["srce_max_panels_bbox_height"] = srce_dim.max_panels_bbox_height
    srce_dest_map["dest_required_bbox_width"] = required_dim.panels_bbox_width
    srce_dest_map["dest_required_bbox_height"] = required_dim.panels_bbox_height

    dest_page_map = dict()
    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        srce_page = {
            "file": os.path.basename(srce_page.page_filename),
            "type": dest_page.page_type.name,
        }
        dest_page_map[os.path.basename(dest_page.page_filename)] = srce_page
    srce_dest_map["pages"] = dest_page_map

    return srce_dest_map


@dataclass
class SrceDependency:
    file: str
    timestamp: float
    independent: bool
    mod_type: ModifiedType = ModifiedType.ORIGINAL


def get_restored_srce_dependencies(comic: ComicBook, srce_page: CleanPage) -> List[SrceDependency]:
    if srce_page.page_type == PageType.BLANK_PAGE:
        return []
    if srce_page.page_type == PageType.TITLE:
        return [
            SrceDependency(comic.ini_file, get_timestamp(comic.ini_file), independent=True),
            SrceDependency(
                comic.intro_inset_file, get_timestamp(comic.intro_inset_file), independent=True
            ),
        ]

    page_num_str = get_page_str(srce_page.page_num)

    srce_panel_segments_file = comic.get_srce_panel_segments_file(page_num_str)
    srce_panel_segments_timestamp = (
        get_timestamp(srce_panel_segments_file) if os.path.isfile(srce_panel_segments_file) else -1
    )
    srce_restored_file, restored_modded = comic.get_final_srce_story_file(
        page_num_str, srce_page.page_type
    )
    srce_restored_timestamp = get_timestamp(srce_restored_file)
    srce_restored_upscayled_file = comic.get_srce_restored_upscayled_story_file(page_num_str)
    srce_restored_upscayled_timestamp = (
        get_timestamp(srce_restored_upscayled_file)
        if os.path.isfile(srce_restored_upscayled_file)
        else -1
    )
    srce_restored_svg_file = comic.get_srce_restored_svg_story_file(page_num_str)
    srce_restored_svg_timestamp = (
        get_timestamp(srce_restored_svg_file) if os.path.isfile(srce_restored_svg_file) else -1
    )
    srce_upscayl_file, upscayl_modded = comic.get_final_srce_upscayled_story_file(
        page_num_str, srce_page.page_type
    )
    srce_upscayl_timestamp = (
        get_timestamp(srce_upscayl_file) if os.path.isfile(srce_upscayl_file) else -1
    )
    srce_original_file, original_modded = comic.get_final_srce_original_story_file(
        page_num_str, srce_page.page_type
    )
    srce_original_timestamp = (
        get_timestamp(srce_original_file) if os.path.isfile(srce_original_file) else -1
    )

    underlying_files = []
    if srce_page.page_type in RESTORABLE_PAGE_TYPES:
        underlying_files.append(
            SrceDependency(
                srce_panel_segments_file, srce_panel_segments_timestamp, independent=False
            )
        )
        panel_bounds_file = comic.get_final_fixes_panel_bounds_file(srce_page.page_num)
        if panel_bounds_file:
            underlying_files.append(
                SrceDependency(
                    panel_bounds_file, get_timestamp(panel_bounds_file), independent=True
                )
            )

    underlying_files.append(
        SrceDependency(
            srce_restored_file, srce_restored_timestamp, independent=False, mod_type=restored_modded
        )
    )

    if srce_page.page_type in RESTORABLE_PAGE_TYPES:
        # noinspection PyProtectedMember
        if not comic._is_added_fixes_special_case(
            get_page_str(srce_page.page_num), srce_page.page_type
        ):
            underlying_files.append(
                SrceDependency(
                    srce_restored_upscayled_file,
                    srce_restored_upscayled_timestamp,
                    independent=False,
                )
            )
            underlying_files.append(
                SrceDependency(
                    srce_restored_svg_file, srce_restored_svg_timestamp, independent=False
                )
            )
            underlying_files.append(
                SrceDependency(
                    srce_upscayl_file,
                    srce_upscayl_timestamp,
                    independent=False,
                    mod_type=upscayl_modded,
                )
            )
            underlying_files.append(
                SrceDependency(
                    srce_original_file,
                    srce_original_timestamp,
                    independent=False,
                    mod_type=original_modded,
                )
            )

    return underlying_files
