import logging
import os
import sys
from typing import Union, Tuple

from barks_fantagraphics.comic_book import ComicBook, get_page_str, ModifiedType
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import PageType, ROMAN_NUMERALS, FRONT_MATTER_PAGES
from barks_fantagraphics.comics_logging import setup_logging
from barks_fantagraphics.fanta_comics_info import get_fanta_volume_str
from barks_fantagraphics.page_classes import CleanPage
from barks_fantagraphics.pages import (
    get_sorted_srce_and_dest_pages,
    get_page_mod_type,
)


def get_srce_dest_mods_map(comic: ComicBook) -> Union[None, Tuple[str, str]]:
    srce_and_dest_pages = get_sorted_srce_and_dest_pages(comic, get_full_paths=True)

    modified_srce_pages = [
        f"{get_page_str(srce.page_num):>4} ({get_mod_type(comic, srce)})"
        for srce in srce_and_dest_pages.srce_pages
        if get_page_mod_type(comic, srce) != ModifiedType.ORIGINAL
    ]
    fanta_vol = get_fanta_volume_str(comic.fanta_book.volume)
    mod_srce_pages_str = f"{fanta_vol} - {','.join(modified_srce_pages)}"

    modified_dest_pages = [
        f"{get_page_num_str(dest):>4}    "
        for srce, dest in zip(srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages)
        if get_page_mod_type(comic, srce) != ModifiedType.ORIGINAL
    ]
    if not modified_dest_pages:
        return None

    mod_dest_pages_str = ",".join(modified_dest_pages)

    return mod_dest_pages_str, mod_srce_pages_str


def get_page_num_str(page: CleanPage) -> str:
    page_number = page.page_num

    if page.page_type not in FRONT_MATTER_PAGES:
        return str(page_number)

    if page.page_type == PageType.FRONT:
        assert page_number == 0
        return " Fr"

    assert page_number in ROMAN_NUMERALS
    return ROMAN_NUMERALS[page_number]


def get_mod_type(comic: ComicBook, srce: CleanPage) -> str:
    page_num = get_page_str(srce.page_num)

    if os.path.isfile(comic.get_srce_original_fixes_story_file(page_num)):
        return "O"
    if os.path.isfile(comic.get_srce_upscayled_fixes_story_file(page_num)):
        return "U"

    raise Exception(f'Expected to find a fixes file for "{srce.page_filename}".')


# TODO(glk): Some issue with type checking inspection?
# noinspection PyTypeChecker
cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
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

    srce_dest_mods_map = get_srce_dest_mods_map(comic_book)
    if not srce_dest_mods_map:
        continue

    title_with_issue_num = comic_book.get_title_with_issue_num()
    if max_title_len < len(title_with_issue_num):
        max_title_len = len(title_with_issue_num)

    mod_dict[title_with_issue_num] = srce_dest_mods_map

for title in mod_dict.keys():
    srce_dest_mods_map = mod_dict[title]
    title_str = title + ":"
    dest_mods = f"{'Dest':<8} - {srce_dest_mods_map[0]}"
    srce_mods = srce_dest_mods_map[1]
    print(f"{title_str:<{max_title_len + 1}} {dest_mods}")
    print(f'{" ":<{max_title_len + 1}} {srce_mods}')
