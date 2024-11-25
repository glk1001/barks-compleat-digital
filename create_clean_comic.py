import argparse
import concurrent.futures
import datetime
import logging
import os
import shlex
import shutil
import sys
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Union

from PIL import Image, ImageFont, ImageDraw

from additional_file_writing import (
    write_readme_file,
    write_metadata_file,
    write_json_metadata,
    write_srce_dest_map,
    write_dest_panels_bboxes,
    write_summary,
)
from barks_fantagraphics.comic_book import (
    ComicBook,
    log_comic_book_params,
)
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from barks_fantagraphics.comics_info import (
    ComicBookInfoDict,
    CENSORED_TITLES,
    CS,
)
from barks_fantagraphics.consts import (
    DRY_RUN_STR,
    BARKS,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
    DEST_TARGET_ASPECT_RATIO,
    DEST_JPG_QUALITY,
    DEST_JPG_COMPRESS_LEVEL,
    FOOTNOTE_CHAR,
    MIN_HD_SRCE_HEIGHT,
    PageType,
    PAGES_WITHOUT_PANELS,
    PAINTING_PAGES,
    SPLASH_PAGES,
    INTRO_TEXT_FONT_FILE,
    PAGE_NUM_FONT_FILE,
    get_font_path,
)
from comics_integrity import check_comics_integrity
from image_io import open_image_for_reading
from out_of_date_checking import is_dest_file_out_of_date
from pages import (
    EMPTY_IMAGE_FILEPATH,
    SrceAndDestPages,
    CleanPage,
    get_max_timestamp,
    get_srce_and_dest_pages_in_order,
    get_page_num_str,
)
from panel_bounding import (
    init_bounding_box_processor,
    get_required_panels_bbox_width_height,
    get_scaled_panels_bbox_height,
    set_srce_panel_bounding_boxes,
    set_dest_panel_bounding_boxes,
)
from timing import Timing
from zipping import zip_comic_book, create_symlinks_to_comic_zip

INTRO_TOP = 350
INTRO_BOTTOM_MARGIN = INTRO_TOP
INTRO_TITLE_SPACING = 50
INTRO_TITLE_COLOR = (0, 0, 0)
INTRO_TITLE_AUTHOR_GAP = 130
INTRO_TITLE_AUTHOR_BY_GAP = INTRO_TITLE_AUTHOR_GAP
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
PAGE_NUM_COLOR = (10, 10, 10)

SPLASH_BORDER_COLOR = (128, 0, 0)
SPLASH_BORDER_WIDTH = 10


@dataclass
class CmdOptions:
    dry_run: bool = False
    no_cache: bool = False
    just_zip: bool = False
    just_symlinks: bool = False


def process_all_comic_books(options: CmdOptions, comics_db: ComicsDatabase) -> int:
    all_story_titles = comics_db.get_all_story_titles()

    logging.info(
        f'Processing all {len(all_story_titles)} titles in "{comics_db.get_story_titles_dir()}".'
    )

    ret_code = 0
    for title in all_story_titles:
        comic = comics_db.get_comic_book(title)
        if 0 != process_comic_book(options, comic):
            ret_code = 1

    return ret_code


def print_all_cmds(options: CmdOptions, comics_db: ComicsDatabase) -> int:
    for title in comics_db.get_all_story_titles():
        if 0 != print_cmd(options, comics_db, title):
            return 1

    return 0


def print_cmd(options: CmdOptions, comics_db: ComicsDatabase, story_title: str) -> int:
    dry_run_arg = "" if not options.dry_run else f" {DRY_RUN_ARG}"
    just_symlinks_arg = "" if not options.just_symlinks else f" {JUST_SYMLINKS_ARG}"
    no_cache_arg = "" if not options.no_cache else f" {NO_CACHE_ARG}"
    print(
        f"python3 {__file__} {BUILD_SINGLE_ARG}"
        f"{dry_run_arg}{just_symlinks_arg}{no_cache_arg}"
        f' {WORK_DIR_ARG} "{work_dir_root}"'
        f' {COMICS_DATABASE_DIR_ARG} "{comics_db.get_comics_database_dir()}"'
        f" {STORY_TITLE_ARG} {shlex.quote(story_title)}"
    )

    return 0


