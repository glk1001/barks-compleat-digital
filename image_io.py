import logging

from PIL import Image

from consts import DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT
from pages import EMPTY_IMAGE_FILES


def open_image_for_reading(filename: str) -> Image:
    current_log_level = logging.getLogger().level
    try:
        logging.getLogger().setLevel(logging.INFO)
        image = Image.open(filename, "r")

        if filename in EMPTY_IMAGE_FILES:
            image = image.resize(
                size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
                resample=Image.Resampling.NEAREST,
            )
    finally:
        logging.getLogger().setLevel(current_log_level)

    return image
