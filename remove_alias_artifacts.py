import os
import time

import cv2 as cv
import numpy as np

DEBUG = True
DEBUG_OUTPUT_DIR = "/tmp"

IN_PAINT_RADIUS = 5
IN_PAINT_CUTOUT_FILL_COLOR = (128, 128, 128)
MEDIAN_BLUR_APERTURE_SIZE = 7
ADAPTIVE_THRESHOLD_BLOCK_SIZE = 21
ADAPTIVE_THRESHOLD_CONST_SUBTRACT = 10


def get_larger_mask(mask):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    return cv.dilate(mask, kernel, iterations=1)


def get_cutout_image(image, mask):
    cutout_image = np.full_like(image, IN_PAINT_CUTOUT_FILL_COLOR)
    cutout_image[mask == 0] = image[mask == 0]
    return cutout_image


def remove_alias_artifacts(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    black_ink_mask = cv.adaptiveThreshold(
        gray_image,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY_INV,
        ADAPTIVE_THRESHOLD_BLOCK_SIZE,
        ADAPTIVE_THRESHOLD_CONST_SUBTRACT,
    )
    if DEBUG:
        cv.imwrite(os.path.join(DEBUG_OUTPUT_DIR, "black-ink-mask.jpg"), black_ink_mask)

    enlarged_black_ink_mask = get_larger_mask(black_ink_mask)
    if DEBUG:
        cv.imwrite(
            os.path.join(DEBUG_OUTPUT_DIR, "enlarged-black-ink-mask.jpg"),
            enlarged_black_ink_mask,
        )

    black_ink_cutout_image = get_cutout_image(image, enlarged_black_ink_mask)
    if DEBUG:
        cv.imwrite(
            os.path.join(DEBUG_OUTPUT_DIR, "black-ink-cutout-image.jpg"),
            black_ink_cutout_image,
        )

    in_painted_image = cv.inpaint(
        black_ink_cutout_image, enlarged_black_ink_mask, IN_PAINT_RADIUS, cv.INPAINT_NS
    )
    if DEBUG:
        cv.imwrite(
            os.path.join(DEBUG_OUTPUT_DIR, "in-painted-image.jpg"), in_painted_image
        )

    blurred_image = cv.medianBlur(in_painted_image, MEDIAN_BLUR_APERTURE_SIZE)
    if DEBUG:
        cv.imwrite(os.path.join(DEBUG_OUTPUT_DIR, "blurred-image.jpg"), blurred_image)

    out_image = image.copy()
    out_image[black_ink_mask == 0] = blurred_image[black_ink_mask == 0]
    out_image[enlarged_black_ink_mask != 0] = image[enlarged_black_ink_mask != 0]

    return out_image


start_time = time.time()

image_file = (
    "/home/greg/Books/Carl Barks/The Comics/"
    "Comics and Stories/055 The Terrible Turkey/images/05.jpg"
)
# image_file = "restore-tests/test-image.jpg"
# image_file = "restore-tests/simple-test-image.jpg"

input_image = cv.imread(image_file)
height, width, num_channels = input_image.shape
print(f"width: {width}, height: {height}, channels: {num_channels}")

improved_image = remove_alias_artifacts(input_image)

cv.imwrite("/tmp/improved-image.jpg", improved_image)

end_time = time.time()
elapsed_time = round(end_time - start_time)
print(f"Execution time: {elapsed_time} seconds")
