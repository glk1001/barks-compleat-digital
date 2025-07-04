import logging
import os
from typing import List, Tuple

from .comics_consts import (
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
    PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN,
    PAGES_WITHOUT_PANELS,
)
from .comics_utils import dest_file_is_older_than_srce
from .page_classes import CleanPage, SrceAndDestPages, ComicDimensions, RequiredDimensions
from .panel_bounding_boxes import BoundingBox, get_panels_bounding_box_from_file


def get_required_panels_bbox_width_height(
    srce_pages: List[CleanPage],
    required_page_height: int,
    required_page_number_height: int,
) -> Tuple[ComicDimensions, RequiredDimensions]:
    (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    ) = _get_min_max_panels_bbox_width_height(srce_pages)

    av_panels_bbox_width, av_panels_bbox_height = _get_average_panels_bbox_width_height(
        max_panels_bbox_height, srce_pages
    )
    assert av_panels_bbox_width > 0
    assert av_panels_bbox_height > 0

    required_panels_bbox_width = DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN)
    required_panels_bbox_height = get_scaled_panels_bbox_height(
        required_panels_bbox_width, av_panels_bbox_width, av_panels_bbox_height
    )
    page_num_y_centre = int(
        round(0.5 * (0.5 * (required_page_height - required_panels_bbox_height)))
    )
    required_page_num_y_bottom = int(page_num_y_centre - (required_page_number_height / 2))

    return (
        ComicDimensions(
            min_panels_bbox_width,
            max_panels_bbox_width,
            min_panels_bbox_height,
            max_panels_bbox_height,
            av_panels_bbox_width,
            av_panels_bbox_height,
        ),
        RequiredDimensions(
            required_panels_bbox_width, required_panels_bbox_height, required_page_num_y_bottom
        ),
    )


def get_scaled_panels_bbox_height(
    scaled_panels_bbox_width: int, panels_bbox_width, panels_bbox_height: int
) -> int:
    return int(round((panels_bbox_height * scaled_panels_bbox_width) / panels_bbox_width))


def _get_average_panels_bbox_width_height(
    max_panels_bbox_height: int, srce_pages: List[CleanPage]
) -> Tuple[int, int]:
    sum_panels_bbox_width = 0
    sum_panels_bbox_height = 0
    num_pages = 0
    for srce_page in srce_pages:
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue

        panels_height = srce_page.panels_bbox.get_height()
        if panels_height < (max_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN):
            continue

        panels_width = srce_page.panels_bbox.get_width()

        sum_panels_bbox_width += panels_width
        sum_panels_bbox_height += panels_height
        num_pages += 1

    assert num_pages > 0
    return int(round(float(sum_panels_bbox_width) / float(num_pages))), int(
        round(float(sum_panels_bbox_height) / float(num_pages))
    )


def _get_min_max_panels_bbox_width_height(
    srce_pages: List[CleanPage],
) -> Tuple[int, int, int, int]:
    big_num = 10000

    min_panels_bbox_width = big_num
    min_panels_bbox_height = big_num
    max_panels_bbox_width = 0
    max_panels_bbox_height = 0

    for srce_page in srce_pages:
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue

        panels_bbox_width = srce_page.panels_bbox.get_width()
        panels_bbox_height = srce_page.panels_bbox.get_height()

        min_panels_bbox_width = min(min_panels_bbox_width, panels_bbox_width)
        min_panels_bbox_height = min(min_panels_bbox_height, panels_bbox_height)
        max_panels_bbox_width = max(max_panels_bbox_width, panels_bbox_width)
        max_panels_bbox_height = max(max_panels_bbox_height, panels_bbox_height)

    return (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    )


def set_srce_panel_bounding_boxes(
    srce_pages: List[CleanPage],
    srce_panels_segment_info_files: List[str],
    check_srce_page_timestamps: bool,
):
    logging.debug("Setting srce panel bounding boxes.")

    for srce_page, srce_panels_segment_info_file in zip(srce_pages, srce_panels_segment_info_files):
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue
        if not os.path.isfile(srce_panels_segment_info_file):
            raise Exception(
                f'Could not find panels segments info file "{srce_panels_segment_info_file}".'
            )
        if check_srce_page_timestamps and dest_file_is_older_than_srce(
            srce_page.page_filename, srce_panels_segment_info_file
        ):
            raise Exception(
                f'Panels segments info file "{srce_panels_segment_info_file}"'
                f' is older than srce image file "{srce_page.page_filename}".'
            )
        srce_page.panels_bbox = get_panels_bounding_box_from_file(srce_panels_segment_info_file)

    logging.debug("")


def set_dest_panel_bounding_boxes(
    srce_dim: ComicDimensions, required_dim: RequiredDimensions, pages: SrceAndDestPages
):
    logging.debug("Setting dest panel bounding boxes.")

    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        dest_page.panels_bbox = _get_dest_panels_bounding_box(srce_dim, required_dim, srce_page)

    logging.debug("")


def _get_dest_panels_bounding_box(
    srce_dim: ComicDimensions, required_dim: RequiredDimensions, srce_page: CleanPage
) -> BoundingBox:
    if srce_page.page_type in PAGES_WITHOUT_PANELS:
        return BoundingBox(0, 0, DEST_TARGET_WIDTH - 1, DEST_TARGET_HEIGHT - 1)

    assert srce_dim.min_panels_bbox_width != -1
    assert required_dim.panels_bbox_width != -1

    required_panels_width = int(DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN))
    srce_panels_bbox_width = srce_page.panels_bbox.get_width()
    srce_panels_bbox_height = srce_page.panels_bbox.get_height()

    assert srce_dim.av_panels_bbox_height > 0

    if srce_panels_bbox_height >= (
        srce_dim.av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    ):
        required_panels_height = required_dim.panels_bbox_height
    else:
        required_panels_height = get_scaled_panels_bbox_height(
            required_panels_width, srce_panels_bbox_width, srce_panels_bbox_height
        )
        logging.warning(
            f'For "{os.path.basename(srce_page.page_filename)}",'
            f" panels bbox height {srce_panels_bbox_height}"
            f" < {srce_dim.av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN}"
            f" (= average height:{srce_dim.av_panels_bbox_height}"
            f" - error:{PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN})."
            f" So setting required bbox height to {required_panels_height},"
            f" not {required_dim.panels_bbox_height}."
        )

    # Centre the dest panels image on an empty page.
    dest_panels_x_min = DEST_TARGET_X_MARGIN
    dest_panels_y_min = int(0.5 * (DEST_TARGET_HEIGHT - required_panels_height))
    dest_panels_x_max = dest_panels_x_min + (required_panels_width - 1)
    dest_panels_y_max = dest_panels_y_min + (required_panels_height - 1)

    return BoundingBox(dest_panels_x_min, dest_panels_y_min, dest_panels_x_max, dest_panels_y_max)
