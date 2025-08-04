# ruff: noqa: T201

import os
import sys
from pathlib import Path

from src.upscale_image import upscale_image_file

if __name__ == "__main__":
    input_image_file = sys.argv[1]

    scale = 4
    if len(sys.argv) >= 3:
        scale = int(sys.argv[2])
        assert 2 <= scale <= 12

    input_image_dir = os.path.dirname(input_image_file)
    input_image_stem = Path(input_image_file).stem
    output_upscayl_file = os.path.join(input_image_dir, f"{input_image_stem}-upscayl-x{scale}.png")

    if os.path.exists(output_upscayl_file):
        print(f'ERROR: Can\'t overwrite target file: "{output_upscayl_file}".')
        sys.exit(1)

    upscale_image_file(input_image_file, output_upscayl_file, scale)
