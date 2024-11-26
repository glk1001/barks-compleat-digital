import os
from dataclasses import dataclass
from typing import List, Tuple, Set

from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_consts import (
    BARKS_ROOT_DIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_YEARS_COMICS_DIR,
    THE_COMICS_DIR,
    IMAGES_SUBDIR,
)
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_info import FAN
from consts import DEST_NON_IMAGE_FILES
from out_of_date_checking import (
    get_dest_file_out_of_date_msg,
    get_file_out_of_date_wrt_max_dest_msg,
)
from pages import (
    get_srce_and_dest_pages_in_order,
    SrceAndDestPages,
    get_timestamp,
    get_timestamp_as_str,
)
from utils import get_shorter_ini_filename


@dataclass
class ZipOutOfDateErrors:
    file: str = ""
    missing: bool = False
    out_of_date_wrt_ini: bool = False
    out_of_date_wrt_srce: bool = False
    out_of_date_wrt_dest: bool = False
    timestamp: float = 0.0


@dataclass
class ZipSymlinkOutOfDateErrors:
    symlink: str = ""
    missing: bool = False
    out_of_date_wrt_ini: bool = False
    out_of_date_wrt_zip: bool = False
    out_of_date_wrt_dest: bool = False
    timestamp: float = 0.0


@dataclass
class OutOfDateErrors:
    ini_file: str
    dest_dir_files_missing: List[str]
    dest_dir_files_out_of_date: List[str]
    srce_and_dest_files_missing: List[Tuple[str, str]]
    srce_and_dest_files_out_of_date: List[Tuple[str, str]]
    unexpected_dest_image_files: List[str]
    zip_errors: ZipOutOfDateErrors
    series_zip_symlink_errors: ZipSymlinkOutOfDateErrors
    year_zip_symlink_errors: ZipSymlinkOutOfDateErrors
    is_error: bool = False
    max_srce_timestamp: float = 0.0
    max_dest_timestamp: float = 0.0
    ini_timestamp: float = 0.0


def make_out_of_date_errors(ini_file: str) -> OutOfDateErrors:
    return OutOfDateErrors(
        ini_file=ini_file,
        dest_dir_files_missing=[],
        dest_dir_files_out_of_date=[],
        srce_and_dest_files_out_of_date=[],
        srce_and_dest_files_missing=[],
        unexpected_dest_image_files=[],
        zip_errors=ZipOutOfDateErrors(),
        series_zip_symlink_errors=ZipSymlinkOutOfDateErrors(),
        year_zip_symlink_errors=ZipSymlinkOutOfDateErrors(),
    )


def check_comics_source_is_readonly() -> int:
    srce_comics_dir = str(os.path.join(BARKS_ROOT_DIR, FAN))

    return check_folder_and_contents_are_readonly(srce_comics_dir)


def check_folder_and_contents_are_readonly(dir_path: str) -> int:
    ret_code = 0

    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)

        if os.path.isdir(file_path):
            if os.access(file_path, os.W_OK):
                print(f'ERROR: Directory "{file_path}" is not readonly.')
                ret_code = 1
            if check_folder_and_contents_are_readonly(file_path) != 0:
                ret_code = 1
                continue

        if os.access(file_path, os.W_OK):
            print(f'ERROR: File "{file_path}" is not readonly.')
            ret_code = 1

    return ret_code


def check_comics_integrity(comics_db: ComicsDatabase) -> int:
    print()

    if check_comics_source_is_readonly() != 0:
        return 1

    dest_dirs = []
    zip_files = []
    zip_series_symlink_dirs = set()
    zip_series_symlinks = []
    zip_year_symlink_dirs = set()
    zip_year_symlinks = []
    ret_code = 0
    for title in comics_db.get_all_story_titles():
        comic = comics_db.get_comic_book(title)

        dest_dirs.append((comics_db.get_ini_file(title), comic.get_dest_dir()))
        zip_files.append(comic.get_dest_comic_zip())
        zip_series_symlink_dirs.add(comic.get_dest_series_zip_symlink_dir())
        zip_series_symlinks.append(comic.get_dest_series_comic_zip_symlink())
        zip_year_symlink_dirs.add(comic.get_dest_year_zip_symlink_dir())
        zip_year_symlinks.append(comic.get_dest_year_comic_zip_symlink())

        if 0 != check_out_of_date_files(comic):
            ret_code = 1

    if 0 != check_unexpected_files(
        dest_dirs,
        zip_files,
        zip_series_symlink_dirs,
        zip_series_symlinks,
        zip_year_symlink_dirs,
        zip_year_symlinks,
    ):
        ret_code = 1

    return ret_code