def show_all_mods(comics_db: ComicsDatabase) -> int:
    mod_dict = OrderedDict()
    max_title_len = 0
    for title in comics_db.get_all_story_titles():
        comic = comics_db.get_comic_book(title)

        mods = get_mods(comic)
        if not mods:
            continue

        if max_title_len < len(mods[0]):
            max_title_len = len(mods[0])

        mod_dict.update({get_mods(comic)})

    for title, mods in mod_dict.items():
        title_str = title + ":"
        dest_mods = f"{'Dest':<6} - {mods[0]}"
        srce_mods = mods[1]
        print(f"{title_str:<{max_title_len + 1}} {dest_mods}")
        print(f'{" ":<{max_title_len + 1}} {srce_mods}')

    return 0


def get_mods(comic: ComicBook) -> Union[None, Tuple[str, Tuple[str, str]]]:
    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    modified_dest_pages = [
        get_page_num_str(dest)
        for dest in srce_and_dest_pages.dest_pages
        if dest.page_is_modified and dest.page_type in [PageType.COVER, PageType.BODY]
    ]
    if not modified_dest_pages:
        return None

    mod_dest_pages_str = ",".join(modified_dest_pages)

    modified_srce_pages = [
        str(srce.page_num)
        for srce in srce_and_dest_pages.srce_pages
        if srce.page_is_modified and srce.page_type in [PageType.COVER, PageType.BODY]
    ]
    fanta_vol = f"FAN {comic.fanta_info.volume:>2}"
    mod_srce_pages_str = f"{fanta_vol} - {','.join(modified_srce_pages)}"

    title = comic.get_title_with_issue_num()

    return title, (mod_dest_pages_str, mod_srce_pages_str)


def process_single_comic_book(
    options: CmdOptions,
    comics_db: ComicsDatabase,
    story_title: str,
) -> int:
    comic = comics_db.get_comic_book(story_title)
    return process_comic_book(options, comic)


def process_comic_book(options: CmdOptions, comic: ComicBook) -> int:
    process_timing = Timing(datetime.now())

    if options.just_symlinks:
        create_symlinks_to_comic_zip(options.dry_run, options.no_cache, comic)
        return 0

    if options.just_zip:
        srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)
        max_dest_timestamp = get_max_timestamp(srce_and_dest_pages.dest_pages)
        zip_comic_book(options.dry_run, options.no_cache, comic, max_dest_timestamp)
        create_symlinks_to_comic_zip(options.dry_run, options.no_cache, comic)
        return 0

    srce_and_dest_pages, max_dest_timestamp = build_comic_book(
        options.dry_run, options.no_cache, comic
    )

    process_timing.end_time = datetime.now()
    logging.info(
        f"Time taken to complete comic: {process_timing.get_elapsed_time_in_seconds()} seconds"
    )

    write_summary(
        options.dry_run,
        comic,
        srce_and_dest_pages,
        max_dest_timestamp,
        process_timing,
        not options.no_cache,
    )

    return 0


def build_comic_book(
    dry_run: bool, no_cache: bool, comic: ComicBook
) -> Tuple[SrceAndDestPages, float]:
    srce_and_dest_pages = create_comic_book(dry_run, comic, not no_cache)
    max_dest_timestamp = get_max_timestamp(srce_and_dest_pages.dest_pages)

    zip_comic_book(dry_run, no_cache, comic, max_dest_timestamp)
    create_symlinks_to_comic_zip(dry_run, no_cache, comic)

    return srce_and_dest_pages, max_dest_timestamp


def create_comic_book(dry_run: bool, comic: ComicBook, caching: bool) -> SrceAndDestPages:
    pages = get_srce_and_dest_pages_in_order(comic)

    set_srce_panel_bounding_boxes(dry_run, caching, comic, pages.srce_pages)
    set_required_dimensions(comic, pages.srce_pages)
    set_dest_panel_bounding_boxes(comic, pages)

    log_comic_book_params(comic, caching, work_dir)

    create_dest_dirs(dry_run, comic)
    process_pages(dry_run, caching, comic, pages)
    process_additional_files(dry_run, comic, pages)

    return pages


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

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
            executor.submit(process_page, dry_run, cache_pages, comic, srce_page, dest_page)


