import logging
import sys

from barks_fantagraphics.comic_book import get_jpg_page_list
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging

cmd_args = CmdArgs("Fantagraphics volume page counts", CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()

page_count = 0
for title in titles:
    comic_book = comics_database.get_comic_book(title)
    page_count += len(get_jpg_page_list(comic_book))

print(f"{len(titles)} titles, {page_count} pages")
