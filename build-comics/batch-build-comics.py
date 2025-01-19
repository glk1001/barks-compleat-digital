import argparse
import datetime
import logging
import os.path
import shlex
import sys
from datetime import datetime
from typing import Tuple, Union, List

from intspan import intspan

from additional_file_writing import write_summary_file
from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_consts import PageType
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from barks_fantagraphics.comics_utils import (
    get_titles_sorted_by_submission_date,
    get_relpath,
    get_timestamp,
    get_timestamp_as_str,
    setup_logging,
)
from build_comics import build_comic_book
from comics_integrity import check_comics_integrity, get_restored_srce_dependencies
from pages import get_srce_and_dest_pages_in_order, get_page_num_str
from timing import Timing


def print_all_cmds(comics_db: ComicsDatabase) -> int:
    for title in comics_db.get_all_story_titles():
        if 0 != print_cmd(comics_db, title):
            return 1

    return 0


def print_cmd(comics_db: ComicsDatabase, story_title: str) -> int:
    print(
        f"python3 {__file__} {BUILD_ARG}"
        f' {COMICS_DATABASE_DIR_ARG} "{comics_db.get_comics_database_dir()}"'
        f" {TITLE_ARG} {shlex.quote(story_title)}"
    )

    return 0


def show_all_mods(comics_db: ComicsDatabase) -> int:
    mod_dict = dict()
    max_title_len = 0
    for title in comics_db.get_all_story_titles():
        comic = comics_db.get_comic_book(title)

        mods = get_mods(comic)
        if not mods:
            continue

        if max_title_len < len(mods[0]):
            max_title_len = len(mods[0])

        mod_dict.update({get_mods(comic)})

    for title in sorted(mod_dict.keys()):
        mods = mod_dict[title]
        title_str = title + ":"
        dest_mods = f"{'Dest':<6} - {mods[0]}"
        srce_mods = mods[1]
        print(f"{title_str:<{max_title_len + 1}} {dest_mods}")
        print(f'{" ":<{max_title_len + 1}} {srce_mods}')

    return 0


def get_mods(comic: ComicBook) -> Union[None, Tuple[str, Tuple[str, str]]]:
    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    modified_dest_pages = [
        get_page_num_str(dest)
        for dest in srce_and_dest_pages.dest_pages
        if dest.page_is_modified and dest.page_type in [PageType.COVER, PageType.BODY]
    ]
    if not modified_dest_pages:
        return None

    mod_dest_pages_str = ",".join(modified_dest_pages)

    modified_srce_pages = [
        str(srce.page_num)
        for srce in srce_and_dest_pages.srce_pages
        if srce.page_is_modified and srce.page_type in [PageType.COVER, PageType.BODY]
    ]
    fanta_vol = f"FAN {comic.fanta_info.volume:>2}"
    mod_srce_pages_str = f"{fanta_vol} - {','.join(modified_srce_pages)}"

    title = comic.get_title_with_issue_num()

    return title, (mod_dest_pages_str, mod_srce_pages_str)


def show_source_files(comics_db: ComicsDatabase, title: str) -> int:
    comic = comics_db.get_comic_book(title)

    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)
    for srce_page, dest_page in zip(srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages):
        print()
        prev_timestamp = get_timestamp(dest_page.page_filename)
        print(get_filepath_with_date(dest_page.page_filename, prev_timestamp, " "))
        for file, timestamp in get_restored_srce_dependencies(comic, srce_page):
            out_of_date_marker = "*" if (timestamp < 0) or (timestamp > prev_timestamp) else " "
            print(f"{get_filepath_with_date(file, timestamp, out_of_date_marker)}")
            prev_timestamp = timestamp
    #   max_dest_timestamp = get_max_timestamp(srce_and_dest_pages.dest_pages)

    return 0


def get_filepath_with_date(file: str, timestamp: float, out_of_date_marker: str) -> str:
    missing_timestamp = "FILE MISSING          "  # same length as timestamp str

    if os.path.isfile(file):
        file_str = get_relpath(file)
        file_timestamp = get_timestamp_as_str(timestamp, "-", date_time_sep=" ", hr_sep=":")
    else:
        file_str = file
        file_timestamp = missing_timestamp

    return f'{file_timestamp}:{out_of_date_marker}"{file_str}"'


def process_comic_book_titles(
    comics_db: ComicsDatabase,
    titles: List[str],
) -> int:
    assert len(titles) > 0

    ret_code = 0

    for title in titles:
        comic = comics_db.get_comic_book(title)
        ret = process_comic_book(comic)
        if ret != 0:
            ret_code = ret

    return ret_code