def check_out_of_date_files(comic: ComicBook) -> int:
    out_of_date_errors = make_out_of_date_errors(comic.ini_file)

    check_srce_and_dest_files(comic, out_of_date_errors)
    check_zip_files(comic, out_of_date_errors)
    check_additional_files(comic, out_of_date_errors)

    out_of_date_errors.is_error = (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        or len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
        or len(out_of_date_errors.unexpected_dest_image_files) > 0
        or out_of_date_errors.zip_errors.missing
        or out_of_date_errors.series_zip_symlink_errors.missing
        or out_of_date_errors.year_zip_symlink_errors.missing
        or out_of_date_errors.zip_errors.out_of_date_wrt_srce
        or out_of_date_errors.zip_errors.out_of_date_wrt_dest
        or out_of_date_errors.series_zip_symlink_errors.out_of_date_wrt_zip
        or out_of_date_errors.year_zip_symlink_errors.out_of_date_wrt_zip
        or out_of_date_errors.series_zip_symlink_errors.out_of_date_wrt_ini
        or out_of_date_errors.year_zip_symlink_errors.out_of_date_wrt_ini
    )

    print_check_errors(out_of_date_errors)

    return 1 if out_of_date_errors.is_error else 0


def check_srce_and_dest_files(comic: ComicBook, errors: OutOfDateErrors) -> None:
    errors.max_srce_timestamp = 0.0
    errors.max_dest_timestamp = 0.0
    errors.num_missing_dest_files = 0
    errors.num_out_of_date_dest_files = 0
    errors.srce_and_dest_files_missing = []
    errors.srce_and_dest_files_out_of_date = []

    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    check_missing_or_out_of_date_dest_files(srce_and_dest_pages, errors)
    check_unexpected_dest_image_files(comic, srce_and_dest_pages, errors)


def check_missing_or_out_of_date_dest_files(
    srce_and_dest_pages: SrceAndDestPages,
    errors: OutOfDateErrors,
) -> None:
    for pages in zip(srce_and_dest_pages.srce_pages, srce_and_dest_pages.dest_pages):
        srce_page = pages[0]
        dest_page = pages[1]
        if not os.path.isfile(dest_page.page_filename):
            errors.srce_and_dest_files_missing.append(
                (srce_page.page_filename, dest_page.page_filename)
            )
        else:
            srce_timestamp = get_timestamp(srce_page.page_filename)
            if errors.max_srce_timestamp < srce_timestamp:
                errors.max_srce_timestamp = srce_timestamp

            dest_timestamp = get_timestamp(dest_page.page_filename)
            if errors.max_dest_timestamp < dest_timestamp:
                errors.max_dest_timestamp = dest_timestamp

            if srce_timestamp > dest_timestamp:
                errors.srce_and_dest_files_out_of_date.append(
                    (srce_page.page_filename, dest_page.page_filename)
                )


def check_unexpected_dest_image_files(
    comic: ComicBook,
    srce_and_dest_pages: SrceAndDestPages,
    errors: OutOfDateErrors,
) -> None:
    allowed_dest_image_files = [f.page_filename for f in srce_and_dest_pages.dest_pages]
    dest_image_dir = comic.get_dest_image_dir()
    if not os.path.isdir(dest_image_dir):
        errors.dest_dir_files_missing.append(dest_image_dir)
        return

    for file in os.listdir(dest_image_dir):
        dest_image_file = os.path.join(dest_image_dir, file)
        if dest_image_file not in allowed_dest_image_files:
            errors.unexpected_dest_image_files.append(dest_image_file)


