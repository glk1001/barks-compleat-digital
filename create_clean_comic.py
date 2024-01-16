import argparse
import configparser
import datetime
import inspect
import json
import logging
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageFont, ImageDraw

from comics_info import (
    ComicBookInfo,
    ComicBookInfoDict,
    check_story_submitted_order,
    get_all_comic_book_info,
    MONTH_AS_LONG_STR,
    SOURCE_COMICS,
)
from consts import (
    THIS_DIR,
    PUBLICATION_INFO_DIRNAME,
    BARKS,
    BARKS_ROOT_DIR,
    THE_COMICS_DIR,
    CONFIGS_SUBDIR,
    IMAGES_SUBDIR,
    INSET_FILE_EXT,
    DEST_FILE_EXT,
    SRCE_FILE_EXT,
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
)
from panel_bounding_boxes import BoundingBox, BoundingBoxProcessor

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
INTRO_AUTHOR_INSET_GAP = 0
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


@dataclass
class OriginalPage:
    filenames: str
    page_type: PageType


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


@dataclass
class CleanPage:
    filename: str
    page_type: PageType
    page_num: int = -1
    panels_bbox: BoundingBox = field(default_factory=BoundingBox)


@dataclass
class ComicBook:
    config_file: str
    title: str
    title_font_file: str
    title_font_size: int
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
    panel_segments_dir: str
    series_name: str
    number_in_series: int
    intro_inset_file: str
    intro_inset_ratio: float
    publication_date: str
    submitted_date: str
    publication_text: str
    images_in_order: List[OriginalPage]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0

    def get_srce_segments_root_dir(self) -> str:
        return os.path.dirname(self.panel_segments_dir)

    def get_dest_root_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            f"{self.series_name}",
        )

    def get_srce_basename(self) -> str:
        return os.path.basename(self.srce_dir)

    def get_segments_basename(self) -> str:
        return os.path.basename(self.panel_segments_dir)

    def get_dest_basename(self) -> str:
        return os.path.basename(self.get_dest_dir())

    def get_dest_rel_dirname(self) -> str:
        safe_title = get_safe_title(self.title)
        return os.path.join(
            os.path.basename(self.get_dest_root_dir()),
            f"{self.number_in_series:03d} {safe_title}",
        )

    def get_dest_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            self.get_dest_rel_dirname(),
        )

    def get_srce_image_dir(self) -> str:
        return os.path.join(self.srce_dir, IMAGES_SUBDIR)

    def get_dest_image_dir(self) -> str:
        return os.path.join(self.get_dest_dir(), IMAGES_SUBDIR)

    def get_dest_comic_zip(self) -> str:
        return self.get_dest_dir() + ".cbz"

    def get_dest_zip_basename(self) -> str:
        return os.path.basename(self.get_dest_comic_zip())


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

        temp_zip_file = comic.get_dest_dir() + ".zip"

        shutil.make_archive(comic.get_dest_dir(), "zip", comic.get_dest_dir())

        shutil.move(temp_zip_file, comic.get_dest_comic_zip())
        if not os.path.isfile(comic.get_dest_comic_zip()):
            raise Exception(
                f'Could not create final comic zip "{comic.get_dest_comic_zip()}".'
            )


