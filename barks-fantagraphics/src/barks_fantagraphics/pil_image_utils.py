from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo

if TYPE_CHECKING:
    import io

Image.MAX_IMAGE_PIXELS = None

SAVE_PNG_COMPRESSION = 9
SAVE_JPG_QUALITY = 95
SAVE_JPG_COMPRESS_LEVEL = 9

METADATA_PROPERTY_GROUP = "BARKS"


def open_pil_image_for_reading(
    file: str | io.BytesIO,
    pil_formats: list[str] | None = None,
) -> Image:
    current_log_level = logging.getLogger().level
    try:
        logging.getLogger().setLevel(logging.INFO)
        return Image.open(file, "r", formats=pil_formats)
    finally:
        logging.getLogger().setLevel(current_log_level)


def copy_file_to_jpg(srce_file: str, dest_file: str) -> None:
    image = open_pil_image_for_reading(srce_file).convert("RGB")

    image.save(
        dest_file,
        optimize=True,
        compress_level=SAVE_PNG_COMPRESSION,
    )


def copy_file_to_png(srce_file: str, dest_file: str) -> None:
    image = open_pil_image_for_reading(srce_file)

    image.save(
        dest_file,
        optimize=True,
        compress_level=SAVE_PNG_COMPRESSION,
        quality=SAVE_PNG_COMPRESSION,
    )


def downscale_jpg(width: int, height: int, srce_file: str, dest_file: str) -> None:
    image = open_pil_image_for_reading(srce_file).convert("RGB")

    image_resized = ImageOps.contain(
        image,
        (width, height),
        Image.Resampling.LANCZOS,
    )

    image_resized.save(
        dest_file,
        optimize=True,
        compress_level=SAVE_JPG_COMPRESS_LEVEL,
        quality=SAVE_JPG_QUALITY,
    )


def add_jpg_metadata(jpg_file: str, metadata: dict[str, str]) -> None:
    pil_image = Image.open(jpg_file, "r")

    jpg_metadata = PngInfo()
    for key in metadata:
        jpg_metadata.add_text(f"{METADATA_PROPERTY_GROUP}:{key}", metadata[key])

    pil_image.save(
        jpg_file,
        jpginfo=jpg_metadata,
        optimize=True,
        compress_level=SAVE_JPG_COMPRESS_LEVEL,
        quality=SAVE_JPG_QUALITY,
    )


def add_png_metadata(png_file: str, metadata: dict[str, str]) -> None:
    pil_image = Image.open(png_file, "r")

    png_metadata = PngInfo()
    for key in metadata:
        png_metadata.add_text(f"{METADATA_PROPERTY_GROUP}:{key}", metadata[key])

    pil_image.save(
        png_file,
        pnginfo=png_metadata,
        optimize=True,
        compress_level=SAVE_PNG_COMPRESSION,
    )


# def get_png_metadata(png_file: str) -> Dict[str, str]:
#     pil_image = Image.open(png_file, "r")
#
#     png_metadata = pil_image.info
#
#     prefix = METADATA_PROPERTY_GROUP + ":"
#     metadata = dict()
#     for key in png_metadata:
#         if key.startswith(prefix):
#             metadata[key[len(prefix) :]] = png_metadata[key]
#
#     return metadata
#
#
# def get_jpg_metadata(jpg_file: str) -> Dict[str, str]:
#     pil_image = Image.open(jpg_file, "r")
#
#     jpg_comments = pil_image.app["COM"]
#
#     metadata = dict()
#     metadata["comments"] = jpg_comments
#
#     return metadata
