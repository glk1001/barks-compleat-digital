import os
import subprocess
import time

import cv2 as cv
import numpy as np
from numba import jit

DEBUG = False
DEBUG_OUTPUT_DIR = "/tmp"
TEMP_DIR = "/tmp"

MEDIAN_BLUR_APERTURE_SIZE = 7
ADAPTIVE_THRESHOLD_BLOCK_SIZE = 21
ADAPTIVE_THRESHOLD_CONST_SUBTRACT = 10


def median_filter_external(original_image, mask_image, kernel_size: int):
    image_file = os.path.join(TEMP_DIR, "src-image.jpg")
    cv.imwrite(image_file, original_image)
    mask_file = os.path.join(TEMP_DIR, "enlarged-black-ink-mask.jpg")
    cv.imwrite(mask_file, mask_image)

    masked_filter_exe = "/home/greg/Prj/github/opencv/test/build/MaskedMedian"
    dest_file = os.path.join(TEMP_DIR, "dest.jpg")
    run_args = [masked_filter_exe, image_file, mask_file, str(kernel_size), dest_file]
    # print(run_args)

    result = subprocess.run(
        run_args,
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise Exception("Could not run masked median filter.")

    return cv.imread(dest_file)


def median_filter(original_image, mask, kernel_size: int):
    filtered_image = np.zeros_like(original_image)
    w = kernel_size // 2

    wrapped_image = cv.copyMakeBorder(
        original_image, w, w, w, w, cv.BORDER_CONSTANT, None, value=(255, 255, 255)
    )
    wrapped_mask = cv.copyMakeBorder(
        mask, w, w, w, w, cv.BORDER_CONSTANT, None, value=(255, 255, 255)
    )

    median_filter_core(wrapped_image, wrapped_mask, kernel_size, filtered_image)

    #    median_filter_core.parallel_diagnostics(level=4)

    return filtered_image


@jit(nopython=True, parallel=False)
def median_filter_core(wrapped_image, wrapped_mask, kernel_size: int, filtered_image):
    image_h, image_w = filtered_image.shape[0], filtered_image.shape[1]
    w: int = kernel_size // 2

    nbrs0 = np.empty((kernel_size * kernel_size, 1), dtype=filtered_image.dtype)
    nbrs1 = np.empty((kernel_size * kernel_size, 1), dtype=filtered_image.dtype)
    nbrs2 = np.empty((kernel_size * kernel_size, 1), dtype=filtered_image.dtype)

    for i in range(w, image_h + w):
        for j in range(w, image_w + w):
            num_nbrs = 0
            for x in range(i - w, i + w + 1):
                for y in range(j - w, j + w + 1):
                    if wrapped_mask[x, y] > 0:
                        assert wrapped_mask[x, y] == 255
                        continue
                    pixel = wrapped_image[x, y]
                    nbrs0[num_nbrs] = pixel[0]
                    nbrs1[num_nbrs] = pixel[1]
                    nbrs2[num_nbrs] = pixel[2]
                    num_nbrs += 1
            filtered_image[i - w, j - w] = get_median(num_nbrs, nbrs0, nbrs1, nbrs2)


@jit(nopython=True, parallel=False)
def get_median(num_nbrs: int, nbrs0, nbrs1, nbrs2):
    if num_nbrs == 0:
        return 0, 0, 0

    if num_nbrs == nbrs0.size:
        return np.median(nbrs0), np.median(nbrs1), np.median(nbrs2)

    return (
        np.median(nbrs0[:num_nbrs]),
        np.median(nbrs1[:num_nbrs]),
        np.median(nbrs2[:num_nbrs]),
    )


def get_larger_mask(mask):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    return cv.dilate(mask, kernel, iterations=1)


def remove_alias_artifacts(input_image):
    gray_image = cv.cvtColor(input_image, cv.COLOR_BGR2GRAY)

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

    filtered_image = median_filter(
        input_image, enlarged_black_ink_mask, MEDIAN_BLUR_APERTURE_SIZE
    )
    # filtered_image = median_filter_external(
    #     input_image, enlarged_black_ink_mask, MEDIAN_BLUR_APERTURE_SIZE
    # )
    if DEBUG:
        cv.imwrite(os.path.join(DEBUG_OUTPUT_DIR, "filtered-image.jpg"), filtered_image)

    output_image = input_image.copy()
    output_image[black_ink_mask == 0] = filtered_image[black_ink_mask == 0]
    output_image[enlarged_black_ink_mask != 0] = input_image[
        enlarged_black_ink_mask != 0
    ]

    return output_image


if __name__ == "__main__":
    start_time = time.time()

    src_image_file = (
        "/home/greg/Books/Carl Barks/The Comics/"
        "Comics and Stories/055 The Terrible Turkey/images/05.jpg"
    )
    # src_image_file = "restore-tests/test-image.jpg"
    # src_image_file = "restore-tests/simple-test-image.jpg"

    src_image = cv.imread(src_image_file)
    print(f"Src image shape: {src_image.shape}")

    improved_image = remove_alias_artifacts(src_image)

    cv.imwrite("/tmp/improved-image.jpg", improved_image)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"Execution time: {elapsed_time} seconds")
