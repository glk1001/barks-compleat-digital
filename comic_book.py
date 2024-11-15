import configparser
import logging
import os
from dataclasses import dataclass
from typing import List

from comics_info import (
    ISSUE_NAME_AS_TITLE,
    MONTH_AS_LONG_STR,
    SHORT_ISSUE_NAME,
    SILENT_NIGHT,
    SILENT_NIGHT_PUBLICATION_ISSUE,
    SOURCE_COMICS,
    ComicBookInfo,
    ComicBookInfoDict,
    SourceBook,
    get_formatted_day,
)
from consts import (
    PageType,
    IMAGES_SUBDIR,
    THE_CHRONOLOGICAL_DIRS_DIR,
    THE_CHRONOLOGICAL_DIR,
    THE_COMICS_DIR,
    THE_YEARS_COMICS_DIR,
    DEST_TARGET_X_MARGIN,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_ASPECT_RATIO,
    DEST_JPG_QUALITY,
    DEST_JPG_COMPRESS_LEVEL,
    CONFIGS_SUBDIR,
    BARKS_ROOT_DIR,
    get_font_path,
    INSET_FILE_EXT,
    INTRO_TITLE_DEFAULT_FONT_FILE,
)

INTRO_TITLE_DEFAULT_FONT_SIZE = 155
INTRO_AUTHOR_DEFAULT_FONT_SIZE = 90


@dataclass
class OriginalPage:
    page_filenames: str
    page_type: PageType


@dataclass
class RequiredDimensions:
    panels_bbox_width: int = -1
    panels_bbox_height: int = -1
    page_num_y_bottom: int = -1


@dataclass
class ComicBook:
    ini_file: str
    title: str
    title_font_file: str
    title_font_size: int
    # NOTE: Need 'issue_title' to force a series title that has
    #       changed from another title. E.g., FC 495 == Uncle Scrooge #3
    issue_title: str
    file_title: str
    author_font_size: int
    srce_min_panels_bbox_width: int
    srce_max_panels_bbox_width: int
    srce_min_panels_bbox_height: int
    srce_max_panels_bbox_height: int
    srce_av_panels_bbox_width: int
    srce_av_panels_bbox_height: int
    required_dim: RequiredDimensions
    fanta_info: SourceBook
    srce_dir: str
    srce_file_ext: str
    srce_fixes_dir: str
    panel_segments_dir: str
    series_name: str
    number_in_series: int
    chronological_number: int
    intro_inset_file: str
    publication_date: str
    submitted_date: str
    submitted_year: int
    publication_text: str
    comic_book_info: ComicBookInfo
    images_in_order: List[OriginalPage]

    def __post_init__(self):
        assert self.series_name != ""
        assert self.number_in_series > 0

    def get_srce_root_dir(self) -> str:
        return os.path.dirname(self.srce_dir)

    def get_srce_fixes_root_dir(self) -> str:
        return os.path.dirname(self.srce_fixes_dir)

    def get_srce_image_dir(self) -> str:
        return os.path.join(self.srce_dir, IMAGES_SUBDIR)

    def get_srce_fixes_image_dir(self) -> str:
        return os.path.join(self.srce_fixes_dir, IMAGES_SUBDIR)

    def get_srce_segments_root_dir(self) -> str:
        return os.path.dirname(self.panel_segments_dir)

    def get_dest_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIRS_DIR

    def get_dest_dir(self) -> str:
        return os.path.join(
            self.get_dest_root_dir(),
            self.get_dest_rel_dirname(),
        )

    def get_dest_rel_dirname(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        return f"{self.chronological_number:03d} {file_title}"

    def get_series_comic_title(self) -> str:
        return f"{self.series_name} {self.number_in_series}"

    def get_dest_image_dir(self) -> str:
        return os.path.join(self.get_dest_dir(), IMAGES_SUBDIR)

    def get_dest_zip_root_dir(self) -> str:
        return THE_CHRONOLOGICAL_DIR

    def get_dest_series_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_COMICS_DIR,
            self.series_name,
        )

    def get_dest_year_zip_symlink_dir(self) -> str:
        return os.path.join(
            THE_YEARS_COMICS_DIR,
            str(self.submitted_year),
        )

    def get_dest_comic_zip_filename(self) -> str:
        return f"{self.get_title_with_issue_num()}.cbz"

    def get_dest_comic_zip(self) -> str:
        return os.path.join(self.get_dest_zip_root_dir(), self.get_dest_comic_zip_filename())

    def get_dest_series_comic_zip_symlink_filename(self) -> str:
        file_title = get_lookup_title(self.title, self.file_title)
        full_title = f"{file_title} [{self.get_comic_issue_title()}]"
        return f"{self.number_in_series:03d} {full_title}.cbz"

    def get_dest_series_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_series_zip_symlink_dir()}",
            f"{self.get_dest_series_comic_zip_symlink_filename()}",
        )

    def get_dest_year_comic_zip_symlink(self) -> str:
        return os.path.join(
            f"{self.get_dest_year_zip_symlink_dir()}",
            f"{self.get_dest_comic_zip_filename()}",
        )

    def get_comic_title(self) -> str:
        if self.title != "":
            return self.title
        if self.issue_title != "":
            return self.issue_title

        return self.__get_comic_title_from_issue_name()

    def __get_comic_title_from_issue_name(self) -> str:
        issue_name = self.comic_book_info.issue_name
        if issue_name not in ISSUE_NAME_AS_TITLE:
            issue_name += "\n"
        else:
            issue_name = ISSUE_NAME_AS_TITLE[issue_name] + " #"

        return f"{issue_name}{self.comic_book_info.issue_number}"

    def get_comic_issue_title(self) -> str:
        issue_name = SHORT_ISSUE_NAME[self.comic_book_info.issue_name]
        return f"{issue_name} {self.comic_book_info.issue_number}"

    def get_title_with_issue_num(self) -> str:
        return f"{self.get_dest_rel_dirname()} [{self.get_comic_issue_title()}]"


