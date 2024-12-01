import json
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

from barks_fantagraphics.comics_info import ALL_SERIES
from barks_fantagraphics.comics_consts import (
    BARKS_ROOT_DIR,
    THE_COMICS_DIR,
    DEST_PANELS_BBOXES_FILENAME,
    DEST_SRCE_MAP_FILENAME,
    PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN,
    PageType,
)
from panel_bounding_boxes import BoundingBox


@dataclass
class PanelsBoundingBoxesDimensions:
    dest_required_bbox_width: int
    dest_required_bbox_height: int


def get_panels_bounding_boxes(
    comic_dir: str,
) -> Tuple[Dict[str, Tuple[PageType, BoundingBox]], PanelsBoundingBoxesDimensions]:
    with open(os.path.join(comic_dir, DEST_SRCE_MAP_FILENAME), "r") as f:
        dest_map = json.load(f)

    bounding_boxes_dim = PanelsBoundingBoxesDimensions(
        dest_map["dest_required_bbox_width"],
        dest_map["dest_required_bbox_height"],
    )

    with open(os.path.join(comic_dir, DEST_PANELS_BBOXES_FILENAME), "r") as f:
        panels_bboxes = json.load(f)

    def get_bbox(vals: List[int]):
        return BoundingBox(vals[0], vals[1], vals[2], vals[3])

    panels_bbox_dict = {
        key: (
            PageType[dest_map["pages"][key]["type"].upper()],
            get_bbox(panels_bboxes[key]),
        )
        for key in panels_bboxes
    }

    return panels_bbox_dict, bounding_boxes_dim


def check_comic_bboxes(
    bbox_dict: Dict[str, Tuple[PageType, BoundingBox]],
    bounding_boxes_dim: PanelsBoundingBoxesDimensions,
):
    min_bbox_width = (
        bounding_boxes_dim.dest_required_bbox_width - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    )
    max_bbox_width = (
        bounding_boxes_dim.dest_required_bbox_width + PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    )
    min_bbox_height = (
        bounding_boxes_dim.dest_required_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    )
    max_bbox_height = (
        bounding_boxes_dim.dest_required_bbox_height + PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    )

    for page in bbox_dict:
        page_type = bbox_dict[page][0]
        if page_type not in [
            PageType.FRONT_MATTER,
            PageType.BODY,
            PageType.BACK_MATTER,
        ]:
            continue

        bbox = bbox_dict[page][1]
        if bbox.get_width() < min_bbox_width:
            print(
                f"Too small width {bbox.get_width()} < {min_bbox_width}: "
                f'"{page}": "{page_type.name}", {bbox}'
                f", width = {bbox.get_width()}, height = {bbox.get_height()}"
            )
        if bbox.get_width() > max_bbox_width:
            print(
                f"Too big width {bbox.get_width()} > {max_bbox_width}: "
                f'"{page}": "{page_type.name}", {bbox}'
                f", width = {bbox.get_width()}, height = {bbox.get_height()}"
            )
        if bbox.get_height() < min_bbox_height:
            print(
                f"Too small height {bbox.get_height()} < {min_bbox_height}: "
                f'"{page}": "{page_type.name}", {bbox}'
                f", width = {bbox.get_width()}, height = {bbox.get_height()}"
            )
        if bbox.get_height() > max_bbox_height:
            print(
                f"Too big height {bbox.get_height()} > {max_bbox_height}: "
                f'"{page}": "{page_type.name}", {bbox}'
                f", width = {bbox.get_width()}, height = {bbox.get_height()}"
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
            bboxes, bboxes_dim = get_panels_bounding_boxes(the_comic_dir)
            check_comic_bboxes(bboxes, bboxes_dim)
