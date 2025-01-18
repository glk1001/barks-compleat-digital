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

titles_and_info = cmd_args.get_titles_and_info()

page_count = 0
for title_and_info in titles_and_info:
    comic_book = comics_database.get_comic_book(title_and_info[0])
    page_count += len(get_jpg_page_list(comic_book))

print(f"{len(titles_and_info)} titles, {page_count} pages")
