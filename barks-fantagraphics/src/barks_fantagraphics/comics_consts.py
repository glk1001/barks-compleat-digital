import os
from enum import Enum, auto
from pathlib import Path
from typing import Dict


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

INSET_FILE_EXT = ".png"


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

FONT_DIR = os.path.join(str(Path.home()), "Prj", "fonts")
INTRO_TITLE_DEFAULT_FONT_FILE = os.path.join(FONT_DIR, "Carl Barks Script.ttf")
INTRO_TEXT_FONT_FILE = "Verdana Italic.ttf"
PAGE_NUM_FONT_FILE = "verdana.ttf"


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)
