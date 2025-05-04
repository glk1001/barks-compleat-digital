import os

HOME_DIR = os.environ.get("HOME")

MCOMIX_PYTHON_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/.venv/bin/python")
MCOMIX_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/mcomixstarter.py")

BARKS_READER_CONFIG_PATH = os.path.join(
    HOME_DIR, "Prj/github/barks-compleat-digital/barks-reader/mcomix-barks-ui-desc.xml"
)
THE_COMICS_DIR = os.path.join(HOME_DIR, "Books/Carl Barks/The Comics")
THE_COMIC_ZIPS_DIR = os.path.join(THE_COMICS_DIR, "Chronological")
THE_COMIC_FILES_DIR = os.path.join(THE_COMICS_DIR, "aaa-Chronological-dirs")
COMIC_INSETS_DIR = os.path.join(
    HOME_DIR, "Prj/github/barks-compleat-digital/barks-fantagraphics/story-titles"
)


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


def get_comic_inset_file(title: str) -> str:
    return os.path.join(COMIC_INSETS_DIR, f"{title} Inset.png")
