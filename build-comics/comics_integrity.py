import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Set

from barks_fantagraphics.comic_book import ComicBook, get_page_str, get_safe_title
from barks_fantagraphics.comics_consts import (
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_YEARS_COMICS_DIR,
    THE_COMICS_DIR,
    IMAGES_SUBDIR,
    PageType,
)
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_info import (
    FIRST_VOLUME_NUMBER,
    LAST_VOLUME_NUMBER,
    JPG_FILE_EXT,
    PNG_FILE_EXT,
)
from barks_fantagraphics.comics_utils import get_relpath, get_timestamp, get_timestamp_as_str
from consts import DEST_NON_IMAGE_FILES
from pages import (
    CleanPage,
    SrceAndDestPages,
    get_srce_and_dest_pages_in_order,
)
from utils import (
    DATE_SEP,
    DATE_TIME_SEP,
    HOUR_SEP,
    get_file_out_of_date_with_other_file_msg,
    get_file_out_of_date_wrt_max_timestamp_msg,
)

ERROR_MSG_PREFIX = "ERROR: "
BLANK_ERR_MSG_PREFIX = f'{" ":<{len(ERROR_MSG_PREFIX)}}'


def check_comics_integrity(comics_db: ComicsDatabase, titles: List[str]) -> int:
    print()

    if check_comics_source_is_readonly(comics_db) != 0:
        return 1

    if check_directory_structure(comics_db) != 0:
        return 1

    if check_fantagraphics_files(comics_db) != 0:
        return 1

    if check_no_unexpected_files(comics_db) != 0:
        return 1

    if not titles:
        ret_code = check_all_titles(comics_db)
    else:
        ret_code = 0
        for title in titles:
            ret = check_single_title(comics_db, title)
            if ret != 0:
                ret_code = ret

    return ret_code


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
    title: str
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