def write_summary(
    comic: ComicBook, srce_page_list: List[CleanPage], dest_page_list: List[CleanPage]
):
    summary_file = os.path.join(comic.get_dest_dir(), "clean_summary.txt")

    calc_panels_bbox_height = int(
        round(
            (
                comic.srce_av_panels_bbox_height
                * comic_book.required_dim.panels_bbox_width
            )
            / comic.srce_av_panels_bbox_width
        )
    )

    with open(summary_file, "w") as f:
        f.write("Config Summary:\n")
        f.write(f'title                    = "{comic.title}"\n')
        f.write(f'srce_dir                 = "{comic.srce_dir}"\n')
        f.write(f'dest_dir                 = "{comic.get_dest_dir()}"\n')
        f.write(
            f'title_font_file          = "{get_font_path(comic.title_font_file)}"\n'
        )
        f.write(f"title_font_size          = {comic.title_font_size}\n")
        f.write(f"author_font_size         = {comic.author_font_size}\n")
        f.write(f'series                   = "{comic.series_name}"\n')
        f.write(f"series_book_num          = {comic.number_in_series}\n")
        f.write(f"DEST_TARGET_X_MARGIN     = {DEST_TARGET_X_MARGIN}\n")
        f.write(f"DEST_TARGET_WIDTH        = {DEST_TARGET_WIDTH}\n")
        f.write(f"DEST_TARGET_HEIGHT       = {DEST_TARGET_HEIGHT}\n")
        f.write(f"DEST_TARGET_ASPECT_RATIO = {DEST_TARGET_ASPECT_RATIO:.2f}\n")
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
        f.write(f"intro_inset_ratio        = {comic.intro_inset_ratio}\n")
        f.write(f"publication_text         = \n{comic.publication_text}\n")
        f.write("\n")

        f.write("Pages Config Summary:\n")
        for pg in comic.images_in_order:
            f.write(
                f"pages = {pg.filenames:11}," f" page_type = {pg.page_type.name:12}\n"
            )
        f.write("\n")

        f.write("Page List Summary:\n")
        for srce_page, dest_page in zip(srce_page_list, dest_page_list):
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
    req_pages: List[CleanPage],
    these_front_pages: List[int],
    these_main_pages: List[int],
) -> Tuple[List[CleanPage], List[CleanPage]]:
    srce_page_list = []
    dest_page_list = []

    img_num = 1
    page_num = 0
    done_front_matter = False
    for page in req_pages:
        srce_file = get_checked_srce_file(comic.get_srce_image_dir(), page)
        num_str = f"{img_num:02d}"
        dest_file = os.path.join(comic.get_dest_image_dir(), num_str + DEST_FILE_EXT)

        if not done_front_matter and page.page_type == PageType.BODY:
            done_front_matter = True
            page_num = 1
        elif page.page_type != PageType.FRONT:
            page_num += 1

        if len(these_front_pages) == 0 and len(these_main_pages) == 0:
            add_page = True
        elif page.page_type in FRONT_MATTER_PAGES and page_num in these_front_pages:
            add_page = True
        elif (
            page.page_type in [PageType.BODY, PageType.BACK_MATTER]
            and page_num in these_main_pages
        ):
            add_page = True
        else:
            add_page = False

        if add_page:
            srce_page_list.append(CleanPage(srce_file, page.page_type))
            dest_page_list.append(CleanPage(dest_file, page.page_type, page_num))

        img_num += 1

    return srce_page_list, dest_page_list


def get_checked_srce_file(srce_dir: str, page: CleanPage) -> str:
    if page.filename == TITLE_EMPTY_FILENAME:
        srce_file = TITLE_EMPTY_IMAGE_FILEPATH
    elif page.filename == EMPTY_FILENAME:
        srce_file = EMPTY_IMAGE_FILEPATH
    else:
        srce_file = os.path.join(srce_dir, page.filename + SRCE_FILE_EXT)

    if not os.path.isfile(srce_file):
        raise Exception(f'Could not find source file "{srce_file}".')

    return srce_file


def process_pages(
    dry_run: bool,
    comic: ComicBook,
    src_pages: List[CleanPage],
    dst_pages: List[CleanPage],
):
    for srce_page, dest_page in zip(src_pages, dst_pages):
        process_page(dry_run, comic, srce_page, dest_page)


def set_required_dimensions(
    comic: ComicBook,
    src_pages: List[CleanPage],
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
    ) = get_required_panels_bbox_width_height(src_pages)

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
    src_pages: List[CleanPage],
) -> Tuple[int, int, int, int, int, int, int, int]:
    (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    ) = get_min_max_panels_bbox_width_height(src_pages)

    av_panels_bbox_width, av_panels_bbox_height = get_average_panels_bbox_width_height(
        max_panels_bbox_height, src_pages
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
    max_panels_bbox_height: int, src_pages: List[CleanPage]
) -> Tuple[int, int]:
    sum_panels_bbox_width = 0
    sum_panels_bbox_height = 0
    num_pages = 0
    for srce_page in src_pages:
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
    src_pages: List[CleanPage],
) -> Tuple[int, int, int, int]:
    min_panels_bbox_width = BIG_NUM
    max_panels_bbox_width = 0
    min_panels_bbox_height = BIG_NUM
    max_panels_bbox_height = 0
    for srce_page in src_pages:
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
    comic: ComicBook,
    src_pages: List[CleanPage],
):
    logging.debug("Setting srce panel bounding boxes.")

    for srce_page in src_pages:
        srce_page_image = open_image_for_reading(srce_page.filename)
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            srce_page.panels_bbox = BoundingBox(
                0, 0, srce_page_image.width - 1, srce_page_image.height - 1
            )
        else:
            srce_page_image = srce_page_image.convert("RGB")
            srce_page.panels_bbox = get_panels_bounding_box(
                dry_run, comic, srce_page_image, srce_page
            )

    logging.debug("")


