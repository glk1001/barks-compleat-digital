import argparse
import configparser
import datetime
import inspect
import logging
import os
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageFont, ImageDraw

from comics_info import (
    ComicBookInfo,
    ComicBookInfoDict,
    check_story_submitted_order,
    get_all_comic_book_info,
    MONTH_AS_LONG_STR,
    SOURCE_COMICS,
)

THIS_SCRIPT_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

DRY_RUN_STR = "DRY_RUN"
README_FILENAME = "readme.txt"
DOUBLE_PAGES_SECTION = "double_pages"
PAGE_NUMBERS_SECTION = "page_numbers"
METADATA_FILENAME = "metadata.txt"

DEST_WIDTH = 2216
DEST_HEIGHT = 3056
# Trim the width to get more art displayed on 16:10 monitor
DEST_X_MARGINS_TRIM = 48
DEST_Y_MARGINS_TRIM = 48
DEST_PRELIM_TARGET_WIDTH = DEST_WIDTH - (2 * DEST_Y_MARGINS_TRIM)
DEST_PRELIM_TARGET_HEIGHT = DEST_HEIGHT - (2 * DEST_Y_MARGINS_TRIM)
DEST_PRELIM_TARGET_ASPECT_RATIO = float(DEST_PRELIM_TARGET_WIDTH) / float(
    DEST_PRELIM_TARGET_HEIGHT
)

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
PAGE_NUM_Y_OFFSET_FROM_BOTTOM = 140
PAGE_NUM_X_BLANK_PIXEL_OFFSET = 250
PAGE_NUM_HEIGHT = 40
PAGE_NUM_FONT_SIZE = 30

BARKS = "Carl Barks"
BARKS_ROOT_DIR = os.path.join(str(Path.home()), "Books", BARKS)
THE_COMICS_DIR = os.path.join(BARKS_ROOT_DIR, "The Comics")
TITLE_EMPTY_IMAGE_FILEPATH = os.path.join(THIS_SCRIPT_DIR, "title_empty.png")
LAST_EMPTY_IMAGE_FILEPATH = os.path.join(THIS_SCRIPT_DIR, "last_empty.png")
EMPTY_IMAGE_FILEPATH = TITLE_EMPTY_IMAGE_FILEPATH
IMAGES_SUBDIR = "images"
CONFIGS_SUBDIR = "Configs"
TITLE_EMPTY_FILENAME = "title_empty"
LAST_EMPTY_FILENAME = "last_empty"
NUMBER_LEN = 3
SRCE_FILE_EXT = ".jpg"
DEST_FILE_EXT = ".jpg"
INSERT_FILE_EXT = ".png"

ROMAN_NUMERALS = {
    1: "i",
    2: "ii",
    3: "iii",
    4: "iv",
    5: "v",
    6: "vi",
    7: "vii",
    8: "viii",
    9: "ix",
    10: "x",
}


class PageType(Enum):
    FRONT = 1
    TITLE = 2
    COVER = 3
    SPLASH = 4
    FRONT_MATTER = 5
    BODY = 6
    BACK_MATTER = 7


FRONT_PAGES = [
    PageType.FRONT,
    PageType.TITLE,
    PageType.COVER,
    PageType.SPLASH,
]
FRONT_MATTER_PAGES = FRONT_PAGES + [PageType.FRONT_MATTER]


@dataclass
class OriginalPage:
    filenames: str
    page_type: PageType
    is_odd_correct: bool = True


@dataclass
class CleanPage:
    filename: str
    trim_left: bool
    page_type: PageType
    page_num: int = -1


@dataclass
class ComicBook:
    config_file: str
    title: str
    title_font_file: str
    title_font_size: int
    author_font_size: int
    trim_amount: int
    source_dir: str
    series_name: str
    number_in_series: int
    intro_inset_file: str
    intro_inset_ratio: float
    publication_text: str
    images_in_order: List[OriginalPage]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0

    def get_target_dir(self):
        safe_title = get_safe_title(self.title)
        return os.path.join(
            THE_COMICS_DIR,
            f"{self.series_name}",
            f"{self.number_in_series:03d} {safe_title}",
        )

    def get_srce_image_dir(self):
        return os.path.join(self.source_dir, IMAGES_SUBDIR)

    def get_dest_image_dir(self):
        return os.path.join(self.get_target_dir(), IMAGES_SUBDIR)

    def get_dest_comic_zip(self):
        return self.get_target_dir() + ".cbz"

    def get_trimmed_width(self):
        return DEST_WIDTH - self.trim_amount

    def get_trimmed_center(self):
        return int(self.get_trimmed_width() / 2)


