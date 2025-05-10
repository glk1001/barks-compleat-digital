import logging
import os
import re
from datetime import datetime, date
from pathlib import Path
from typing import Union, List, Tuple, Dict

from .comic_issues import Issues, ISSUE_NAME
from .comics_consts import BARKS_ROOT_DIR, MONTH_AS_SHORT_STR, MONTH_AS_LONG_STR
from .fanta_comics_info import FantaComicBookInfo


def get_dest_comic_dirname(title: str, chrono_num: int) -> str:
    return f"{chrono_num:03d} {title}"


def get_dest_comic_zip_file_stem(title: str, chrono_num: int, issue_name: str) -> str:
    return f"{get_dest_comic_dirname(title, chrono_num)} [{issue_name}]"


def get_titles_and_info_chronologically_sorted(
    titles_and_info: List[Tuple[str, FantaComicBookInfo]]
) -> List[Tuple[str, FantaComicBookInfo]]:

    return sorted(titles_and_info, key=lambda x: x[1].fanta_chronological_number)


def get_titles_sorted_by_submission_date(
    titles_and_info: List[Tuple[str, FantaComicBookInfo]]
) -> List[str]:

    return [t[0] for t in sorted(titles_and_info, key=get_submitted_date)]


def get_titles_and_info_sorted_by_submission_date(
    titles_and_info: List[Tuple[str, FantaComicBookInfo]]
) -> List[Tuple[str, FantaComicBookInfo]]:

    return sorted(titles_and_info, key=get_submitted_date)


def get_submitted_date(title_and_info: Tuple[str, FantaComicBookInfo]) -> date:
    fanta_info = title_and_info[1]
    submitted_day = (
        1
        if fanta_info.comic_book_info.submitted_day == -1
        else fanta_info.comic_book_info.submitted_day
    )
    return date(
        fanta_info.comic_book_info.submitted_year,
        fanta_info.comic_book_info.submitted_month,
        submitted_day,
    )


def get_work_dir(work_dir_root: str) -> str:
    os.makedirs(work_dir_root, exist_ok=True)
    if not os.path.isdir(work_dir_root):
        raise Exception(f'Could not find work root directory "{work_dir_root}".')

    work_dir = os.path.join(work_dir_root, datetime.now().strftime("%Y_%m_%d-%H_%M_%S.%f"))
    os.makedirs(work_dir)

    return work_dir


def get_abbrev_path(file: Union[str, Path]) -> str:
    abbrev = get_relpath(file)

    abbrev = re.sub(r"Carl Barks ", "**", abbrev)
    abbrev = re.sub(r" -.*- ", " - ", abbrev)
    abbrev = re.sub(r" \(.*\)", "", abbrev)

    return abbrev


def get_relpath(file: Union[str, Path]) -> str:
    if str(file).startswith(BARKS_ROOT_DIR):
        return os.path.relpath(file, BARKS_ROOT_DIR)

    file_parts = Path(file).parts[-2:]
    # noinspection PyArgumentList
    return str(os.path.join(*file_parts))


def get_abspath_from_relpath(relpath: str, root_dir=BARKS_ROOT_DIR) -> str:
    if os.path.isabs(relpath):
        return relpath
    return os.path.join(root_dir, relpath)


def get_clean_path(file: Union[str, Path]) -> str:
    return str(file).replace(str(Path.home()), "$HOME")


def get_timestamp(file: str) -> float:
    if os.path.islink(file):
        return os.lstat(file).st_mtime

    return os.path.getmtime(file)


def get_max_timestamp(files: List[str]) -> float:
    max_timestamp = -1.0
    for file in files:
        timestamp = get_timestamp(file)
        if timestamp > max_timestamp:
            max_timestamp = timestamp

    return max_timestamp


def get_timestamp_str(file: str, date_sep: str = "_", date_time_sep="-", hr_sep="_") -> str:
    return get_timestamp_as_str(get_timestamp(file), date_sep, date_time_sep, hr_sep)


def get_timestamp_as_str(
    timestamp: float, date_sep: str = "_", date_time_sep="-", hr_sep="_"
) -> str:
    timestamp_as_date = datetime.fromtimestamp(timestamp)
    timestamp_as_date_as_str = timestamp_as_date.strftime(
        f"%Y{date_sep}%m{date_sep}%d{date_time_sep}%H{hr_sep}%M{hr_sep}%S.%f"
    )
    return timestamp_as_date_as_str[:-4]  # trim microseconds to two places


