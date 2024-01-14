import os
from pathlib import Path

DRY_RUN_STR = "DRY_RUN"

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
IMAGES_SUBDIR = "images"
CONFIGS_SUBDIR = "Configs"
TITLE_EMPTY_FILENAME = "title_empty"
EMPTY_FILENAME = "empty"
NUMBER_LEN = 3
SRCE_FILE_EXT = ".jpg"
DEST_FILE_EXT = ".jpg"
INSET_FILE_EXT = ".png"

DEST_SRCE_MAP_FILENAME = "srce-dest-map.json"
PANEL_BOUNDS_FILENAME_SUFFIX = "_panel_bounds.txt"
