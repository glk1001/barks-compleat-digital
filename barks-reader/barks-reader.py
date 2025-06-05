import logging
import sys
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from barks_comic_reader import get_barks_comic_reader
from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import setup_logging
from filtered_title_lists import FilteredTitleLists
from main_screen import MainScreen
from reader_tree_builder import ReaderTreeBuilder
from reader_ui_classes import ReaderTreeBuilderEventDispatcher

APP_TITLE = "The Compleat Barks Reader"
MAIN_SCREEN = "main_screen"
COMIC_READER = "comic_reader"

KV_FILE = Path(__file__).stem + ".kv"

# TODO: how to nicely handle main window
DEFAULT_ASPECT_RATIO = 1.5
DEFAULT_WINDOW_HEIGHT = 1000
DEFAULT_WINDOW_WIDTH = int(round(DEFAULT_WINDOW_HEIGHT / DEFAULT_ASPECT_RATIO))
DEFAULT_LEFT_POS = 400
DEFAULT_TOP_POS = 50


# def get_str_pixel_width(text: str, **kwargs) -> int:
#     return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.screen_manager = ScreenManager()
        self.comics_database = comics_db

        logging.debug("Instantiating main screen...")
        filtered_title_lists = FilteredTitleLists()
        reader_tree_events = ReaderTreeBuilderEventDispatcher()
        self.main_screen = MainScreen(
            reader_tree_events, filtered_title_lists, self.switch_to_comic_reader, name=MAIN_SCREEN
        )

        Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        Window.left = DEFAULT_LEFT_POS
        Window.top = DEFAULT_TOP_POS

    def build(self):
        logging.debug("Building app...")

        self.set_custom_title_bar()
        self.title = APP_TITLE

        self.build_tree_view()

        root = self.screen_manager
        root.add_widget(self.main_screen)
        root.current = MAIN_SCREEN

        comic_reader = get_barks_comic_reader(self.close_comic_reader, COMIC_READER)
        root.add_widget(comic_reader)

        self.main_screen.comic_reader = comic_reader.children[0]

        return root

    @staticmethod
    def on_action_bar_quit():
        App.get_running_app().stop()
        Window.close()

    def switch_to_comic_reader(self):
        self.screen_manager.current = COMIC_READER

    def close_comic_reader(self):
        self.screen_manager.current = MAIN_SCREEN

    def set_custom_title_bar(self):
        Window.custom_titlebar = True
        title_bar = self.main_screen.ids.action_bar
        if Window.set_custom_titlebar(title_bar):
            logging.info("Window: setting custom titlebar successful")
        else:
            logging.info("Window: setting custom titlebar " "Not allowed on this system ")

    def build_tree_view(self):
        Clock.schedule_once(self.main_screen.loading_data_popup.open, 0)

        logging.debug("Building the tree view...")
        tree_builder = ReaderTreeBuilder(self.main_screen)
        tree_builder.build_main_screen_tree()
        self.main_screen.year_range_nodes = tree_builder.year_range_nodes
        logging.debug("Finished building.")


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

    logging.debug("Running kivy app...")
    BarksReaderApp(cmd_args.get_comics_database()).run()

    logging.debug("Terminating...")