def check_unexpected_files(
    dest_dirs_info_list: List[Tuple[str, str]],
    allowed_zip_files: List[str],
    allowed_zip_series_symlink_dirs: Set[str],
    allowed_zip_series_symlinks: List[str],
    allowed_zip_year_symlink_dirs: Set[str],
    allowed_zip_year_symlinks: List[str],
) -> int:
    print()

    ret_code = 0

    allowed_main_dir_files = [
        THE_CHRONOLOGICAL_DIRS_DIR,
        THE_CHRONOLOGICAL_DIR,
        THE_YEARS_COMICS_DIR,
    ] + list(allowed_zip_series_symlink_dirs)

    if 0 != check_files_in_dir("main", THE_COMICS_DIR, allowed_main_dir_files):
        ret_code = 1

    for dest_dir_info in dest_dirs_info_list:
        ini_file = os.path.basename(dest_dir_info[0])
        dest_dir = dest_dir_info[1]

        if not os.path.isdir(dest_dir):
            print(f'ERROR: The dest directory "{dest_dir}" is missing.')
            ret_code = 1
            continue

        for file in os.listdir(dest_dir):
            if file in [IMAGES_SUBDIR, ini_file]:
                continue
            if file not in DEST_NON_IMAGE_FILES:
                print(f'ERROR: The info file "{os.path.join(dest_dir, file)}" was unexpected.')
                ret_code = 1

    if dest_dirs_info_list:
        allowed_dest_dirs = [d[1] for d in dest_dirs_info_list]
        dest_dir = os.path.dirname(allowed_dest_dirs[0])
        if 0 != check_files_in_dir("dest", dest_dir, allowed_dest_dirs):
            ret_code = 1

    if allowed_zip_files:
        dest_dir = os.path.dirname(allowed_zip_files[0])
        if 0 != check_files_in_dir("zip", dest_dir, allowed_zip_files):
            ret_code = 1

    if allowed_zip_series_symlinks:
        for dest_dir in allowed_zip_series_symlink_dirs:
            if check_files_in_dir("series", dest_dir, list(allowed_zip_series_symlinks)):
                ret_code = 1

    if allowed_zip_year_symlinks:
        year_symlink_parent_dir = os.path.dirname(list(allowed_zip_year_symlink_dirs)[0])
        if 0 != check_files_in_dir(
            "year dir", year_symlink_parent_dir, list(allowed_zip_year_symlink_dirs)
        ):
            ret_code = 1

        for dest_dir in allowed_zip_year_symlink_dirs:
            if check_files_in_dir("year", dest_dir, list(allowed_zip_year_symlinks)):
                ret_code = 1

    if ret_code != 0:
        print()

    return ret_code


def check_files_in_dir(file_type: str, the_dir: str, allowed_files: List[str]) -> int:
    ret_code = 0

    if not os.path.isdir(the_dir):
        print(f'ERROR: The directory "{the_dir}" is missing.')
        return 1

    for file in os.listdir(the_dir):
        full_file = os.path.join(the_dir, file)
        if full_file not in allowed_files:
            print(f'ERROR: The {file_type} file "{full_file}" was unexpected.')
            ret_code = 1

    return ret_code


