import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from .comics_consts import JPG_FILE_EXT, PNG_FILE_EXT
from .comics_image_io import open_pil_image_for_reading
from .comics_utils import get_abbrev_path
from .panel_segmentation import KumikoPanelSegmentation, get_min_max_panel_values


class BoundingBoxProcessor(object):
    def __init__(self, work_dir: str, no_panel_expansion: bool = False):
        self.__kumiko = KumikoPanelSegmentation(work_dir, no_panel_expansion)

    def get_panels_segment_info_from_kumiko(
        self,
        srce_file: str,
        srce_bounded_override_dir: str,
    ) -> Dict[str, Any]:
        logging.debug("Getting panels segment info from kumiko.")

        override_file_with_bbox = self._get_override_filename(srce_bounded_override_dir, srce_file)

        if not os.path.isfile(override_file_with_bbox):
            srce_bounded_image = open_pil_image_for_reading(srce_file)
        else:
            logging.warning(
                f'Using panels bounds override file "{get_abbrev_path(override_file_with_bbox)}".'
            )
            srce_bounded_image = open_pil_image_for_reading(override_file_with_bbox)

        srce_bounded_image = srce_bounded_image.convert("RGB")

        segment_info = self.__kumiko.get_panels_segment_info(srce_bounded_image, srce_file)

        segment_info["overall_bounds"] = get_min_max_panel_values(segment_info)

        return segment_info

    @staticmethod
    def _get_override_filename(srce_bounded_override_dir: str, srce_filename: str) -> str:
        bad_override_filename = Path(srce_filename).stem + PNG_FILE_EXT
        bad_override_file = os.path.join(srce_bounded_override_dir, bad_override_filename)
        if os.path.isfile(bad_override_file):
            raise Exception(
                f'Override panels bounds files should not be .png: "{bad_override_file}".'
            )

        override_filename = Path(srce_filename).stem + JPG_FILE_EXT
        return os.path.join(srce_bounded_override_dir, override_filename)

    @staticmethod
    def save_panels_segment_info(segment_info_filename, segment_info: Dict[str, Any]):
        logging.debug(f'Saving panel segment info to "{get_abbrev_path(segment_info_filename)}".')

        segment_info_filtered = {k: v for k, v in segment_info.items() if k != "processing_time"}
        with open(segment_info_filename, "w") as f:
            json.dump(segment_info_filtered, f, indent=4)