def get_panels_bounding_box(
    dry_run: bool, comic: ComicBook, srce_page_image: Image, srce_page: CleanPage
) -> BoundingBox:
    if srce_page.page_type in PAGES_WITHOUT_PANELS:
        return BoundingBox(0, 0, srce_page_image.width - 1, srce_page_image.height - 1)

    srce_page_bounding_box_filename = str(
        os.path.join(
            comic.panel_segments_dir,
            os.path.splitext(os.path.basename(srce_page.filename))[0]
            + "_panel_bounds.txt",
        )
    )
    if os.path.isfile(srce_page_bounding_box_filename):
        return boundingBoxProcessor.get_panels_bounding_box_from_file(
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

    bounding_box = boundingBoxProcessor.get_panels_bounding_box_from_kumiko(
        dry_run, comic.panel_segments_dir, srce_page_image, srce_page.filename
    )

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Saving panel bounding box to "{srce_page_bounding_box_filename}".'
        )
    else:
        boundingBoxProcessor.save_panels_bounding_box(
            srce_page_bounding_box_filename, bounding_box
        )

    return bounding_box


def set_dest_panel_bounding_boxes(
    comic: ComicBook,
    src_pages: List[CleanPage],
    dst_pages: List[CleanPage],
):
    logging.debug("Setting dest panel bounding boxes.")

    for srce_page, dest_page in zip(src_pages, dst_pages):
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
    dry_run: bool, comic: ComicBook, srce_page: CleanPage, dest_page: CleanPage
):
    logging.info(
        f'Convert "{os.path.basename(srce_page.filename)}" (page-type {srce_page.page_type.name})'
        f' to "{os.path.basename(dest_page.filename)}"'
        f" (page number = {get_page_num_str(dest_page)})..."
    )

    srce_page_image = open_image_for_reading(srce_page.filename)
    dest_page_image = get_dest_page_image(comic, srce_page_image, srce_page, dest_page)
    rgb_dest_page_image = dest_page_image.convert("RGB")

    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Save changes to image "{dest_page.filename}".')
    else:
        rgb_dest_page_image.save(dest_page.filename, optimize=True, compress_level=9)
        logging.info(f'Saved changes to image "{dest_page.filename}".')

    logging.info("")


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

    log_page_info("Dest", dest_page_image, dest_page)

    return dest_page_image


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
    if dest_page.page_type == PageType.SPLASH:
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