def get_safe_title(title: str) -> str:
    safe_title = title.replace("\n", " ")
    safe_title = safe_title.replace("- ", "-")
    safe_title = safe_title.replace('"', "")
    return safe_title


def zip_comic_book(dry_run: bool, comic: ComicBook):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Zipping directory "{comic.get_target_dir()}"'
            f' to "{comic.get_dest_comic_zip()}".'
        )
    else:
        logging.info(
            f'Zipping directory "{comic.get_target_dir()}" to "{comic.get_dest_comic_zip()}".'
        )

        temp_zip_file = comic.get_target_dir() + ".zip"

        shutil.make_archive(comic.get_target_dir(), "zip", comic.get_target_dir())

        shutil.move(temp_zip_file, comic.get_dest_comic_zip())
        if not os.path.isfile(comic.get_dest_comic_zip()):
            raise Exception(
                f'Could not create final comic zip "{comic.get_dest_comic_zip()}".'
            )


def print_comic_book_properties(
    comic: ComicBook, srce_page_list: List[CleanPage], dest_page_list: List[CleanPage]
):
    logging.debug("Config Summary:")
    logging.debug(f'title = "{comic.title}"')
    logging.debug(f'source_dir = "{comic.source_dir}"')
    logging.debug(f'target_dir = "{comic.get_target_dir()}"')
    logging.debug(f'title_font_file = "{get_font_path(comic.title_font_file)}"')
    logging.debug(f"title_font_size = {comic.title_font_size}")
    logging.debug(f"author_font_size = {comic.author_font_size}")
    logging.debug(f"trim_amount = {comic.trim_amount}")
    logging.debug(f"series = {comic.series_name}")
    logging.debug(f"series_book_num = {comic.number_in_series}")
    logging.debug(f'intro_inset_file = "{comic.intro_inset_file}"')
    logging.debug(f"intro_inset_ratio = {comic.intro_inset_ratio}")
    logging.debug(f"publication_text = \n{comic.publication_text}")
    logging.debug("")

    logging.debug("Pages Config Summary:")
    for pg in comic.images_in_order:
        logging.debug(
            f"pages = {pg.filenames:11},"
            f" page_type = {pg.page_type.name:12},"
            f" oddness = {pg.is_odd_correct}"
        )
    logging.debug("")

    logging.debug("Page List Summary:")
    for srce_page, dest_page in zip(srce_page_list, dest_page_list):
        srce_filename = f'"{os.path.basename(srce_page.filename)}"'
        dest_filename = f'"{os.path.basename(dest_page.filename)}"'
        dest_page_type = f'"{dest_page.page_type.name}"'
        left_trim_amount, right_trim_amount = get_trim_amounts(comic, dest_page)
        logging.debug(
            f"Added srce {srce_filename:17}"
            f" as dest {dest_filename:6},"
            f" type {dest_page_type:14}, "
            f" page {dest_page.page_num:2} ({get_page_num_str(dest_page):>3}),"
            f" trim ({left_trim_amount:2}, {right_trim_amount:2})."
        )
    logging.debug("")


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)


def get_trim_left(page_image: OriginalPage, file_num: int) -> bool:
    if page_image.page_type in FRONT_PAGES:
        return True

    trim_left = file_num % 2 != 0
    if not page_image.is_odd_correct:
        trim_left = not trim_left

    return trim_left


def get_required_pages_in_order(
    page_images_in_book: List[OriginalPage],
) -> List[CleanPage]:
    req_pages = []

    for page_image in page_images_in_book:
        if page_image.filenames == TITLE_EMPTY_FILENAME:
            assert page_image.page_type == PageType.TITLE
            req_pages.append(
                CleanPage(page_image.filenames, True, page_image.page_type)
            )
            continue
        if page_image.filenames == LAST_EMPTY_FILENAME:
            assert page_image.page_type == PageType.BACK_MATTER
            req_pages.append(
                CleanPage(page_image.filenames, True, page_image.page_type)
            )
            continue

        if "-" not in page_image.filenames:
            filename = page_image.filenames
            file_num = int(filename)
            trim_left = get_trim_left(page_image, file_num)
            req_pages.append(
                CleanPage(filename, trim_left, page_image.page_type, file_num)
            )
        else:
            start, end = page_image.filenames.split("-")
            start_num = int(start)
            end_num = int(end)
            for file_num in range(start_num, end_num + 1):
                filename = f"{file_num:03d}"
                trim_left = get_trim_left(page_image, file_num)
                req_pages.append(
                    CleanPage(filename, trim_left, page_image.page_type, file_num)
                )

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
            srce_page_list.append(CleanPage(srce_file, page.trim_left, page.page_type))
            dest_page_list.append(
                CleanPage(dest_file, page.trim_left, page.page_type, page_num)
            )

        img_num += 1

    return srce_page_list, dest_page_list


