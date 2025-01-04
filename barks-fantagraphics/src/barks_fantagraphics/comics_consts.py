import os
from enum import Enum
from pathlib import Path

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
PUBLICATION_INFO_SUBDIR = "story-indexes"
SUBMISSION_DATES_SUBDIR = "story-indexes"
STORIES_INFO_FILENAME = "the-stories.csv"

INSET_FILE_EXT = ".png"


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


FONT_DIR = os.path.join(str(Path.home()), "Prj", "fonts")
INTRO_TITLE_DEFAULT_FONT_FILE = os.path.join(FONT_DIR, "Carl Barks Script.ttf")
INTRO_TEXT_FONT_FILE = "Verdana Italic.ttf"
PAGE_NUM_FONT_FILE = "verdana.ttf"


def get_font_path(font_filename: str) -> str:
    return os.path.join(FONT_DIR, font_filename)
