import argparse
import collections
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
    DONALD_DUCK_ADVENTURES,
    DONALD_DUCK_ADVENTURES_START_NUM,
    SOURCE_COMICS,
)

THIS_SCRIPT_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

DRY_RUN_STR = "DRY_RUN"

DEST_WIDTH = 2216
DEST_HEIGHT = 3056
DEST_X_MARGINS_TRIM = 48
DEST_Y_MARGINS_TRIM = 48
DEST_TARGET_WIDTH = DEST_WIDTH - (2 * DEST_Y_MARGINS_TRIM)
DEST_TARGET_HEIGHT = DEST_HEIGHT - (2 * DEST_Y_MARGINS_TRIM)

FONT_DIR = str(Path.home()) + "/Prj/fonts"
# INTRO_TITLE_DEFAULT_FONT_FILE = 'Expressa-Heavy.ttf'
# INTRO_TITLE_DEFAULT_FONT_FILE = 'Blenda Script.otf'
INTRO_TITLE_DEFAULT_FONT_FILE = FONT_DIR + "/Carl Barks Script.ttf"
# INTRO_TITLE_DEFAULT_FONT_FILE = 'Square.ttf'
# INTRO_TITLE_DEFAULT_FONT_FILE = 'chiselscript.ttf'
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

PAGE_NUM_X_OFFSET_FROM_CENTRE = 100
PAGE_NUM_Y_OFFSET_FROM_BOTTOM = 140
PAGE_NUM_X_BLANK_PIXEL_OFFSET = 200
PAGE_NUM_HEIGHT = 40
PAGE_NUM_FONT_SIZE = 30

BARKS = "Carl Barks"
BARKS_ROOT_DIR = str(Path.home()) + f"/Books/{BARKS}"
TITLE_EMPTY_IMAGE_FILEPATH = f"{THIS_SCRIPT_DIR}/title_empty.png"
LAST_EMPTY_IMAGE_FILEPATH = f"{THIS_SCRIPT_DIR}/last_empty.png"
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
    FRONT_MATTER = 4
    BODY = 5
    BACK_MATTER = 6


FRONT_PAGES = [PageType.FRONT, PageType.TITLE, PageType.COVER, PageType.FRONT_MATTER]


@dataclass
class OriginalPage:
    filenames: str
    page_type: PageType
    is_odd_correct: bool = True


@dataclass
class CleanPage:
    filename: str
    is_odd: bool
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
    series: str
    series_book_num: int
    intro_inset_file: str
    intro_inset_ratio: float
    publication_text: str
    images_in_order: List[OriginalPage]

    def get_target_dir(self):
        safe_title = self.title.replace("\n", " ")
        return os.path.join(
            BARKS_ROOT_DIR, f"{self.series}", f"{self.series_book_num:03d} {safe_title}"
        )

    def get_srce_image_dir(self):
        return os.path.join(self.source_dir, IMAGES_SUBDIR)

    def get_dest_image_dir(self):
        return os.path.join(self.get_target_dir(), IMAGES_SUBDIR)

    def get_trimmed_width(self):
        return DEST_WIDTH - self.trim_amount

    def get_trimmed_center(self):
        return int(self.get_trimmed_width() / 2)


def print_comic_book_properties(comic: ComicBook):
    logging.debug(f'title = "{comic.title}"')
    logging.debug(f'source_dir = "{comic.source_dir}"')
    logging.debug(f'target_dir = "{comic.get_target_dir()}"')
    logging.debug(f'title_font_file = "{get_font_path(comic.title_font_file)}"')
    logging.debug(f"title_font_size = {comic.title_font_size}")
    logging.debug(f"author_font_size = {comic.author_font_size}")
    logging.debug(f"trim_amount = {comic.trim_amount}")
    logging.debug(f"series = {comic.series}")
    logging.debug(f"series_book_num = {comic.series_book_num}")
    logging.debug(f'intro_inset_file = "{comic.intro_inset_file}"')
    logging.debug(f"intro_inset_ratio = {comic.intro_inset_ratio}")
    logging.debug(f"publication_text = \n{comic.publication_text}")
    for pg in comic.images_in_order:
        logging.debug(
            f"pages = {pg.filenames}, page_type = {pg.page_type}, oddness = {pg.is_odd_correct}"
        )


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)


