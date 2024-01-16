import json
import os

from typing import Dict

from comics_info import ALL_SERIES
from consts import (
    BARKS_ROOT_DIR,
    THE_COMICS_DIR,
    DEST_SRCE_MAP_FILENAME,
    PANEL_BOUNDS_FILENAME_SUFFIX,
)
from panel_bounding_boxes import BoundingBox, BoundingBoxProcessor


def get_panels_bounding_boxes(comic_dir: str) -> Dict[str, BoundingBox]:
    with open(os.path.join(comic_dir, DEST_SRCE_MAP_FILENAME), "r") as f:
        dest_map = json.load(f)
    srce_comic_dirname = dest_map["srce_dirname"]
    comic_bbox_dir = os.path.join(bbox_dir, srce_comic_dirname)

    print(f'srce_min_panels_bbox_width = {dest_map["srce_min_panels_bbox_width"]}')
    print(f'srce_max_panels_bbox_width = {dest_map["srce_max_panels_bbox_width"]}')
    print(f'srce_min_panels_bbox_height = {dest_map["srce_min_panels_bbox_height"]}')
    print(f'srce_max_panels_bbox_height = {dest_map["srce_max_panels_bbox_height"]}')

    boundingBoxProcessor = BoundingBoxProcessor("/tmp")

    #    print(dest_map)
    bbox_dict = dict()
    for page in dest_map["pages"]:
        if dest_map["pages"][page]["type"] != "BODY":
            continue

        bbox_key = os.path.splitext(dest_map["pages"][page]["file"])[0]
        panel_bounds_file = os.path.join(
            comic_bbox_dir,
            f"{bbox_key}{PANEL_BOUNDS_FILENAME_SUFFIX}",
        )
        panels_bbox = boundingBoxProcessor.get_panels_bounding_box_from_file(
            panel_bounds_file
        )
        bbox_dict[bbox_key] = panels_bbox

    return bbox_dict


def check_comic_bboxes(bbox_dict: Dict[str, BoundingBox]):
    for page in bbox_dict:
        bbox = bbox_dict[page]
        print(
            f'"{page}": {bbox}, width = {bbox.get_width()}, height = {bbox.get_height()}'
        )


if __name__ == "__main__":
    bbox_dir = os.path.join(BARKS_ROOT_DIR, "Fantagraphics-panel-segments")

    for series in ALL_SERIES:
        series_dir = str(os.path.join(THE_COMICS_DIR, series))

        for comic_dirname in sorted(os.listdir(series_dir)):
            the_comic_dir = os.path.join(series_dir, comic_dirname)
            if not os.path.isdir(the_comic_dir):
                continue

            print(the_comic_dir)
            bboxes = get_panels_bounding_boxes(the_comic_dir)
            check_comic_bboxes(bboxes)
