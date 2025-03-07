import argparse
from dataclasses import dataclass
from enum import Flag, auto
from typing import List, Tuple

from intspan import intspan

from .comics_database import ComicsDatabase, get_default_comics_database_dir
from .comics_info import ComicBookInfo
from .comics_utils import get_titles_sorted_by_submission_date

LOG_LEVEL_ARG = "--log-level"
COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"
TITLE_ARG = "--title"
WORK_DIR_ARG = "--work-dir"
PAGE_ARG = "--page"


class CmdArgNames(Flag):
    COMICS_DATABASE_DIR = auto()
    VOLUME = auto()
    TITLE = auto()
    WORK_DIR = auto()
    PAGE = auto()


@dataclass
class ExtraArg:
    name: str
    action: str
    type: any
    default: any


class CmdArgs:
    def __init__(
        self,
        description: str,
        required_args: CmdArgNames = CmdArgNames.COMICS_DATABASE_DIR,
        extra_args: List[ExtraArg] = None,
    ):
        self._description = description
        self._required_args = required_args
        self.extra_args = extra_args if extra_args else []
        self._error_msg = ""
        self._cmd_args = self._get_args()
        self._comics_database = ComicsDatabase(self._cmd_args.comics_database_dir)

    def args_are_valid(self) -> Tuple[bool, str]:
        if not self._error_msg:
            return True, ""
        return False, self._error_msg

    def get_log_level(self) -> str:
        return self._cmd_args.log_level

    def get_comics_database(self) -> ComicsDatabase:
        return self._comics_database

    def get_title(self) -> str:
        if CmdArgNames.TITLE not in self._required_args:
            raise Exception(f"'{TITLE_ARG}' was not specified as an argument.")
        return self._cmd_args.title

    def get_titles(self, submission_date_sorted=True, configured_only=True) -> List[str]:
        titles_and_info = self.get_titles_and_info(configured_only)

        if submission_date_sorted:
            return get_titles_sorted_by_submission_date(titles_and_info)

        return [t[0] for t in titles_and_info]

    def get_titles_and_info(self, configured_only=True) -> List[Tuple[str, ComicBookInfo]]:
        if (
            CmdArgNames.TITLE not in self._required_args
            and CmdArgNames.VOLUME not in self._required_args
        ):
            raise Exception(
                f"One of '{TITLE_ARG}' or '{VOLUME_ARG}' were not specified as an argument."
            )

        if self._cmd_args.title:
            cb_info = self._comics_database.get_comic_book_info(self._cmd_args.title)
            return [(self._cmd_args.title, cb_info)]

        assert self._cmd_args.volume is not None
        vol_list = list(intspan(self._cmd_args.volume))

        if configured_only:
            return self._comics_database.get_configured_titles_in_fantagraphics_volumes(vol_list)

        return self._comics_database.get_all_titles_in_fantagraphics_volumes(vol_list)

    def get_work_dir(self) -> str:
        if CmdArgNames.WORK_DIR not in self._required_args:
            raise Exception(f"'{WORK_DIR_ARG}' was not specified as an argument.")
        return self._cmd_args.work_dir

    def one_or_more_volumes(self) -> bool:
        return self._cmd_args.volume is not None

    def get_volume(self) -> str:
        volumes = self.get_volumes()
        if len(volumes) > 1:
            raise Exception(f"'{VOLUME_ARG}' specified more than one volume.")

        return volumes[0]

    def get_volumes(self) -> List[str]:
        if CmdArgNames.VOLUME not in self._required_args:
            raise Exception(f"'{VOLUME_ARG}' was not specified as an argument.")

        assert self._cmd_args.volume is not None
        return list(intspan(self._cmd_args.volume))

    def get_pages(self) -> List[str]:
        if CmdArgNames.PAGE not in self._required_args:
            raise Exception(f"'{PAGE_ARG}' was not specified as an argument.")

        assert self._cmd_args.page is not None
        return list(intspan(self._cmd_args.page))

    def get_extra_arg(self, name: str) -> any:
        return getattr(self._cmd_args, name[2:])

    def _get_args(self):
        parser = argparse.ArgumentParser(description=self._description)

        parser.add_argument(
            LOG_LEVEL_ARG,
            action="store",
            type=str,
            default="INFO",
        )
        parser.add_argument(
            COMICS_DATABASE_DIR_ARG,
            action="store",
            type=str,
            default=get_default_comics_database_dir(),
        )
        parser.add_argument(
            VOLUME_ARG,
            action="store",
            type=str,
            required=False,
        )
        parser.add_argument(
            WORK_DIR_ARG,
            action="store",
            type=str,
            required=False,
        )
        parser.add_argument(
            TITLE_ARG,
            action="store",
            type=str,
            required=False,
        )
        parser.add_argument(
            PAGE_ARG,
            action="store",
            type=str,
            required=False,
        )

        for extra in self.extra_args:
            parser.add_argument(
                extra.name,
                action=extra.action,
                type=extra.type,
                default=extra.default,
                required=False,
            )

        args = parser.parse_args()

        self._validate(args)

        return args

    def _validate(self, args) -> None:
        if args.volume and args.title:
            self._error_msg = f"You must specify only one of '{VOLUME_ARG}' or '{TITLE_ARG}."
            return

        if args.volume and args.page:
            self._error_msg = f"You cannot specify '{PAGE_ARG}' with '{VOLUME_ARG}'."
            return

        if CmdArgNames.VOLUME in self._required_args and (
            not args.volume and CmdArgNames.TITLE not in self._required_args
        ):
            self._error_msg = f"You must specify a '{VOLUME_ARG}' argument."
            return
        if CmdArgNames.TITLE in self._required_args and (
            not args.title and CmdArgNames.VOLUME not in self._required_args
        ):
            self._error_msg = f"You must specify a '{TITLE_ARG}' argument."
            return
        if CmdArgNames.WORK_DIR in self._required_args and not args.work_dir:
            self._error_msg = f"You must specify a '{WORK_DIR_ARG}' argument."
            return
        if CmdArgNames.PAGE in self._required_args and not args.page:
            self._error_msg = f"You must specify a '{PAGE_ARG}' argument."
            return

        if CmdArgNames.VOLUME not in self._required_args and args.volume:
            self._error_msg = f"Unexpected argument: '{VOLUME_ARG}'."
            return
        if CmdArgNames.TITLE not in self._required_args and args.title:
            self._error_msg = f"Unexpected argument: '{TITLE_ARG}'."
            return
        if CmdArgNames.WORK_DIR not in self._required_args and args.work_dir:
            self._error_msg = f"Unexpected argument: '{WORK_DIR_ARG}'."
            return
        if CmdArgNames.PAGE not in self._required_args and args.page:
            self._error_msg = f"Unexpected argument: '{PAGE_ARG}'."
            return
