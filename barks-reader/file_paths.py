import os
from typing import List

from barks_fantagraphics.comics_consts import JPG_FILE_EXT

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
BARKS_READER_SPLASH_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Splash")
BARKS_READER_COVER_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Covers")
BARKS_READER_SILHOUETTE_FILES_DIR = os.path.join(BARKS_READER_FILES_DIR, "Silhouettes")

EMERGENCY_INSET_FILE = "Biceps Blues"


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


def get_comic_splash_files_dir() -> str:
    return BARKS_READER_SPLASH_FILES_DIR


def get_comic_cover_files_dir() -> str:
    return BARKS_READER_COVER_FILES_DIR


def get_comic_silhouette_files_dir() -> str:
    return BARKS_READER_SILHOUETTE_FILES_DIR


def get_comic_inset_file(title: str) -> str:
    main_inset_file = os.path.join(get_comic_inset_files_dir(), title + JPG_FILE_EXT)
    if os.path.isfile(main_inset_file):
        return main_inset_file

    edited_inset_file = os.path.join(BARKS_READER_INSET_EDITED_FILES_DIR, title + JPG_FILE_EXT)

    # assert os.path.isfile(edited_inset_file)
    # TODO: Fix this when all titles are configured.
    if not os.path.isfile(edited_inset_file):
        return get_comic_inset_file(EMERGENCY_INSET_FILE)

    return edited_inset_file


def get_comic_splash_files(title: str) -> List[str]:
    image_dir = os.path.join(get_comic_splash_files_dir(), title)
    if not os.path.isdir(image_dir):
        return list()

    image_files = []
    for file in os.listdir(image_dir):
        image_files.append(os.path.join(image_dir, file))

    return image_files


def get_comic_silhouette_files(title: str) -> List[str]:
    image_dir = os.path.join(get_comic_silhouette_files_dir(), title)
    if not os.path.isdir(image_dir):
        return list()

    image_files = []
    for file in os.listdir(image_dir):
        image_files.append(os.path.join(image_dir, file))

    return image_files


def get_comic_cover_file(title: str) -> str:
    cover_file = os.path.join(get_comic_cover_files_dir(), title + JPG_FILE_EXT)
    if not os.path.isfile(cover_file):
        return ""

    return cover_file