def process_comic_book(comic: ComicBook) -> int:
    process_timing = Timing(datetime.now())

    try:
        srce_and_dest_pages, max_dest_timestamp = build_comic_book(comic)

        process_timing.end_time = datetime.now()
        logging.info(
            f"Time taken to complete comic: {process_timing.get_elapsed_time_in_seconds()} seconds"
        )

        write_summary_file(comic, srce_and_dest_pages, max_dest_timestamp, process_timing)
    except Exception as e:
        logging.error(e)
        return 1

    return 0


LOG_LEVEL_ARG = "--log-level"
COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"
TITLE_ARG = "--title"
JUST_ZIP_ARG = "--just-zip"
JUST_SYMLINKS_ARG = "--just-symlinks"

BUILD_ARG = "build"
LIST_CMDS_ARG = "list-cmds"
CHECK_INTEGRITY_ARG = "check-integrity"
SHOW_MODS_ARG = "show-mods"
SHOW_SOURCE_ARG = "show-source"


def get_args():
    global_parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Create a clean Barks comic from Fantagraphics source."
    )

    subparsers = global_parser.add_subparsers(
        dest="cmd_name",
        title="subcommands",
        help="comic building commands",
        required=True,
    )

    build_comics_parser = subparsers.add_parser(BUILD_ARG, help="build comics")
    build_comics_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    build_comics_parser.add_argument(VOLUME_ARG, action="store", type=str, required=False)
    build_comics_parser.add_argument(TITLE_ARG, action="store", type=str, required=False)
    build_comics_parser.add_argument(
        JUST_ZIP_ARG, action="store_true", required=False, default=False
    )
    build_comics_parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    build_comics_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    list_cmds_parser = subparsers.add_parser(
        LIST_CMDS_ARG, help="list the python commands to build all comics"
    )
    list_cmds_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    list_cmds_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    check_integrity_parser = subparsers.add_parser(
        CHECK_INTEGRITY_ARG, help="check the integrity of all previously built comics"
    )
    check_integrity_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    check_integrity_parser.add_argument(VOLUME_ARG, action="store", type=str, required=False)
    check_integrity_parser.add_argument(TITLE_ARG, action="store", type=str, required=False)
    check_integrity_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    show_mods_parser = subparsers.add_parser(SHOW_MODS_ARG, help="list all modified pages")
    show_mods_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    show_mods_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    show_source_parser = subparsers.add_parser(
        SHOW_SOURCE_ARG, help="list all source files used in title"
    )
    show_source_parser.add_argument(TITLE_ARG, action="store", type=str, required=True)
    show_source_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    show_source_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    args = global_parser.parse_args()

    if args.cmd_name == CHECK_INTEGRITY_ARG:
        if args.title and args.volume:
            raise Exception(f"Cannot have both '{TITLE_ARG} and '{VOLUME_ARG}'.")
    if args.cmd_name == BUILD_ARG:
        if args.title and args.volume:
            raise Exception(f"Cannot have both '{TITLE_ARG} and '{VOLUME_ARG}'.")

    return args


def get_titles(args) -> List[str]:
    assert args.cmd_name == CHECK_INTEGRITY_ARG or args.cmd_name == BUILD_ARG

    if args.title:
        return [args.title]

    if args.volume is not None:
        vol_list = list(intspan(args.volume))
        titles_and_info = comics_database.get_configured_titles_in_fantagraphics_volumes(vol_list)
        titles = get_titles_sorted_by_submission_date(titles_and_info)
        return titles

    return []


if __name__ == "__main__":
    cmd_args = get_args()

    setup_logging(cmd_args.log_level)

    comics_database = ComicsDatabase(cmd_args.comics_database_dir)

    if cmd_args.cmd_name == CHECK_INTEGRITY_ARG:
        exit_code = check_comics_integrity(comics_database, get_titles(cmd_args))
    elif cmd_args.cmd_name == LIST_CMDS_ARG:
        exit_code = print_all_cmds(comics_database)
    elif cmd_args.cmd_name == SHOW_MODS_ARG:
        exit_code = show_all_mods(comics_database)
    elif cmd_args.cmd_name == SHOW_SOURCE_ARG:
        exit_code = show_source_files(comics_database, cmd_args.title)
    elif cmd_args.cmd_name == BUILD_ARG:
        exit_code = process_comic_book_titles(comics_database, get_titles(cmd_args))
    else:
        raise Exception(f'ERROR: Unknown cmd_arg "{cmd_args.cmd_name}".')

    if exit_code != 0:
        print(f"\nThere were errors: exit code = {exit_code}.")
        sys.exit(exit_code)
