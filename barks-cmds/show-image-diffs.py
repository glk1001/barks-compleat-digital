import logging
import os.path
import sys
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import structural_similarity

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_utils import setup_logging

image1_file = sys.argv[1]
image2_file = sys.argv[2]


def get_image_diffs(diff_thresh: float, image1_file: str, image2_file: str):
    image1 = cv2.imread(image1_file)
    image2 = cv2.imread(image2_file)

    # Convert images to grayscale.
    image1_grey = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_grey = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images.
    (score, diffs) = structural_similarity(image1_grey, image2_grey, full=True)

    # The diff image contains the actual image differences between the two images and
    # is represented as a floating point data type in the range [0,1]. So we must
    # convert the array to 8-bit unsigned integers in the range [0,255] before we
    # can use it with OpenCV.
    diffs = np.where(diffs < diff_thresh, diffs, 1.0)
    diffs = (diffs * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to obtain the
    # regions of the two input images that differ.
    thresh = cv2.threshold(diffs, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(image1.shape, dtype="uint8")
    image2_filled = image2.copy()

    num_diff_areas = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            num_diff_areas += 1
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image1, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(image2, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(image2_filled, [c], 0, (0, 255, 0), -1)

    return score, num_diff_areas, image1, image2


def show_diffs_for_title(title: str, out_dir: str) -> None:
    out_dir = os.path.join(out_dir, title)

    logging.info(f'Checking fixes for for "{title}"...')

    comic = comics_database.get_comic_book(title)

    orig_files = comic.get_original_srce_story_files(RESTORABLE_PAGE_TYPES)
    fixes_files = comic.get_srce_with_fixes_story_files(RESTORABLE_PAGE_TYPES)

    diff_threshold = 0.9

    made_out_dir = False
    for orig_file, fixes_file in zip(orig_files, fixes_files):
        modified = fixes_file[1]
        if not modified:
            continue

        ssim, num_diffs, image1_with_diffs, image2_with_diffs = get_image_diffs(
            diff_threshold, orig_file, fixes_file[0]
        )

        page = Path(orig_file).stem

        print(f'"{title}-{page}": image similarity = {ssim:.6f}, num diffs = {num_diffs}.')

        if num_diffs == 0:
            continue

        if not made_out_dir:
            os.makedirs(out_dir, exist_ok=True)
            made_out_dir = True

        diff1_file = os.path.join(out_dir, page + "-orig.png")
        diff2_file = os.path.join(out_dir, page + "-fix.png")
        cv2.imwrite(diff1_file, image1_with_diffs)
        cv2.imwrite(diff2_file, image2_with_diffs)
        # cv2.imwrite(os.path.join(out_dir, "diffs.png"), diffs)
        # cv2.imwrite(os.path.join(out_dir, "mask.png"), mask)
        # cv2.imwrite(os.path.join(out_dir, "image2-with-filled-diffs.png"), image2_filled)


cmd_args = CmdArgs("Fantagraphics info", CmdArgNames.VOLUME | CmdArgNames.TITLE)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

out_dir = "/tmp/fixes-diffs"

for title in cmd_args.get_titles():
    show_diffs_for_title(title, out_dir)
