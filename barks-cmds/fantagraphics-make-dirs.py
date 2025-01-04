import logging
import sys

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_utils import setup_logging

setup_logging(logging.INFO)

cmd_args = CmdArgs("Make required Fantagraphics directories.")
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

comics_database = cmd_args.get_comics_database()

comics_database.make_all_fantagraphics_directories()
