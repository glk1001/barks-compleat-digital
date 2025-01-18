import logging
import sys

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging

cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles_and_info = cmd_args.get_titles_and_info()

for title_and_info in titles_and_info:
    comic_book = comics_database.get_comic_book(title_and_info[0])

    srce_files = comic_book.get_final_srce_story_files(None)

    print()
    print(f'"{title_and_info[0]}" source files:')
    for srce_file in srce_files:
        print(f'    "{srce_file[0]}"')
    print()