def get_required_pages_in_order(images_in_book: List[OriginalPage]) -> List[CleanPage]:
    req_pages = []

    for image in images_in_book:
        if image.filenames == TITLE_EMPTY_FILENAME:
            req_pages.append(CleanPage(image.filenames, True, PageType.FRONT_MATTER))
            continue
        if image.filenames == LAST_EMPTY_FILENAME:
            req_pages.append(CleanPage(image.filenames, True, PageType.BACK_MATTER))
            continue

        if "-" not in image.filenames:
            filename = image.filenames
            page_type = image.page_type
            file_num = int(filename)
            is_odd = file_num % 2 != 0
            if not image.is_odd_correct:
                is_odd = not is_odd
            req_pages.append(CleanPage(filename, is_odd, page_type, file_num))
        else:
            page_type = image.page_type
            start, end = image.filenames.split("-")
            start_num = int(start)
            end_num = int(end)
            for file_num in range(start_num, end_num + 1):
                filename = f"{file_num:03d}"
                is_odd = file_num % 2 != 0
                if not image.is_odd_correct:
                    is_odd = not is_odd
                req_pages.append(CleanPage(filename, is_odd, page_type, file_num))

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
        else:
            page_num += 1

        if len(these_front_pages) == 0 and len(these_main_pages) == 0:
            add_page = True
        elif page.page_type in FRONT_PAGES and page_num in these_front_pages:
            add_page = True
        elif (
            page.page_type in [PageType.BODY, PageType.BACK_MATTER]
            and page_num in these_main_pages
        ):
            add_page = True
        else:
            add_page = False

        if add_page:
            logging.debug(
                f'Adding "{os.path.basename(srce_file)}" as type'
                + f' "{page.page_type.name}" with page number {page_num}.'
            )
            srce_page_list.append(CleanPage(srce_file, page.is_odd, page.page_type))
            dest_page_list.append(
                CleanPage(dest_file, page.is_odd, page.page_type, page_num)
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
        f'Convert "{srce_page.page_type.name}" page "{os.path.basename(srce_page.filename)}"'
        + f' to "{os.path.basename(dest_page.filename)}"...'
    )

    im = Image.open(srce_page.filename, "r")
    width, height = im.size
    logging.debug(
        f'Srce: width = {width}, height = {height}, page_type = "{srce_page.page_type.name}".'
    )

    new_im = im.resize(size=(DEST_WIDTH, DEST_HEIGHT), resample=Image.BICUBIC)

    if dest_page.page_type not in [PageType.FRONT, PageType.COVER]:
        new_im = new_im.crop(get_crop_box(comic, dest_page))
        if new_im.width != DEST_TARGET_WIDTH:
            raise Exception(
                f'Width mismatch for page "{srce_page.filename}":'
                f"{new_im.width} != {DEST_TARGET_WIDTH}"
            )
        if new_im.height != DEST_TARGET_HEIGHT:
            raise Exception(
                f'Height mismatch for page "{srce_page.filename}":'
                f"{new_im.height} != {DEST_TARGET_HEIGHT}"
            )

    new_width, new_height = new_im.size
    logging.debug(
        f"Dest: width = {new_width}, height = {new_height}, page number = {dest_page.page_num}"
    )

    if dest_page.page_type not in [PageType.FRONT, PageType.COVER]:
        write_page_number(comic, new_im, dest_page, PAGE_NUM_COLOR)

    if srce_page.filename == TITLE_EMPTY_IMAGE_FILEPATH:
        write_introduction(comic, new_im)

    rgb_im = new_im.convert("RGB")

    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Save changes to image "{dest_page.filename}".')
    else:
        rgb_im.save(dest_page.filename, optimize=True, compress_level=9)
        logging.info(f'Saved changes to image "{dest_page.filename}".')

    logging.info("")


