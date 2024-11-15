import os
from enum import Enum
from pathlib import Path

DRY_RUN_STR = "DRY_RUN"
BIG_NUM = 10000

ROMAN_NUMERALS = {
    1: "i",
    2: "ii",
    3: "iii",
    4: "iv",
    5: "v",
    6: "vi",
    7: "vii",
    8: "viii",
    9: "ix",
    10: "x",
}

DEST_TARGET_WIDTH = 2120
DEST_TARGET_HEIGHT = 3200
DEST_TARGET_X_MARGIN = 100
DEST_TARGET_ASPECT_RATIO = float(DEST_TARGET_HEIGHT) / float(DEST_TARGET_WIDTH)

THIS_DIR = os.path.realpath(os.path.dirname(__file__))
BARKS = "Carl Barks"
BARKS_ROOT_DIR = os.path.join(str(Path.home()), "Books", BARKS)
THE_COMICS_SUBDIR = "The Comics"
THE_COMICS_DIR = os.path.join(BARKS_ROOT_DIR, THE_COMICS_SUBDIR)
THE_CHRONOLOGICAL_DIRS_SUBDIR = "aaa-Chronological-dirs"
THE_CHRONOLOGICAL_SUBDIR = "Chronological"
THE_CHRONOLOGICAL_DIRS_DIR = os.path.join(THE_COMICS_DIR, THE_CHRONOLOGICAL_DIRS_SUBDIR)
THE_CHRONOLOGICAL_DIR = os.path.join(THE_COMICS_DIR, THE_CHRONOLOGICAL_SUBDIR)
THE_YEARS_SUBDIR = "Chronological Years"
THE_YEARS_COMICS_DIR = os.path.join(THE_COMICS_DIR, THE_YEARS_SUBDIR)
CONFIGS_SUBDIR = "Configs"
IMAGES_SUBDIR = "images"
PUBLICATION_INFO_SUBDIR = "story-indexes"
SUBMISSION_DATES_SUBDIR = "story-indexes"
TITLE_EMPTY_FILENAME = "title_empty"
EMPTY_FILENAME = "empty"
DEST_FILE_EXT = ".jpg"
INSET_FILE_EXT = ".png"
DEST_JPG_QUALITY = 95
DEST_JPG_COMPRESS_LEVEL = 9
MIN_HD_SRCE_HEIGHT = 3000
NUMBER_LEN = 3
FOOTNOTE_CHAR = "*"

DEST_SRCE_MAP_FILENAME = "srce-dest-map.json"
DEST_PANELS_BBOXES_FILENAME = "dest-panels-bboxes.json"
PANEL_BOUNDS_FILENAME_SUFFIX = "_panel_bounds.txt"
PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN = 100

README_FILENAME = "readme.txt"
SUMMARY_FILENAME = "clean_summary.txt"
METADATA_FILENAME = "metadata.txt"
JSON_METADATA_FILENAME = "comic-metadata.json"
DOUBLE_PAGES_SECTION = "double_pages"
PAGE_NUMBERS_SECTION = "page_numbers"
DEST_NON_IMAGE_FILES = {
    SUMMARY_FILENAME,
    JSON_METADATA_FILENAME,
    DEST_PANELS_BBOXES_FILENAME,
    METADATA_FILENAME,
    README_FILENAME,
    DEST_SRCE_MAP_FILENAME,
}


class PageType(Enum):
    FRONT = 1
    TITLE = 2
    COVER = 3
    SPLASH = 4
    SPLASH_NO_BORDER = 5
    PAINTING = 6
    PAINTING_NO_BORDER = 7
    FRONT_MATTER = 8
    BODY = 9
    BACK_MATTER = 10
    BACK_NO_PANELS = 11
    BLANK_PAGE = 12


FRONT_PAGES = [
    PageType.FRONT,
    PageType.TITLE,
    PageType.COVER,
    PageType.SPLASH,
    PageType.SPLASH_NO_BORDER,
    PageType.PAINTING,
    PageType.PAINTING_NO_BORDER,
]
FRONT_MATTER_PAGES = FRONT_PAGES + [PageType.FRONT_MATTER]
PAGES_WITHOUT_PANELS = FRONT_PAGES + [PageType.BACK_NO_PANELS, PageType.BLANK_PAGE]
SPLASH_PAGES = [
    PageType.SPLASH,
    PageType.SPLASH_NO_BORDER,
]
PAINTING_PAGES = [
    PageType.PAINTING,
    PageType.PAINTING_NO_BORDER,
]

FONT_DIR = os.path.join(str(Path.home()), "Prj", "fonts")
INTRO_TITLE_DEFAULT_FONT_FILE = os.path.join(FONT_DIR, "Carl Barks Script.ttf")
INTRO_TEXT_FONT_FILE = "Verdana Italic.ttf"
PAGE_NUM_FONT_FILE = "verdana.ttf"


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)
