import logging
import os.path
import sys
from typing import List, Tuple, Dict

from barks_fantagraphics.comic_book import get_abbrev_jpg_page_list, get_safe_title, ComicBook
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames, ExtraArg
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_info import ComicBookInfo
from barks_fantagraphics.comics_utils import (
    dest_file_is_older_than_srce,
    get_timestamp,
    get_max_timestamp,
    get_titles_sorted_by_submission_date,
    setup_logging,
)

EMPTY_FLAG = " "
FIXES_FLAG = "F"

NOT_CONFIGURED_FLAG = "X"
CONFIGURED_FLAG = "C"
UPSCAYLED_FLAG = "U"
RESTORED_FLAG = "R"
PANELLED_FLAG = "P"
INSET_FLAG = "I"
BUILT_FLAG = "B"

BUILD_STATE_FLAGS = [
    NOT_CONFIGURED_FLAG,
    CONFIGURED_FLAG,
    UPSCAYLED_FLAG,
    RESTORED_FLAG,
    PANELLED_FLAG,
    INSET_FLAG,
    BUILT_FLAG,
]


def get_issue_titles(title_list: List[str]) -> List[Tuple[str, bool]]:
    comic_issue_titles = []
    for ttl in title_list:
        title_is_configured, _ = comics_database.is_story_title(ttl)
        if not title_is_configured:
            comic_issue_title = ttl
        else:
            comic = comics_database.get_comic_book(ttl)
            comic_issue_title = get_safe_title(comic.get_comic_issue_title())
        comic_issue_titles.append((comic_issue_title, title_is_configured))

    return comic_issue_titles


def is_upscayled(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES))


def is_restored(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES))


def has_inset_file(comic: ComicBook) -> bool:
    return os.path.isfile(comic.intro_inset_file)


def has_fixes(comic: ComicBook) -> bool:
    mods = [f[1] for f in comic.get_srce_with_fixes_story_files(RESTORABLE_PAGE_TYPES)]
    if any(mods):
        return True

    mods = [f[1] for f in comic.get_final_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES)]
    return any(mods)


def has_panel_bounds(comic: ComicBook) -> bool:
    if not is_restored(comic):
        return False
    if not all_files_exist(comic.get_srce_panel_segments_files(RESTORABLE_PAGE_TYPES)):
        return False

    restored_files = comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES)
    panel_segments_files = comic.get_srce_panel_segments_files(RESTORABLE_PAGE_TYPES)

    for restored_file, panel_segments_file in zip(restored_files, panel_segments_files):
        if dest_file_is_older_than_srce(restored_file, panel_segments_file):
            logging.debug(
                f'Panels segments file "{panel_segments_file}" is'
                f' out of date WRT restored file "{restored_file}".'
            )
            return False

    return True


def is_built(comic: ComicBook) -> bool:
    if not has_panel_bounds(comic):
        return False
    if not is_restored(comic):
        return False

    panel_segments_files = comic.get_srce_panel_segments_files(RESTORABLE_PAGE_TYPES)
    max_panel_segments_timestamp = get_max_timestamp(panel_segments_files)
    zip_file = comic.get_dest_comic_zip()
    if not os.path.isfile(zip_file):
        return False
    zip_file_timestamp = get_timestamp(zip_file)

    if zip_file_timestamp < max_panel_segments_timestamp:
        logging.debug(f'Zip file is out of date WRT panel segments files: "{zip_file}".')
        return False

    series_comic_zip_symlink = comic.get_dest_series_comic_zip_symlink()
    if not os.path.islink(series_comic_zip_symlink):
        return False
    series_comic_zip_symlink_timestamp = get_timestamp(series_comic_zip_symlink)

    if series_comic_zip_symlink_timestamp < zip_file_timestamp:
        logging.debug(f'Series symlink is out of date WRT zip file: "{series_comic_zip_symlink}".')
        return False

    year_comic_zip_symlink = comic.get_dest_year_comic_zip_symlink()
    if not os.path.islink(year_comic_zip_symlink):
        return False
    year_comic_zip_symlink_timestamp = get_timestamp(series_comic_zip_symlink)

    if year_comic_zip_symlink_timestamp < zip_file_timestamp:
        logging.debug(f'Year symlink is out of date WRT zip file: "{year_comic_zip_symlink}".')
        return False

    return True


def all_files_exist(file_list: List[str]) -> bool:
    for file in file_list:
        if not os.path.isfile(file):
            return False
    return True