def get_crop_box(comic: ComicBook, page: CleanPage) -> Tuple[int, int, int, int]:
    upper = DEST_Y_MARGINS_TRIM
    lower = DEST_HEIGHT - DEST_Y_MARGINS_TRIM
    if page.is_odd:
        # Crop the left
        left = comic.trim_amount + DEST_X_MARGINS_TRIM
        right = DEST_WIDTH - DEST_X_MARGINS_TRIM
    else:
        # Crop the right
        left = DEST_X_MARGINS_TRIM
        right = (DEST_WIDTH - DEST_X_MARGINS_TRIM) - comic.trim_amount

    return left, upper, right, lower


def write_introduction(comic: ComicBook, image: Image):
    logging.info(f'Writing introduction - using inset file "{comic.intro_inset_file}".')

    draw = ImageDraw.Draw(image)

    top = INTRO_TOP
    text = comic.title
    title_font = ImageFont.truetype(comic.title_font_file, comic.title_font_size)
    text_width, text_height = draw.multiline_textsize(
        text, font=title_font, spacing=INTRO_TITLE_SPACING
    )
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
    text_width, text_height = draw.textsize(text, font=author_font)
    draw_centered_text(text, image, draw, author_font, INTRO_AUTHOR_COLOR, top)
    top += text_height

    top += INTRO_TITLE_AUTHOR_BY_GAP
    text = f"{BARKS}"
    author_font = ImageFont.truetype(comic.title_font_file, comic.author_font_size)
    text_width, text_height = draw.textsize(text, font=author_font)
    draw_centered_text(text, image, draw, author_font, INTRO_AUTHOR_COLOR, top)
    top += text_height + INTRO_AUTHOR_INSET_GAP

    #    remaining_height = HEIGHT - BOTTOM_MARGIN - top

    inset = Image.open(comic.intro_inset_file, "r")
    inset_width, inset_height = inset.size
    new_inset_width = int(0.40 * comic.intro_inset_ratio * comic.get_trimmed_width())
    new_inset_height = int((inset_height / inset_width) * new_inset_width)
    new_inset = inset.resize(
        size=(new_inset_width, new_inset_height), resample=Image.BICUBIC
    )

    pub_text_font = ImageFont.truetype(
        get_font_path(INTRO_TEXT_FONT_FILE), INTRO_PUB_TEXT_FONT_SIZE
    )
    text_width, text_height = draw.multiline_textsize(
        comic.publication_text, font=pub_text_font, spacing=INTRO_PUB_TEXT_SPACING
    )
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
    w, h = draw.textsize(text, font)
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
    w, h = draw.textsize(text, font)
    left = (image.width - w) / 2
    draw.multiline_text(
        (left, top), text, fill=color, font=font, align="center", spacing=spacing
    )