def get_lookup_title(title: str, file_title: str) -> str:
    if title != "":
        return get_safe_title(title)

    assert file_title != ""
    return file_title


def get_safe_title(title: str) -> str:
    safe_title = title.replace("\n", " ")
    safe_title = safe_title.replace("- ", "-")
    safe_title = safe_title.replace('"', "")
    return safe_title


def log_comic_book_params(comic: ComicBook, caching: bool, work_dir: str):
    logging.info("")

    calc_panels_bbox_height = int(
        round(
            (comic.srce_av_panels_bbox_height * comic.required_dim.panels_bbox_width)
            / comic.srce_av_panels_bbox_width
        )
    )

    fixes_basename = os.path.basename(comic.srce_fixes_dir)
    panel_segments_basename = os.path.basename(comic.panel_segments_dir)
    dest_basename = os.path.basename(comic.get_dest_dir())
    dest_comic_zip_basename = os.path.basename(comic.get_dest_comic_zip())

    logging.info(f'Comic book series:   "{comic.series_name}".')
    logging.info(f'Comic book title:    "{get_safe_title(comic.get_comic_title())}".')
    logging.info(f'Comic issue title:   "{comic.get_comic_issue_title()}".')
    logging.info(f"Number in series:    {comic.number_in_series}.")
    logging.info(f"Chronological number {comic.chronological_number}.")
    logging.info(f"Caching:             {caching}.")
    logging.info(f"Dest x margin:       {DEST_TARGET_X_MARGIN}.")
    logging.info(f"Dest width:          {DEST_TARGET_WIDTH}.")
    logging.info(f"Dest height:         {DEST_TARGET_HEIGHT}.")
    logging.info(f"Dest aspect ratio:   {DEST_TARGET_ASPECT_RATIO :.2f}.")
    logging.info(f"Dest jpeg quality:   {DEST_JPG_QUALITY}.")
    logging.info(f"Dest compress level: {DEST_JPG_COMPRESS_LEVEL}.")
    logging.info(f"Srce min bbox wid:   {comic.srce_min_panels_bbox_width}.")
    logging.info(f"Srce max bbox wid:   {comic.srce_max_panels_bbox_width}.")
    logging.info(f"Srce min bbox hgt:   {comic.srce_min_panels_bbox_height}.")
    logging.info(f"Srce max bbox hgt:   {comic.srce_max_panels_bbox_height}.")
    logging.info(f"Srce av bbox wid:    {comic.srce_av_panels_bbox_width}.")
    logging.info(f"Srce av bbox hgt:    {comic.srce_av_panels_bbox_height}.")
    logging.info(f"Req panels bbox wid: {comic.required_dim.panels_bbox_width}.")
    logging.info(f"Req panels bbox hgt: {comic.required_dim.panels_bbox_height}.")
    logging.info(f"Calc panels bbox ht: {calc_panels_bbox_height}.")
    logging.info(f"Page num y bottom:   {comic.required_dim.page_num_y_bottom}.")
    logging.info(f'Ini file:            "{comic.ini_file}".')
    logging.info(f'Srce root:           "{comic.get_srce_root_dir()}".')
    logging.info(f'Srce comic dir:      "SRCE ROOT/{os.path.basename(comic.srce_dir)}".')
    logging.info(f'Srce fixes root:     "{comic.get_srce_fixes_root_dir()}".')
    logging.info(f'Srce fixes dir:      "FIXES ROOT/{fixes_basename}".')
    logging.info(f'Srce segments root:  "{comic.get_srce_segments_root_dir()}".')
    logging.info(f'Srce segments dir:   "SEGMENTS ROOT/{panel_segments_basename}".')
    logging.info(f'Srce file ext:       "{comic.srce_file_ext}".')
    logging.info(f'Dest root:           "{comic.get_dest_root_dir()}".')
    logging.info(f'Dest comic dir:      "DEST ROOT/{dest_basename}".')
    logging.info(f'Dest zip root:       "{comic.get_dest_zip_root_dir()}".')
    logging.info(f'Dest comic zip:      "ZIP ROOT/{dest_comic_zip_basename}".')
    logging.info(f'Dest series symlink: "{comic.get_dest_series_comic_zip_symlink()}".')
    logging.info(f'Dest year symlink:   "{comic.get_dest_year_comic_zip_symlink()}".')
    logging.info(f'Work directory:      "{work_dir}".')
    logging.info("")


