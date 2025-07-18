import logging
import os
import sys
from enum import Enum, auto
from pathlib import Path
from typing import Union, List, Tuple

from PIL import Image

from barks_fantagraphics.comic_book import ComicBook, get_page_str, ModifiedType
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import JPG_FILE_EXT, PageType
from barks_fantagraphics.comics_logging import setup_logging
from barks_fantagraphics.comics_utils import delete_all_files_in_directory
from barks_fantagraphics.fanta_comics_info import (
    FANTA_VOLUME_OVERRIDES_ROOT,
    FANTA_OVERRIDE_DIRECTORIES,
)
from barks_fantagraphics.page_classes import CleanPage
from barks_fantagraphics.pages import get_sorted_srce_and_dest_pages, get_page_mod_type
from barks_fantagraphics.pil_image_utils import (
    open_pil_image_for_reading,
    downscale_jpg,
    SAVE_JPG_COMPRESS_LEVEL,
    SAVE_JPG_QUALITY,
)

Image.MAX_IMAGE_PIXELS = None

# TODO: Put these somewhere else
SRCE_STANDARD_WIDTH = 2175
SRCE_STANDARD_HEIGHT = 3000


class FileType(Enum):
    ORIGINAL = auto()
    UPSCAYLED = auto()
    TITLE = auto()


def get_srce_mod_files(comic: ComicBook) -> Union[None, List[Tuple[str, FileType]]]:
    srce_and_dest_pages = get_sorted_srce_and_dest_pages(comic, get_full_paths=True)

    modified_srce_files = [
        get_mod_file(comic, srce)
        for srce in srce_and_dest_pages.srce_pages
        if get_page_mod_type(comic, srce) != ModifiedType.ORIGINAL
    ]

    modified_srce_files.append(get_title_file(srce_and_dest_pages.dest_pages))

    return modified_srce_files


def get_title_file(dest_pages: List[CleanPage]) -> Tuple[str, FileType]:
    for page in dest_pages:
        if page.page_type == PageType.TITLE:
            return page.page_filename, FileType.TITLE

    assert False


def get_mod_file(comic: ComicBook, srce: CleanPage) -> Tuple[str, FileType]:
    page_num = get_page_str(srce.page_num)

    if os.path.isfile(comic.get_srce_original_fixes_story_file(page_num)):
        return comic.get_srce_original_fixes_story_file(page_num), FileType.ORIGINAL
    if os.path.isfile(comic.get_srce_upscayled_fixes_story_file(page_num)):
        return comic.get_srce_upscayled_fixes_story_file(page_num), FileType.UPSCAYLED

    raise Exception(f'Expected to find a fixes file for "{srce.page_filename}".')


def downscale(srce_file: str, dest_file: str) -> None:
    print(f'Downscale "{srce_file}" to "{dest_file}"')

    downscale_jpg(SRCE_STANDARD_WIDTH, SRCE_STANDARD_HEIGHT, srce_file, dest_file)


def copy_file(srce_file: str, dest_file: str) -> None:
    print(f'Copy "{srce_file}" to "{dest_file}"...')

    image = open_pil_image_for_reading(srce_file).convert("RGB")

    image.save(
        dest_file,
        optimize=True,
        compress_level=SAVE_JPG_COMPRESS_LEVEL,
        quality=SAVE_JPG_QUALITY,
    )


# TODO(glk): Some issue with type checking inspection?
# noinspection PyTypeChecker
cmd_args = CmdArgs(
    "Write Fantagraphics edited files to overrides directory",
    CmdArgNames.VOLUME,
)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

volumes = [int(v) for v in cmd_args.get_volumes()]

for volume in volumes:
    override_dir = os.path.join(FANTA_VOLUME_OVERRIDES_ROOT, FANTA_OVERRIDE_DIRECTORIES[volume])
    print(f'Deleting all files in override dir "{override_dir}".')
    delete_all_files_in_directory(override_dir)

    titles = [t[0] for t in comics_database.get_configured_titles_in_fantagraphics_volume(volume)]

    print()
    for title in titles:
        comic_book = comics_database.get_comic_book(title)

        srce_mod_files = get_srce_mod_files(comic_book)
        if not srce_mod_files:
            continue

        for srce_mod_file in srce_mod_files:
            mod_file = srce_mod_file[0]
            file_type = srce_mod_file[1]

            mod_basename = Path(mod_file).stem + JPG_FILE_EXT
            override_file = os.path.join(override_dir, mod_basename)

            if file_type == FileType.UPSCAYLED:
                downscale(mod_file, override_file)
            elif file_type == FileType.ORIGINAL:
                copy_file(mod_file, override_file)
            else:
                assert False
                # assert file_type == FileType.TITLE
                # override_file = os.path.join(override_dir, title + JPG_FILE_EXT)
                # copy_file(mod_file, override_file)

            print()
