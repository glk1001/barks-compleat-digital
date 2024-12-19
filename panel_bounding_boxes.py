import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

from PIL import Image, ImageDraw

from barks_fantagraphics.comics_info import JPG_FILE_EXT, PNG_FILE_EXT
from barks_fantagraphics.comics_utils import get_relpath
from barks_fantagraphics.panel_segmentation import KumikoPanelSegmentation, get_min_max_panel_values
from consts import DRY_RUN_STR
from image_io import open_image_for_reading

PANEL_BOUNDS_WORK_FILE_SUFFIX = "_panel_bounds.txt"


@dataclass
class BoundingBox:
    x_min: int = -1
    y_min: int = -1
    x_max: int = -1
    y_max: int = -1

    def get_box(self) -> Tuple[int, int, int, int]:
        return self.x_min, self.y_min, self.x_max, self.y_max

    def get_width(self) -> int:
        return (self.x_max - self.x_min) + 1

    def get_height(self) -> int:
        return (self.y_max - self.y_min) + 1


class BoundingBoxProcessor(object):
    def __init__(self, work_dir: str):
        self.__work_dir = work_dir
        self.__kumiko = KumikoPanelSegmentation(work_dir)

    @staticmethod
    def get_panels_bounding_box_from_file(filename: str) -> BoundingBox:
        with open(filename, "r") as f:
            segment_info = json.load(f)

        x_min, y_min, x_max, y_max = get_min_max_panel_values(segment_info)

        logging.debug(
            f'Using panels segment info file "{get_relpath(filename)}".'
            f"Box: {x_min}, {y_min}, {x_max}, {y_max}."
        )

        return BoundingBox(x_min, y_min, x_max, y_max)

    def get_panels_segment_info_from_kumiko(
        self,
        dry_run: bool,
        srce_page_image: Image,
        srce_filename: str,
        srce_bounded_override_dir: str,
    ) -> Tuple[BoundingBox, Dict[str, Any]]:
        logging.debug("Getting panels segment info from kumiko.")

        bad_override_filename = Path(srce_filename).stem + PNG_FILE_EXT
        bad_override_file = os.path.join(srce_bounded_override_dir, bad_override_filename)
        if os.path.isfile(bad_override_file):
            raise Exception(
                f'Override panels bounds files should not be .png: "{bad_override_file}".'
            )

        override_filename = Path(srce_filename).stem + JPG_FILE_EXT
        override_file_with_bbox = os.path.join(srce_bounded_override_dir, override_filename)

        if not os.path.isfile(override_file_with_bbox):
            srce_bounded_image = srce_page_image
        else:
            logging.warning(f'Using panels bounds override file "{override_file_with_bbox}".')
            srce_bounded_image = Image.open(override_file_with_bbox, "r")

        srce_bounded_image = srce_bounded_image.convert("RGB")

        segment_info = self.__kumiko.get_panels_segment_info(srce_bounded_image, srce_filename)
        x_min, y_min, x_max, y_max = get_min_max_panel_values(segment_info)

        if dry_run:
            logging.info(
                f"{DRY_RUN_STR}: Saving panels bounding box info to work dir"
                f' "{self.__work_dir}".'
            )
        else:
            self.__dump_panels_bounding_box(srce_filename, x_min, y_min, x_max, y_max)

        return BoundingBox(x_min, y_min, x_max, y_max), segment_info

    @staticmethod
    def save_panels_segment_info(segment_info_filename, segment_info: Dict[str, Any]):
        logging.debug(f'Saving panel segment info to "{get_relpath(segment_info_filename)}".')

        segment_info_filtered = {k: v for k, v in segment_info.items() if k != "processing_time"}
        with open(segment_info_filename, "w") as f:
            json.dump(segment_info_filtered, f, indent=4)

    def __dump_panels_bounding_box(
        self, page_filename: str, x_min: int, y_min: int, x_max: int, y_max: int
    ):
        bounds_filename = os.path.join(
            self.__work_dir,
            os.path.splitext(os.path.basename(page_filename))[0] + PANEL_BOUNDS_WORK_FILE_SUFFIX,
        )
        logging.debug(f'Saving panel bounds to work file "{bounds_filename}".')
        with open(bounds_filename, "w") as f:
            f.write(f"{x_min}, {y_min}, {x_max}, {y_max}\n")

        # Draw the panel bounds on page image.
        page_image = open_image_for_reading(page_filename)
        draw = ImageDraw.Draw(page_image)
        draw.line([(x_min, y_min), (x_max, y_min)], width=3, fill=(256, 0, 0))
        draw.line([(x_max, y_min), (x_max, y_max)], width=3, fill=(256, 0, 0))
        draw.line([(x_max, y_max), (x_min, y_max)], width=3, fill=(256, 0, 0))
        draw.line([(x_min, y_max), (x_min, y_min)], width=3, fill=(256, 0, 0))

        marked_image_filename = os.path.join(
            self.__work_dir,
            os.path.splitext(os.path.basename(page_filename))[0] + "-panel-bounds-marked.jpg",
        )
        logging.debug(f'Saving panel bounds image to work file "{marked_image_filename}".')
        page_image = page_image.convert("RGB")
        page_image.save(marked_image_filename, optimize=True, compress_level=5)