def get_main_publication_info(
    file_title: str, cb_info: ComicBookInfo, fanta_info: SourceBook
) -> str:
    if file_title == SILENT_NIGHT:
        # Originally intended for WDCS 64
        publication_text = (
            f"(*) Rejected by Western editors in 1945, this story was originally\n"
            f" intended for publication in {get_formatted_first_published_str(cb_info)}\n"
            + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
            + f"\n"
            + f"The story was also not published in the Fantagraphics CBDL but\n"
            + f"fortunately did appear in {SILENT_NIGHT_PUBLICATION_ISSUE}\n"
            + f"Color restoration by {cb_info.colorist}"
        )
        return publication_text

    publication_text = (
        f"First published in {get_formatted_first_published_str(cb_info)}\n"
        + f"Submitted to Western Publishing{get_formatted_submitted_date(cb_info)}\n"
        + f"\n"
        + f"This edition published in {fanta_info.pub} CBDL,"
        + f" Volume {fanta_info.volume}, {fanta_info.year}\n"
        + f"Color restoration by {cb_info.colorist}"
    )

    return publication_text


def get_comic_book(stories: ComicBookInfoDict, ini_file: str) -> ComicBook:
    logging.info(f'Getting comic book info from config file "{ini_file}".')

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(ini_file)

    title = config["info"]["title"]
    issue_title = "" if "issue_title" not in config["info"] else config["info"]["issue_title"]
    file_title = config["info"]["file_title"]
    lookup_title = get_lookup_title(title, file_title)
    intro_inset_file = str(os.path.join(CONFIGS_SUBDIR, get_inset_filename(ini_file, file_title)))

    cb_info: ComicBookInfo = stories[lookup_title]
    fanta_info = SOURCE_COMICS[config["info"]["source_comic"]]
    srce_root_dir = str(os.path.join(BARKS_ROOT_DIR, fanta_info.subdir))
    srce_dir = os.path.join(srce_root_dir, fanta_info.title)
    srce_file_ext = fanta_info.srce_file_ext
    srce_fixup_dir = os.path.join(srce_root_dir + "-fixes-and-additions", fanta_info.title)
    panel_segments_dir = str(os.path.join(srce_root_dir + "-panel-segments", fanta_info.title))

    publication_date = get_formatted_first_published_str(cb_info)
    submitted_date = get_formatted_submitted_date(cb_info)

    publication_text = get_main_publication_info(file_title, cb_info, fanta_info)
    if "extra_pub_info" in config["info"]:
        publication_text += "\n" + config["info"]["extra_pub_info"]

    comic = ComicBook(
        ini_file=ini_file,
        title=title,
        title_font_file=get_font_path(
            config["info"].get("title_font_file", INTRO_TITLE_DEFAULT_FONT_FILE)
        ),
        title_font_size=config["info"].getint("title_font_size", INTRO_TITLE_DEFAULT_FONT_SIZE),
        file_title=file_title,
        issue_title=issue_title,
        author_font_size=config["info"].getint("author_font_size", INTRO_AUTHOR_DEFAULT_FONT_SIZE),
        srce_min_panels_bbox_width=-1,
        srce_max_panels_bbox_width=-1,
        srce_min_panels_bbox_height=-1,
        srce_max_panels_bbox_height=-1,
        srce_av_panels_bbox_width=-1,
        srce_av_panels_bbox_height=-1,
        required_dim=RequiredDimensions(),
        fanta_info=fanta_info,
        srce_dir=srce_dir,
        srce_file_ext=srce_file_ext,
        srce_fixes_dir=srce_fixup_dir,
        panel_segments_dir=panel_segments_dir,
        series_name=cb_info.series_name,
        number_in_series=cb_info.number_in_series,
        chronological_number=cb_info.chronological_number,
        intro_inset_file=intro_inset_file,
        publication_date=publication_date,
        submitted_date=submitted_date,
        submitted_year=cb_info.submitted_year,
        publication_text=publication_text,
        comic_book_info=cb_info,
        images_in_order=[
            OriginalPage(key, PageType[config["pages"][key]]) for key in config["pages"]
        ],
    )

    if not os.path.isdir(comic.srce_dir):
        raise Exception(f'Could not find srce directory "{comic.srce_dir}".')
    if not os.path.isdir(comic.get_srce_image_dir()):
        raise Exception(f'Could not find srce image directory "{comic.get_srce_image_dir()}".')
    if not os.path.isdir(comic.srce_fixes_dir):
        raise Exception(f'Could not find srce fixup directory "{comic.srce_fixes_dir}".')
    if not os.path.isdir(comic.get_srce_fixes_image_dir()):
        raise Exception(
            f'Could not find srce fixup image directory "{comic.get_srce_fixes_image_dir()}".'
        )

    return comic


def get_inset_filename(ini_file: str, file_title: str) -> str:
    if file_title:
        return file_title + " Inset" + INSET_FILE_EXT

    ini_filename = os.path.splitext(os.path.basename(ini_file))[0]

    return ini_filename + " Inset" + INSET_FILE_EXT


def get_formatted_first_published_str(info: ComicBookInfo) -> str:
    issue = f"{info.issue_name} #{info.issue_number}"

    if info.issue_month == -1:
        issue_date = info.issue_year
    else:
        issue_date = f"{MONTH_AS_LONG_STR[info.issue_month]} {info.issue_year}"

    return f"{issue}, {issue_date}"


def get_formatted_submitted_date(info: ComicBookInfo) -> str:
    if info.submitted_day == -1:
        return f", {MONTH_AS_LONG_STR[info.submitted_month]} {info.submitted_year}"

    return (
        f" on {MONTH_AS_LONG_STR[info.submitted_month]}"
        f" {get_formatted_day(info.submitted_day)}, {info.submitted_year}"
    )