def delete_all_files_in_directory(dry_run: bool, directory_path: str):
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Deleting all files in directory "{directory_path}".')
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

    page_num_y_centre = int(round(0.5 * (0.5 * (DEST_TARGET_HEIGHT - required_panels_bbox_height))))
    comic.required_dim.page_num_y_bottom = int(page_num_y_centre - (PAGE_NUM_HEIGHT / 2))

    logging.debug(f"Set srce average panels bbox width to {comic.srce_av_panels_bbox_width}.")
    logging.debug(f"Set srce average panels bbox height to {comic.srce_av_panels_bbox_height}.")
    logging.debug(f"Set required panels bbox width to {comic.required_dim.panels_bbox_width}.")
    logging.debug(f"Set required panels bbox height to {comic.required_dim.panels_bbox_height}.")
    logging.debug(f"Set page num y bottom to {comic.required_dim.page_num_y_bottom}.")
    logging.debug("")


def process_page(
    dry_run: bool,
    cache_pages: bool,
    comic: ComicBook,
    srce_page: CleanPage,
    dest_page: CleanPage,
):
    logging.info(
        f'Convert "{os.path.basename(srce_page.page_filename)}"'
        f" (page-type {srce_page.page_type.name})"
        f' to "{os.path.basename(dest_page.page_filename)}"'
        f" (page number = {get_page_num_str(dest_page)},"
        f" cache pages = {cache_pages})..."
    )

    srce_page_image = open_image_for_reading(srce_page.page_filename)
    if srce_page.page_type == PageType.BODY and srce_page_image.height < MIN_HD_SRCE_HEIGHT:
        raise Exception(
            f"Srce image error: min required height {MIN_HD_SRCE_HEIGHT}."
            f' Poor srce file resolution for "{srce_page.page_filename}":'
            f" {srce_page_image.width} x {srce_page_image.height}."
        )

    if (
        cache_pages
        and os.path.exists(dest_page.page_filename)
        and not is_dest_file_out_of_date(srce_page.page_filename, dest_page.page_filename)
    ):
        logging.debug(f'Caching on - using existing page file "{dest_page.page_filename}".')
        return

    dest_page_image = get_dest_page_image(comic, srce_page_image, srce_page, dest_page)

    if dry_run:
        logging.info(f'{DRY_RUN_STR}: Save changes to image "{dest_page.page_filename}".')
    else:
        dest_page_image.save(
            dest_page.page_filename,
            optimize=True,
            compress_level=DEST_JPG_COMPRESS_LEVEL,
            quality=DEST_JPG_QUALITY,
            comment="\n".join(get_dest_jpg_comments(srce_page, dest_page)),
        )
        logging.info(f'Saved changes to image "{dest_page.page_filename}".')

    logging.info("")


def get_dest_jpg_comments(srce_page: CleanPage, dest_page: CleanPage) -> List[str]:
    indent = "      "
    comments = [
        indent,
        f"{indent}Srce page num: {srce_page.page_num}",
        f"{indent}Srce page type: {srce_page.page_type.name}",
        f"{indent}Srce panels bbox: {dest_page.panels_bbox.x_min}, {dest_page.panels_bbox.y_min},"
        + f" {dest_page.panels_bbox.x_max}, {dest_page.panels_bbox.y_max}",
        f"{indent}Dest page num: {dest_page.page_num}",
    ]

    return comments


def get_dest_page_image(
    comic: ComicBook, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
) -> Image:
    log_page_info("Srce", srce_page_image, srce_page)
    log_page_info("Dest", None, dest_page)

    if dest_page.page_type in PAGES_WITHOUT_PANELS:
        dest_page_image = get_dest_non_body_page_image(comic, srce_page_image, srce_page, dest_page)
    else:
        dest_page_image = get_dest_main_page_image(comic, srce_page_image, srce_page, dest_page)

    rgb_dest_page_image = dest_page_image.convert("RGB")

    log_page_info("Dest", rgb_dest_page_image, dest_page)

    return rgb_dest_page_image


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
        return get_dest_no_panels_page_image(comic, srce_page_image, srce_page, dest_page)
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

    dest_page_image = get_dest_centred_page_image(no_panels_image, srce_page, dest_page_image)

    write_page_number(comic, dest_page_image, dest_page, PAGE_NUM_COLOR)

    return dest_page_image


