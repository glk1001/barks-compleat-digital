import json
import os

from consts import (
    BARKS_ROOT_DIR,
    THE_COMICS_DIR,
    DEST_SRCE_MAP_FILENAME,
    PANEL_BOUNDS_FILENAME_SUFFIX,
)


def check_bbox_dir(dir_path: str):
    pass


if __name__ == "__main__":
    bbox_dir = os.path.join(BARKS_ROOT_DIR, "Fantagraphics-panel-segments")

    comic_dir = os.path.join(
        THE_COMICS_DIR, "Uncle Scrooge Short Stories", "001 Somethin' Fishy Here"
    )
    with open(os.path.join(comic_dir, DEST_SRCE_MAP_FILENAME), "r") as f:
        dest_map = json.load(f)
    srce_comic_dirname = dest_map["srce_dirname"]
    comic_bbox_dir = os.path.join(bbox_dir, srce_comic_dirname)

    #    print(dest_map)
    bbox_file_list = []
    for page in dest_map["pages"]:
        if dest_map["pages"][page]["type"] != "BODY":
            continue
        bounds_filename = os.path.join(
            comic_bbox_dir,
            f'{os.path.splitext(dest_map["pages"][page]["file"])[0]}{PANEL_BOUNDS_FILENAME_SUFFIX}',
        )
        bbox_file_list.append(bounds_filename)

    for f in bbox_file_list:
        print(f)