def make_out_of_date_errors(title: str, ini_file: str) -> OutOfDateErrors:
    return OutOfDateErrors(
        title=title,
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


def check_comics_source_is_readonly(comics_db: ComicsDatabase) -> int:
    logging.info("Checking Fantagraphics original directories are readonly.")

    ret_code = check_folder_and_contents_are_readonly(comics_db.get_fantagraphics_original_dir())

    if ret_code == 0:
        logging.info("All Fantagraphics original directories are readonly.")
    else:
        logging.error("There are Fantagraphics original directories that are not readonly.")

    return ret_code


def check_fantagraphics_files(comics_db: ComicsDatabase) -> int:
    logging.info("Checking Fantagraphics files.")

    # ret_code = check_fantagraphics_original_dirs(comics_db)
    ret_code = check_all_fixes_and_additions_files(comics_db)

    if ret_code == 0:
        logging.info("All Fantagraphics files are OK.")
    else:
        logging.error("There are issues with some Fantagraphics files.")

    return ret_code


MAX_FIXES_PAGE_NUM = 300


def check_all_fixes_and_additions_files(comics_db: ComicsDatabase) -> int:
    ret_code = 0

    for volume in range(FIRST_VOLUME_NUMBER, LAST_VOLUME_NUMBER + 1):
        if check_standard_fixes_and_additions_files(comics_db, volume) != 0:
            ret_code = 1
        if check_restored_fixes_and_additions_files(comics_db, volume) != 0:
            ret_code = 1
        if check_upscayled_fixes_and_additions_files(comics_db, volume) != 0:
            ret_code = 1

    return ret_code


def check_standard_fixes_and_additions_files(comics_db: ComicsDatabase, volume: int) -> int:
    fanta_original_image_dir = comics_db.get_fantagraphics_volume_image_dir(volume)
    num_fanta_pages = comics_db.get_num_pages_in_fantagraphics_volume(volume)

    ret_code = 0

    # Basic 'fixes' check.
    fixes_root_dir = comics_db.get_fantagraphics_fixes_volume_dir(volume)
    if _get_num_files_in_dir(fixes_root_dir) != 1:
        print(f'{ERROR_MSG_PREFIX}Directory "{fixes_root_dir}" has too many files.')
        ret_code = 1
        return ret_code

    fixes_dir = comics_db.get_fantagraphics_fixes_volume_image_dir(volume)
    if not os.path.isdir(fixes_dir):
        print(f'{ERROR_MSG_PREFIX}Could not find fixes directory "{fixes_dir}".')
        ret_code = 1
        return ret_code

    # Standard fixes files.
    for file in os.listdir(fixes_dir):
        file_stem = Path(file).stem
        original_file = os.path.join(fanta_original_image_dir, file_stem + JPG_FILE_EXT)
        fixes_file = os.path.join(fixes_dir, file)

        # TODO: Should 'bounded' be here?
        if file == "bounded":
            continue

        # TODO: Another special case. Needed?
        if file.endswith("-fix.txt"):
            matching_fixes_file = os.path.join(fixes_dir, file[: -len("-fix.txt")] + JPG_FILE_EXT)
            if not os.path.isfile(matching_fixes_file):
                print(f'{ERROR_MSG_PREFIX}Fixes text file has no match: "{fixes_file}".')
                ret_code = 1
            continue

        # Must be a jpeg file.
        file_ext = Path(file).suffix
        if file_ext != JPG_FILE_EXT:
            print(f'{ERROR_MSG_PREFIX}Fixes file must be a jpeg: "{fixes_file}".')
            ret_code = 1
            continue

        if not os.path.isfile(original_file):
            # If it's an added file it must have a valid page number.
            page_num = Path(file).stem
            if not page_num.isnumeric():
                print(f"{ERROR_MSG_PREFIX}Invalid fixes file:" f' "{fixes_file}".')
                ret_code = 1
                continue
            page_num = int(page_num)
            if page_num <= num_fanta_pages or page_num > MAX_FIXES_PAGE_NUM:
                print(
                    f"{ERROR_MSG_PREFIX}Fixes file is outside page num range"
                    f' [{num_fanta_pages}..{MAX_FIXES_PAGE_NUM}]: "{fixes_file}".'
                )
                ret_code = 1
                continue

    return ret_code


def check_upscayled_fixes_and_additions_files(comics_db: ComicsDatabase, volume: int) -> int:
    fanta_original_image_dir = comics_db.get_fantagraphics_volume_image_dir(volume)
    fixes_dir = comics_db.get_fantagraphics_fixes_volume_image_dir(volume)
    restored_fixes_dir = comics_db.get_fantagraphics_restored_fixes_volume_image_dir(volume)

    ret_code = 0

    # Basic 'upscayled fixes' check.
    upscayled_fixes_root_dir = comics_db.get_fantagraphics_upscayled_fixes_volume_dir(volume)
    if _get_num_files_in_dir(upscayled_fixes_root_dir) != 1:
        print(f'{ERROR_MSG_PREFIX}Directory "{upscayled_fixes_root_dir}" has too many files.')
        ret_code = 1
        return ret_code

    upscayled_fixes_dir = comics_db.get_fantagraphics_upscayled_fixes_volume_image_dir(volume)
    if not os.path.isdir(fixes_dir):
        print(
            f"{ERROR_MSG_PREFIX}Could not find upscayled fixes directory"
            f' "{upscayled_fixes_dir}".'
        )
        ret_code = 1
        return ret_code

    # Upscayled fixes files.
    for file in os.listdir(upscayled_fixes_dir):
        file_stem = Path(file).stem
        original_file = os.path.join(fanta_original_image_dir, file_stem + JPG_FILE_EXT)
        fixes_file = os.path.join(fixes_dir, file)
        upscayled_fixes_file = os.path.join(upscayled_fixes_dir, file)
        restored_fixes_file = os.path.join(restored_fixes_dir, file)

        # TODO: Another special case. Needed?
        if file.endswith("-fix.txt"):
            matching_fixes_file = os.path.join(
                upscayled_fixes_dir, file[: -len("-fix.txt")] + PNG_FILE_EXT
            )
            if not os.path.isfile(matching_fixes_file):
                print(
                    f"{ERROR_MSG_PREFIX}Upscayled fixes text file has no match:"
                    f' "{upscayled_fixes_file}".'
                )
                ret_code = 1
            continue

        # Must be a png file.
        file_ext = Path(file).suffix
        if file_ext != PNG_FILE_EXT:
            print(
                f"{ERROR_MSG_PREFIX}Upscayled fixes file must be a png: "
                f'"{upscayled_fixes_file}".'
            )
            ret_code = 1
            continue

        # Upscayled fixes cannot be additions?
        if not os.path.isfile(original_file):
            print(
                f"{ERROR_MSG_PREFIX}Upscayled fixes file does not have matching original file:"
                f' "{upscayled_fixes_file}".'
            )
            ret_code = 1
            continue

        if os.path.isfile(fixes_file):
            print(
                f"{ERROR_MSG_PREFIX}Upscayled fixes file cannot have a matching fixes"
                f' file: "{upscayled_fixes_file}".'
            )
            ret_code = 1
            continue

        if os.path.isfile(restored_fixes_file):
            print(
                f"{ERROR_MSG_PREFIX}Upscayled fixes file cannot have a matching restored fixes"
                f' file: "{upscayled_fixes_file}".'
            )
            ret_code = 1
            continue

    return ret_code


def check_restored_fixes_and_additions_files(comics_db: ComicsDatabase, volume: int) -> int:
    fanta_original_image_dir = comics_db.get_fantagraphics_volume_image_dir(volume)
    num_fanta_pages = comics_db.get_num_pages_in_fantagraphics_volume(volume)
    fixes_dir = comics_db.get_fantagraphics_fixes_volume_image_dir(volume)
    upscayled_fixes_dir = comics_db.get_fantagraphics_upscayled_fixes_volume_image_dir(volume)

    ret_code = 0

    # Basic 'restored fixes' check.
    restored_fixes_root_dir = comics_db.get_fantagraphics_restored_fixes_volume_dir(volume)
    if _get_num_files_in_dir(restored_fixes_root_dir) != 1:
        print(f'{ERROR_MSG_PREFIX}Directory "{restored_fixes_root_dir}" has too many files.')
        ret_code = 1
        return ret_code

    restored_fixes_dir = comics_db.get_fantagraphics_restored_fixes_volume_image_dir(volume)
    if not os.path.isdir(fixes_dir):
        print(f'{ERROR_MSG_PREFIX}Could not find restored fixes directory "{restored_fixes_dir}".')
        ret_code = 1
        return ret_code

    # Restored fixes files.
    for file in os.listdir(restored_fixes_dir):
        file_stem = Path(file).stem
        original_file = os.path.join(fanta_original_image_dir, file_stem + JPG_FILE_EXT)
        fixes_file = os.path.join(fixes_dir, file)
        upscayled_fixes_file = os.path.join(upscayled_fixes_dir, file)
        restored_fixes_file = os.path.join(restored_fixes_dir, file)

        # TODO: Another special case. Needed?
        if file.endswith("-fix.txt"):
            matching_fixes_file = os.path.join(
                restored_fixes_dir, file[: -len("-fix.txt")] + PNG_FILE_EXT
            )
            if not os.path.isfile(matching_fixes_file):
                print(
                    f"{ERROR_MSG_PREFIX}Restored fixes text file has no match:"
                    f' "{restored_fixes_file}".'
                )
                ret_code = 1
            continue

        # Must be a png file.
        file_ext = Path(file).suffix
        if file_ext != PNG_FILE_EXT:
            print(
                f"{ERROR_MSG_PREFIX}Restored fixes file must be a png:" f' "{restored_fixes_file}".'
            )
            ret_code = 1
            continue

        if os.path.isfile(fixes_file):
            print(
                f"{ERROR_MSG_PREFIX}Restored fixes file cannot have a matching fixes"
                f' file: "{restored_fixes_file}".'
            )
            ret_code = 1
            continue

        if os.path.isfile(upscayled_fixes_file):
            print(
                f"{ERROR_MSG_PREFIX}Restored fixes file cannot have a matching upscayled"
                f' fixes file: "{restored_fixes_file}".'
            )
            ret_code = 1
            continue

        if not os.path.isfile(original_file):
            # If it's an added file it must have a valid page number.
            page_num = Path(file).stem
            if not page_num.isnumeric():
                print(
                    f"{ERROR_MSG_PREFIX}Invalid restored fixes file:" f' "{restored_fixes_file}".'
                )
                ret_code = 1
                continue
            page_num = int(page_num)
            if page_num <= num_fanta_pages or page_num > MAX_FIXES_PAGE_NUM:
                print(
                    f"{ERROR_MSG_PREFIX}Restored fixes file is outside page num range"
                    f' [{num_fanta_pages}..{MAX_FIXES_PAGE_NUM}]: "{restored_fixes_file}".'
                )
                ret_code = 1
                continue

    return ret_code


def _get_num_files_in_dir(dirname: str) -> int:
    return len([file for file in os.listdir(dirname)])


def check_folder_and_contents_are_readonly(dir_path: str) -> int:
    ret_code = 0

    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)

        if os.path.isdir(file_path):
            if os.access(file_path, os.W_OK):
                print(f'{ERROR_MSG_PREFIX}Directory "{file_path}" is not readonly.')
                ret_code = 1
            if check_folder_and_contents_are_readonly(file_path) != 0:
                ret_code = 1
                continue

        if os.access(file_path, os.W_OK):
            print(f'{ERROR_MSG_PREFIX}File "{file_path}" is not readonly.')
            ret_code = 1

    return ret_code


