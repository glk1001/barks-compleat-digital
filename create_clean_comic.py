import argparse
import datetime
import logging
import os
import shlex
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Union

from additional_file_writing import write_summary_file
from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_consts import PageType
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from building_comics import build_comic_book
from comics_integrity import check_comics_integrity
from pages import get_max_timestamp, get_srce_and_dest_pages_in_order, get_page_num_str
from panel_bounding import init_bounding_box_processor
from timing import Timing
from zipping import zip_comic_book, create_symlinks_to_comic_zip


@dataclass
class CmdOptions:
    dry_run: bool = False
    no_cache: bool = False
    just_zip: bool = False
    just_symlinks: bool = False
    work_dir_root: str = ""


def process_all_comic_books(options: CmdOptions, comics_db: ComicsDatabase) -> int:
    all_story_titles = comics_db.get_all_story_titles()

    logging.info(
        f'Processing all {len(all_story_titles)} titles in "{comics_db.get_story_titles_dir()}".'
    )

    ret_code = 0
    for title in all_story_titles:
        comic = comics_db.get_comic_book(title)
        if 0 != process_comic_book(options, comic):
            ret_code = 1

    return ret_code


def print_all_cmds(options: CmdOptions, comics_db: ComicsDatabase) -> int:
    for title in comics_db.get_all_story_titles():
        if 0 != print_cmd(options, comics_db, title):
            return 1

    return 0


def print_cmd(options: CmdOptions, comics_db: ComicsDatabase, story_title: str) -> int:
    dry_run_arg = "" if not options.dry_run else f" {DRY_RUN_ARG}"
    just_symlinks_arg = "" if not options.just_symlinks else f" {JUST_SYMLINKS_ARG}"
    no_cache_arg = "" if not options.no_cache else f" {NO_CACHE_ARG}"
    print(
        f"python3 {__file__} {BUILD_SINGLE_ARG}"
        f"{dry_run_arg}{just_symlinks_arg}{no_cache_arg}"
        f' {WORK_DIR_ARG} "{options.work_dir_root}"'
        f' {COMICS_DATABASE_DIR_ARG} "{comics_db.get_comics_database_dir()}"'
        f" {STORY_TITLE_ARG} {shlex.quote(story_title)}"
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


def process_single_comic_book(
    options: CmdOptions,
    comics_db: ComicsDatabase,
    story_title: str,
) -> int:
    comic = comics_db.get_comic_book(story_title)
    return process_comic_book(options, comic)


def process_comic_book(options: CmdOptions, comic: ComicBook) -> int:
    process_timing = Timing(datetime.now())

    if options.just_symlinks:
        create_symlinks_to_comic_zip(options.dry_run, options.no_cache, comic)
        return 0

    if options.just_zip:
        srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)
        max_dest_timestamp = get_max_timestamp(srce_and_dest_pages.dest_pages)
        zip_comic_book(options.dry_run, options.no_cache, comic, max_dest_timestamp)
        create_symlinks_to_comic_zip(options.dry_run, options.no_cache, comic)
        return 0

    srce_and_dest_pages, max_dest_timestamp = build_comic_book(
        options.dry_run, options.no_cache, comic
    )

    process_timing.end_time = datetime.now()
    logging.info(
        f"Time taken to complete comic: {process_timing.get_elapsed_time_in_seconds()} seconds"
    )

    write_summary_file(
        options.dry_run,
        comic,
        srce_and_dest_pages,
        max_dest_timestamp,
        process_timing,
        not options.no_cache,
    )

    return 0


LOG_LEVEL_ARG = "--log-level"
WORK_DIR_ARG = "--work-dir"
DRY_RUN_ARG = "--dry-run"
NO_CACHE_ARG = "--no-cache"
JUST_ZIP_ARG = "--just-zip"
JUST_SYMLINKS_ARG = "--just-symlinks"
COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
STORY_TITLE_ARG = "--story-title"

