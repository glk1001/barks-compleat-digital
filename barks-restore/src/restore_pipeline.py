import logging
import os
import time
from pathlib import Path
from typing import List, Union

import cv2 as cv

from barks_fantagraphics.comics_utils import get_clean_path
from .image_io import svg_file_to_png, resize_image_file, write_cv_image_file
from .inpaint import inpaint_image_file
from .overlay import overlay_inpainted_file_with_black_ink
from .remove_alias_artifacts import get_median_filter
from .remove_colors import remove_colors_from_image
from .smooth_image import smooth_image_file
from .vtracer_to_svg import image_file_to_svg

USE_EXISTING_WORK_FILES = False  # Use with care


class RestorePipeline:
    def __init__(
        self,
        work_dir: str,
        srce_file: Path,
        srce_upscale_file: Path,
        scale: int,
        dest_restored_file: Path,
        dest_upscayled_restored_file: Path,
        dest_svg_restored_file: Path,
    ):
        self.work_dir = work_dir
        self.out_dir = os.path.dirname(dest_restored_file)
        self.srce_file = srce_file
        self.srce_upscale_file = srce_upscale_file
        self.scale = scale
        self.dest_restored_file = str(dest_restored_file)
        self.dest_upscayled_restored_file = str(dest_upscayled_restored_file)
        self.dest_svg_restored_file = str(dest_svg_restored_file)

        self.errors_occurred = False

        if not os.path.isdir(self.work_dir):
            raise Exception(f'Work directory not found: "{self.work_dir}".')
        if not os.path.isdir(self.out_dir):
            raise Exception(f'Restored directory not found: "{self.out_dir}".')
        if not os.path.exists(self.srce_upscale_file):
            raise Exception(f'Upscayl file not found: "{self.srce_upscale_file}".')

        self.srce_upscale_stem = f"{self.srce_upscale_file.stem}-upscayled"

        self.removed_artifacts_file = os.path.join(
            work_dir, f"{self.srce_upscale_stem}-median-filtered.png"
        )
        self.removed_colors_file = os.path.join(
            work_dir, f"{self.srce_upscale_stem}-color-removed.png"
        )
        self.smoothed_removed_colors_file = os.path.join(
            work_dir, f"{self.srce_upscale_stem}-color-removed-smoothed.png"
        )
        self.png_of_svg_file = self.dest_svg_restored_file + ".png"
        self.inpainted_file = os.path.join(work_dir, f"{self.srce_upscale_stem}-inpainted.png")

    def do_part1(self):
        self.do_remove_jpg_artifacts()
        self.do_remove_colors()

    def do_part2_memory_hungry(self):
        self.do_smooth_removed_colors()

    def do_part3(self):
        self.do_generate_svg()

    def do_part4_memory_hungry(self):
        self.do_inpaint()
        self.do_overlay_inpaint_with_black_ink()
        self.do_resize_restored_file()

    def do_remove_jpg_artifacts(self):
        if USE_EXISTING_WORK_FILES and os.path.isfile(self.removed_artifacts_file):
            logging.warning(
                f"Removed artifacts file already exists - skipping:"
                f' "{self.removed_artifacts_file}".'
            )
            return

        try:
            start = time.time()
            logging.info(
                f'\nGenerating file with jpeg artifacts removed: "{self.removed_artifacts_file}"...'
            )

            upscale_image = cv.imread(str(self.srce_upscale_file))
            out_image = get_median_filter(upscale_image)
            write_cv_image_file(self.removed_artifacts_file, out_image)

            logging.info(
                f"Time taken to remove jpeg artifacts for"
                f' "{os.path.basename(self.removed_artifacts_file)}":'
                f" {int(time.time() - start)}s."
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_remove_colors(self):
        if USE_EXISTING_WORK_FILES and os.path.isfile(self.removed_colors_file):
            logging.warning(
                f"Removed colors file already exists - skipping:" f' "{self.removed_colors_file}".'
            )
            return

        try:
            start = time.time()
            logging.info(f'\nGenerating color removed file "{self.removed_colors_file}"...')

            remove_colors_from_image(
                self.work_dir,
                self.srce_upscale_stem,
                self.removed_artifacts_file,
                self.removed_colors_file,
            )

            logging.info(
                f'Time taken to remove colors for "{os.path.basename(self.removed_colors_file)}":'
                f" {int(time.time() - start)}s."
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_smooth_removed_colors(self):
        if USE_EXISTING_WORK_FILES and os.path.isfile(self.smoothed_removed_colors_file):
            logging.warning(
                f"Smoothed removed colors file already exists - skipping:"
                f' "{self.smoothed_removed_colors_file}".'
            )
            return

        try:
            start = time.time()
            logging.info(f'\nGenerating smoothed file "{self.smoothed_removed_colors_file}"...')

            smooth_image_file(self.removed_colors_file, self.smoothed_removed_colors_file)

            logging.info(
                f'Time taken to smooth "{os.path.basename(self.smoothed_removed_colors_file)}":'
                f" {int(time.time() - start)}s."
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_generate_svg(self):
        try:
            start = time.time()
            logging.info(f'\nGenerating svg file "{self.dest_svg_restored_file}"...')

            image_file_to_svg(self.smoothed_removed_colors_file, self.dest_svg_restored_file)

            logging.info(
                f'Time taken to generate svg "{os.path.basename(self.dest_svg_restored_file)}":'
                f" {int(time.time() - start)}s."
            )

            logging.info(f'\nSaving svg file to png file "{self.png_of_svg_file}"...')
            svg_file_to_png(self.dest_svg_restored_file, self.png_of_svg_file)
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_inpaint(self):
        if USE_EXISTING_WORK_FILES and os.path.isfile(self.inpainted_file):
            logging.warning(
                f"Inpainted file already exists - skipping:" f' "{self.inpainted_file}".'
            )
            return

        try:
            start = time.time()
            logging.info(f'\nInpainting upscayled file to "{self.inpainted_file}"...')

            inpaint_image_file(
                self.work_dir,
                self.srce_upscale_stem,
                str(self.srce_upscale_file),
                self.removed_colors_file,
                self.inpainted_file,
            )

            logging.info(
                f'Time taken to inpaint "{os.path.basename(self.inpainted_file)}":'
                f" {int(time.time() - start)}s."
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_overlay_inpaint_with_black_ink(self):
        try:
            start = time.time()
            logging.info(
                f'\nOverlaying inpainted file "{self.inpainted_file}"'
                f' with black ink file "{self.png_of_svg_file}"...'
            )

            overlay_inpainted_file_with_black_ink(
                self.inpainted_file, self.png_of_svg_file, self.dest_upscayled_restored_file
            )

            logging.info(
                f'Time taken to overlay inpainted file "{os.path.basename(self.inpainted_file)}":'
                f" {int(time.time() - start)}s."
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)

    def do_resize_restored_file(self):
        try:
            logging.info(f'\nResizing restored file to "{self.dest_restored_file}"...')

            srce_file = (
                "N/A" if not os.path.isfile(self.srce_file) else get_clean_path(self.srce_file)
            )

            # TODO: Save other params used in process.
            restored_file_metadata = {
                "Source file": f'"{srce_file}"',
                "Upscayl file": f'"{get_clean_path(self.srce_upscale_file)}"',
                "Upscayl scale": str(self.scale),
            }

            resize_image_file(
                self.dest_upscayled_restored_file,
                self.scale,
                self.dest_restored_file,
                restored_file_metadata,
            )
        except Exception as e:
            self.errors_occurred = True
            logging.exception(e)


def check_file_exists(proc: RestorePipeline, file: Union[str, Path]):
    if not os.path.exists(file):
        logging.error(f'Could not find output artifact "{file}".')
        proc.errors_occurred = True


def check_for_errors(restore_procs: List[RestorePipeline]):
    for proc in restore_procs:
        check_file_exists(proc, proc.removed_artifacts_file)
        check_file_exists(proc, proc.removed_colors_file)
        check_file_exists(proc, proc.smoothed_removed_colors_file)
        check_file_exists(proc, proc.dest_svg_restored_file)
        check_file_exists(proc, proc.png_of_svg_file)
        check_file_exists(proc, proc.inpainted_file)
        check_file_exists(proc, proc.dest_upscayled_restored_file)
        check_file_exists(proc, proc.dest_restored_file)

        if proc.errors_occurred:
            logging.error(f'Errors occurred while processing "{proc.srce_upscale_file}".')