def write_page_number(comic: ComicBook, image: Image, page: CleanPage, color):
    draw = ImageDraw.Draw(image)

    page_num_x_start = comic.get_trimmed_center() - PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_x_end = comic.get_trimmed_center() + PAGE_NUM_X_OFFSET_FROM_CENTRE
    page_num_y_start = (DEST_HEIGHT - PAGE_NUM_Y_OFFSET_FROM_BOTTOM) - PAGE_NUM_HEIGHT
    page_num_y_end = page_num_y_start + PAGE_NUM_HEIGHT

    # Get the color of a blank part of the page
    page_blank_color = image.getpixel(
        (
            page_num_x_start + PAGE_NUM_X_BLANK_PIXEL_OFFSET,
            page_num_y_end,
        )
    )

    # Remove the existing page number
    shape = (
        (
            page_num_x_start,
            page_num_y_start - 1,
        ),
        (
            page_num_x_end,
            page_num_y_end + 1,
        ),
    )
    draw.rectangle(shape, fill=page_blank_color)

    font = ImageFont.truetype(get_font_path(PAGE_NUM_FONT_FILE), PAGE_NUM_FONT_SIZE)
    text = (
        str(page.page_num)
        if page.page_type != PageType.FRONT_MATTER
        else ROMAN_NUMERALS[page.page_num]
    )
    draw_centered_text(
        text,
        image,
        draw,
        font,
        color,
        page_num_y_start,
    )


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
    README_FILENAME = "readme.txt"

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
    DOUBLE_PAGES_SECTION = "double_pages"
    PAGE_NUMBERS_SECTION = "page_numbers"
    METADATA_FILENAME = "metadata.txt"

    metadata_file = os.path.join(comic.get_target_dir(), METADATA_FILENAME)
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Write metadata to "{metadata_file}".')
    else:
        with open(metadata_file, "w") as f:
            f.write(f"[{DOUBLE_PAGES_SECTION}]\n")
            orig_page_num = 0
            for page in dst_pages:
                orig_page_num += 1
                if page.page_type not in FRONT_PAGES:
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


def get_key_number(ordered_dict: collections.OrderedDict, key: str) -> int:
    n = DONALD_DUCK_ADVENTURES_START_NUM
    for k in ordered_dict:
        if k == key:
            return n
        n += 1
    return -1


def get_comic_book(ini_file: str) -> ComicBook:
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    config.read(ini_file)

    title = config["info"]["title"]
    safe_title = title.replace("\n", " ")
    intro_inset_file = os.path.join(
        CONFIGS_SUBDIR, safe_title + " Inset" + INSERT_FILE_EXT
    )

    comic_book_info: ComicBookInfo = DONALD_DUCK_ADVENTURES[safe_title]
    source_info = SOURCE_COMICS[config["info"]["source_comic"]]
    source_dir = os.path.join(BARKS_ROOT_DIR, source_info.pub, source_info.title)

    publication_text = (
        f"First published in {comic_book_info.first_published}\n"
        + f"Submitted to Western Publishing on {comic_book_info.first_submitted}\n"
        + f"\n"
        + f"This edition published by {source_info.pub}, {source_info.year}\n"
        + f"Pages recolored by {source_info.colorist}"
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
        series=comic_book_info.grouping,
        series_book_num=get_key_number(DONALD_DUCK_ADVENTURES, safe_title),
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

    front_pages = get_list_of_numbers(args.front_pages)
    main_pages = get_list_of_numbers(args.main_pages)

    comic_book = get_comic_book(config_file)

    if not os.path.isdir(comic_book.get_srce_image_dir()):
        raise Exception(
            f'Could not find directory "{comic_book.get_srce_image_dir()}".'
        )

    logging.info("")
    logging.info(f'Srce image directory: "{comic_book.get_srce_image_dir()}".')
    logging.info(f'Dest image directory: "{comic_book.get_dest_image_dir()}".')
    logging.info("")
    logging.info(f"Dest width, height:        {DEST_WIDTH}, {DEST_HEIGHT}.")
    logging.info(
        f"Dest x, y trim:            {DEST_X_MARGINS_TRIM}, {DEST_Y_MARGINS_TRIM}."
    )
    logging.info(
        f"Dest target width, height: {DEST_TARGET_WIDTH}, {DEST_TARGET_HEIGHT}."
    )

    required_pages = get_required_pages_in_order(comic_book.images_in_order)
    srce_pages, dest_pages = get_srce_and_dest_pages_in_order(
        comic_book, required_pages, front_pages, main_pages
    )

    create_dest_dirs(args.dry_run, comic_book)
    process_pages(args.dry_run, comic_book, srce_pages, dest_pages)
    process_additional_files(args.dry_run, comic_book, dest_pages)

    print_comic_book_properties(comic_book)