def check_directory_structure(comics_db: ComicsDatabase) -> int:
    logging.info("Check complete directory structure.")

    ret_code = 0
    for volume in range(FIRST_VOLUME_NUMBER, LAST_VOLUME_NUMBER + 1):
        if not _found_dir(comics_db.get_fantagraphics_upscayled_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_restored_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_restored_upscayled_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_restored_svg_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_restored_ocr_volume_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_fixes_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_upscayled_fixes_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_restored_fixes_volume_image_dir(volume)):
            ret_code = 1

        if not _found_dir(comics_db.get_fantagraphics_panel_segments_volume_dir(volume)):
            ret_code = 1

    if ret_code == 0:
        logging.info("The directory structure is correct.")
    else:
        logging.error("There are issues with the directory structure.")

    return ret_code


def _found_dir(dirname: str) -> bool:
    if not os.path.isdir(dirname):
        print(f'{ERROR_MSG_PREFIX}Could not find directory "{dirname}".')
        return False
    return True


def check_no_unexpected_files(comics_db: ComicsDatabase) -> int:
    logging.info("Check no unexpected files.")

    ret_code = 0

    dest_dirs = []
    zip_files = []
    zip_series_symlink_dirs = set()
    zip_series_symlinks = []
    zip_year_symlink_dirs = set()
    zip_year_symlinks = []
    for title in comics_db.get_all_story_titles():
        comic = comics_db.get_comic_book(title)

        dest_dirs.append((comics_db.get_ini_file(title), comic.get_dest_dir()))
        zip_files.append(comic.get_dest_comic_zip())
        zip_series_symlink_dirs.add(comic.get_dest_series_zip_symlink_dir())
        zip_series_symlinks.append(comic.get_dest_series_comic_zip_symlink())
        zip_year_symlink_dirs.add(comic.get_dest_year_zip_symlink_dir())
        zip_year_symlinks.append(comic.get_dest_year_comic_zip_symlink())

    if 0 != check_unexpected_files(
        dest_dirs,
        zip_files,
        zip_series_symlink_dirs,
        zip_series_symlinks,
        zip_year_symlink_dirs,
        zip_year_symlinks,
    ):
        ret_code = 1

    if ret_code == 0:
        logging.info("There are no unexpected files.")
    else:
        logging.error("There are some unexpected files.")

    return ret_code