def get_dest_splash_page_image(splash_image: Image, srce_page: CleanPage) -> Image:
    dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

    return get_dest_centred_page_image(splash_image, srce_page, dest_page_image)


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
    text = comic.title
    title_font = ImageFont.truetype(comic.title_font_file, comic.title_font_size)
    text_bbox = draw.multiline_textbbox(
        (0, top), text, font=title_font, spacing=INTRO_TITLE_SPACING
    )
    # text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    draw_centered_multiline_text(
        text,
        dest_page_image,
        draw,
        title_font,
        INTRO_TITLE_COLOR,
        top,
        spacing=INTRO_TITLE_SPACING,
    )
    top += text_height

    top += INTRO_TITLE_AUTHOR_GAP
    text = "by"
    author_font = ImageFont.truetype(
        comic.title_font_file, int(0.6 * comic.author_font_size)
    )
    text_bbox = draw.multiline_textbbox((0, top), text, font=author_font)
    text_height = text_bbox[3] - text_bbox[1]
    draw_centered_text(
        text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top
    )
    top += text_height

    top += INTRO_TITLE_AUTHOR_BY_GAP
    text = f"{BARKS}"
    author_font = ImageFont.truetype(comic.title_font_file, comic.author_font_size)
    text_bbox = draw.multiline_textbbox((0, top), text, font=author_font)
    text_height = text_bbox[3] - text_bbox[1]
    draw_centered_text(
        text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top
    )
    top += text_height + INTRO_AUTHOR_INSET_GAP

    #    remaining_height = HEIGHT - BOTTOM_MARGIN - top

    inset = open_image_for_reading(comic.intro_inset_file)
    inset_width, inset_height = inset.size
    new_inset_width = int(
        0.40
        * comic.intro_inset_ratio
        * (dest_page_image.width - 2 * DEST_TARGET_X_MARGIN)
    )
    new_inset_height = int((inset_height / inset_width) * new_inset_width)
    new_inset = inset.resize(
        size=(new_inset_width, new_inset_height), resample=Image.Resampling.BICUBIC
    )

    pub_text_font = ImageFont.truetype(
        get_font_path(INTRO_TEXT_FONT_FILE), INTRO_PUB_TEXT_FONT_SIZE
    )
    text_bbox = draw.multiline_textbbox(
        (0, top),
        comic.publication_text,
        font=pub_text_font,
        spacing=INTRO_PUB_TEXT_SPACING,
    )
    text_height = text_bbox[3] - text_bbox[1]
    pub_text_top = dest_page_image.height - INTRO_BOTTOM_MARGIN - text_height

    dest_page_centre = int(dest_page_image.width / 2)
    inset_top = top + int((pub_text_top - top) / 2 - new_inset_height / 2)
    insert_pos = (int(dest_page_centre - (new_inset_width / 2)), inset_top)
    dest_page_image.paste(new_inset, insert_pos)

    draw_centered_multiline_text(
        comic.publication_text,
        dest_page_image,
        draw,
        pub_text_font,
        INTRO_PUB_TEXT_COLOR,
        pub_text_top,
        INTRO_PUB_TEXT_SPACING,
    )


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
    text_bounding_box = draw.multiline_textbbox((0, top), text, font)
    left = (image.width - (text_bounding_box[2] - text_bounding_box[0])) / 2
    draw.multiline_text(
        (left, top), text, fill=color, font=font, align="center", spacing=spacing
    )


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
    dry_run: bool,
    comic: ComicBook,
    src_pages: List[CleanPage],
    dst_pages: List[CleanPage],
):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: shutil.copy2("{config_file}", "{comic.get_dest_dir()}")'
        )
    else:
        shutil.copy2(config_file, comic.get_dest_dir())

    write_readme_file(dry_run, comic)
    write_metadata_file(dry_run, comic, dst_pages)
    write_json_metadata(dry_run, comic, dst_pages)
    write_srce_dest_map(dry_run, comic, src_pages, dst_pages)
    write_dest_panels_bboxes(dry_run, comic, dst_pages)


