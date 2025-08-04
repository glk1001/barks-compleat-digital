import logging
import os
import sys
import time

from barks_fantagraphics.barks_titles import is_non_comic_title
from barks_fantagraphics.comics_cmd_args import CmdArgNames, CmdArgs
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_logging import setup_logging
from barks_fantagraphics.comics_utils import get_abbrev_path
from src.upscale_image import upscale_image_file

SCALE = 4


def upscayl(title_list: list[str]) -> None:
    start = time.time()

    num_upscayled_files = 0
    for title in title_list:
        if is_non_comic_title(title):
            logging.info(f'Not a comic title - not upscayling "{title}".')
            continue

        logging.info(f'Upscayling story "{title}"...')
        comic = comics_database.get_comic_book(title)

        srce_files = comic.get_final_srce_original_story_files(RESTORABLE_PAGE_TYPES)
        upscayl_files = comic.get_final_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES)

        for srce_file, (dest_file, _is_mod_file) in zip(srce_files, upscayl_files):
            if upscayl_file(srce_file[0], dest_file):
                num_upscayled_files += 1

    logging.info(
        f"\nTime taken to upscayl all {num_upscayled_files} files: {int(time.time() - start)}s.",
    )


def upscayl_file(srce_file: str, dest_file: str) -> bool:
    if not os.path.isfile(srce_file):
        raise FileNotFoundError(f'Could not find srce file: "{srce_file}".')
    if os.path.isfile(dest_file):
        logging.warning(f'Dest upscayl file exists - skipping: "{get_abbrev_path(dest_file)}".')
        return False

    start = time.time()

    logging.info(
        f'Upscayling srce file "{get_abbrev_path(srce_file)}"'
        f' to dest upscayl file "{get_abbrev_path(dest_file)}".',
    )
    upscale_image_file(srce_file, dest_file, SCALE)

    logging.info(f"\nTime taken to upscayl file: {int(time.time() - start)}s.")

    return True


setup_logging(logging.INFO)

# TODO(glk): Some issue with type checking inspection?
# noinspection PyTypeChecker
cmd_args = CmdArgs("Upscayl volume titles", CmdArgNames.TITLE | CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

comics_database = cmd_args.get_comics_database()

upscayl(cmd_args.get_titles())