def get_checked_srce_file(srce_dir: str, page: CleanPage) -> str:
    if page.filename == TITLE_EMPTY_FILENAME:
        srce_file = TITLE_EMPTY_IMAGE_FILEPATH
    elif page.filename == LAST_EMPTY_FILENAME:
        srce_file = LAST_EMPTY_IMAGE_FILEPATH
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


def process_page(
    dry_run: bool, comic: ComicBook, srce_page: CleanPage, dest_page: CleanPage
):
    logging.info(
        f'Convert "{os.path.basename(srce_page.filename)}" (page-type {srce_page.page_type.name})'
        + f' to "{os.path.basename(dest_page.filename)}" (page number = {dest_page.page_num})...'
    )

    srce_page_image = Image.open(srce_page.filename, "r")

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

    if dest_page.page_type in FRONT_PAGES:
        dest_page_image = get_dest_front_page_image(
            comic, srce_page_image, srce_page, dest_page
        )
    else:
        dest_page_image = get_dest_main_page_image(
            comic, srce_page_image, srce_page, dest_page
        )

    log_page_info("Dest", dest_page_image, dest_page)

    return dest_page_image


def log_page_info(prefix: str, image: Image, page: CleanPage):
    logging.debug(
        f"{prefix}: width = {image.width}, height = {image.height},"
        f" page_type = {page.page_type.name}, trim_left = {page.trim_left}."
    )


def get_dest_front_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    if dest_page.page_type == PageType.SPLASH:
        return get_dest_splash_page(srce_page_image, srce_page)

    return get_dest_non_splash_front_page_image(
        comic, srce_page_image, srce_page, dest_page
    )


def get_dest_non_splash_front_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    page_width, page_height = srce_page_image.size

    if dest_page.page_type == PageType.COVER:
        if page_width != DEST_WIDTH:
            raise Exception(
                f"Wrong width for cover '{srce_page.filename}':"
                f" {page_width} != {DEST_WIDTH}."
            )
        if page_height != DEST_HEIGHT:
            raise Exception(
                f"Wrong width for cover '{srce_page.filename}':"
                f" {page_height} != {DEST_HEIGHT}."
            )
    else:
        if page_width != DEST_PRELIM_TARGET_WIDTH:
            raise Exception(
                f"Wrong width for front page '{srce_page.filename}':"
                f" {page_width} != {DEST_PRELIM_TARGET_WIDTH}."
            )
        if page_height != DEST_PRELIM_TARGET_HEIGHT:
            raise Exception(
                f"Wrong width for front page '{srce_page.filename}':"
                f" {page_height} != {DEST_PRELIM_TARGET_HEIGHT}."
            )

    dest_image = srce_page_image.resize(
        size=(DEST_PRELIM_TARGET_WIDTH, DEST_PRELIM_TARGET_HEIGHT),
        resample=Image.Resampling.BICUBIC,
    )

    if srce_page.filename == TITLE_EMPTY_IMAGE_FILEPATH:
        write_introduction(comic, dest_image)

    return dest_image


def get_dest_splash_page(splash_image: Image, srce_page: CleanPage) -> Image:
    splash_width, splash_height = splash_image.size
    if splash_width != DEST_PRELIM_TARGET_WIDTH:
        raise Exception(
            f"Wrong width for splash '{srce_page.filename}':"
            f" {splash_width} != {DEST_PRELIM_TARGET_WIDTH}."
        )

    dest_page_image = Image.open(EMPTY_IMAGE_FILEPATH, "r")
    dest_page_width, dest_page_height = dest_page_image.size
    if dest_page_width != splash_width:
        raise Exception(
            f"Wrong width for empty splash '{EMPTY_IMAGE_FILEPATH}':"
            f" {dest_page_width} != {splash_width}."
        )
    if dest_page_height != DEST_PRELIM_TARGET_HEIGHT:
        raise Exception(
            f"Wrong height for empty splash '{EMPTY_IMAGE_FILEPATH}':"
            f" {dest_page_height} != {DEST_PRELIM_TARGET_HEIGHT}."
        )
    if splash_height > dest_page_height:
        raise Exception(
            f"Wrong height for splash '{srce_page.filename}':"
            f" {splash_height} > {dest_page_height}."
        )

    splash_top = (dest_page_height - splash_height) / 2
    insert_pos = (0, int(splash_top))
    dest_page_image.paste(splash_image, insert_pos)

    return dest_page_image


