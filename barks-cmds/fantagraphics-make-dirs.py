import logging
import sys

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_logging import setup_logging

cmd_args = CmdArgs("Make required Fantagraphics directories.")
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

comics_database.make_all_fantagraphics_directories()
