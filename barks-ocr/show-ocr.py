import json
import logging
import os.path
import sys
from pathlib import Path
from typing import List, Dict

import cv2 as cv
from PIL import Image, ImageDraw, ImageFont

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_image_io import get_bw_image_from_alpha
from barks_fantagraphics.comics_info import PNG_FILE_EXT
from barks_fantagraphics.comics_utils import get_abbrev_path, get_ocr_no_json_suffix, setup_logging
from utils.ocr_box import OcrBox

COLORS = [
    "green",
    "yellow",
    "blue",
    "red",
    "brown",
    "purple",
    "orange",
    "pink",
    "teal",
    "orchid",
    "blueviolet",
    "tan",
    "olive",
    "palegreen",
    "plum",
    "wheat",
    "gold",
    "hotpink",
]


def get_color(group_id: int) -> str:
    group_id %= len(COLORS)
    return COLORS[group_id]


def ocr_annotate_titles(titles: List[str], out_dir: str) -> None:
    for title in titles:
        ocr_annotate_title(title, out_dir)


def ocr_annotate_title(title: str, out_dir: str) -> None:
    out_dir = os.path.join(out_dir, title)

    logging.info(f'OCR annotating all pages in "{title}" to directory "{out_dir}"...')

    os.makedirs(out_dir, exist_ok=True)
    comic = comics_database.get_comic_book(title)
    svg_files = comic.get_srce_restored_svg_story_files(RESTORABLE_PAGE_TYPES)
    ocr_files = comic.get_srce_restored_ocr_story_files(RESTORABLE_PAGE_TYPES)

    for svg_file, ocr_file in zip(svg_files, ocr_files):
        svg_stem = Path(svg_file).stem
        png_file = svg_file + PNG_FILE_EXT

        for ocr_type_file in ocr_file:
            ocr_suffix = get_ocr_no_json_suffix(ocr_type_file)

            ocr_group_file = get_ocr_group_filename(svg_stem, ocr_suffix, out_dir)
            final_text_annotated_image_file = get_final_text_annotated_filename(
                svg_stem, ocr_suffix, out_dir
            )
            boxes_annotated_image_file = get_boxes_annotated_filename(svg_stem, ocr_suffix, out_dir)

            ocr_annotate_image_with_final_text(
                png_file, ocr_group_file, final_text_annotated_image_file
            )
            ocr_annotate_image_with_individual_boxes(
                png_file, ocr_group_file, boxes_annotated_image_file
            )


def get_final_text_annotated_filename(svg_stem: str, ocr_suffix, out_dir: str) -> str:
    return os.path.join(out_dir, svg_stem + f"-ocr-gemini-final-text-annotated{ocr_suffix}.png")
    # return os.path.join(out_dir, svg_stem + f"-ocr-calculated-annotated{ocr_suffix}.png")


def get_boxes_annotated_filename(svg_stem: str, ocr_suffix, out_dir: str) -> str:
    return os.path.join(out_dir, svg_stem + f"-ocr-gemini-boxes-annotated{ocr_suffix}.png")
    # return os.path.join(out_dir, svg_stem + f"-ocr-calculated-annotated{ocr_suffix}.png")


def get_ocr_group_filename(svg_stem: str, ocr_suffix, out_dir: str) -> str:
    # return os.path.join(out_dir, svg_stem + f"-gemini-groups{ocr_suffix}.json")
    return os.path.join(out_dir, svg_stem + f"-gemini-final-groups{ocr_suffix}.json")
    # return os.path.join(out_dir, svg_stem + f"-calculated-groups{ocr_suffix}.json")


def get_image_to_annotate(png_file: str) -> Image:
    if not os.path.isfile(png_file):
        raise Exception(f'Could not find image file "{png_file}".')

    return get_bw_image_from_alpha(png_file)


