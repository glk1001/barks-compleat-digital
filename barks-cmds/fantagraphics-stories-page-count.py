import logging
import sys

from barks_fantagraphics.comic_book import get_total_num_pages
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_logging import setup_logging

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
    num_pages = get_total_num_pages(comic_book)
    if num_pages <= 1:
        raise Exception(f'For title "{title}", the page count is too small.')
    page_count += num_pages

print(f"{len(titles)} titles, {page_count} pages")
