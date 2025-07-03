import os
from enum import Enum, auto
from pathlib import Path
from typing import Dict

# TODO: Should this dest stuff be here?
DEST_TARGET_WIDTH = 2120
DEST_TARGET_HEIGHT = 3200
DEST_TARGET_X_MARGIN = 100
DEST_TARGET_ASPECT_RATIO = float(DEST_TARGET_HEIGHT) / float(DEST_TARGET_WIDTH)
PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN = 100

PAGE_NUM_X_OFFSET_FROM_CENTRE = 150
PAGE_NUM_X_BLANK_PIXEL_OFFSET = 250
PAGE_NUM_HEIGHT = 40
PAGE_NUM_FONT_SIZE = 30
PAGE_NUM_COLOR = (10, 10, 10)

JPG_FILE_EXT = ".jpg"
PNG_FILE_EXT = ".png"
SVG_FILE_EXT = ".svg"
JSON_FILE_EXT = ".json"
TEXT_FILE_EXT = ".txt"

JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

MONTH_AS_SHORT_STR: Dict[int, str] = {
    JAN: "Jan",
    FEB: "Feb",
    MAR: "Mar",
    APR: "Apr",
    MAY: "May",
    JUN: "Jun",
    JUL: "Jul",
    AUG: "Aug",
    SEP: "Sep",
    OCT: "Oct",
    NOV: "Nov",
    DEC: "Dec",
}

MONTH_AS_LONG_STR: Dict[int, str] = {
    JAN: "January",
    FEB: "February",
    MAR: "March",
    APR: "April",
    MAY: "May",
    JUN: "June",
    JUL: "July",
    AUG: "August",
    SEP: "September",
    OCT: "October",
    NOV: "November",
    DEC: "December",
}

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
STORY_TITLES_DIR = "story-titles"
IMAGES_SUBDIR = "images"
BOUNDED_SUBDIR = "bounded"

PNG_INSET_DIR = os.path.join(BARKS_ROOT_DIR, "Barks Panels Pngs", "Insets")
PNG_INSET_EXT = PNG_FILE_EXT

FONT_DIR = os.path.join(str(Path.home()), "Prj", "fonts")
INTRO_TITLE_DEFAULT_FONT_FILE = os.path.join(FONT_DIR, "Carl Barks Script.ttf")
INTRO_TEXT_FONT_FILE = "Verdana Italic.ttf"
PAGE_NUM_FONT_FILE = "verdana.ttf"


class PageType(Enum):
    FRONT = auto()
    TITLE = auto()
    COVER = auto()
    SPLASH = auto()
    PAINTING = auto()
    PAINTING_NO_BORDER = auto()
    FRONT_MATTER = auto()
    BODY = auto()
    BACK_MATTER = auto()
    BACK_NO_PANELS = auto()
    BACK_NO_PANELS_DOUBLE = auto()
    BACK_PAINTING = auto()
    BACK_PAINTING_NO_BORDER = auto()
    BLANK_PAGE = auto()


RESTORABLE_PAGE_TYPES = [
    PageType.BODY,
    PageType.FRONT_MATTER,
    PageType.BACK_MATTER,
]

STORY_PAGE_TYPES = [
    PageType.COVER,
    PageType.BODY,
    PageType.FRONT_MATTER,
    PageType.BACK_MATTER,
]
STORY_PAGE_TYPES_STR_LIST = [e.name for e in STORY_PAGE_TYPES]

FRONT_PAGES = [
    PageType.FRONT,
    PageType.TITLE,
    PageType.COVER,
    PageType.SPLASH,
    PageType.PAINTING,
    PageType.PAINTING_NO_BORDER,
]
FRONT_MATTER_PAGES = FRONT_PAGES + [PageType.FRONT_MATTER]
BACK_MATTER_PAGES = [
    PageType.BACK_MATTER,
    PageType.BACK_NO_PANELS,
    PageType.BACK_NO_PANELS_DOUBLE,
    PageType.BACK_PAINTING,
    PageType.BACK_PAINTING_NO_BORDER,
    PageType.BLANK_PAGE,
]
BACK_MATTER_SINGLE_PAGES = [p for p in BACK_MATTER_PAGES if p != PageType.BLANK_PAGE]
BACK_NO_PANELS_PAGES = [PageType.BACK_NO_PANELS, PageType.BACK_NO_PANELS_DOUBLE]
PAINTING_PAGES = [
    PageType.PAINTING,
    PageType.PAINTING_NO_BORDER,
    PageType.BACK_PAINTING,
    PageType.BACK_PAINTING_NO_BORDER,
]
PAGES_WITHOUT_PANELS = set(
    FRONT_PAGES + PAINTING_PAGES + BACK_NO_PANELS_PAGES + [PageType.BLANK_PAGE]
)


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)