def get_build_state_flag(comic: ComicBook) -> str:
    flag = CONFIGURED_FLAG

    restored = is_restored(comic)
    panels = has_panel_bounds(comic)

    if is_built(comic):
        flag = BUILT_FLAG
    elif has_inset_file(comic) and restored and panels:
        flag = INSET_FLAG
    elif panels:
        flag = PANELLED_FLAG
    elif restored:
        flag = RESTORED_FLAG
    elif is_upscayled(comic):
        flag = UPSCAYLED_FLAG

    return flag


def get_title_flags(
    title_list: List[str],
    titles_and_info_list: List[Tuple[str, ComicBookInfo]],
    issue_titles_info_list: List[Tuple[str, bool]],
) -> Tuple[Dict[str, Tuple[str, str, str, str]], int, int]:
    max_ttl_len = 0
    max_issue_ttl_len = 0
    ttl_flags = dict()

    for ttl, ttl_and_info, issue_ttl_info in zip(
        title_list, titles_and_info_list, issue_titles_info_list
    ):
        ttl_info = ttl_and_info[1]
        issue_ttl = issue_ttl_info[0]
        is_configured = issue_ttl_info[1]

        if not is_configured:
            display_ttl = ttl if ttl_info.is_barks_title else f"({ttl})"
            fixes_flg = EMPTY_FLAG
            build_state_flg = NOT_CONFIGURED_FLAG
            page_lst = ""
        else:
            comic_book = comics_database.get_comic_book(ttl)

            display_ttl = ttl if comic_book.is_barks_title() else f"({ttl})"
            fixes_flg = FIXES_FLAG if has_fixes(comic_book) else EMPTY_FLAG
            build_state_flg = get_build_state_flag(comic_book)
            page_lst = ", ".join(get_abbrev_jpg_page_list(comic_book))

        if fixes_flg not in fixes_filter:
            continue
        if build_state_flg not in built_filter:
            continue

        max_ttl_len = max(max_ttl_len, len(display_ttl))
        max_issue_ttl_len = max(max_issue_ttl_len, len(issue_ttl))

        ttl_flags[ttl] = (
            display_ttl,
            fixes_flg,
            build_state_flg,
            page_lst,
        )

    return ttl_flags, max_ttl_len, max_issue_ttl_len


FIXES_ARG = "--fixes"
BUILT_ARG = "--built"


def get_fixes_filter(args: CmdArgs) -> List[str]:
    fixes_arg = args.get_extra_arg(FIXES_ARG)
    if not fixes_arg:
        return [EMPTY_FLAG, FIXES_FLAG]

    filt = [fixes_arg]
    if not set(filt).issubset(set(FIXES_FLAG)):
        raise Exception(f'Not a valid fixes filter: "{filt}".')

    return filt


def get_built_filter(args: CmdArgs) -> List[str]:
    built_arg = args.get_extra_arg(BUILT_ARG)
    if not built_arg:
        return BUILD_STATE_FLAGS

    filt = built_arg.split(",")
    if not set(filt).issubset(set(BUILD_STATE_FLAGS)):
        raise Exception(f'Not a valid built filter: "{filt}".')

    return filt


extra_args: List[ExtraArg] = [
    ExtraArg(FIXES_ARG, action="store", type=str, default=""),
    ExtraArg(BUILT_ARG, action="store", type=str, default=""),
]

cmd_args = CmdArgs("Fantagraphics info", CmdArgNames.VOLUME, extra_args)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

fixes_filter = get_fixes_filter(cmd_args)
built_filter = get_built_filter(cmd_args)

titles_and_info = cmd_args.get_titles_and_info(configured_only=False)
titles = get_titles_sorted_by_submission_date(titles_and_info)
issue_titles_info = get_issue_titles(titles)

title_flags, max_title_len, max_issue_title_len = get_title_flags(
    titles, titles_and_info, issue_titles_info
)

for title, issue_title_info in zip(titles, issue_titles_info):
    if title not in title_flags:
        continue

    issue_title = issue_title_info[0]
    display_title = title_flags[title][0]
    fixes_flag = title_flags[title][1]
    build_state_flag = title_flags[title][2]
    page_list = title_flags[title][3]

    print(
        f'Title: "{display_title:<{max_title_len}}", {issue_title:<{max_issue_title_len}},'
        f" {fixes_flag} {build_state_flag},"
        f" jpgs: {page_list}"
    )
