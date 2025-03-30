import json
import logging
import os
import sys
from typing import List, Tuple

from barks_fantagraphics.comic_book import ComicBook, get_page_str
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_info import get_fanta_volume_str
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.pages import PageType, get_srce_and_dest_pages_in_order
from barks_fantagraphics.panel_segmentation import BIG_NUM, get_kumiko_panel_bound


def get_story_splashes(comic: ComicBook) -> List[str]:
    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    splashes = []
    for srce_page, dest_page in zip(srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages):
        if srce_page.page_type is not PageType.BODY:
            continue
        if dest_page.page_num == 1:  # Don't count large panels on first page
            continue

        srce_page_str = get_page_str(srce_page.page_num)

        panels_info_file = comic.get_srce_panel_segments_file(srce_page_str)
        if not os.path.isfile(panels_info_file):
            raise Exception(f'Could not find panels segments info file "{panels_info_file}".')

        with open(panels_info_file, "r") as f:
            panels = json.load(f)["panels"]

        if has_splash_page(panels):
            splashes.append(srce_page_str)

    return splashes


MIN_MAX_MARGIN = 200


def has_splash_page(panels: List[Tuple[int, int, int, int]]) -> bool:
    if len(panels) > 5:
        return False

    max_width = -1
    max_height = -1
    min_width = BIG_NUM
    min_height = BIG_NUM
    for index, panel in enumerate(panels):
        bound = get_kumiko_panel_bound(panel)
#        print(bound)

        min_width = min(min_width, bound.width)
        min_height = min(min_height, bound.height)
        max_width = max(max_width, bound.width)
        max_height = max(max_height, bound.height)

    # print(min_width, max_width, min_height, max_height)
    # print()

    return (
        abs(max_width - min_width) > MIN_MAX_MARGIN
        and abs(max_height - min_height) > MIN_MAX_MARGIN
    )


cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()
titles = cmd_args.get_titles()

splashes_dict = dict()
max_title_len = 0
for title in titles:
    comic_book = comics_database.get_comic_book(title)

    story_splashes = get_story_splashes(comic_book)
    if not story_splashes:
        continue

    title_with_issue_num = comic_book.get_title_with_issue_num()
    if max_title_len < len(title_with_issue_num):
        max_title_len = len(title_with_issue_num)

    volume = comic_book.get_fanta_volume()

    splashes_dict[title_with_issue_num] = (volume, story_splashes)

for title in splashes_dict.keys():
    volume, story_splashes = splashes_dict[title]
    volume_str = get_fanta_volume_str(volume)
    splashes_str = ", ".join(story_splashes)

    print(f'"{title:<{max_title_len}}", {volume_str}, Splashes: {splashes_str}')