def write_readme_file(dry_run: bool, comic: ComicBook):
    readme_file = os.path.join(comic.get_dest_dir(), README_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write info to "{readme_file}".')
    else:
        with open(readme_file, "w") as f:
            f.write(f"{comic.title}\n")
            f.write("".ljust(len(comic.title), "-") + "\n")
            f.write("\n")
            now_str = datetime.now().strftime("%b %d %Y %H:%M:%S")
            f.write(f"Created:           {now_str}\n")
            f.write(f'Archived ini file: "{os.path.basename(config_file)}"\n')


def write_metadata_file(dry_run: bool, comic: ComicBook, dst_pages: List[CleanPage]):
    metadata_file = os.path.join(comic.get_dest_dir(), METADATA_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write metadata to "{metadata_file}".')
    else:
        with open(metadata_file, "w") as f:
            f.write(f"[{DOUBLE_PAGES_SECTION}]\n")
            orig_page_num = 0
            for page in dst_pages:
                orig_page_num += 1
                if page.page_type not in FRONT_MATTER_PAGES:
                    break
                f.write(f"{orig_page_num} = False" + "\n")
            f.write("\n")

            body_start_page_num = orig_page_num
            f.write(f"[{PAGE_NUMBERS_SECTION}]\n")
            f.write(f"body_start = {body_start_page_num}\n")


def write_json_metadata(dry_run: bool, comic: ComicBook, dst_pages: List[CleanPage]):
    metadata_file = os.path.join(comic.get_dest_dir(), JSON_METADATA_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write json metadata to "{metadata_file}".')
    else:
        metadata = dict()
        metadata["title"] = get_safe_title(comic.title)
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
        metadata["page_counts"] = get_page_counts(comic, dst_pages)
        with open(metadata_file, "w") as f:
            json.dump(metadata, f)


def get_page_counts(comic: ComicBook, dst_pages: List[CleanPage]) -> Dict[str, int]:
    page_counts = dict()

    painting_page_count = len([p for p in dst_pages if p.page_type == PageType.FRONT])
    assert painting_page_count <= 1

    title_page_count = len([p for p in dst_pages if p.page_type == PageType.TITLE])
    assert title_page_count == 1

    cover_page_count = len([p for p in dst_pages if p.page_type == PageType.COVER])
    assert cover_page_count <= 1

    splash_page_count = len([p for p in dst_pages if p.page_type == PageType.SPLASH])

    front_matter_page_count = len(
        [p for p in dst_pages if p.page_type == PageType.FRONT_MATTER]
    )

    story_page_count = len([p for p in dst_pages if p.page_type == PageType.BODY])

    back_matter_page_count = len(
        [
            p
            for p in dst_pages
            if p.page_type in [PageType.BACK_MATTER, PageType.BACK_NO_PANELS]
        ]
    )

    blank_page_count = len([p for p in dst_pages if p.page_type == PageType.BLANK_PAGE])

    total_page_count = len(dst_pages)
    assert total_page_count == (
        painting_page_count
        + title_page_count
        + cover_page_count
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
    src_pages: List[CleanPage],
    dst_pages: List[CleanPage],
):
    src_dst_map_file = os.path.join(comic.get_dest_dir(), DEST_SRCE_MAP_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write srce dest map to "{src_dst_map_file}".')
    else:
        srce_dest_map = dict()
        srce_dest_map["srce_dirname"] = comic.get_srce_basename()
        srce_dest_map["dest_dirname"] = comic.get_dest_rel_dirname()

        srce_dest_map["srce_min_panels_bbox_width"] = comic.srce_min_panels_bbox_width
        srce_dest_map["srce_max_panels_bbox_width"] = comic.srce_max_panels_bbox_width
        srce_dest_map["srce_min_panels_bbox_height"] = comic.srce_min_panels_bbox_height
        srce_dest_map["srce_max_panels_bbox_height"] = comic.srce_max_panels_bbox_height
        srce_dest_map["dest_required_bbox_width"] = comic.required_dim.panels_bbox_width
        srce_dest_map[
            "dest_required_bbox_height"
        ] = comic.required_dim.panels_bbox_height

        dest_page_map = dict()
        for srce_page, dest_page in zip(src_pages, dst_pages):
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
    dst_pages: List[CleanPage],
):
    dst_bboxes_file = os.path.join(comic.get_dest_dir(), DEST_PANELS_BBOXES_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write dest panels bboxes to "{dst_bboxes_file}".')
    else:
        bboxes_dict = dict()
        for dest_page in dst_pages:
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


def get_comic_book(ini_file: str) -> ComicBook:
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    config.read(ini_file)

    title = config["info"]["title"]
    safe_title = get_safe_title(title)
    intro_inset_file = str(
        os.path.join(CONFIGS_SUBDIR, safe_title + " Inset" + INSET_FILE_EXT)
    )

    cb_info: ComicBookInfo = all_comic_book_info[safe_title]
    srce_info = SOURCE_COMICS[config["info"]["source_comic"]]
    srce_root_dir = str(os.path.join(BARKS_ROOT_DIR, srce_info.pub))
    srce_dir = os.path.join(srce_root_dir, srce_info.title)
    panel_segments_dir = str(
        os.path.join(BARKS_ROOT_DIR, srce_info.pub + "-panel-segments", srce_info.title)
    )

    publication_date = get_formatted_first_published_str(cb_info)
    submitted_date = get_formatted_submitted_date(cb_info)
    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published by {srce_info.pub}, {srce_info.year}\n"
        + f"Color restoration by {cb_info.colorist}"
    )

    return ComicBook(
        config_file=ini_file,
        title=title,
        title_font_file=get_font_path(
            config["info"].get("title_font_file", INTRO_TITLE_DEFAULT_FONT_FILE)
        ),
        title_font_size=config["info"].getint(
            "title_font_size", INTRO_TITLE_DEFAULT_FONT_SIZE
        ),
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
        panel_segments_dir=panel_segments_dir,
        series_name=cb_info.series_name,
        number_in_series=cb_info.number_in_series,
        intro_inset_file=intro_inset_file,
        intro_inset_ratio=config["introduction"].getfloat("intro_inset_ratio", 1.0),
        publication_date=publication_date,
        submitted_date=submitted_date,
        publication_text=publication_text,
        images_in_order=[
            OriginalPage(key, PageType[config["pages"][key]]) for key in config["pages"]
        ],
    )


def log_comic_book_params(comic: ComicBook):
    logging.info("")

    calc_panels_bbox_height = int(
        round(
            (
                comic.srce_av_panels_bbox_height
                * comic_book.required_dim.panels_bbox_width
            )
            / comic.srce_av_panels_bbox_width
        )
    )

    logging.info(f'Comic book series:   "{comic.series_name}".')
    logging.info(f'Comic book title:    "{get_safe_title(comic.title)}".')
    logging.info(f"Number in series:    {comic.number_in_series}.")
    logging.info(f"Dest x margin:       {DEST_TARGET_X_MARGIN}.")
    logging.info(f"Dest width:          {DEST_TARGET_WIDTH}.")
    logging.info(f"Dest height:         {DEST_TARGET_HEIGHT}.")
    logging.info(f"Dest aspect ratio:   {DEST_TARGET_ASPECT_RATIO:.2f}.")
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
    logging.info(f'Srce comic dir:      "ROOT: {comic.get_srce_basename()}".')
    logging.info(f'Srce segments root:  "{comic.get_srce_segments_root_dir()}".')
    logging.info(f'Srce segments dir:   "ROOT: {comic.get_segments_basename()}".')
    logging.info(f'Dest root:           "{comic.get_dest_root_dir()}".')
    logging.info(f'Dest comic dir:      "ROOT: {comic.get_dest_basename()}".')
    logging.info(f'Dest comic zip:      "ROOT: {comic.get_dest_zip_basename()}".')
    logging.info(f'Work directory:      "{work_dir}".')
    logging.info("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a clean Barks comic from Fantagraphics source."
    )
    parser.add_argument("--ini-file", action="store", type=str, required=True)
    parser.add_argument(
        "--front-pages", action="store", type=str, required=False, default=""
    )
    parser.add_argument(
        "--main-pages", action="store", type=str, required=False, default=""
    )
    parser.add_argument(
        "--log-level", action="store", type=str, required=False, default="INFO"
    )
    parser.add_argument("--dry-run", action="store_true", required=False, default=False)
    parser.add_argument("--work-dir", type=str, required=True)
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=args.log_level,
    )

    work_dir = args.work_dir
    if not os.path.isdir(work_dir):
        raise Exception(f'Could not find work directory "{work_dir}".')
    work_dir = os.path.join(work_dir, datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
    os.makedirs(work_dir)

    boundingBoxProcessor = BoundingBoxProcessor(work_dir)

    config_file = args.ini_file
    if not os.path.isfile(config_file):
        raise Exception(f'Could not find ini file "{config_file}".')
    logging.info(f'Processing config file "{config_file}".')

    all_comic_book_info = get_all_comic_book_info(
        str(os.path.join(THIS_DIR, PUBLICATION_INFO_DIRNAME, STORIES_INFO_FILENAME))
    )
    check_story_submitted_order(all_comic_book_info)

    front_pages = get_list_of_numbers(args.front_pages)
    main_pages = get_list_of_numbers(args.main_pages)

    comic_book = get_comic_book(config_file)
    if not os.path.isdir(comic_book.get_srce_image_dir()):
        raise Exception(
            f'Could not find directory "{comic_book.get_srce_image_dir()}".'
        )

    required_pages = get_required_pages_in_order(comic_book.images_in_order)
    srce_pages, dest_pages = get_srce_and_dest_pages_in_order(
        comic_book, required_pages, front_pages, main_pages
    )
    set_srce_panel_bounding_boxes(args.dry_run, comic_book, srce_pages)
    set_required_dimensions(comic_book, srce_pages)
    set_dest_panel_bounding_boxes(comic_book, srce_pages, dest_pages)

    log_comic_book_params(comic_book)

    create_dest_dirs(args.dry_run, comic_book)
    process_pages(args.dry_run, comic_book, srce_pages, dest_pages)
    process_additional_files(args.dry_run, comic_book, srce_pages, dest_pages)

    write_summary(comic_book, srce_pages, dest_pages)

    zip_comic_book(args.dry_run, comic_book)
