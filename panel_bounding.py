import logging
import os
from typing import List, Tuple

from PIL import Image

from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.consts import (
    PAGES_WITHOUT_PANELS,
    PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN,
    BIG_NUM,
    DRY_RUN_STR,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
)
from image_io import open_image_for_reading
from pages import CleanPage, SrceAndDestPages
from panel_bounding_boxes import BoundingBox, BoundingBoxProcessor

bounding_box_processor: BoundingBoxProcessor


def init_bounding_box_processor(work_dir: str) -> None:
    global bounding_box_processor
    bounding_box_processor = BoundingBoxProcessor(work_dir)


def get_required_panels_bbox_width_height(
    srce_pages: List[CleanPage],
) -> Tuple[int, int, int, int, int, int, int, int]:
    (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    ) = get_min_max_panels_bbox_width_height(srce_pages)

    av_panels_bbox_width, av_panels_bbox_height = get_average_panels_bbox_width_height(
        max_panels_bbox_height, srce_pages
    )
    assert av_panels_bbox_width > 0
    assert av_panels_bbox_height > 0

    required_panels_bbox_width = DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN)
    required_panels_bbox_height = get_scaled_panels_bbox_height(
        required_panels_bbox_width, av_panels_bbox_width, av_panels_bbox_height
    )

    return (
        required_panels_bbox_width,
        required_panels_bbox_height,
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
        av_panels_bbox_width,
        av_panels_bbox_height,
    )


def get_scaled_panels_bbox_height(
    scaled_panels_bbox_width: int, panels_bbox_width, panels_bbox_height: int
) -> int:
    return int(round((panels_bbox_height * scaled_panels_bbox_width) / panels_bbox_width))


def get_average_panels_bbox_width_height(
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


def get_min_max_panels_bbox_width_height(
    srce_pages: List[CleanPage],
) -> Tuple[int, int, int, int]:
    min_panels_bbox_width = BIG_NUM
    max_panels_bbox_width = 0
    min_panels_bbox_height = BIG_NUM
    max_panels_bbox_height = 0
    for srce_page in srce_pages:
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            continue

        panels_bbox_width = srce_page.panels_bbox.get_width()
        panels_bbox_height = srce_page.panels_bbox.get_height()
        if min_panels_bbox_width > panels_bbox_width:
            min_panels_bbox_width = panels_bbox_width
        if min_panels_bbox_height > panels_bbox_height:
            min_panels_bbox_height = panels_bbox_height
        if max_panels_bbox_width < panels_bbox_width:
            max_panels_bbox_width = panels_bbox_width
        if max_panels_bbox_height < panels_bbox_height:
            max_panels_bbox_height = panels_bbox_height

    return (
        min_panels_bbox_width,
        max_panels_bbox_width,
        min_panels_bbox_height,
        max_panels_bbox_height,
    )


def set_srce_panel_bounding_boxes(
    dry_run: bool,
    use_cached_bboxes: bool,
    comic: ComicBook,
    srce_pages: List[CleanPage],
):
    logging.debug("Setting srce panel bounding boxes.")

    for srce_page in srce_pages:
        srce_page_image = open_image_for_reading(srce_page.page_filename)
        if srce_page.page_type in PAGES_WITHOUT_PANELS:
            srce_page.panels_bbox = BoundingBox(
                0, 0, srce_page_image.width - 1, srce_page_image.height - 1
            )
        else:
            srce_page_image = srce_page_image.convert("RGB")
            srce_page.panels_bbox = get_panels_bounding_box(
                dry_run, use_cached_bboxes, comic, srce_page_image, srce_page
            )

    logging.debug("")


def get_panels_bounding_box(
    dry_run: bool,
    use_cached_bboxes: bool,
    comic: ComicBook,
    srce_page_image: Image,
    srce_page: CleanPage,
) -> BoundingBox:
    assert srce_page.page_type not in PAGES_WITHOUT_PANELS

    srce_page_bounding_box_filename = str(
        os.path.join(
            comic.panel_segments_dir,
            os.path.splitext(os.path.basename(srce_page.page_filename))[0] + "_panel_bounds.txt",
        )
    )

    if not use_cached_bboxes and os.path.isfile(srce_page_bounding_box_filename):
        if dry_run:
            logging.info(
                f"{DRY_RUN_STR}: "
                f'Caching off - deleting panel bbox file "{srce_page_bounding_box_filename}".'
            )
        else:
            logging.debug(
                f'Caching off - deleting panel bbox file "{srce_page_bounding_box_filename}".'
            )
            os.remove(srce_page_bounding_box_filename)
            assert not os.path.isfile(srce_page_bounding_box_filename)

    if os.path.isfile(srce_page_bounding_box_filename):
        return bounding_box_processor.get_panels_bounding_box_from_file(
            srce_page_bounding_box_filename
        )

    logging.info(
        f"Getting Kumiko panel segment info for srce file"
        f' "{os.path.basename(srce_page.page_filename)}".'
    )

    if not os.path.isdir(comic.panel_segments_dir):
        if dry_run:
            logging.info(
                f'{DRY_RUN_STR}: Making panel segments directory "{comic.panel_segments_dir}".'
            )
        else:
            os.makedirs(comic.panel_segments_dir, exist_ok=True)

    srce_bounded_dir = os.path.join(comic.get_srce_fixes_image_dir(), "bounded")

    bounding_box = bounding_box_processor.get_panels_bounding_box_from_kumiko(
        dry_run,
        comic.panel_segments_dir,
        srce_page_image,
        srce_page.page_filename,
        srce_bounded_dir,
    )

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Saving panel bounding box to "{srce_page_bounding_box_filename}".'
        )
    else:
        bounding_box_processor.save_panels_bounding_box(
            srce_page_bounding_box_filename, bounding_box
        )

    return bounding_box


