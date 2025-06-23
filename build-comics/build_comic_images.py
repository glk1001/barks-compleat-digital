import logging
import os
from typing import Tuple, List

from PIL import Image, ImageDraw, ImageFont

from barks_fantagraphics.comic_book import ComicBook, RequiredDimensions
from barks_fantagraphics.comic_issues import ISSUE_NAME, Issues
from barks_fantagraphics.comics_consts import (
    PageType,
    BARKS,
    get_font_path,
    PAGE_NUM_FONT_FILE,
    INTRO_TEXT_FONT_FILE,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
    DEST_TARGET_ASPECT_RATIO,
    PAGE_NUM_X_OFFSET_FROM_CENTRE,
    PAGE_NUM_X_BLANK_PIXEL_OFFSET,
    PAGE_NUM_HEIGHT,
    PAGE_NUM_FONT_SIZE,
    PAGE_NUM_COLOR,
    BACK_NO_PANELS_PAGES,
    PAINTING_PAGES,
    PAGES_WITHOUT_PANELS,
)
from barks_fantagraphics.comics_utils import get_relpath
from barks_fantagraphics.fanta_comics_info import CENSORED_TITLES
from barks_fantagraphics.pages import (
    EMPTY_IMAGE_FILEPATH,
    get_page_num_str,
)
from barks_fantagraphics.page_classes import CleanPage
from barks_fantagraphics.panel_bounding import get_scaled_panels_bbox_height
from consts import FOOTNOTE_CHAR
from image_io import open_image_for_reading

INTRO_TOP = 350
INTRO_BOTTOM_MARGIN = INTRO_TOP
INTRO_TITLE_SPACING = 50
INTRO_TITLE_COLOR = (0, 0, 0)
INTRO_TITLE_AUTHOR_GAP = 130
INTRO_TITLE_AUTHOR_BY_GAP = INTRO_TITLE_AUTHOR_GAP
INTRO_AUTHOR_COLOR = (0, 0, 0)
INTRO_AUTHOR_INSET_GAP = 8
INTRO_MAX_WIDTH_INSET_MARGIN_FRAC = 0.05
INTRO_MAX_HEIGHT_INSET_MARGIN_FRAC = 0.18
INTRO_PUB_TEXT_FONT_SIZE = 35
INTRO_PUB_TEXT_COLOR = (0, 0, 0)
INTRO_PUB_TEXT_SPACING = 20

SPLASH_BORDER_COLOR = (0, 0, 0)
SPLASH_BORDER_WIDTH = 10
SPLASH_MARGIN = DEST_TARGET_X_MARGIN


