from dataclasses import dataclass
from typing import List

from barks_fantagraphics.comics_consts import PageType
from barks_fantagraphics.panel_bounding_boxes import BoundingBox


@dataclass
class OriginalPage:
    page_filenames: str
    page_type: PageType


class CleanPage:
    def __init__(
        self,
        page_filename: str,
        page_type: PageType,
        page_num: int = -1,
    ):
        self.page_filename = page_filename
        self.page_type = page_type
        self.page_num: int = page_num
        self.panels_bbox: BoundingBox = BoundingBox()


@dataclass
class SrceAndDestPages:
    srce_pages: List[CleanPage]
    dest_pages: List[CleanPage]


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


@dataclass
class ComicDimensions:
    min_panels_bbox_width: int = -1
    max_panels_bbox_width: int = -1
    min_panels_bbox_height: int = -1
    max_panels_bbox_height: int = -1
    av_panels_bbox_width: int = -1
    av_panels_bbox_height: int = -1