def get_dest_black_bars_page_image(srce_page_image: Image, srce_page: CleanPage) -> Image:
    dest_page_image = Image.new("RGB", (DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT), (0, 0, 0))
    return get_dest_centred_page_image(srce_page_image, srce_page, dest_page_image)


def get_dest_centred_page_image(
    srce_page_image: Image, srce_page: CleanPage, dest_page_image: Image
) -> Image:
    srce_aspect_ratio = float(srce_page_image.height) / float(srce_page_image.width)
    if abs(srce_aspect_ratio - DEST_TARGET_ASPECT_RATIO) > 0.01:
        logging.debug(
            f"Wrong aspect ratio for page '{srce_page.page_filename}':"
            f" {srce_aspect_ratio:.2f} != {DEST_TARGET_ASPECT_RATIO :.2f}."
            f" Using black bars."
        )

    required_height = get_scaled_panels_bbox_height(
        DEST_TARGET_WIDTH, srce_page_image.width, srce_page_image.height
    )

    no_margins_image = srce_page_image.resize(
        size=(DEST_TARGET_WIDTH, required_height),
        resample=Image.Resampling.BICUBIC,
    )
    no_margins_aspect_ratio = float(no_margins_image.height) / float(no_margins_image.width)
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
            f'Width mismatch for page "{srce_page.page_filename}":'
            f"{dest_page_image.width} != {DEST_TARGET_WIDTH}"
        )
    if dest_page_image.height != DEST_TARGET_HEIGHT:
        raise Exception(
            f'Height mismatch for page "{srce_page.page_filename}":'
            f"{dest_page_image.height} != {DEST_TARGET_HEIGHT}"
        )

    write_page_number(comic, dest_page_image, dest_page, PAGE_NUM_COLOR)

    return dest_page_image


def get_centred_dest_page_image(dest_page: CleanPage, dest_panels_image: Image) -> Image:
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

    title, title_fonts, text_height = get_title_and_fonts(draw, comic)

    draw_centered_multiline_title_text(
        comic,
        title,
        title_fonts,
        INTRO_TITLE_COLOR,
        top,
        spacing=INTRO_TITLE_SPACING,
        image=dest_page_image,
        draw=draw,
    )
    top += text_height + INTRO_TITLE_SPACING

    top += INTRO_TITLE_AUTHOR_GAP
    text = "by"
    by_font_size = int(0.6 * comic.author_font_size)
    by_font = ImageFont.truetype(comic.title_font_file, by_font_size)
    text_height = get_intro_text_height(draw, text, by_font)
    draw_centered_text(text, dest_page_image, draw, by_font, INTRO_AUTHOR_COLOR, top)
    top += text_height

    top += INTRO_TITLE_AUTHOR_BY_GAP
    text = f"{BARKS}"
    author_font = ImageFont.truetype(comic.title_font_file, comic.author_font_size)
    text_height = get_intro_text_height(draw, text, author_font)
    draw_centered_text(text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top)
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
    text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=INTRO_TITLE_SPACING)
    return text_bbox[3] - text_bbox[1]


def get_intro_text_width(draw: ImageDraw.Draw, text: str, font: ImageFont) -> int:
    text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=INTRO_TITLE_SPACING)
    return text_bbox[2] - text_bbox[0]


def get_title_and_fonts(
    draw: ImageDraw.Draw, comic: ComicBook
) -> Tuple[List[str], List[ImageFont.truetype], int]:
    title = comic.get_comic_title()
    font_file = comic.title_font_file
    font_size = comic.title_font_size

    if title.startswith(CS):
        add_footnote = comic.file_title in CENSORED_TITLES

        title_and_fonts = get_comics_and_stories_title_and_fonts(
            draw, title, font_file, font_size, add_footnote
        )
        return title_and_fonts

    title_font = ImageFont.truetype(font_file, font_size)
    text_height = get_intro_text_height(draw, title, title_font)
    return [title], [title_font], text_height


