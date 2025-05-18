import logging
import sys
from typing import Union

import kivy.core.text
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.title_search import BarksTitleSearch
from filtered_title_lists import FilteredTitleLists
from main_screen import MainScreen
from reader_tree_builder import ReaderTreeBuilder

TOP_VIEW_EVENT_TIMEOUT_SECS = 1000.0
BOTTOM_VIEW_EVENT_TIMEOUT_SECS = 1000.0
APP_TITLE = "The Compleat Barks Reader"

# TODO: how to nicely handle main window
DEFAULT_ASPECT_RATIO = 1.5
DEFAULT_WINDOW_HEIGHT = 1000
DEFAULT_WINDOW_WIDTH = int(round(DEFAULT_WINDOW_HEIGHT / DEFAULT_ASPECT_RATIO))
DEFAULT_LEFT_POS = 400
DEFAULT_TOP_POS = 50

Builder.load_file("barks-reader.kv")


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.filtered_title_lists = FilteredTitleLists()
        self.title_search = BarksTitleSearch()

        self.main_screen: Union[MainScreen, None] = None

        Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        Window.left = DEFAULT_LEFT_POS
        Window.top = DEFAULT_TOP_POS

    def on_request_close_window(self, *_args):
        return self.main_screen.comic_reader.on_app_request_close()

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.main_screen = MainScreen(self.filtered_title_lists)

        tree_builder = ReaderTreeBuilder(self.filtered_title_lists, self.title_search, self.main_screen)
        tree_builder.build_main_screen_tree()

        self.title = APP_TITLE

        return self.main_screen


if __name__ == "__main__":
    # TODO(glk): Some issue with type checking inspection?
    # noinspection PyTypeChecker
    cmd_args = CmdArgs("Fantagraphics source files")
    args_ok, error_msg = cmd_args.args_are_valid()
    if not args_ok:
        logging.error(error_msg)
        sys.exit(1)

    setup_logging(log_level=logging.DEBUG)
#    setup_logging(cmd_args.get_log_level())

    comics_database = cmd_args.get_comics_database()

    BarksReaderApp(comics_database).run()
