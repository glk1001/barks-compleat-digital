import argparse
import datetime
import logging
import sys
import traceback
from datetime import datetime
from typing import List

from intspan import intspan

from additional_file_writing import write_summary_file
from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from barks_fantagraphics.comics_utils import (
    get_titles_sorted_by_submission_date,
    setup_logging,
)
from build_comics import ComicBookBuilder
from comics_integrity import check_comics_integrity
from timing import Timing


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
        comic_book_builder = ComicBookBuilder(comic)
        srce_and_dest_pages, max_dest_timestamp = comic_book_builder.build()

        process_timing.end_time = datetime.now()
        logging.info(
            f"Time taken to complete comic: {process_timing.get_elapsed_time_in_seconds()} seconds"
        )

        write_summary_file(
            comic,
            comic_book_builder.get_srce_dim(),
            comic_book_builder.get_required_dim(),
            srce_and_dest_pages,
            max_dest_timestamp,
            process_timing,
        )
    except AssertionError:
        _, _, tb = sys.exc_info()
        tb_info = traceback.extract_tb(tb)
        filename, line, func, text = tb_info[-1]
        err_msg = f'Assert failed at "{filename}:{line}" for statement "{text}".'
        logging.error(err_msg)
        return 1
    except Exception as e:
        # raise Exception
        logging.error(e)
        return 1

    return 0


LOG_LEVEL_ARG = "--log-level"
COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"
TITLE_ARG = "--title"

BUILD_ARG = "build"
CHECK_INTEGRITY_ARG = "check-integrity"


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
    elif cmd_args.cmd_name == BUILD_ARG:
        exit_code = process_comic_book_titles(comics_database, get_titles(cmd_args))
    else:
        raise Exception(f'ERROR: Unknown cmd_arg "{cmd_args.cmd_name}".')

    if exit_code != 0:
        print(f"\nThere were errors: exit code = {exit_code}.")
        sys.exit(exit_code)