def get_comics_and_stories_title_and_fonts(
    draw: ImageDraw.Draw, title: str, font_file: str, font_size: int, add_footnote: bool
) -> Tuple[List[str], List[ImageFont.truetype], int]:
    assert title.startswith(CS)

    comic_num = title[len(CS) :]
    if add_footnote:
        comic_num += FOOTNOTE_CHAR

    title_split = ["Comics", "and Stories", comic_num]
    title_fonts = [
        ImageFont.truetype(font_file, font_size),
        ImageFont.truetype(font_file, int(0.5 * font_size)),
        ImageFont.truetype(font_file, font_size),
    ]

    text_height = get_intro_text_height(draw, title, title_fonts[0])

    return title_split, title_fonts, text_height


def draw_centered_text(text: str, image: Image, draw: ImageDraw, font: ImageFont, color, top: int):
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
    draw.multiline_text((left, top), text, fill=color, font=font, align="center", spacing=spacing)


def draw_centered_multiline_title_text(
    comic: ComicBook,
    text_vals: List[str],
    fonts: List[ImageFont],
    color: Tuple[int, int, int],
    top: int,
    spacing: int,
    image: Image,
    draw: ImageDraw,
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

            has_footnote = False
            if text[-1] == FOOTNOTE_CHAR:
                has_footnote = True
                text = text[:-1]
                text_width -= 1

            draw.multiline_text(
                (left, line_top + line_top_extra),
                text,
                fill=color,
                font=font,
                align="center",
                spacing=spacing,
            )
            left += text_width

            if has_footnote:
                draw_superscript_title_text(
                    comic,
                    FOOTNOTE_CHAR,
                    color,
                    left,
                    line_top + line_top_extra,
                    spacing,
                    draw,
                )

            line_start = False
        line_top += int(1.5 * max_font_height)


def draw_superscript_title_text(
    comic: ComicBook,
    text: str,
    color: Tuple[int, int, int],
    left: int,
    top: int,
    spacing: int,
    draw: ImageDraw,
):
    superscript_font_size = int(0.7 * comic.title_font_size)
    superscript_font = ImageFont.truetype(comic.title_font_file, superscript_font_size)
    draw.multiline_text(
        (
            left - int(0.75 * superscript_font_size),
            top - 20,
        ),
        text,
        fill=color,
        font=superscript_font,
        align="center",
        spacing=spacing,
    )


def write_page_number(comic: ComicBook, dest_page_image: Image, dest_page: CleanPage, color):
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


def process_additional_files(dry_run: bool, comic: ComicBook, pages: SrceAndDestPages):
    if dry_run:
        logging.info(f'{DRY_RUN_STR}: shutil.copy2("{comic.ini_file}", "{comic.get_dest_dir()}")')
    else:
        shutil.copy2(comic.ini_file, comic.get_dest_dir())

    write_readme_file(dry_run, comic)
    write_metadata_file(dry_run, comic, pages.dest_pages)
    write_json_metadata(dry_run, comic, pages.dest_pages)
    write_srce_dest_map(dry_run, comic, pages)
    write_dest_panels_bboxes(dry_run, comic, pages.dest_pages)


def create_dest_dirs(dry_run: bool, comic: ComicBook):
    if not os.path.isdir(comic.get_dest_image_dir()):
        if dry_run:
            logging.info(f'{DRY_RUN_STR} Would have made directory "{comic.get_dest_image_dir()}".')
            return
        os.makedirs(comic.get_dest_image_dir())

    if not os.path.isdir(comic.get_dest_image_dir()):
        raise Exception(f'Could not make directory "{comic.get_dest_image_dir()}".')


def get_key_number(ordered_dict: ComicBookInfoDict, key: str) -> int:
    n = 1
    for k in ordered_dict:
        if k == key:
            return n
        n += 1
    return -1


def setup_logging(log_level) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=log_level,
    )


def get_work_dir(wrk_dir_root: str) -> str:
    os.makedirs(wrk_dir_root, exist_ok=True)
    if not os.path.isdir(wrk_dir_root):
        raise Exception(f'Could not find work root directory "{wrk_dir_root}".')

    wrk_dir = os.path.join(wrk_dir_root, datetime.now().strftime("%Y_%m_%d-%H_%M_%S.%f"))
    os.makedirs(wrk_dir)

    return wrk_dir