class ComicBookImageBuilder:
    def __init__(self, comic: ComicBook):
        self.__comic = comic
        self.__required_dim: RequiredDimensions = RequiredDimensions()

    def set_required_dim(self, required_dim: RequiredDimensions) -> None:
        self.__required_dim = required_dim

    @staticmethod
    def _log_page_info(prefix: str, image: Image, page: CleanPage):
        width = image.width if image else 0
        height = image.height if image else 0
        logging.debug(
            f"{prefix}: width = {width:4}, height = {height:4},"
            f" page_type = {page.page_type.name:13},"
            f" panels bbox = {page.panels_bbox.x_min:4}, {page.panels_bbox.y_min:4},"
            f" {page.panels_bbox.x_max:4}, {page.panels_bbox.y_max:4}."
        )

    def get_dest_page_image(
        self, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
    ) -> Image:
        self._log_page_info(f"{srce_page.page_num}-Srce", srce_page_image, srce_page)
        self._log_page_info(f"{srce_page.page_num}-Dest", None, dest_page)

        if dest_page.page_type in PAGES_WITHOUT_PANELS:
            dest_page_image = self._get_no_panels_dest_image(srce_page_image, srce_page, dest_page)
        else:
            dest_page_image = self._get_main_page_dest_image(srce_page_image, srce_page, dest_page)

        rgb_dest_page_image = dest_page_image.convert("RGB")

        self._log_page_info("Dest", rgb_dest_page_image, dest_page)

        return rgb_dest_page_image

    def _get_no_panels_dest_image(
        self, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
    ) -> Image:
        if dest_page.page_type == PageType.FRONT:
            return self._get_front_page_dest_image(srce_page_image, srce_page)
        if dest_page.page_type == PageType.COVER:
            return self._get_cover_page_dest_image(srce_page_image, srce_page)
        if dest_page.page_type in PAINTING_PAGES:
            return self._get_painting_page_dest_image(srce_page_image, srce_page)
        if dest_page.page_type == PageType.SPLASH:
            return self._get_splash_page_dest_image(srce_page_image, srce_page)
        if dest_page.page_type in BACK_NO_PANELS_PAGES:
            return self._get_no_panels_back_page_dest_image(srce_page_image, srce_page, dest_page)
        if dest_page.page_type == PageType.BLANK_PAGE:
            return self._get_blank_page_dest_image(srce_page_image)
        if dest_page.page_type == PageType.TITLE:
            return self._get_dest_title_page_image(srce_page_image)
        assert False

    def _get_front_page_dest_image(self, srce_page_image: Image, srce_page: CleanPage) -> Image:
        return self._get_black_bars_page_dest_image(srce_page_image, srce_page)

    def _get_cover_page_dest_image(self, srce_page_image: Image, srce_page: CleanPage) -> Image:
        return self._get_black_bars_page_dest_image(srce_page_image, srce_page)

    def _get_painting_page_dest_image(self, painting_image: Image, srce_page: CleanPage) -> Image:
        assert srce_page.page_type in PAINTING_PAGES

        if srce_page.page_type in [PageType.PAINTING_NO_BORDER, PageType.BACK_PAINTING_NO_BORDER]:
            return self._get_black_bars_page_dest_image(painting_image, srce_page)

        assert srce_page.page_type in [PageType.PAINTING, PageType.BACK_PAINTING]
        self._draw_border_around_image(painting_image)
        dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)
        return self._get_centred_page_dest_image(painting_image, srce_page, dest_page_image)

    def _get_splash_page_dest_image(self, splash_image: Image, srce_page: CleanPage) -> Image:
        assert srce_page.page_type == PageType.SPLASH

        splash_width = splash_image.width
        splash_height = splash_image.height

        smaller_splash_image = splash_image.resize(
            size=(splash_width - (2 * SPLASH_MARGIN), splash_height - (2 * SPLASH_MARGIN)),
            resample=Image.Resampling.BICUBIC,
        )
        self._draw_border_around_image(smaller_splash_image)

        dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

        splash_image = dest_page_image.resize(size=(splash_width, splash_height))
        splash_image.paste(smaller_splash_image, (SPLASH_MARGIN, SPLASH_MARGIN))

        return self._get_centred_page_dest_image(splash_image, srce_page, dest_page_image)

    @staticmethod
    def _draw_border_around_image(image: Image):
        x_min = 0
        y_min = 0
        x_max = image.width - 1
        y_max = image.height - 1
        border = [
            (x_min, y_min),
            (x_max, y_min),
            (x_max, y_max),
            (x_min, y_max),
            (x_min, y_min),
        ]
        draw = ImageDraw.Draw(image)
        draw.line(border, fill=SPLASH_BORDER_COLOR, width=SPLASH_BORDER_WIDTH)

    def _get_no_panels_back_page_dest_image(
        self, no_panels_image: Image, srce_page: CleanPage, dest_page: CleanPage
    ) -> Image:
        dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

        dest_page_image = self._get_centred_page_dest_image(
            no_panels_image, srce_page, dest_page_image
        )

        self._write_page_number(dest_page_image, dest_page, PAGE_NUM_COLOR)

        return dest_page_image

    def _get_black_bars_page_dest_image(
        self, srce_page_image: Image, srce_page: CleanPage
    ) -> Image:
        dest_page_image = Image.new("RGB", (DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT), (0, 0, 0))
        return self._get_centred_page_dest_image(srce_page_image, srce_page, dest_page_image)

    @staticmethod
    def _get_centred_page_dest_image(
        srce_page_image: Image, srce_page: CleanPage, dest_page_image: Image
    ) -> Image:
        srce_aspect_ratio = float(srce_page_image.height) / float(srce_page_image.width)
        if abs(srce_aspect_ratio - DEST_TARGET_ASPECT_RATIO) > 0.01:
            logging.debug(
                f"Wrong aspect ratio for page '{get_relpath(srce_page.page_filename)}':"
                f" {srce_aspect_ratio:.2f} != {DEST_TARGET_ASPECT_RATIO :.2f}."
                f" Using black bars."
            )

        required_height = get_scaled_panels_bbox_height(
            DEST_TARGET_WIDTH, srce_page_image.width, srce_page_image.height
        )

        no_margins_image = srce_page_image.resize(
            size=(DEST_TARGET_WIDTH, required_height),
            resample=Image.Resampling.BICUBIC,
        )
        no_margins_aspect_ratio = float(no_margins_image.height) / float(no_margins_image.width)
        assert abs(srce_aspect_ratio - no_margins_aspect_ratio) <= 0.01

        if required_height == DEST_TARGET_HEIGHT:
            return no_margins_image

        cover_top = int(round(0.5 * (DEST_TARGET_HEIGHT - required_height)))
        dest_page_image.paste(no_margins_image, (0, cover_top))

        return dest_page_image

    @staticmethod
    def _get_blank_page_dest_image(srce_page_image: Image) -> Image:
        dest_page_image = srce_page_image.resize(
            size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
            resample=Image.Resampling.BICUBIC,
        )

        return dest_page_image

    def _get_main_page_dest_image(
        self, srce_page_image: Image, srce_page: CleanPage, dest_page: CleanPage
    ) -> Image:
        dest_panels_image = srce_page_image.crop(srce_page.panels_bbox.get_box())
        dest_page_image = self._get_centred_dest_page_image(dest_page, dest_panels_image)

        if dest_page_image.width != DEST_TARGET_WIDTH:
            raise Exception(
                f'Width mismatch for page "{srce_page.page_filename}":'
                f"{dest_page_image.width} != {DEST_TARGET_WIDTH}"
            )
        if dest_page_image.height != DEST_TARGET_HEIGHT:
            raise Exception(
                f'Height mismatch for page "{srce_page.page_filename}":'
                f"{dest_page_image.height} != {DEST_TARGET_HEIGHT}"
            )

        self._write_page_number(dest_page_image, dest_page, PAGE_NUM_COLOR)

        return dest_page_image

    @staticmethod
    def _get_centred_dest_page_image(dest_page: CleanPage, dest_panels_image: Image) -> Image:
        dest_page_image = open_image_for_reading(EMPTY_IMAGE_FILEPATH)

        if dest_page.page_type not in PAGES_WITHOUT_PANELS:
            dest_panels_image = dest_panels_image.resize(
                size=(dest_page.panels_bbox.get_width(), dest_page.panels_bbox.get_height()),
                resample=Image.Resampling.BICUBIC,
            )

        dest_panels_pos = (dest_page.panels_bbox.x_min, dest_page.panels_bbox.y_min)
        dest_page_image.paste(dest_panels_image, dest_panels_pos)

        return dest_page_image

    def _write_page_number(self, dest_page_image: Image, dest_page: CleanPage, color):
        draw = ImageDraw.Draw(dest_page_image)

        dest_page_centre = int(dest_page_image.width / 2)
        page_num_x_start = dest_page_centre - PAGE_NUM_X_OFFSET_FROM_CENTRE
        page_num_x_end = dest_page_centre + PAGE_NUM_X_OFFSET_FROM_CENTRE
        page_num_y_start = (
            dest_page_image.height - self.__required_dim.page_num_y_bottom
        ) - PAGE_NUM_HEIGHT
        page_num_y_end = page_num_y_start + PAGE_NUM_HEIGHT

        # Get the color of a blank part of the page
        page_blank_color = dest_page_image.getpixel(
            (
                page_num_x_start + PAGE_NUM_X_BLANK_PIXEL_OFFSET,
                page_num_y_end,
            )
        )

        # Remove the existing page number
        shape = (
            (
                page_num_x_start - 1,
                page_num_y_start - 1,
            ),
            (
                page_num_x_end + 1,
                page_num_y_end + 1,
            ),
        )
        draw.rectangle(shape, fill=page_blank_color)

        font = ImageFont.truetype(get_font_path(PAGE_NUM_FONT_FILE), PAGE_NUM_FONT_SIZE)
        text = get_page_num_str(dest_page)
        self._draw_centered_text(
            text,
            dest_page_image,
            draw,
            font,
            color,
            page_num_y_start,
        )

    @staticmethod
    def _draw_centered_text(
        text: str, image: Image, draw: ImageDraw, font: ImageFont, color, top: int
    ):
        w = draw.textlength(text, font)
        left = (image.width - w) / 2
        draw.text((left, top), text, fill=color, font=font, align="center")

    def _get_dest_title_page_image(self, srce_page_image: Image) -> Image:
        dest_page_image = srce_page_image.resize(
            size=(DEST_TARGET_WIDTH, DEST_TARGET_HEIGHT),
            resample=Image.Resampling.BICUBIC,
        )

        self._write_introduction(dest_page_image)

        return dest_page_image

    def _write_introduction(self, dest_page_image: Image):
        if not os.path.isfile(self.__comic.intro_inset_file):
            raise Exception(f'Could not find inset file "{self.__comic.intro_inset_file}".')

        logging.info(
            f"Writing introduction - using inset file"
            f' "{get_relpath(self.__comic.intro_inset_file)}".'
        )

        draw = ImageDraw.Draw(dest_page_image)

        top = INTRO_TOP

        title, title_fonts, text_height = self._get_title_and_fonts(draw)

        self._draw_centered_multiline_title_text(
            title,
            title_fonts,
            INTRO_TITLE_COLOR,
            top,
            spacing=INTRO_TITLE_SPACING,
            image=dest_page_image,
            draw=draw,
        )
        top += text_height + INTRO_TITLE_SPACING

        top += INTRO_TITLE_AUTHOR_GAP
        text = "by"
        by_font_size = int(0.6 * self.__comic.author_font_size)
        by_font = ImageFont.truetype(self.__comic.title_font_file, by_font_size)
        text_height = self._get_intro_text_height(draw, text, by_font)
        self._draw_centered_text(text, dest_page_image, draw, by_font, INTRO_AUTHOR_COLOR, top)
        top += text_height

        top += INTRO_TITLE_AUTHOR_BY_GAP
        text = f"{BARKS}"
        author_font = ImageFont.truetype(
            self.__comic.title_font_file, self.__comic.author_font_size
        )
        text_height = self._get_intro_text_height(draw, text, author_font)
        self._draw_centered_text(text, dest_page_image, draw, author_font, INTRO_AUTHOR_COLOR, top)
        top += text_height + INTRO_AUTHOR_INSET_GAP

        pub_text_font = ImageFont.truetype(
            get_font_path(INTRO_TEXT_FONT_FILE), INTRO_PUB_TEXT_FONT_SIZE
        )
        text_height = self._get_intro_text_height(
            draw, self.__comic.publication_text, pub_text_font
        )
        pub_text_top = dest_page_image.height - INTRO_BOTTOM_MARGIN - text_height

        inset_pos, new_inset = self._get_resized_inset(
            self.__comic.intro_inset_file,
            top,
            pub_text_top,
            dest_page_image.width,
        )
        dest_page_image.paste(new_inset, inset_pos)

        self._draw_centered_multiline_text(
            self.__comic.publication_text,
            dest_page_image,
            draw,
            pub_text_font,
            INTRO_PUB_TEXT_COLOR,
            pub_text_top,
            INTRO_PUB_TEXT_SPACING,
        )

    @staticmethod
    def _get_resized_inset(
        inset_file: str, top: int, bottom: int, page_width: int
    ) -> Tuple[Tuple[int, int], Image]:
        inset = open_image_for_reading(inset_file)
        inset_width, inset_height = inset.size

        usable_width = page_width - (2 * DEST_TARGET_X_MARGIN)
        usable_height = bottom - top

        width_margin = int(INTRO_MAX_WIDTH_INSET_MARGIN_FRAC * usable_width)
        height_margin = int(INTRO_MAX_HEIGHT_INSET_MARGIN_FRAC * usable_height)

        new_inset_width = usable_width - (2 * width_margin)
        new_inset_height = int((inset_height / inset_width) * new_inset_width)

        max_inset_height = usable_height - (2 * height_margin)
        if new_inset_height > max_inset_height:
            new_inset_height = max_inset_height
            new_inset_width = int((inset_width / inset_height) * new_inset_height)

        new_inset = inset.resize(
            size=(new_inset_width, new_inset_height), resample=Image.Resampling.BICUBIC
        )

        inset_left = int((page_width - new_inset_width) / 2)
        inset_top = top + int(((bottom - top) - new_inset_height) / 2)

        return (inset_left, inset_top), new_inset

    @staticmethod
    def _get_intro_text_height(draw: ImageDraw.Draw, text: str, font: ImageFont) -> int:
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=INTRO_TITLE_SPACING)
        return text_bbox[3] - text_bbox[1]

    @staticmethod
    def _get_intro_text_width(draw: ImageDraw.Draw, text: str, font: ImageFont) -> int:
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=INTRO_TITLE_SPACING)
        return text_bbox[2] - text_bbox[0]

    def _get_title_and_fonts(
        self, draw: ImageDraw.Draw
    ) -> Tuple[List[str], List[ImageFont.truetype], int]:
        title = self.__comic.get_comic_title()
        font_file = self.__comic.title_font_file
        font_size = self.__comic.title_font_size
        comic_book_info = self.__comic.fanta_info.comic_book_info

        if (not comic_book_info.is_barks_title) and (comic_book_info.issue_name == Issues.CS):
            add_footnote = self.__comic.get_ini_title() in CENSORED_TITLES

            title_and_fonts = self._get_comics_and_stories_title_and_fonts(
                draw, title, font_file, font_size, add_footnote
            )
            return title_and_fonts

        title_font = ImageFont.truetype(font_file, font_size)
        text_height = self._get_intro_text_height(draw, title, title_font)
        return [title], [title_font], text_height

    def _get_comics_and_stories_title_and_fonts(
        self, draw: ImageDraw.Draw, title: str, font_file: str, font_size: int, add_footnote: bool
    ) -> Tuple[List[str], List[ImageFont.truetype], int]:
        assert title.startswith(ISSUE_NAME[Issues.CS])

        comic_num = title[len(ISSUE_NAME[Issues.CS]) :]
        if add_footnote:
            comic_num += FOOTNOTE_CHAR

        title_split = ["Comics", "and Stories", comic_num]
        title_fonts = [
            ImageFont.truetype(font_file, font_size),
            ImageFont.truetype(font_file, int(0.5 * font_size)),
            ImageFont.truetype(font_file, font_size),
        ]

        text_height = self._get_intro_text_height(draw, title, title_fonts[0])

        return title_split, title_fonts, text_height

    def _draw_centered_multiline_text(
        self,
        text: str,
        image: Image,
        draw: ImageDraw,
        font: ImageFont,
        color,
        top: int,
        spacing: int,
    ):
        text_width = self._get_intro_text_width(draw, text, font)
        left = (image.width - text_width) / 2
        draw.multiline_text(
            (left, top), text, fill=color, font=font, align="center", spacing=spacing
        )

    def _draw_centered_multiline_title_text(
        self,
        text_vals: List[str],
        fonts: List[ImageFont],
        color: Tuple[int, int, int],
        top: int,
        spacing: int,
        image: Image,
        draw: ImageDraw,
    ):
        lines = []
        line = []
        for text, font in zip(text_vals, fonts):
            if not text.startswith("\n"):
                line.append((text, font))
            else:
                lines.append(line)
                line = [(text[1:], font)]
        lines.append(line)

        line_widths = []
        text_lines = []
        for line in lines:
            line_width = 0
            text_line = []
            for text, font in line:
                text_width = self._get_intro_text_width(draw, text, font)
                line_width += text_width
                text_line.append((text, font, text_width))
            line_widths.append(line_width)
            text_lines.append(text_line)

        max_font_height = self._get_intro_text_height(draw, text_vals[0], fonts[0])
        line_top = top
        for text_line, line_width in zip(text_lines, line_widths):
            left = (image.width - line_width) / 2
            line_start = True
            for text, font, text_width in text_line:
                font_height = self._get_intro_text_height(draw, text, font)
                assert font_height <= max_font_height

                if line_start or font_height == max_font_height:
                    line_top_extra = 0
                    width_spacing = 0
                else:
                    line_top_extra = 10
                    width_spacing = int(1.1 * ((font_height * spacing) / max_font_height))
                left += width_spacing

                has_footnote = False
                if text[-1] == FOOTNOTE_CHAR:
                    has_footnote = True
                    text = text[:-1]
                    text_width -= 1

                draw.multiline_text(
                    (left, line_top + line_top_extra),
                    text,
                    fill=color,
                    font=font,
                    align="center",
                    spacing=spacing,
                )
                left += text_width

                if has_footnote:
                    self._draw_superscript_title_text(
                        FOOTNOTE_CHAR,
                        color,
                        left,
                        line_top + line_top_extra,
                        spacing,
                        draw,
                    )

                line_start = False
            line_top += int(1.5 * max_font_height)

    def _draw_superscript_title_text(
        self,
        text: str,
        color: Tuple[int, int, int],
        left: int,
        top: int,
        spacing: int,
        draw: ImageDraw,
    ):
        superscript_font_size = int(0.7 * self.__comic.title_font_size)
        superscript_font = ImageFont.truetype(self.__comic.title_font_file, superscript_font_size)
        draw.multiline_text(
            (
                left - int(0.75 * superscript_font_size),
                top - 20,
            ),
            text,
            fill=color,
            font=superscript_font,
            align="center",
            spacing=spacing,
        )