def check_single_title(comics_db: ComicsDatabase, title: str) -> int:
    ret_code = 0

    comic = comics_db.get_comic_book(title)
    if 0 != check_out_of_date_files(comic):
        ret_code = 1

    return ret_code


def check_all_titles(comics_db: ComicsDatabase) -> int:
    ret_code = 0

    for title in comics_db.get_all_story_titles():
        comic = comics_db.get_comic_book(title)

        if 0 != check_out_of_date_files(comic):
            ret_code = 1

    return ret_code


def check_out_of_date_files(comic: ComicBook) -> int:
    title = get_safe_title(comic.get_comic_title())
    logging.info(f'Checking title "{title}".')

    out_of_date_errors = make_out_of_date_errors(title, comic.ini_file)

    check_srce_and_dest_files(comic, out_of_date_errors)
    check_zip_files(comic, out_of_date_errors)
    check_additional_files(comic, out_of_date_errors)

    out_of_date_errors.is_error = (
        len(out_of_date_errors.srce_and_dest_files_missing) > 0
        or len(out_of_date_errors.srce_and_dest_files_out_of_date) > 0
        or len(out_of_date_errors.dest_dir_files_missing) > 0
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

    ret_code = 1 if out_of_date_errors.is_error else 0

    if ret_code == 0:
        logging.info(f'There are no problems with "{title}".')

    return ret_code


def check_srce_and_dest_files(comic: ComicBook, errors: OutOfDateErrors) -> None:
    errors.max_srce_timestamp = 0.0
    errors.max_dest_timestamp = 0.0
    errors.num_missing_dest_files = 0
    errors.num_out_of_date_dest_files = 0
    errors.srce_and_dest_files_missing = []
    errors.srce_and_dest_files_out_of_date = []

    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic)

    check_missing_or_out_of_date_dest_files(comic, srce_and_dest_pages, errors)
    check_unexpected_dest_image_files(comic, srce_and_dest_pages, errors)