def check_zip_files(comic: ComicBook, errors: OutOfDateErrors) -> None:
    if not os.path.exists(comic.get_dest_comic_zip()):
        errors.zip_errors.missing = True
        errors.zip_errors.file = comic.get_dest_comic_zip()
        return

    zip_timestamp = get_timestamp(comic.get_dest_comic_zip())
    if zip_timestamp < errors.max_srce_timestamp:
        errors.zip_errors.out_of_date_wrt_srce = True
        errors.zip_errors.timestamp = zip_timestamp
        errors.zip_errors.file = comic.get_dest_comic_zip()

    if zip_timestamp < errors.max_dest_timestamp:
        errors.zip_errors.out_of_date_wrt_dest = True
        errors.zip_errors.timestamp = zip_timestamp
        errors.zip_errors.file = comic.get_dest_comic_zip()

    ini_timestamp = get_timestamp(errors.ini_file)
    if zip_timestamp < ini_timestamp:
        errors.zip_errors.out_of_date_wrt_ini = True
        errors.zip_errors.timestamp = zip_timestamp
        errors.zip_errors.file = comic.get_dest_comic_zip()
        errors.ini_timestamp = ini_timestamp

    if not os.path.exists(comic.get_dest_series_comic_zip_symlink()):
        errors.series_zip_symlink_errors.missing = True
        errors.series_zip_symlink_errors.symlink = comic.get_dest_series_comic_zip_symlink()
        return

    series_zip_symlink_timestamp = get_timestamp(comic.get_dest_series_comic_zip_symlink())
    if series_zip_symlink_timestamp < zip_timestamp:
        errors.series_zip_symlink_errors.out_of_date_wrt_zip = True
        errors.series_zip_symlink_errors.timestamp = series_zip_symlink_timestamp
        errors.series_zip_symlink_errors.symlink = comic.get_dest_series_comic_zip_symlink()
        errors.zip_errors.timestamp = zip_timestamp
        errors.zip_errors.file = comic.get_dest_comic_zip()

    if series_zip_symlink_timestamp < ini_timestamp:
        errors.series_zip_symlink_errors.out_of_date_wrt_ini = True
        errors.series_zip_symlink_errors.timestamp = series_zip_symlink_timestamp
        errors.series_zip_symlink_errors.symlink = comic.get_dest_series_comic_zip_symlink()
        errors.ini_timestamp = ini_timestamp

    if series_zip_symlink_timestamp < errors.max_dest_timestamp:
        errors.series_zip_symlink_errors.out_of_date_wrt_dest = True
        errors.series_zip_symlink_errors.timestamp = series_zip_symlink_timestamp
        errors.series_zip_symlink_errors.symlink = comic.get_dest_series_comic_zip_symlink()

    if not os.path.exists(comic.get_dest_year_comic_zip_symlink()):
        errors.year_zip_symlink_errors.missing = True
        errors.year_zip_symlink_errors.symlink = comic.get_dest_year_comic_zip_symlink()
        return

    year_zip_symlink_timestamp = get_timestamp(comic.get_dest_year_comic_zip_symlink())
    if year_zip_symlink_timestamp < zip_timestamp:
        errors.year_zip_symlink_errors.out_of_date_wrt_zip = True
        errors.year_zip_symlink_errors.timestamp = year_zip_symlink_timestamp
        errors.year_zip_symlink_errors.symlink = comic.get_dest_year_comic_zip_symlink()
        errors.zip_errors.timestamp = zip_timestamp
        errors.zip_errors.file = comic.get_dest_comic_zip()

    if year_zip_symlink_timestamp < ini_timestamp:
        errors.year_zip_symlink_errors.out_of_date_wrt_ini = True
        errors.year_zip_symlink_errors.timestamp = year_zip_symlink_timestamp
        errors.year_zip_symlink_errors.symlink = comic.get_dest_year_comic_zip_symlink()
        errors.ini_timestamp = ini_timestamp

    if year_zip_symlink_timestamp < errors.max_dest_timestamp:
        errors.year_zip_symlink_errors.out_of_date_wrt_dest = True
        errors.year_zip_symlink_errors.timestamp = year_zip_symlink_timestamp
        errors.year_zip_symlink_errors.symlink = comic.get_dest_year_comic_zip_symlink()


def check_additional_files(comic: ComicBook, errors: OutOfDateErrors) -> None:
    dest_dir = comic.get_dest_dir()
    if not os.path.exists(dest_dir):
        errors.dest_dir_files_missing.append(dest_dir)
        return

    for file in DEST_NON_IMAGE_FILES:
        full_file = os.path.join(dest_dir, file)
        if not os.path.exists(full_file):
            errors.dest_dir_files_missing.append(full_file)
            continue
        file_timestamp = get_timestamp(full_file)
        if file_timestamp < errors.max_srce_timestamp:
            errors.dest_dir_files_out_of_date.append(full_file)


