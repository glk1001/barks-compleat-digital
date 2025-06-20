import logging
import os
import sys
from pathlib import Path
from typing import Union, List, Tuple

from PIL import Image, ImageOps

from barks_fantagraphics.comic_book import ComicBook, get_page_str, ModifiedType
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import JPG_FILE_EXT
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.fanta_comics_info import (
    FANTA_VOLUME_OVERRIDES_ROOT,
    FANTA_OVERRIDE_DIRECTORIES,
)
from barks_fantagraphics.pages import get_srce_and_dest_pages_in_order, CleanPage

Image.MAX_IMAGE_PIXELS = None

# TODO: Put these somewhere else
SRCE_STANDARD_WIDTH = 2175
SRCE_STANDARD_HEIGHT = 3000
DEST_JPG_QUALITY = 92
DEST_JPG_COMPRESS_LEVEL = 9


def get_srce_mod_files(comic: ComicBook) -> Union[None, List[Tuple[str, bool]]]:
    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    modified_srce_files = [
        get_mod_file(comic, srce)
        for srce in srce_and_dest_pages.srce_pages
        if srce.page_mod_type != ModifiedType.ORIGINAL
    ]

    return modified_srce_files


def get_mod_file(comic: ComicBook, srce: CleanPage) -> Tuple[str, bool]:
    page_num = get_page_str(srce.page_num)

    if os.path.isfile(comic.get_srce_original_fixes_story_file(page_num)):
        return comic.get_srce_original_fixes_story_file(page_num), False
    if os.path.isfile(comic.get_srce_upscayled_fixes_story_file(page_num)):
        return comic.get_srce_upscayled_fixes_story_file(page_num), True

    raise Exception(f'Expected to find a fixes file for "{srce.page_filename}".')


def downscale(srce_file: str, dest_file: str) -> None:
    print(f'Downscale "{srce_file}" to "{dest_file}"')

    image = Image.open(srce_file).convert("RGB")

    image_resized = ImageOps.contain(
        image,
        (SRCE_STANDARD_WIDTH, SRCE_STANDARD_HEIGHT),
        Image.Resampling.LANCZOS,
    )

    image_resized.save(
        dest_file,
        optimize=True,
        compress_level=DEST_JPG_COMPRESS_LEVEL,
        quality=DEST_JPG_QUALITY,
    )


def copy_file(srce_file: str, dest_file: str) -> None:
    print(f'Copy "{srce_file}" to "{dest_file}"...')

    image = Image.open(srce_file).convert("RGB")

    image.save(
        dest_file,
        optimize=True,
        compress_level=DEST_JPG_COMPRESS_LEVEL,
        quality=DEST_JPG_QUALITY,
    )


# TODO(glk): Some issue with type checking inspection?
# noinspection PyTypeChecker
cmd_args = CmdArgs(
    "Write Fantagraphics edited files to overrides directory",
    CmdArgNames.TITLE | CmdArgNames.VOLUME,
)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()

mod_dict = dict()
max_title_len = 0
for title in titles:
    comic_book = comics_database.get_comic_book(title)

    srce_mod_files = get_srce_mod_files(comic_book)
    if not srce_mod_files:
        continue

    override_dir = os.path.join(
        FANTA_VOLUME_OVERRIDES_ROOT, FANTA_OVERRIDE_DIRECTORIES[comic_book.get_fanta_volume()]
    )

    for srce_mod_file in srce_mod_files:
        mod_file = srce_mod_file[0]
        is_upscayled = srce_mod_file[1]

        mod_basename = Path(mod_file).stem + JPG_FILE_EXT
        override_file = os.path.join(override_dir, mod_basename)

        if is_upscayled:
            downscale(mod_file, override_file)
        else:
            copy_file(mod_file, override_file)