def get_dest_main_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    dest_page_image = srce_page_image.resize(
        size=(DEST_WIDTH, DEST_HEIGHT), resample=Image.Resampling.BICUBIC
    )
    dest_page_image = dest_page_image.crop(get_crop_box(comic, dest_page))

    dest_final_target_width = DEST_PRELIM_TARGET_WIDTH - comic.trim_amount
    if dest_page_image.width != dest_final_target_width:
        raise Exception(
            f'Width mismatch for page "{srce_page.filename}":'
            f"{dest_page_image.width} != {dest_final_target_width}"
        )
    if dest_page_image.height != DEST_PRELIM_TARGET_HEIGHT:
        raise Exception(
            f'Height mismatch for page "{srce_page.filename}":'
            f"{dest_page_image.height} != {DEST_PRELIM_TARGET_HEIGHT}"
        )

    write_page_number(comic, dest_page_image, dest_page, PAGE_NUM_COLOR)

    return dest_page_image


def get_crop_box(comic: ComicBook, page: CleanPage) -> Tuple[int, int, int, int]:
    left_trim_amount, right_trim_amount = get_trim_amounts(comic, page)

    upper = DEST_Y_MARGINS_TRIM
    lower = DEST_HEIGHT - DEST_Y_MARGINS_TRIM
    left = left_trim_amount + DEST_X_MARGINS_TRIM
    right = (DEST_WIDTH - DEST_X_MARGINS_TRIM) - right_trim_amount

    return left, upper, right, lower


def get_trim_amounts(comic: ComicBook, page: CleanPage) -> Tuple[int, int]:
    if page.page_type in FRONT_PAGES:
        return 0, 0

    if page.trim_left:
        left_trim_amount = comic.trim_amount
        right_trim_amount = 0
    else:
        left_trim_amount = 0
        right_trim_amount = comic.trim_amount

    return left_trim_amount, right_trim_amount