def print_check_errors(errors: OutOfDateErrors) -> None:
    if (
        len(errors.srce_and_dest_files_missing) > 0
        or len(errors.srce_and_dest_files_out_of_date) > 0
        or len(errors.dest_dir_files_missing) > 0
        or len(errors.dest_dir_files_out_of_date) > 0
    ):
        print_out_of_date_or_missing_errors(errors)

    if errors.zip_errors.missing:
        print(
            f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the zip file "{errors.zip_errors.file}" is missing.'
        )

    if errors.series_zip_symlink_errors.missing:
        print(
            f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the series symlink "{errors.series_zip_symlink_errors.symlink}" is missing.'
        )

    if errors.year_zip_symlink_errors.missing:
        print(
            f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the year symlink "{errors.year_zip_symlink_errors.symlink}" is missing.'
        )

    if errors.zip_errors.out_of_date_wrt_srce:
        max_srce_date = get_timestamp_as_str(errors.max_srce_timestamp)
        file_date = get_timestamp_as_str(errors.zip_errors.timestamp)
        print(
            f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the zip file "{errors.zip_errors.file}" timestamp'
            f" '{file_date}', is less than the max srce file timestamp '{max_srce_date}'."
        )

    if errors.zip_errors.out_of_date_wrt_dest:
        max_dest_date = get_timestamp_as_str(errors.max_dest_timestamp)
        file_date = get_timestamp_as_str(errors.zip_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the zip file "{errors.zip_errors.file}" timestamp'
            f" '{file_date}', is less than the max dest file timestamp '{max_dest_date}'."
        )

    if errors.zip_errors.out_of_date_wrt_ini:
        ini_date = get_timestamp_as_str(errors.ini_timestamp)
        file_date = get_timestamp_as_str(errors.zip_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the zip file "{errors.zip_errors.file}" timestamp'
            f" '{file_date}', is less than the ini file timestamp '{ini_date}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_zip:
        symlink_date = get_timestamp_as_str(errors.series_zip_symlink_errors.timestamp)
        zip_date = get_timestamp_as_str(errors.zip_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the series symlink "{errors.series_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the zip file"
            f" \"{errors.zip_errors.file}\" timestamp '{zip_date}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_ini:
        ini_date = get_timestamp_as_str(errors.ini_timestamp)
        symlink_date = get_timestamp_as_str(errors.series_zip_symlink_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the series symlink "{errors.series_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the ini file timestamp '{ini_date}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_dest:
        max_dest_date = get_timestamp_as_str(errors.max_dest_timestamp)
        symlink_date = get_timestamp_as_str(errors.series_zip_symlink_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the series symlink "{errors.series_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the max dest image timestamp '{max_dest_date}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_zip:
        symlink_date = get_timestamp_as_str(errors.year_zip_symlink_errors.timestamp)
        zip_date = get_timestamp_as_str(errors.zip_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the year symlink "{errors.year_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the zip"
            f" file \"{errors.zip_errors.file}\" timestamp '{zip_date}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_ini:
        ini_date = get_timestamp_as_str(errors.ini_timestamp)
        symlink_date = get_timestamp_as_str(errors.year_zip_symlink_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the year symlink "{errors.year_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the ini file timestamp '{ini_date}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_dest:
        max_dest_date = get_timestamp_as_str(errors.max_dest_timestamp)
        symlink_date = get_timestamp_as_str(errors.year_zip_symlink_errors.timestamp)
        print(
            f'\nERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f' the year symlink "{errors.year_zip_symlink_errors.symlink}" timestamp'
            f" '{symlink_date}', is less than the max dest image timestamp '{max_dest_date}'."
        )

    if len(errors.unexpected_dest_image_files) > 0:
        print()
        print_unexpected_dest_image_files_errors(errors)


def print_unexpected_dest_image_files_errors(errors: OutOfDateErrors) -> None:
    for file in errors.unexpected_dest_image_files:
        print(f'ERROR: The dest image file "{file}" was unexpected.')


def print_out_of_date_or_missing_errors(errors: OutOfDateErrors) -> None:
    for srce_dest in errors.srce_and_dest_files_missing:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(f'ERROR: There is no dest file "{dest_file}"' f' matching srce file "{srce_file}".')
    for srce_dest in errors.srce_and_dest_files_out_of_date:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(f"ERROR: {get_dest_file_out_of_date_msg(srce_file, dest_file)}")

    if (
        len(errors.srce_and_dest_files_missing) > 0
        or len(errors.srce_and_dest_files_out_of_date) > 0
        or len(errors.dest_dir_files_missing) > 0
        or len(errors.dest_dir_files_out_of_date) > 0
    ):
        print()

    if len(errors.dest_dir_files_missing) > 0:
        for file in errors.dest_dir_files_missing:
            print(f'ERROR: The dest file "{file}" is missing.')
        print()

    if len(errors.dest_dir_files_out_of_date) > 0:
        for file in errors.dest_dir_files_missing:
            print(
                f"ERROR: {get_file_out_of_date_wrt_max_dest_msg(file, errors.max_dest_timestamp)}"
            )
        print()

    if (
        len(errors.srce_and_dest_files_missing) > 0
        and len(errors.srce_and_dest_files_out_of_date) > 0
    ):
        print(
            f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
            f" there are {len(errors.srce_and_dest_files_missing)} missing dest files"
            f" and {len(errors.srce_and_dest_files_out_of_date)} out of date"
            f" dest files.\n"
        )
    else:
        if len(errors.srce_and_dest_files_missing) > 0:
            print(
                f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
                f" there are {len(errors.srce_and_dest_files_missing)} missing"
                f" dest files.\n"
            )

        if len(errors.srce_and_dest_files_out_of_date) > 0:
            print(
                f'ERROR: For "{get_shorter_ini_filename(errors.ini_file)}",'
                f" there are {len(errors.srce_and_dest_files_out_of_date)} out of"
                f" date dest files.\n"
            )
