import json
import logging
import os.path
import sys
from pathlib import Path

import cv2 as cv
from PIL import Image, ImageDraw

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_image_io import get_bw_image_from_alpha
from barks_fantagraphics.comics_info import PNG_FILE_EXT
from barks_fantagraphics.comics_utils import get_abbrev_path, setup_logging
from barks_fantagraphics.panel_segmentation import get_min_max_panel_values


def show_panel_bounds(title: str, out_dir: str) -> None:
    out_dir = os.path.join(out_dir, title)

    logging.info(f'Generating panel bounds images for "{title}" to directory "{out_dir}"...')

    os.makedirs(out_dir, exist_ok=True)
    comic = comics_database.get_comic_book(title)
    svg_files = comic.get_srce_restored_svg_story_files(RESTORABLE_PAGE_TYPES)
    panel_segments_files = comic.get_srce_panel_segments_files(RESTORABLE_PAGE_TYPES)

    for svg_file, panel_segments_file in zip(svg_files, panel_segments_files):
        png_file = svg_file + PNG_FILE_EXT
        bounds_img_file = os.path.join(out_dir, Path(svg_file).stem + "-with-bounds.png")
        if not write_bounds_to_image_file(png_file, panel_segments_file, bounds_img_file):
            raise Exception("There were process errors.")


def write_bounds_to_image_file(
    png_file: str, panel_segments_file: str, bounds_img_file: str
) -> bool:
    logging.info(f'Writing bounds for image "{get_abbrev_path(png_file)}"...')

    if not os.path.isfile(png_file):
        logging.error(f'Could not find image file "{png_file}".')
        return False
    if not os.path.isfile(panel_segments_file):
        logging.error(f'Could not find panel segments file "{panel_segments_file}".')
        return False
    if os.path.isfile(bounds_img_file):
        logging.info(f'Found existing image bounds file "{bounds_img_file}" -- skipping.')
        return True

    logging.info(f'Loading panel segments file "{get_abbrev_path(panel_segments_file)}".')
    with open(panel_segments_file, "r") as f:
        panel_segment_info = json.load(f)

    bw_image = get_bw_image_from_alpha(png_file)

    pil_image = Image.fromarray(cv.merge([bw_image, bw_image, bw_image]))
    assert pil_image.size[0] == panel_segment_info["size"][0]
    assert pil_image.size[1] == panel_segment_info["size"][1]

    img_rects = ImageDraw.Draw(pil_image)
    for box in panel_segment_info["panels"]:
        x0 = box[0]
        y0 = box[1]
        w = box[2]
        h = box[3]
        x1 = x0 + (w - 1)
        y1 = y0 + (h - 1)
        img_rects.rectangle([x0, y0, x1, y1], outline="green", width=10)

    x_min, y_min, x_max, y_max = get_min_max_panel_values(panel_segment_info)
    img_rects.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)

    img_rects._image.save(bounds_img_file)

    return True


if __name__ == "__main__":

    cmd_args = CmdArgs("Show panel bounds for title", CmdArgNames.TITLE | CmdArgNames.WORK_DIR)
    args_ok, error_msg = cmd_args.args_are_valid()
    if not args_ok:
        logging.error(error_msg)
        sys.exit(1)

    setup_logging(cmd_args.get_log_level())

    comics_database = cmd_args.get_comics_database()

    show_panel_bounds(cmd_args.get_title(), cmd_args.get_work_dir())