BUILD_ALL_ARG = "build-all"
BUILD_SINGLE_ARG = "build-single"
LIST_CMDS_ARG = "list-cmds"
CHECK_INTEGRITY_ARG = "check-integrity"
SHOW_MODS_ARG = "show-mods"


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

    build_all_parser = subparsers.add_parser(BUILD_ALL_ARG, help="build all available comics")
    build_all_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    build_all_parser.add_argument(JUST_ZIP_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    build_all_parser.add_argument(DRY_RUN_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(NO_CACHE_ARG, action="store_true", required=False, default=False)
    build_all_parser.add_argument(WORK_DIR_ARG, type=str, required=True)
    build_all_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )

    build_single_parser = subparsers.add_parser(BUILD_SINGLE_ARG, help="build a single comic")
    build_single_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    build_single_parser.add_argument(STORY_TITLE_ARG, action="store", type=str, required=True)
    build_single_parser.add_argument(
        JUST_ZIP_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        JUST_SYMLINKS_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        DRY_RUN_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        NO_CACHE_ARG, action="store_true", required=False, default=False
    )
    build_single_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    build_single_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    list_cmds_parser = subparsers.add_parser(
        LIST_CMDS_ARG, help="list the python commands to build all comics"
    )
    list_cmds_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    list_cmds_parser.add_argument(DRY_RUN_ARG, action="store_true", required=False, default=False)
    list_cmds_parser.add_argument(NO_CACHE_ARG, action="store_true", required=False, default=False)
    list_cmds_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    list_cmds_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    check_integrity_parser = subparsers.add_parser(
        CHECK_INTEGRITY_ARG, help="check the integrity of all previously built comics"
    )
    check_integrity_parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    check_integrity_parser.add_argument(
        LOG_LEVEL_ARG, action="store", type=str, required=False, default="INFO"
    )
    check_integrity_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

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
    show_mods_parser.add_argument(WORK_DIR_ARG, type=str, required=True)

    args = global_parser.parse_args()

    return args


def get_cmd_options(args) -> CmdOptions:
    return CmdOptions(
        dry_run=hasattr(args, "dry_run") and args.dry_run,
        no_cache=hasattr(args, "no_cache") and args.no_cache,
        just_zip=hasattr(args, "just_zip") and args.just_zip,
        just_symlinks=hasattr(args, "just_symlinks") and args.just_symlinks,
        work_dir_root=hasattr(args, "work_dir") and args.work_dir,
    )


def setup_logging(log_level) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=log_level,
    )


def get_work_dir(work_dir_root: str) -> str:
    os.makedirs(work_dir_root, exist_ok=True)
    if not os.path.isdir(work_dir_root):
        raise Exception(f'Could not find work root directory "{work_dir_root}".')

    wrk_dir = os.path.join(work_dir_root, datetime.now().strftime("%Y_%m_%d-%H_%M_%S.%f"))
    os.makedirs(wrk_dir)

    logging.debug(f'Work directory: "{wrk_dir}".')

    return wrk_dir


if __name__ == "__main__":
    cmd_args = get_args()

    setup_logging(cmd_args.log_level)

    work_dir = get_work_dir(cmd_args.work_dir)

    cmd_options = get_cmd_options(cmd_args)
    comics_database = ComicsDatabase(cmd_args.comics_database_dir)

    init_bounding_box_processor(work_dir)

    if cmd_args.cmd_name == CHECK_INTEGRITY_ARG:
        exit_code = check_comics_integrity(comics_database)
    elif cmd_args.cmd_name == LIST_CMDS_ARG:
        exit_code = print_all_cmds(cmd_options, comics_database)
    elif cmd_args.cmd_name == SHOW_MODS_ARG:
        exit_code = show_all_mods(comics_database)
    elif cmd_args.cmd_name == BUILD_ALL_ARG:
        exit_code = process_all_comic_books(cmd_options, comics_database)
    elif cmd_args.cmd_name == BUILD_SINGLE_ARG:
        exit_code = process_single_comic_book(cmd_options, comics_database, cmd_args.story_title)
    else:
        raise Exception(f'ERROR: Unknown cmd_arg "{cmd_args.cmd_name}".')

    if exit_code != 0:
        print(f"\nThere were errors: exit code = {exit_code}.")
        sys.exit(exit_code)
