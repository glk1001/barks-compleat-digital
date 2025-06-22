import json
import logging
import os
import sys
from dataclasses import dataclass

from PIL import Image

from barks_fantagraphics.comic_book import ComicBook, ComicDimensions
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import (
    setup_logging,
)
from barks_fantagraphics.pages import (
    get_srce_and_dest_pages_in_order,
    PageType,
)


@dataclass
class Dimensions:
    srce_dims: ComicDimensions
    front_width: int
    front_height: int


def get_story_dimensions(comic: ComicBook) -> Dimensions:
    srce_and_dest_pages = get_srce_and_dest_pages_in_order(comic, get_full_paths=True)

    front_width = -1
    front_height = -1
    front_page = srce_and_dest_pages.srce_pages[0]
    if front_page.page_type == PageType.FRONT:
        image = Image.open(front_page.page_filename, "r")
        front_width = image.width
        front_height = image.height

    srce_dims = ComicDimensions()
    metadata_file = os.path.join(comic.get_dest_dir(), "comic-metadata.json")
    with open(metadata_file, "r") as f:
        comic_metadata = json.load(f)
        srce_dims.min_panels_bbox_width = comic_metadata["srce_min_panels_bbox_width"]
        srce_dims.max_panels_bbox_width = comic_metadata["srce_max_panels_bbox_width"]
        srce_dims.min_panels_bbox_height = comic_metadata["srce_min_panels_bbox_height"]
        srce_dims.max_panels_bbox_height = comic_metadata["srce_max_panels_bbox_height"]
        srce_dims.av_panels_bbox_width = comic_metadata["srce_av_panels_bbox_width"]
        srce_dims.av_panels_bbox_height = comic_metadata["srce_av_panels_bbox_height"]

    return Dimensions(srce_dims, front_width, front_height)


# TODO(glk): Some issue with type checking inspection?
# noinspection PyTypeChecker
cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()

dimensions_dict = dict()
max_title_len = 0
for title in titles:
    comic_book = comics_database.get_comic_book(title)

    story_dims = get_story_dimensions(comic_book)

    title_with_issue_num = comic_book.get_title_with_issue_num()
    if max_title_len < len(title_with_issue_num):
        max_title_len = len(title_with_issue_num)

    dimensions_dict[title_with_issue_num] = story_dims

for title in dimensions_dict.keys():
    title_str = title + ":"

    story_dims = dimensions_dict[title]

    box_dims = story_dims.srce_dims
    bboxes_str = (
        f"{box_dims.min_panels_bbox_width:4},{box_dims.max_panels_bbox_width}"
        f" {box_dims.min_panels_bbox_height:4},{box_dims.max_panels_bbox_height}"
        f" {box_dims.av_panels_bbox_width:4},{box_dims.av_panels_bbox_height}"
    )

    front_str = (
        ""
        if story_dims.front_width == -1
        else f"Front: {story_dims.front_width:4} x {story_dims.front_height:4}"
    )

    print(f"{title_str:<{max_title_len + 1}} BBoxes: {bboxes_str}  {front_str}")
