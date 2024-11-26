import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from PIL import Image, ImageDraw

from consts import DRY_RUN_STR, PANEL_BOUNDS_FILENAME_SUFFIX
from panel_segmentation import KumikoPanelSegmentation


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

    def get_panels_bounding_box_from_file(self, filename: str) -> BoundingBox:
        with open(filename, "r") as f:
            line = f.readline()
            vals = line.split(", ")
            x_min = int(vals[0])
            y_min = int(vals[1])
            x_max = int(vals[2])
            y_max = int(vals[3])

            logging.debug(
                f'Got panel bounding box file "PANEL_SEGMENTS_DIR: {os.path.basename(filename)}".'
                f"Box: {x_min}, {y_min}, {x_max}, {y_max}."
            )

            return BoundingBox(x_min, y_min, x_max, y_max)

    def save_panels_bounding_box(self, filename: str, bounding_box: BoundingBox):
        logging.debug(f'Saving panel bounding box to file "{filename}".')

        with open(filename, "w") as f:
            f.write(
                f"{bounding_box.x_min}, {bounding_box.y_min}, "
                f"{bounding_box.x_max}, {bounding_box.y_max}\n"
            )

    def get_panels_bounding_box_from_kumiko(
        self,
        dry_run: bool,
        panel_segments_dir: str,
        srce_page_image: Image,
        srce_filename: str,
        srce_bounded_dir: str,
    ) -> BoundingBox:
        logging.debug("Getting panel bounding box from kumiko.")

        file_basename = os.path.basename(srce_filename)
        file_with_bbox = os.path.join(srce_bounded_dir, file_basename)

        if not os.path.isfile(file_with_bbox):
            (
                x_min,
                y_min,
                x_max,
                y_max,
            ), segment_info = self.__kumiko.get_panel_bounding_box(srce_page_image, srce_filename)
        else:
            logging.warning(f'Using bounded srce file "{file_with_bbox}".')
            srce_bounded_image = Image.open(file_with_bbox, "r")
            (
                x_min,
                y_min,
                x_max,
                y_max,
            ), segment_info = self.__kumiko.get_panel_bounding_box(
                srce_bounded_image, srce_filename
            )

        self.__save_segment_info(self.__work_dir, srce_filename, segment_info)
        if dry_run:
            logging.info(f'{DRY_RUN_STR}: Saving panel segment info to "{panel_segments_dir}".')
        else:
            self.__save_segment_info(panel_segments_dir, srce_filename, segment_info)

        self.__dump_panels_bounding_box(srce_filename, x_min, y_min, x_max, y_max)

        return BoundingBox(x_min, y_min, x_max, y_max)

    def __save_segment_info(
        self, output_dir: str, page_filename: str, segment_info: Dict[str, Any]
    ):
        segment_info_filename = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(page_filename))[0] + "-panel-segments.json",
        )

        if output_dir == self.__work_dir:
            logging.debug(f'Saving panel segment info to work file "{segment_info_filename}".')
        else:
            logging.debug(f'Saving panel segment info to "{segment_info_filename}".')

        segment_info_filtered = {k: v for k, v in segment_info.items() if k != "processing_time"}
        with open(segment_info_filename, "w") as f:
            f.write(f"{segment_info_filtered}\n")

    def __dump_panels_bounding_box(
        self, page_filename: str, x_min: int, y_min: int, x_max: int, y_max: int
    ):
        bounds_filename = os.path.join(
            self.__work_dir,
            os.path.splitext(os.path.basename(page_filename))[0] + PANEL_BOUNDS_FILENAME_SUFFIX,
        )
        logging.debug(f'Saving panel bounds to work file "{bounds_filename}".')
        with open(bounds_filename, "w") as f:
            f.write(f"{x_min}, {y_min}, {x_max}, {y_max}\n")

        # Draw the panel bounds on page image.
        page_image = Image.open(page_filename, "r")
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
        page_image.save(marked_image_filename, optimize=True, compress_level=5)
