import logging
import os
from typing import List

from barks_fantagraphics.comic_book import ComicBook, get_safe_title
from consts import (
    DEST_JPG_QUALITY,
    DEST_JPG_COMPRESS_LEVEL,
    DEST_TARGET_WIDTH,
    DEST_TARGET_HEIGHT,
    DEST_TARGET_X_MARGIN,
    DEST_TARGET_ASPECT_RATIO,
)


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]


def log_comic_book_params(comic: ComicBook, caching: bool):
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
    logging.info(f'Dest root:           "{comic.get_dest_root_dir()}".')
    logging.info(f'Dest comic dir:      "DEST ROOT/{dest_basename}".')
    logging.info(f'Dest zip root:       "{comic.get_dest_zip_root_dir()}".')
    logging.info(f'Dest comic zip:      "ZIP ROOT/{dest_comic_zip_basename}".')
    logging.info(f'Dest series symlink: "{comic.get_dest_series_comic_zip_symlink()}".')
    logging.info(f'Dest year symlink:   "{comic.get_dest_year_comic_zip_symlink()}".')
    logging.info("")