def dest_file_is_older_than_srce(srce_file: str, dest_file: str, include_missing_dest=True) -> bool:
    if include_missing_dest and not os.path.exists(dest_file):
        return True

    srce_timestamp = get_timestamp(srce_file)
    dest_timestamp = get_timestamp(dest_file)

    return srce_timestamp > dest_timestamp


def file_is_older_than_timestamp(file: str, timestamp: float) -> bool:
    file_timestamp = get_timestamp(file)

    return file_timestamp < timestamp


def setup_logging(log_level) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=log_level,
    )
    # TODO: Hack to stop third-party modules screwing with our logging.
    # Must be a better way.
    logging.root.setLevel(log_level)


def get_ocr_no_json_suffix(ocr_json_file: str) -> str:
    return Path(Path(ocr_json_file).stem).suffix


def get_ocr_json_suffix(ocr_json_file: str) -> str:
    return get_ocr_no_json_suffix(ocr_json_file) + ".json"


def get_formatted_day(day: int) -> str:
    if day == 1 or day == 31:
        day_str = str(day) + "st"
    elif day == 2 or day == 22:
        day_str = str(day) + "nd"
    elif day == 3 or day == 23:
        day_str = str(day) + "rd"
    else:
        day_str = str(day) + "th"

    return day_str


def get_short_formatted_first_published_str(fanta_info: FantaComicBookInfo) -> str:
    issue = fanta_info.comic_book_info.get_short_issue_title()

    if fanta_info.comic_book_info.issue_month == -1:
        issue_date = fanta_info.comic_book_info.issue_year
    else:
        issue_date = (
            f"{MONTH_AS_SHORT_STR[fanta_info.comic_book_info.issue_month]}"
            f" {fanta_info.comic_book_info.issue_year}"
        )

    return f"{issue}, {issue_date}"


def get_short_formatted_submitted_date(fanta_info: FantaComicBookInfo) -> str:
    if fanta_info.comic_book_info.submitted_day == -1:
        return (
            f"{MONTH_AS_SHORT_STR[fanta_info.comic_book_info.submitted_month]}"
            f" {fanta_info.comic_book_info.submitted_year}"
        )

    return (
        f"{get_formatted_day(fanta_info.comic_book_info.submitted_day)}"
        f" {MONTH_AS_SHORT_STR[fanta_info.comic_book_info.submitted_month]}"
        f" {fanta_info.comic_book_info.submitted_year}"
    )


def get_long_formatted_submitted_date(fanta_info: FantaComicBookInfo) -> str:
    if fanta_info.comic_book_info.submitted_day == -1:
        return (
            f"{MONTH_AS_LONG_STR[fanta_info.comic_book_info.submitted_month]},"
            f" {fanta_info.comic_book_info.submitted_year}"
        )

    return (
        f"{get_formatted_day(fanta_info.comic_book_info.submitted_day)}"
        f" {MONTH_AS_LONG_STR[fanta_info.comic_book_info.submitted_month]},"
        f" {fanta_info.comic_book_info.submitted_year}"
    )


def get_formatted_first_published_str(
    fanta_info: FantaComicBookInfo, issue_name_dict: Dict[Issues, str] = ISSUE_NAME
) -> str:
    issue_name = issue_name_dict[fanta_info.comic_book_info.issue_name]
    issue = f"{issue_name} #{fanta_info.comic_book_info.issue_number}"

    if fanta_info.comic_book_info.issue_month == -1:
        issue_date = fanta_info.comic_book_info.issue_year
    else:
        issue_date = (
            f"{MONTH_AS_LONG_STR[fanta_info.comic_book_info.issue_month]},"
            f" {fanta_info.comic_book_info.issue_year}"
        )

    return f"{issue}, {issue_date}"


def get_formatted_submitted_date(fanta_info: FantaComicBookInfo) -> str:
    if fanta_info.comic_book_info.submitted_day == -1:
        return (
            f", {MONTH_AS_LONG_STR[fanta_info.comic_book_info.submitted_month]}"
            f" {fanta_info.comic_book_info.submitted_year}"
        )

    return (
        f" on {MONTH_AS_LONG_STR[fanta_info.comic_book_info.submitted_month]}"
        f" {get_formatted_day(fanta_info.comic_book_info.submitted_day)},"
        f" {fanta_info.comic_book_info.submitted_year}"
    )