def get_json_text_data_boxes(ocr_file: str) -> Dict[str, any]:
    if not os.path.isfile(ocr_file):
        raise Exception(f'Could not find ocr file "{ocr_file}".')

    with open(ocr_file, "r") as f:
        json_text_data_boxes = json.load(f)

    return json_text_data_boxes


def ocr_annotate_image_with_final_text(
    png_file: str,
    ocr_file: str,
    annotated_img_file: str,
) -> None:
    if os.path.isfile(annotated_img_file):
        logging.info(f'Found annotation file - skipping: "{annotated_img_file}".')
        return

    logging.info(f'OCR annotating image with final text: "{get_abbrev_path(png_file)}"...')

    json_text_data_boxes = get_json_text_data_boxes(ocr_file)
    bw_image = get_image_to_annotate(png_file)

    pil_image = Image.fromarray(cv.merge([bw_image, bw_image, bw_image]))
    img_rects_draw = ImageDraw.Draw(pil_image)
    font_file = "/home/greg/Prj/fonts/verdana.ttf"
    font_size = 25
    font = ImageFont.truetype(font_file, font_size)

    for group in json_text_data_boxes:
        group_id = int(group)

        text_data = json_text_data_boxes[group]
        ocr_box = OcrBox(
            text_data["text_box"],
            text_data["ocr_text"],
            1.0,
            text_data["ai_text"],
        )
        print(f'group: {group_id:02} - text: "{text_data["ai_text"]}",'
              f' box: {text_data["text_box"]}, approx: {ocr_box.is_approx_rect}, rect: {ocr_box.min_rotated_rectangle}')
        img_rects_draw.rectangle(
            ocr_box.min_rotated_rectangle, outline=get_color(group_id), width=7, fill="white"
        )

        text = text_data["ai_text"]
        top_left = ocr_box.min_rotated_rectangle[0]
        top_left = (top_left[0] + 5, top_left[1] + 5)
        img_rects_draw.text(top_left, text, fill="green", font=font, align="left")

    img_rects_draw._image.save(annotated_img_file)


def ocr_annotate_image_with_individual_boxes(
    png_file: str,
    ocr_file: str,
    annotated_img_file: str,
) -> None:
    if os.path.isfile(annotated_img_file):
        logging.info(f'Found annotation file - skipping: "{annotated_img_file}".')
        return

    logging.info(f'OCR annotating image with individual boxes: "{get_abbrev_path(png_file)}"...')

    json_text_data_boxes = get_json_text_data_boxes(ocr_file)
    bw_image = get_image_to_annotate(png_file)

    pil_image = Image.fromarray(cv.merge([bw_image, bw_image, bw_image]))
    img_rects_draw = ImageDraw.Draw(pil_image)

    for group in json_text_data_boxes:
        group_id = int(group)

        for box_id in json_text_data_boxes[group]["cleaned_box_texts"]:
            text_data = json_text_data_boxes[group]["cleaned_box_texts"][box_id]
            ocr_box = OcrBox(
                text_data["text_box"],
                text_data["text_frag"],
                0.0,
                "N/A",
            )

            if ocr_box.is_approx_rect:
                img_rects_draw.rectangle(
                    ocr_box.min_rotated_rectangle, outline=get_color(group_id), width=4
                )
            else:
                box = [item for point in ocr_box.min_rotated_rectangle for item in point]
                img_rects_draw.polygon(box, outline=get_color(group_id), width=2)

    img_rects_draw._image.save(annotated_img_file)


if __name__ == "__main__":
    setup_logging(logging.INFO)

    cmd_args = CmdArgs(
        "OCR annotate titles", CmdArgNames.VOLUME | CmdArgNames.TITLE | CmdArgNames.WORK_DIR
    )
    args_ok, error_msg = cmd_args.args_are_valid()
    if not args_ok:
        logging.error(error_msg)
        sys.exit(1)

    comics_database = cmd_args.get_comics_database()

    ocr_annotate_titles(cmd_args.get_titles(), cmd_args.get_work_dir())
