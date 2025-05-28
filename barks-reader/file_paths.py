import os
from pathlib import Path
from typing import List

from barks_fantagraphics.barks_titles import Titles, BARKS_TITLE_INFO, BARKS_TITLES
from barks_fantagraphics.comics_consts import JPG_FILE_EXT, PNG_FILE_EXT

HOME_DIR = os.environ.get("HOME")

MCOMIX_PYTHON_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/.venv/bin/python")
MCOMIX_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/mcomixstarter.py")

BARKS_READER_CONFIG_PATH = os.path.join(
    HOME_DIR, "Prj/github/barks-compleat-digital/barks-reader/mcomix-barks-ui-desc.xml"
)
THE_COMICS_DIR = os.path.join(HOME_DIR, "Books/Carl Barks/The Comics")
THE_COMIC_ZIPS_DIR = os.path.join(THE_COMICS_DIR, "Chronological")
THE_COMIC_FILES_DIR = os.path.join(THE_COMICS_DIR, "aaa-Chronological-dirs")
BARKS_READER_FILES_DIR = os.path.join(THE_COMICS_DIR, "Reader Files")
BARKS_READER_INSET_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Insets")
BARKS_READER_INSET_EDITED_FILES_DIR = os.path.join(BARKS_READER_INSET_FILES_DIR, "Edited")
BARKS_READER_COVER_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Covers")
BARKS_READER_SILHOUETTE_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Silhouettes")
BARKS_READER_SPLASH_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Splash")
BARKS_READER_CENSORSHIP_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Censorship")
BARKS_READER_FAVOURITE_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Favourites")
BARKS_READER_ORIGINAL_ART_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Original Art")
BARKS_READER_APP_ICON = os.path.join(BARKS_READER_FILES_DIR, "Barks Reader Icon 1.png")

EMERGENCY_INSET_FILE = Titles.BICEPS_BLUES
EMERGENCY_INSET_FILE_PATH = os.path.join(
    BARKS_READER_INSET_FILES_DIR,
    BARKS_TITLE_INFO[EMERGENCY_INSET_FILE].get_title_str() + JPG_FILE_EXT,
)


def check_dirs_and_files() -> None:
    dirs_to_check = [
        THE_COMICS_DIR,
        THE_COMIC_ZIPS_DIR,
        THE_COMIC_FILES_DIR,
        BARKS_READER_FILES_DIR,
        BARKS_READER_INSET_FILES_DIR,
        BARKS_READER_INSET_EDITED_FILES_DIR,
        BARKS_READER_COVER_FILES_DIR,
        BARKS_READER_SILHOUETTE_FILES_DIR,
        BARKS_READER_SPLASH_FILES_DIR,
        BARKS_READER_CENSORSHIP_FILES_DIR,
        BARKS_READER_FAVOURITE_FILES_DIR,
        BARKS_READER_ORIGINAL_ART_FILES_DIR,
    ]
    files_to_check = [
        MCOMIX_PYTHON_PATH,
        MCOMIX_PATH,
        EMERGENCY_INSET_FILE_PATH,
        BARKS_READER_CONFIG_PATH,
        BARKS_READER_APP_ICON,
    ]

    if HOME_DIR is None:
        raise EnvironmentError("HOME environment variable is not set. Cannot determine base paths.")
    if not os.path.isdir(HOME_DIR):
        raise FileNotFoundError(f'The HOME directory specified does not exist: "{HOME_DIR}".')

    for dir_path in dirs_to_check:
        if not os.path.isdir(dir_path):
            raise FileNotFoundError(f'Required directory not found: "{dir_path}".')

    for file_path in files_to_check:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f'Required file not found: "{file_path}".')


check_dirs_and_files()


def get_mcomix_python_bin_path() -> str:
    return MCOMIX_PYTHON_PATH


def get_mcomix_path() -> str:
    return MCOMIX_PATH


def get_mcomix_barks_reader_config_path() -> str:
    return BARKS_READER_CONFIG_PATH


def get_the_comic_zips_dir() -> str:
    return THE_COMIC_ZIPS_DIR


def get_the_comic_files_dir() -> str:
    return THE_COMIC_FILES_DIR


def get_comic_inset_files_dir() -> str:
    return BARKS_READER_INSET_FILES_DIR


def get_comic_cover_files_dir() -> str:
    return BARKS_READER_COVER_FILES_DIR


def get_comic_silhouette_files_dir() -> str:
    return BARKS_READER_SILHOUETTE_FILES_DIR


def get_comic_splash_files_dir() -> str:
    return BARKS_READER_SPLASH_FILES_DIR


def get_comic_censorship_files_dir() -> str:
    return BARKS_READER_CENSORSHIP_FILES_DIR


def get_comic_favourite_files_dir() -> str:
    return BARKS_READER_FAVOURITE_FILES_DIR


def get_comic_original_art_files_dir() -> str:
    return BARKS_READER_ORIGINAL_ART_FILES_DIR


def get_barks_reader_app_icon_file() -> str:
    return BARKS_READER_APP_ICON


def get_comic_inset_file(title: Titles, use_edited: bool = False) -> str:
    title_str = BARKS_TITLES[title]

    if use_edited:
        edited_file = os.path.join(BARKS_READER_INSET_EDITED_FILES_DIR, title_str + PNG_FILE_EXT)
        if os.path.isfile(edited_file):
            return edited_file

    main_file = os.path.join(get_comic_inset_files_dir(), title_str + JPG_FILE_EXT)
    # TODO: Fix this when all titles are configured.
    # assert os.path.isfile(edited_file)
    if os.path.isfile(main_file):
        return main_file

    return EMERGENCY_INSET_FILE_PATH


def get_comic_cover_file(title: str) -> str:
    edited_file = os.path.join(get_comic_cover_files_dir(), "edited", title + PNG_FILE_EXT)
    if os.path.isfile(edited_file):
        return edited_file

    cover_file = os.path.join(get_comic_cover_files_dir(), title + JPG_FILE_EXT)
    if not os.path.isfile(cover_file):
        return ""

    return cover_file


def get_comic_silhouette_files(title: str) -> List[str]:
    return get_files(get_comic_silhouette_files_dir(), title)


def get_comic_splash_files(title: str) -> List[str]:
    return get_files(get_comic_splash_files_dir(), title)


def get_comic_censorship_files(title: str) -> List[str]:
    return get_files(get_comic_censorship_files_dir(), title)


def get_comic_favourite_files(title: str) -> List[str]:
    return get_files(get_comic_favourite_files_dir(), title)


def get_comic_original_art_files(title: str) -> List[str]:
    return get_files(get_comic_original_art_files_dir(), title)


def get_files(parent_image_dir: str, title: str) -> List[str]:
    image_dir = os.path.join(parent_image_dir, title)
    if not os.path.isdir(image_dir):
        return list()

    edited_image_dir = os.path.join(image_dir, "edited")

    image_files = []
    for file in os.listdir(image_dir):
        image_file = os.path.join(image_dir, file)
        if not os.path.isfile(image_file):
            continue

        edited_image_file = os.path.join(edited_image_dir, Path(file).stem + PNG_FILE_EXT)
        if os.path.isfile(edited_image_file):
            image_files.append(edited_image_file)
        else:
            image_files.append(image_file)

    return image_files
