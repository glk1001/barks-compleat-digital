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

THIS_DIR = os.path.realpath(os.path.dirname(__file__))
BARKS = "Carl Barks"
BARKS_ROOT_DIR = os.path.join(str(Path.home()), "Books", BARKS)
THE_COMICS_SUBDIR = "The Comics"
THE_COMICS_DIR = os.path.join(BARKS_ROOT_DIR, THE_COMICS_SUBDIR)
IMAGES_SUBDIR = "images"
CONFIGS_SUBDIR = "Configs"
PUBLICATION_INFO_DIRNAME = "story-indexes"
SUBMISSION_DATES_DIRNAME = "story-indexes"
TITLE_EMPTY_FILENAME = "title_empty"
EMPTY_FILENAME = "empty"
NUMBER_LEN = 3
SRCE_FILE_EXT = ".jpg"
DEST_FILE_EXT = ".jpg"
INSET_FILE_EXT = ".png"
MIN_HD_SRCE_HEIGHT = 3000

DEST_SRCE_MAP_FILENAME = "srce-dest-map.json"
DEST_PANELS_BBOXES_FILENAME = "dest-panels-bboxes.json"
PANEL_BOUNDS_FILENAME_SUFFIX = "_panel_bounds.txt"
PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN = 100


class PageType(Enum):
    FRONT = 1
    TITLE = 2
    COVER = 3
    SPLASH = 4
    FRONT_MATTER = 5
    BODY = 6
    BACK_MATTER = 7
    BACK_NO_PANELS = 8
    BLANK_PAGE = 9


FRONT_PAGES = [
    PageType.FRONT,
    PageType.TITLE,
    PageType.COVER,
    PageType.SPLASH,
]
FRONT_MATTER_PAGES = FRONT_PAGES + [PageType.FRONT_MATTER]
PAGES_WITHOUT_PANELS = FRONT_PAGES + [PageType.BACK_NO_PANELS, PageType.BLANK_PAGE]
