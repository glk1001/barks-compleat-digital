import logging
import os.path
import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict

from barks_fantagraphics.comic_book import (
    ComicBook,
    get_abbrev_jpg_page_list,
    get_total_num_pages,
    get_num_splashes,
    get_has_front,
)
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames, ExtraArg
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_info import ComicBookInfo
from barks_fantagraphics.comics_utils import (
    dest_file_is_older_than_srce,
    get_timestamp,
    get_max_timestamp,
    get_titles_and_info_sorted_by_submission_date,
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


def get_issue_titles(
    title_info_list: List[Tuple[str, ComicBookInfo]]
) -> List[Tuple[str, str, ComicBookInfo, bool]]:
    comic_issue_title_info_list = []
    for title_info in title_info_list:
        ttl = title_info[0]
        cb_info = title_info[1]
        title_is_configured, _ = comics_database.is_story_title(ttl)
        comic_issue_title = cb_info.get_issue_title()
        comic_issue_title_info_list.append(
            (ttl, comic_issue_title, title_info[1], title_is_configured)
        )

    return comic_issue_title_info_list


def is_upscayled(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES))


def is_restored(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES))


def has_inset_file(comic: ComicBook) -> bool:
    return os.path.isfile(comic.intro_inset_file)


def has_fixes(comic: ComicBook) -> bool:
    mods = [f[1] for f in comic.get_final_srce_original_story_files(RESTORABLE_PAGE_TYPES)]
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
    if not file_list:
        return False

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


@dataclass
class Flags:
    display_title: str
    fixes_flag: str
    build_state_flag: str
    num_pages: int
    page_list: str
    has_front: bool
    num_splashes: int


def get_title_flags(
    issue_titles_info_list: List[Tuple[str, str, ComicBookInfo, bool]]
) -> Tuple[Dict[str, Flags], int, int]:
    max_ttl_len = 0
    max_issue_ttl_len = 0
    ttl_flags = dict()

    for issue_ttl_info in issue_titles_info_list:
        ttl = issue_ttl_info[0]
        issue_ttl = issue_ttl_info[1]
        ttl_info = issue_ttl_info[2]
        is_configured = issue_ttl_info[3]

        if not is_configured:
            display_ttl = ttl if ttl_info.is_barks_title else f"({ttl})"
            fixes_flg = EMPTY_FLAG
            build_state_flg = NOT_CONFIGURED_FLAG
            num_pgs = -1
            page_lst = ""
            has_front = False
            num_splashes = 0
        else:
            comic_book = comics_database.get_comic_book(ttl)

            display_ttl = ttl if comic_book.is_barks_title() else f"({ttl})"
            fixes_flg = FIXES_FLAG if has_fixes(comic_book) else EMPTY_FLAG
            build_state_flg = get_build_state_flag(comic_book)
            page_lst = ", ".join(get_abbrev_jpg_page_list(comic_book))
            num_pgs = get_total_num_pages(comic_book)
            if num_pgs <= 1:
                raise Exception(f'For title "{ttl}", the page count is to small.')
            has_front = get_has_front(comic_book)
            num_splashes = get_num_splashes(comic_book)

        if fixes_flg not in fixes_filter:
            continue
        if build_state_flg not in built_filter:
            continue

        max_ttl_len = max(max_ttl_len, len(display_ttl))
        max_issue_ttl_len = max(max_issue_ttl_len, len(issue_ttl))

        ttl_flags[ttl] = Flags(
            display_ttl,
            fixes_flg,
            build_state_flg,
            num_pgs,
            page_lst,
            has_front,
            num_splashes,
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

cmd_args = CmdArgs("Fantagraphics info", CmdArgNames.TITLE | CmdArgNames.VOLUME, extra_args)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

fixes_filter = get_fixes_filter(cmd_args)
built_filter = get_built_filter(cmd_args)
display_volumes = not cmd_args.one_or_more_volumes() or len(cmd_args.get_volumes()) > 1

titles_and_info = cmd_args.get_titles_and_info(configured_only=False)
titles_and_info = get_titles_and_info_sorted_by_submission_date(titles_and_info)
issue_titles_info = get_issue_titles(titles_and_info)

title_flags, max_title_len, max_issue_title_len = get_title_flags(issue_titles_info)

for issue_title_info in issue_titles_info:
    title = issue_title_info[0]
    comic_book_info = issue_title_info[2]

    if title not in title_flags:
        continue

    issue_title = issue_title_info[1]
    flags = title_flags[title]
    volume_str = "" if not display_volumes else f" {comic_book_info.fantagraphics_volume}, "
    num_front = 1 if flags.has_front else 0
    front_str = f"f:{num_front}"
    splash_str = f"s:{flags.num_splashes}"

    print(
        f'"{flags.display_title:<{max_title_len}}", {issue_title:<{max_issue_title_len}},'
        f"{volume_str}"
        f" {flags.fixes_flag} {flags.build_state_flag}, "
        f" {flags.num_pages:2d} pp,"
        f" {front_str},{splash_str},"
        f" jpgs: {flags.page_list}"
    )