def write_introduction(comic: ComicBook, image: Image):
    logging.info(f'Writing introduction - using inset file "{comic.intro_inset_file}".')

    draw = ImageDraw.Draw(image)

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
        image,
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
    draw_centered_text(text, image, draw, author_font, INTRO_AUTHOR_COLOR, top)
    top += text_height

    top += INTRO_TITLE_AUTHOR_BY_GAP
    text = f"{BARKS}"
    author_font = ImageFont.truetype(comic.title_font_file, comic.author_font_size)
    text_bbox = draw.multiline_textbbox((0, top), text, font=author_font)
    text_height = text_bbox[3] - text_bbox[1]
    draw_centered_text(text, image, draw, author_font, INTRO_AUTHOR_COLOR, top)
    top += text_height + INTRO_AUTHOR_INSET_GAP

    #    remaining_height = HEIGHT - BOTTOM_MARGIN - top

    inset = Image.open(comic.intro_inset_file, "r")
    inset_width, inset_height = inset.size
    new_inset_width = int(0.40 * comic.intro_inset_ratio * comic.get_trimmed_width())
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
    pub_text_top = DEST_HEIGHT - INTRO_BOTTOM_MARGIN - text_height

    inset_top = top + int((pub_text_top - top) / 2 - new_inset_height / 2)
    insert_pos = (int(comic.get_trimmed_center() - new_inset_width / 2), inset_top)
    image.paste(new_inset, insert_pos)

    draw_centered_multiline_text(
        comic.publication_text,
        image,
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


def write_page_number(comic: ComicBook, page_image: Image, page: CleanPage, color):
    draw = ImageDraw.Draw(page_image)

    page_num_x_start = comic.get_trimmed_center() - PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_x_end = comic.get_trimmed_center() + PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_y_start = (DEST_HEIGHT - PAGE_NUM_Y_OFFSET_FROM_BOTTOM) - PAGE_NUM_HEIGHT
    page_num_y_end = page_num_y_start + PAGE_NUM_HEIGHT

    # Get the color of a blank part of the page
    page_blank_color = page_image.getpixel(
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
    text = get_page_num_str(page)
    draw_centered_text(
        text,
        page_image,
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
    dry_run: bool, comic: ComicBook, dst_pages: List[CleanPage]
):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: shutil.copy2("{config_file}", "{comic.get_target_dir()}")'
        )
    else:
        shutil.copy2(config_file, comic.get_target_dir())

    write_readme_file(dry_run, comic)
    write_metadata_file(dry_run, comic, dst_pages)


def write_readme_file(dry_run: bool, comic: ComicBook):
    readme_file = os.path.join(comic.get_target_dir(), README_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write info to "{readme_file}".')
    else:
        with open(readme_file, "w") as f:
            f.write(f"{comic.title}\n")
            f.write("".ljust(len(comic.title), "-") + "\n")
            f.write("\n")
            now_str = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
            f.write(f"Created:           {now_str}\n")
            f.write(f'Archived ini file: "{os.path.basename(config_file)}"\n')


def write_metadata_file(dry_run: bool, comic: ComicBook, dst_pages: List[CleanPage]):
    metadata_file = os.path.join(comic.get_target_dir(), METADATA_FILENAME)
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
    intro_inset_file = os.path.join(
        CONFIGS_SUBDIR, safe_title + " Inset" + INSERT_FILE_EXT
    )

    cb_info: ComicBookInfo = all_comic_book_info[safe_title]
    source_info = SOURCE_COMICS[config["info"]["source_comic"]]
    source_dir = os.path.join(BARKS_ROOT_DIR, source_info.pub, source_info.title)

    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published by {source_info.pub}, {source_info.year}\n"
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
        trim_amount=config["info"].getint("trim_amount"),
        source_dir=source_dir,
        series_name=cb_info.series_name,
        number_in_series=cb_info.number_in_series,
        intro_inset_file=intro_inset_file,
        intro_inset_ratio=config["introduction"].getfloat("intro_inset_ratio", 1.0),
        publication_text=publication_text,
        images_in_order=[
            OriginalPage(
                key,
                PageType[config["pages"][key]],
                config["wrong_oddness"].getboolean(key, True),
            )
            for key in config["pages"]
        ],
    )


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
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=args.log_level,
    )

    config_file = args.ini_file
    if not os.path.isfile(config_file):
        raise Exception(f'Could not find ini file "{config_file}".')

    all_comic_book_info = get_all_comic_book_info("Configs/the-stories.csv")
    check_story_submitted_order(all_comic_book_info)

    front_pages = get_list_of_numbers(args.front_pages)
    main_pages = get_list_of_numbers(args.main_pages)

    comic_book = get_comic_book(config_file)

    if not os.path.isdir(comic_book.get_srce_image_dir()):
        raise Exception(
            f'Could not find directory "{comic_book.get_srce_image_dir()}".'
        )

    logging.info("")
    logging.info(f'Srce comic directory: "{comic_book.source_dir}".')
    logging.info(f'Dest comic directory: "{comic_book.get_target_dir()}".')
    logging.info(f'Dest comic zip:       "{comic_book.get_dest_comic_zip()}".')
    logging.info(f'Comic book series:    "{comic_book.series_name}".')
    logging.info("")
    logging.info(f"Dest width, height:        {DEST_WIDTH}, {DEST_HEIGHT}.")
    logging.info(
        f"Dest x, y trim:            {DEST_X_MARGINS_TRIM}, {DEST_Y_MARGINS_TRIM}."
    )
    logging.info(
        f"Dest target width, height: {DEST_PRELIM_TARGET_WIDTH}, {DEST_PRELIM_TARGET_HEIGHT}."
    )
    logging.info("")

    required_pages = get_required_pages_in_order(comic_book.images_in_order)
    srce_pages, dest_pages = get_srce_and_dest_pages_in_order(
        comic_book, required_pages, front_pages, main_pages
    )

    create_dest_dirs(args.dry_run, comic_book)
    process_pages(args.dry_run, comic_book, srce_pages, dest_pages)
    process_additional_files(args.dry_run, comic_book, dest_pages)

    print_comic_book_properties(comic_book, srce_pages, dest_pages)

    zip_comic_book(args.dry_run, comic_book)
