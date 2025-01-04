import logging
import sys

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import STORY_PAGE_TYPES
from barks_fantagraphics.comics_utils import setup_logging

cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()

for title in titles:
    comic_book = comics_database.get_comic_book(title)

    srce_files = comic_book.get_final_srce_story_files(STORY_PAGE_TYPES)

    print(title)
    for srce_file in srce_files:
        print(f'    "{srce_file[0]}"')
    print()
