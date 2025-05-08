import logging
import sys
from typing import List

from barks_fantagraphics.barks_titles import BARKS_TITLE_INFO
from barks_fantagraphics.comics_cmd_args import CmdArgs, ExtraArg
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.title_search import BarksTitleSearch, unique_extend

extra_args: List[ExtraArg] = [
    ExtraArg("--prefix", action="store", type=str, default=""),
    ExtraArg("--word", action="store", type=str, default=""),
    ExtraArg("--sort", action="store_true", type=bool, default=False),
]

cmd_args = CmdArgs("Find title", extra_args=extra_args)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()
prefix = cmd_args.get_extra_arg("--prefix")
word = cmd_args.get_extra_arg("--word")

title_search = BarksTitleSearch()

titles = []

if prefix:
    unique_extend(titles, title_search.get_titles(prefix))
if word:
    unique_extend(titles, title_search.get_titles_containing(word))

if not titles:
    print(f"No titles found.")
else:
    title_info_list = []
    for title in titles:
        title_info_list.append(BARKS_TITLE_INFO[title])

    if cmd_args.get_extra_arg("--sort"):
        title_info_list = sorted(title_info_list, key=lambda x: x.title_str)

    for info in title_info_list:
        print(info.get_display_title())
