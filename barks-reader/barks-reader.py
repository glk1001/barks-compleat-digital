import logging
import sys
from pathlib import Path

import kivy.core.text
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import setup_logging
from filtered_title_lists import FilteredTitleLists
from main_screen import MainScreen
from reader_tree_builder import ReaderTreeBuilder
from reader_ui_classes import ReaderTreeBuilderEventDispatcher

KV_FILE = Path(__file__).stem + ".kv"

APP_TITLE = "The Compleat Barks Reader"

# TODO: how to nicely handle main window
DEFAULT_ASPECT_RATIO = 1.5
DEFAULT_WINDOW_HEIGHT = 1000
DEFAULT_WINDOW_WIDTH = int(round(DEFAULT_WINDOW_HEIGHT / DEFAULT_ASPECT_RATIO))
DEFAULT_LEFT_POS = 400
DEFAULT_TOP_POS = 50


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, main_screen: MainScreen, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.main_screen = main_screen

        Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        Window.left = DEFAULT_LEFT_POS
        Window.top = DEFAULT_TOP_POS

    def on_request_close_window(self, *_args):
        return self.main_screen.comic_reader.on_app_request_close()

    def on_action_bar_quit(self):
        if self.main_screen.comic_reader.on_app_request_close() == True:
            return
        App.get_running_app().stop()
        Window.close()

    def build(self):
        logging.debug("Building app...")

        Window.bind(on_request_close=self.on_request_close_window)

        Window.custom_titlebar = True
        title_bar = self.main_screen.ids.action_bar
        if Window.set_custom_titlebar(title_bar):
            logging.info("Window: setting custom titlebar successful")
        else:
            logging.info("Window: setting custom titlebar " "Not allowed on this system ")

        Clock.schedule_once(self.main_screen.popup.open, 0)

        logging.debug("Building the tree view...")
        tree_builder = ReaderTreeBuilder(self.main_screen)
        tree_builder.build_main_screen_tree()

        self.title = APP_TITLE

        self.main_screen.year_range_nodes = tree_builder.year_range_nodes

        logging.debug("Finished building.")

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

    logging.debug("Loading kv files...")
    Builder.load_file(KV_FILE)

    logging.debug("Instantiating main screen...")
    comics_database = cmd_args.get_comics_database()
    filtered_title_lists = FilteredTitleLists()
    reader_tree_events = ReaderTreeBuilderEventDispatcher()
    the_main_screen = MainScreen(reader_tree_events, filtered_title_lists)

    logging.debug("Running kivy app...")
    BarksReaderApp(comics_database, the_main_screen).run()

    logging.debug("Terminating...")