def set_dest_panel_bounding_boxes(
    comic: ComicBook,
    pages: SrceAndDestPages,
):
    logging.debug("Setting dest panel bounding boxes.")

    for srce_page, dest_page in zip(pages.srce_pages, pages.dest_pages):
        dest_page.panels_bbox = get_dest_panel_bounding_box(comic, srce_page)

    logging.debug("")


def get_dest_panel_bounding_box(comic: ComicBook, srce_page: CleanPage) -> BoundingBox:
    if srce_page.page_type in PAGES_WITHOUT_PANELS:
        return BoundingBox(0, 0, DEST_TARGET_WIDTH - 1, DEST_TARGET_HEIGHT - 1)

    required_panels_width = int(DEST_TARGET_WIDTH - (2 * DEST_TARGET_X_MARGIN))
    srce_panels_bbox_width = srce_page.panels_bbox.get_width()
    srce_panels_bbox_height = srce_page.panels_bbox.get_height()

    if srce_panels_bbox_height >= (
        comic.srce_av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN
    ):
        required_panels_height = comic.required_dim.panels_bbox_height
    else:
        required_panels_height = get_scaled_panels_bbox_height(
            required_panels_width, srce_panels_bbox_width, srce_panels_bbox_height
        )
        logging.warning(
            f'For "{os.path.basename(srce_page.page_filename)}",'
            f" panels bbox height {srce_panels_bbox_height}"
            f" < {comic.srce_av_panels_bbox_height - PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN}"
            f" (average height {comic.srce_av_panels_bbox_height}"
            f" - error {PANELS_BBOX_HEIGHT_SIMILARITY_MARGIN})."
            f" So setting required bbox height to {required_panels_height},"
            f" not {comic.required_dim.panels_bbox_height}."
        )

    # Centre the dest panels image on an empty page.
    dest_panels_x_min = DEST_TARGET_X_MARGIN
    dest_panels_y_min = int(0.5 * (DEST_TARGET_HEIGHT - required_panels_height))
    dest_panels_x_max = dest_panels_x_min + (required_panels_width - 1)
    dest_panels_y_max = dest_panels_y_min + (required_panels_height - 1)

    return BoundingBox(dest_panels_x_min, dest_panels_y_min, dest_panels_x_max, dest_panels_y_max)
