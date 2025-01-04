import logging
import sys

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging

cmd_args = CmdArgs("Verify title", CmdArgNames.TITLE)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()
title = cmd_args.get_title()

found, titles, close = comics_database.get_story_title_from_issue(title)
if found:
    titles_str = ", ".join([f'"{t}"' for t in titles])
    print(f'This is an issue title: "{title}" -> title: {titles_str}')
elif close:
    print(f'"{title}" is not a valid issue title. Did you mean: "{close}".')
else:
    found, close = comics_database.is_story_title(title)
    if found:
        print(f'This is a valid title: "{title}".')
    elif close:
        print(f'"{title}" is not a valid title. Did you mean: "{close}".')
    else:
        print(f'"{title}" is not a valid title. Cannot find anything close to this.')