def check_missing_or_out_of_date_dest_files(
    comic: ComicBook,
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
            srce_dependencies = get_restored_srce_dependencies(comic, srce_page)
            prev_timestamp = get_timestamp(dest_page.page_filename)
            prev_file = dest_page.page_filename
            for dep_file, dep_timestamp in srce_dependencies:
                if (dep_timestamp < 0) or (dep_timestamp > prev_timestamp):
                    errors.srce_and_dest_files_out_of_date.append((dep_file, prev_file))
                    prev_timestamp = dep_timestamp
                    prev_file = dep_file
                if errors.max_srce_timestamp < dep_timestamp:
                    errors.max_srce_timestamp = dep_timestamp

            dest_timestamp = get_timestamp(dest_page.page_filename)
            if errors.max_dest_timestamp < dest_timestamp:
                errors.max_dest_timestamp = dest_timestamp


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
            print(f'{ERROR_MSG_PREFIX}The dest directory "{dest_dir}" is missing.')
            ret_code = 1
            continue

        for file in os.listdir(dest_dir):
            if file in [IMAGES_SUBDIR, ini_file]:
                continue
            if file not in DEST_NON_IMAGE_FILES:
                print(
                    f"{ERROR_MSG_PREFIX}The info file"
                    f' "{os.path.join(dest_dir, file)}" was unexpected.'
                )
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
        print(f'{ERROR_MSG_PREFIX}The directory "{the_dir}" is missing.')
        return 1

    for file in os.listdir(the_dir):
        full_file = os.path.join(the_dir, file)
        if full_file not in allowed_files:
            print(f'{ERROR_MSG_PREFIX}The {file_type} directory file "{full_file}" was unexpected.')
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
            f'{ERROR_MSG_PREFIX}For "{errors.title}",'
            f' the zip file "{errors.zip_errors.file}" is missing.'
        )

    if errors.series_zip_symlink_errors.missing:
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}",'
            f' the series symlink "{errors.series_zip_symlink_errors.symlink}" is missing.'
        )

    if errors.year_zip_symlink_errors.missing:
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}",'
            f' the year symlink "{errors.year_zip_symlink_errors.symlink}" is missing.'
        )

    if errors.zip_errors.out_of_date_wrt_srce:
        zip_file_timestamp = get_timestamp_as_str(
            errors.zip_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        max_srce_timestamp = get_timestamp_as_str(
            errors.max_srce_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the zip file\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.zip_errors.file}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the max srce file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{zip_file_timestamp}' < '{max_srce_timestamp}'."
        )

    if errors.zip_errors.out_of_date_wrt_dest:
        zip_file_timestamp = get_timestamp_as_str(
            errors.zip_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        max_dest_timestamp = get_timestamp_as_str(errors.max_dest_timestamp)
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the zip file\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.zip_errors.file}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the max dest file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{zip_file_timestamp}' < '{max_dest_timestamp}'."
        )

    if errors.zip_errors.out_of_date_wrt_ini:
        zip_file_timestamp = get_timestamp_as_str(
            errors.zip_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        ini_file_timestamp = get_timestamp_as_str(
            errors.ini_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the zip file\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.zip_errors.file}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the ini file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{zip_file_timestamp}' < '{ini_file_timestamp}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_zip:
        symlink_timestamp = get_timestamp_as_str(
            errors.series_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        zip_file_timestamp = get_timestamp_as_str(
            errors.zip_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the series symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.series_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the zip file\n"
            f'{BLANK_ERR_MSG_PREFIX}"{errors.zip_errors.file}":\n'
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{zip_file_timestamp}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_ini:
        symlink_timestamp = get_timestamp_as_str(
            errors.series_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        ini_file_timestamp = get_timestamp_as_str(
            errors.ini_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the series symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.series_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the ini file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{ini_file_timestamp}'."
        )

    if errors.series_zip_symlink_errors.out_of_date_wrt_dest:
        symlink_timestamp = get_timestamp_as_str(
            errors.series_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        max_dest_timestamp = get_timestamp_as_str(
            errors.max_dest_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the series symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.series_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the max dest file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{max_dest_timestamp}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_zip:
        symlink_timestamp = get_timestamp_as_str(
            errors.year_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        zip_file_timestamp = get_timestamp_as_str(
            errors.zip_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the year symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.year_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the zip file\n"
            f'{BLANK_ERR_MSG_PREFIX}"{errors.zip_errors.file}":\n'
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{zip_file_timestamp}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_ini:
        symlink_timestamp = get_timestamp_as_str(
            errors.year_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        ini_file_timestamp = get_timestamp_as_str(
            errors.ini_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the year symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.year_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the ini file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{ini_file_timestamp}'."
        )

    if errors.year_zip_symlink_errors.out_of_date_wrt_dest:
        symlink_timestamp = get_timestamp_as_str(
            errors.year_zip_symlink_errors.timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        max_dest_timestamp = get_timestamp_as_str(
            errors.max_dest_timestamp, DATE_SEP, DATE_TIME_SEP, HOUR_SEP
        )
        print(
            f'{ERROR_MSG_PREFIX}For "{errors.title}", the year symlink\n'
            f'{BLANK_ERR_MSG_PREFIX}"{errors.year_zip_symlink_errors.symlink}"\n'
            f"{BLANK_ERR_MSG_PREFIX}is out of date with the max dest file timestamp:\n"
            f"{BLANK_ERR_MSG_PREFIX}'{symlink_timestamp}' < '{max_dest_timestamp}'."
        )

    if len(errors.unexpected_dest_image_files) > 0:
        print()
        print_unexpected_dest_image_files_errors(errors)


def print_unexpected_dest_image_files_errors(errors: OutOfDateErrors) -> None:
    for file in errors.unexpected_dest_image_files:
        print(f'{ERROR_MSG_PREFIX} The dest image file "{get_relpath(file)}" was unexpected.')


def print_out_of_date_or_missing_errors(errors: OutOfDateErrors) -> None:
    for srce_dest in errors.srce_and_dest_files_missing:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(
            f'{ERROR_MSG_PREFIX} There is no dest file "{dest_file}"'
            f' matching srce file "{srce_file}".'
        )
    for srce_dest in errors.srce_and_dest_files_out_of_date:
        srce_file = srce_dest[0]
        dest_file = srce_dest[1]
        print(get_file_out_of_date_with_other_file_msg(dest_file, srce_file, ERROR_MSG_PREFIX))

    if (
        len(errors.srce_and_dest_files_missing) > 0
        or len(errors.srce_and_dest_files_out_of_date) > 0
        or len(errors.dest_dir_files_missing) > 0
        or len(errors.dest_dir_files_out_of_date) > 0
    ):
        print()

    if len(errors.dest_dir_files_missing) > 0:
        for file in errors.dest_dir_files_missing:
            print(f'{ERROR_MSG_PREFIX}The dest file "{file}" is missing.')
        print()

    if len(errors.dest_dir_files_out_of_date) > 0:
        for file in errors.dest_dir_files_out_of_date:
            print(
                get_file_out_of_date_wrt_max_timestamp_msg(
                    file, errors.max_dest_timestamp, ERROR_MSG_PREFIX
                )
            )
        print()

    if (
        len(errors.srce_and_dest_files_missing) > 0
        and len(errors.srce_and_dest_files_out_of_date) > 0
    ):
        print(
            f'{ERROR_MSG_PREFIX} For "{errors.title}",'
            f" there are {len(errors.srce_and_dest_files_missing)} missing dest files"
            f" and {len(errors.srce_and_dest_files_out_of_date)} out of date"
            f" dest files.\n"
        )
    else:
        if len(errors.srce_and_dest_files_missing) > 0:
            print(
                f'{ERROR_MSG_PREFIX} For "{errors.title}",'
                f" there are {len(errors.srce_and_dest_files_missing)} missing"
                f" dest files.\n"
            )

        if len(errors.srce_and_dest_files_out_of_date) > 0:
            print(
                f'{ERROR_MSG_PREFIX} For "{errors.title}",'
                f" there are {len(errors.srce_and_dest_files_out_of_date)} out of"
                f" date dest files.\n"
            )


def get_restored_srce_dependencies(
    comic: ComicBook, srce_page: CleanPage
) -> List[Tuple[str, float]]:
    page_num_str = get_page_str(srce_page.page_num)

    srce_page_timestamp = get_timestamp(srce_page.page_filename)

    srce_upscayl_file = comic.get_srce_upscayled_story_file(page_num_str)
    srce_with_fixes_file = comic.get_srce_with_fixes_story_file(page_num_str, srce_page.page_type)[
        0
    ]
    srce_upscayl_timestamp = (
        get_timestamp(srce_upscayl_file) if os.path.isfile(srce_upscayl_file) else -1
    )
    srce_panel_segments_file = comic.get_srce_panel_segments_file(page_num_str)
    srce_panel_segments_timestamp = (
        get_timestamp(srce_panel_segments_file) if os.path.isfile(srce_panel_segments_file) else -1
    )

    underlying_files = []

    if srce_page.page_type in [PageType.FRONT_MATTER, PageType.BODY, PageType.BACK_MATTER]:
        underlying_files.append((srce_panel_segments_file, srce_panel_segments_timestamp))
        panel_bounds_file = comic.get_fixes_panel_bounds_file(srce_page.page_num)
        if panel_bounds_file:
            underlying_files.append((panel_bounds_file, get_timestamp(panel_bounds_file)))

    underlying_files.append((comic.ini_file, get_timestamp(comic.ini_file)))
    underlying_files.append((comic.intro_inset_file, get_timestamp(comic.intro_inset_file)))
    underlying_files.append((srce_page.page_filename, srce_page_timestamp))

    if srce_page.page_type in [PageType.FRONT_MATTER, PageType.BODY, PageType.BACK_MATTER]:
        underlying_files.append((srce_upscayl_file, srce_upscayl_timestamp))
        underlying_files.append((srce_with_fixes_file, get_timestamp(srce_with_fixes_file)))

    return underlying_files
