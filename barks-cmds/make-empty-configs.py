import logging
import os.path
import sys
from typing import List, Tuple

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo, get_fanta_volume_str
from barks_fantagraphics.comics_utils import setup_logging, get_abbrev_path


def get_issue_titles(
    title_info_list: List[Tuple[str, FantaComicBookInfo]]
) -> List[Tuple[str, bool, bool]]:
    comic_issue_title_info_list = []
    for title_info in title_info_list:
        ttl = title_info[0]
        cb_info = title_info[1]
        is_configured, _ = comics_database.is_story_title(ttl)
        comic_issue_title_info_list.append((ttl, is_configured, cb_info.is_barks_title))

    return comic_issue_title_info_list


def create_empty_config_file(ttl: str, is_barks_ttl: bool) -> None:
    ini_file = comics_database.get_ini_file(ttl)
    # ini_file = os.path.join("/tmp", ttl + ".ini")
    if os.path.exists(ini_file):
        raise Exception(f'Ini file "{ini_file}" already exists.')

    logging.info(f'Creating empty config file: "{get_abbrev_path(ini_file)}".')
    with open(ini_file, "w") as f:
        f.write(f"[info]\n")
        if is_barks_ttl:
            f.write(f"title = {ttl}\n")
        else:
            f.write(f"title =\n")
        f.write(f"source_comic = {get_fanta_volume_str(volume)}\n")
        f.write(f"\n")
        f.write(f"[pages]\n")
        f.write(f"title_empty = TITLE\n")
        f.write(f"? - ? = BODY\n")


cmd_args = CmdArgs("Make empty configs", CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()
volume = int(cmd_args.get_volume())

titles_and_info = cmd_args.get_titles_and_info(configured_only=False)
titles_config_info = get_issue_titles(titles_and_info)

titles = []
for title_config_info in titles_config_info:
    title = title_config_info[0]
    title_is_configured = title_config_info[1]
    is_barks_title = title_config_info[2]

    if title_is_configured:
        logging.info(f'Title: "{title}" is already configured - skipping.')
        continue

    titles.append((title, is_barks_title))

logging.info("")
for title, is_barks_title in titles:
    create_empty_config_file(title, is_barks_title)
