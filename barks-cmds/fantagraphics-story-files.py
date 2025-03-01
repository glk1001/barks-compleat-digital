import logging
import sys
from pathlib import Path

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import get_abbrev_path, setup_logging
from barks_fantagraphics.pages import get_srce_and_dest_pages_in_order

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

    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic_book)

    srce_pages = srce_and_dest_pages.srce_pages
    dest_pages = srce_and_dest_pages.dest_pages

    max_len_page_type = max([len(dp.page_type.name) for dp in dest_pages])

    print()
    print(f'"{title}" source files:')
    for srce_page, dest_page in zip(srce_pages, dest_pages):
        dest_page_num = Path(dest_page.page_filename).stem
        page_type = dest_page.page_type.name
        print(
            f'    "{dest_page_num} ({dest_page.page_num:02}) - {page_type:{max_len_page_type}}":'
            f' "{get_abbrev_path(srce_page.page_filename)}"'
        )
    print()