LOG_LEVEL_ARG = "--log-level"
WORK_DIR_ARG = "--work-dir"
DRY_RUN_ARG = "--dry-run"
NO_CACHE_ARG = "--no-cache"
JUST_ZIP_ARG = "--just-zip"
JUST_SYMLINKS_ARG = "--just-symlinks"
COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
STORY_TITLE_ARG = "--story-title"

BUILD_ALL_ARG = "build-all"
BUILD_SINGLE_ARG = "build-single"
LIST_CMDS_ARG = "list-cmds"
CHECK_INTEGRITY_ARG = "check-integrity"
SHOW_MODS_ARG = "show-mods"


def get_args():
    global_parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Create a clean Barks comic from Fantagraphics source."
    )

    subparsers = global_parser.add_subparsers(
        dest="cmd_name",
        title="subcommands",
        help="comic building commands",
        required=True,
    )

    build_all_parser = subparsers.add_parser(BUILD_ALL_ARG, help="build all available comics")
    build_all_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    build_all_parser.add_argument(JUST_ZIP_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    build_all_parser.add_argument(DRY_RUN_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(NO_CACHE_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(WORK_DIR_ARG, type=str, required=True)
    build_all_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    build_single_parser = subparsers.add_parser(BUILD_SINGLE_ARG, help="build a single comic")
    build_single_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    build_single_parser.add_argument(STORY_TITLE_ARG, action="store", type=str, required=True)
    build_single_parser.add_argument(
        JUST_ZIP_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        DRY_RUN_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        NO_CACHE_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    build_single_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    list_cmds_parser = subparsers.add_parser(
        LIST_CMDS_ARG, help="list the python commands to build all comics"
    )
    list_cmds_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    list_cmds_parser.add_argument(DRY_RUN_ARG, action="store_true", required=False, default=False)
    list_cmds_parser.add_argument(NO_CACHE_ARG, action="store_true", required=False, default=False)
    list_cmds_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    list_cmds_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    check_integrity_parser = subparsers.add_parser(
        CHECK_INTEGRITY_ARG, help="check the integrity of all previously built comics"
    )
    check_integrity_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    check_integrity_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    check_integrity_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    show_mods_parser = subparsers.add_parser(SHOW_MODS_ARG, help="list all modified pages")
    show_mods_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    show_mods_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    show_mods_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    args = global_parser.parse_args()

    return args


def get_cmd_options(args) -> CmdOptions:
    return CmdOptions(
        dry_run=args.dry_run,
        no_cache=args.no_cache,
        just_zip=hasattr(args, "just_zip") and args.just_zip,
        just_symlinks=hasattr(args, "just_symlinks") and args.just_symlinks,
    )


if __name__ == "__main__":
    cmd_args = get_args()

    setup_logging(cmd_args.log_level)

    work_dir_root = cmd_args.work_dir
    work_dir = get_work_dir(work_dir_root)

    cmd_options = get_cmd_options(cmd_args)
    comics_database = ComicsDatabase(cmd_args.comics_database_dir)

    init_bounding_box_processor(work_dir)

    if cmd_args.cmd_name == CHECK_INTEGRITY_ARG:
        exit_code = check_comics_integrity(comics_database)
    elif cmd_args.cmd_name == LIST_CMDS_ARG:
        exit_code = print_all_cmds(cmd_options, comics_database)
    elif cmd_args.cmd_name == SHOW_MODS_ARG:
        exit_code = show_all_mods(comics_database)
    elif cmd_args.cmd_name == BUILD_ALL_ARG:
        exit_code = process_all_comic_books(cmd_options, comics_database)
    elif cmd_args.cmd_name == BUILD_SINGLE_ARG:
        exit_code = process_single_comic_book(cmd_options, comics_database, cmd_args.story_title)
    else:
        raise Exception(f'ERROR: Unknown cmd_arg "{cmd_args.cmd_name}".')

    if exit_code != 0:
        print(f"\nThere were errors: exit code = {exit_code}.")
        sys.exit(exit_code)
