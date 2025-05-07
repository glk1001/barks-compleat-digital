import logging
import os.path
import sys
from enum import Enum, auto
from random import randrange
from typing import List, Union

import kivy.core.text
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import (
    setup_logging,
    get_short_formatted_submitted_date,
    get_short_formatted_first_published_str,
    get_dest_comic_zip_file_stem,
    get_formatted_first_published_str,
    get_long_formatted_submitted_date,
)
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo, FAN, FANTA_SOURCE_COMICS
from file_paths import (
    get_mcomix_python_bin_path,
    get_mcomix_path,
    get_mcomix_barks_reader_config_path,
    get_the_comic_zips_dir,
    get_comic_inset_file,
    get_comic_cover_file,
    get_comic_splash_files,
    get_comic_silhouette_files,
    EMERGENCY_INSET_FILE,
)
from filtered_title_lists import FilteredTitleLists
from mcomix_reader import ComicReader

APP_TITLE = "The Compleat Barks Reader"

Builder.load_file("tree-example.kv")


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


def get_display_title(fanta_info: FantaComicBookInfo) -> str:
    return (
        fanta_info.comic_book_info.title
        if fanta_info.comic_book_info.is_barks_title
        else f"({fanta_info.comic_book_info.title})"
    )


TREE_VIEW_NODE_TEXT_COLOR = (1, 1, 1, 1)
TREE_VIEW_NODE_SELECTED_COLOR = (1, 0, 1, 0.8)
TREE_VIEW_NODE_BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)


class ReaderTreeView(TreeView):
    TREE_VIEW_INDENT_LEVEL = dp(30)


class TitlePageImage(ButtonBehavior, Image):
    TITLE_IMAGE_X_FRAC_OF_PARENT = 0.98
    TITLE_IMAGE_Y_FRAC_OF_PARENT = 0.98 * 0.97


class MainTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = TREE_VIEW_NODE_TEXT_COLOR
    SELECTED_COLOR = TREE_VIEW_NODE_SELECTED_COLOR
    BACKGROUND_COLOR = TREE_VIEW_NODE_BACKGROUND_COLOR
    NODE_SIZE = (dp(100), dp(30))


class CategoryTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = TREE_VIEW_NODE_TEXT_COLOR
    SELECTED_COLOR = TREE_VIEW_NODE_SELECTED_COLOR
    BACKGROUND_COLOR = TREE_VIEW_NODE_BACKGROUND_COLOR
    NODE_WIDTH = dp(170)
    NODE_HEIGHT = dp(30)


class YearRangeTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = TREE_VIEW_NODE_TEXT_COLOR
    SELECTED_COLOR = TREE_VIEW_NODE_SELECTED_COLOR
    BACKGROUND_COLOR = TREE_VIEW_NODE_BACKGROUND_COLOR
    NODE_WIDTH = dp(100)
    NODE_HEIGHT = dp(30)


class TitleTreeViewNode(BoxLayout, TreeViewNode):
    TEXT_COLOR = TREE_VIEW_NODE_TEXT_COLOR
    SELECTED_COLOR = TREE_VIEW_NODE_SELECTED_COLOR
    BACKGROUND_COLOR = TREE_VIEW_NODE_BACKGROUND_COLOR
    ROW_BACKGROUND_COLOR = BACKGROUND_COLOR
    EVEN_COLOR = [0, 0, 0.4, 0.4]
    ODD_COLOR = [0, 0, 1.0, 0.4]

    ROW_HEIGHT = dp(30)
    NUM_LABEL_WIDTH = dp(40)
    TITLE_LABEL_WIDTH = dp(400)
    ISSUE_LABEL_WIDTH = TITLE_LABEL_WIDTH

    NUM_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)
    TITLE_LABEL_COLOR = (1.0, 1.0, 0.0, 1.0)
    ISSUE_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)

    def __init__(self, fanta_info: FantaComicBookInfo, **kwargs):
        super().__init__(**kwargs)
        self.fanta_info = fanta_info


class TreeViewButton(Button):
    pass


class TitleTreeViewLabel(Button):
    pass


class ScreenCategories(Enum):
    INITIAL = auto()
    INTRO = auto()
    THE_STORIES = auto()
    SEARCH = auto()
    APPENDIX = auto()
    INDEX = auto()
    CHRONO_BY_YEAR = auto()
    YEAR_RANGE = auto()
    DDA = auto()


class MainScreen(BoxLayout):
    TITLE_INFO_LABEL_COLOR = (0.0, 1.0, 1.0, 1.0)
    TITLE_EXTRA_INFO_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)
    DEBUG_BACKGROUND_OPACITY = 0

    top_view_image = ObjectProperty()
    top_view_image_bg = ColorProperty()
    bottom_view = ObjectProperty()
    bottom_view_before_image = ObjectProperty()
    bottom_view_before_image_bg = ColorProperty()
    bottom_view_after_image_bg = ColorProperty()

    BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG = (1, 0, 0, 1.0)
    BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG = (1, 0, 0, 0.0)

    intro_text = ObjectProperty()
    reader_contents = ObjectProperty()
    title_page_image = ObjectProperty()
    title_page_button = ObjectProperty()
    main_title = ObjectProperty()
    title_info = ObjectProperty()

    def __init__(self, filtered_title_lists: FilteredTitleLists, **kwargs):
        super().__init__(**kwargs)

        self.filtered_title_lists = filtered_title_lists

        self.fanta_info: Union[FantaComicBookInfo, None] = None
        self.title_page_button.visible = True

        self.comic_reader = ComicReader(
            get_mcomix_python_bin_path(),
            get_mcomix_path(),
            get_mcomix_barks_reader_config_path(),
            get_the_comic_zips_dir(),
        )

        self.bottom_view_before_image = ""

        self.bottom_view_before_image_bg = (1, 0, 0, 0.5)
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.top_view_image_bg = (1, 1, 1, 0.5)

        self.bottom_view.opacity = 1.0

        self.current_screen_category = ScreenCategories.INITIAL
        self.current_year_range = ""

        self.top_view_change_event = None
        self.bottom_view_change_after_event = None

        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def node_expanded(self, tree: ReaderTreeView, node: TreeViewNode):
        if isinstance(node, YearRangeTreeViewNode):
            self.current_screen_category = ScreenCategories.YEAR_RANGE
            self.current_year_range = node.text
            self.set_next_top_view_image()
            self.set_next_bottom_view_image()
        elif isinstance(node, CategoryTreeViewNode):
            if node.text == "Donald Duck Adventures":
                self.current_screen_category = ScreenCategories.DDA
                self.set_next_top_view_image()
                self.set_next_bottom_view_image()

    def image_pressed(self):
        if self.fanta_info is None:
            self.intro_text.opacity = 0.0
            print(f'Image "{self.title_page_image.source}" pressed. No title selected.')
            return

        if self.comic_reader.reader_is_running:
            print(f'Image "{self.title_page_image.source}" pressed. Already reading comic.')
            return

        comic_file_stem = get_dest_comic_zip_file_stem(
            self.fanta_info.comic_book_info.title,
            self.fanta_info.fanta_chronological_number,
            self.fanta_info.get_short_issue_title(),
        )

        print(f'Image "{self.title_page_image.source}" pressed. Want to run "{comic_file_stem}".')

        self.comic_reader.show_comic(comic_file_stem)

        print(f"Exited image press.")

    def intro_pressed(self, button: Button):
        self.bottom_view.opacity = 0.0
        self.intro_text.opacity = 1.0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG

        self.current_screen_category = ScreenCategories.INTRO
        self.intro_text.text = "hello line 1\nhello line 2\nhello line 3\n"

        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def the_stories_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.THE_STORIES
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def search_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.SEARCH
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def appendix_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.APPENDIX
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def index_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.INDEX
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def chrono_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.CHRONO_BY_YEAR
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def dda_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_screen_category = ScreenCategories.DDA
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def year_range_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG

        self.current_year_range = button.text
        self.current_screen_category = ScreenCategories.YEAR_RANGE
        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def title_row_button_pressed(self, button: Button):
        self.bottom_view.opacity = 1.0
        self.intro_text.opacity = 0.0
        self.bottom_view_after_image_bg = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG

        self.fanta_info = button.parent.fanta_info
        title = self.fanta_info.comic_book_info.title

        comic_inset_file = get_comic_inset_file(title)
        title_info_image = self.get_title_info_image(title)

        print(
            f'Title row button "{button.text}" pressed. Inset file = "{comic_inset_file}", '
            f'title info image = "{title_info_image}".'
        )

        self.main_title.text = get_display_title(button.parent.fanta_info)
        self.title_info.text = self.get_title_info()
        self.title_page_image.source = comic_inset_file
        self.bottom_view_before_image = title_info_image
        self.title_page_button.visible = True

    #        self.set_next_top_view_image()

    def get_title_info_image(self, title: str) -> str:
        num_categories = 3
        silhouette_percent = int(round(100 / num_categories))
        splashes_percent = 2 * int(round(100 / num_categories))
        covers_percent = 3 * int(round(100 / num_categories))

        for num_attempts in range(10):
            rand_percent = randrange(0, 100)
            print(f"Attempt {num_attempts}: rand percent = {rand_percent}.")

            if rand_percent <= silhouette_percent:
                title_files = get_comic_silhouette_files(title)
                if title_files:
                    index = randrange(0, len(title_files))
                    return title_files[index]
                silhouette_percent = -1
                print(f"No silhouettes.")

            if rand_percent <= splashes_percent:
                title_files = get_comic_splash_files(title)
                if title_files:
                    index = randrange(0, len(title_files))
                    return title_files[index]
                splashes_percent = -1
                print(f"No splashes.")

            if rand_percent <= covers_percent:
                title_file = get_comic_cover_file(title)
                if title_file:
                    return title_file
                covers_percent = -1
                print(f"No covers.")

            if silhouette_percent == -1 and splashes_percent == -1 and covers_percent == -1:
                break

        return get_comic_inset_file(EMERGENCY_INSET_FILE)

    def get_title_info(self) -> str:
        issue_info = get_formatted_first_published_str(self.fanta_info)
        submitted_info = get_long_formatted_submitted_date(self.fanta_info)
        fanta_book = FANTA_SOURCE_COMICS[self.fanta_info.fantagraphics_volume]
        source = f"{FAN} CBDL, Vol {fanta_book.volume}, {fanta_book.year}"
        return (
            f"[i]1st Issue:[/i]   [b]{issue_info}[/b]\n"
            f"[i]Submitted:[/i] [b]{submitted_info}[/b]\n"
            f"[i]Source:[/i]       [b]{source}[/b]"
        )

    def set_next_top_view_image(self):
        if self.current_screen_category == ScreenCategories.INITIAL:
            self.top_view_image.source = get_comic_inset_file("A Cold Bargain")
        elif self.current_screen_category == ScreenCategories.INTRO:
            self.top_view_image.source = get_comic_inset_file("Adventure Down Under")
        elif self.current_screen_category == ScreenCategories.THE_STORIES:
            self.top_view_image.source = self.get_random_image("All")
        elif self.current_screen_category == ScreenCategories.SEARCH:
            self.top_view_image.source = get_comic_inset_file("Tracking Sandy")
        elif self.current_screen_category == ScreenCategories.APPENDIX:
            self.top_view_image.source = get_comic_inset_file("The Fabulous Philosopher's Stone")
        elif self.current_screen_category == ScreenCategories.INDEX:
            self.top_view_image.source = get_comic_inset_file("Truant Officer Donald")
        elif self.current_screen_category == ScreenCategories.CHRONO_BY_YEAR:
            self.top_view_image.source = self.get_random_image("All")
        elif self.current_screen_category == ScreenCategories.DDA:
            self.top_view_image.source = self.get_random_image("Donald Duck Adventures")
        elif self.current_screen_category == ScreenCategories.YEAR_RANGE:
            print(f"Year range: {self.current_year_range}")
            if not self.current_year_range:
                self.top_view_image.source = get_comic_inset_file("Good Neighbors")
            else:
                self.top_view_image.source = self.get_random_image(self.current_year_range)
        else:
            assert False

        print(
            f"Category: {self.current_screen_category}."
            f" Image: '{os.path.basename(self.top_view_image.source)}'."
        )

        self.set_next_top_view_image_bg()
        self.schedule_top_view_event()

    def get_random_image(self, title_category: str) -> str:
        titles = self.filtered_title_lists.get_title_lists()[title_category]
        title_index = randrange(0, len(titles))
        title_image = get_comic_inset_file(titles[title_index].comic_book_info.title)

        return title_image

    def set_next_top_view_image_bg(self):
        random_color = (
            randrange(100, 255) / 255.0,
            randrange(100, 255) / 255.0,
            randrange(100, 255) / 255.0,
            randrange(220, 250) / 255.0,
        )
        self.top_view_image_bg = random_color
        print(f"Top view image bg = {self.top_view_image_bg}")

    def set_next_bottom_view_image(self):
        self.bottom_view_after_image.source = self.get_random_image("All")
        print(
            f"Bottom view after image: '{os.path.basename(self.bottom_view_after_image.source)}'."
        )

        self.set_next_bottom_view_after_image_bg()
        self.schedule_bottom_view_after_event()

    def set_next_bottom_view_after_image_bg(self):
        rand_index = randrange(0, 3)
        rand_color_val = randrange(230, 255) / 255.0
        rand_color = [0, 0, 0, self.bottom_view_after_image_bg[3]]
        rand_color[rand_index] = rand_color_val

        self.bottom_view_after_image_bg = tuple(rand_color)
        print(f"Bottom view after image bg = {self.bottom_view_after_image_bg}")

    def schedule_top_view_event(self):
        if self.top_view_change_event:
            self.top_view_change_event.cancel()

        self.top_view_change_event = Clock.schedule_interval(
            lambda dt: self.set_next_top_view_image(), 10.0
        )

    def schedule_bottom_view_after_event(self):
        if self.bottom_view_change_after_event:
            self.bottom_view_change_after_event.cancel()

        self.bottom_view_change_after_event = Clock.schedule_interval(
            lambda dt: self.set_next_bottom_view_image(), 10.0
        )


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.filtered_title_lists = FilteredTitleLists()

        self.main_screen: Union[MainScreen, None] = None

        # TODO: how to nicely handle main window
        DEFAULT_ASPECT_RATIO = 1.5
        DEFAULT_WINDOW_HEIGHT = 1000
        DEFAULT_WINDOW_WIDTH = int(round(DEFAULT_WINDOW_HEIGHT / DEFAULT_ASPECT_RATIO))
        DEFAULT_LEFT_POS = 400
        DEFAULT_TOP_POS = 50
        Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        Window.left = DEFAULT_LEFT_POS
        Window.top = DEFAULT_TOP_POS

    def on_request_close_window(self, *args):
        return self.main_screen.comic_reader.on_app_request_close()

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.main_screen = MainScreen(self.filtered_title_lists)

        self.build_main_screen_tree()

        self.title = APP_TITLE

        return self.main_screen

    def build_main_screen_tree(self):
        tree = self.main_screen.reader_contents_tree

        tree.bind(on_node_expand=self.main_screen.node_expanded)

        intro_label = MainTreeViewNode(text="Introduction")
        intro_label.bind(on_press=self.main_screen.intro_pressed)
        tree.add_node(intro_label)

        the_stories_label = MainTreeViewNode(text="The Stories")
        the_stories_label.bind(on_press=self.main_screen.the_stories_pressed)
        the_stories_node = tree.add_node(the_stories_label)
        self.add_story_nodes(tree, the_stories_node)

        search_label = MainTreeViewNode(text="Search")
        search_label.bind(on_press=self.main_screen.search_pressed)
        tree.add_node(search_label)

        appendix_label = MainTreeViewNode(text="Appendix")
        appendix_label.bind(on_press=self.main_screen.appendix_pressed)
        tree.add_node(appendix_label)

        index_label = MainTreeViewNode(text="Index")
        index_label.bind(on_press=self.main_screen.index_pressed)
        tree.add_node(index_label)

        tree.bind(minimum_height=tree.setter("height"))

    def add_story_nodes(self, tree, the_stories_node):
        by_year_label = CategoryTreeViewNode(text="Chronological by Year")
        by_year_label.bind(on_press=self.main_screen.chrono_pressed)
        the_years_node = tree.add_node(by_year_label, parent=the_stories_node)
        self.add_year_range_nodes(tree, the_years_node)

        dda_label = CategoryTreeViewNode(text="Donald Duck Adventures")
        dda_label.bind(on_press=self.main_screen.dda_pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_range_nodes(self, tree, the_years_node):
        title_lists = self.filtered_title_lists.get_title_lists()

        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            year_range_label = YearRangeTreeViewNode(text=range_str)
            year_range_label.bind(on_press=self.main_screen.year_range_pressed)

            year_range_node = tree.add_node(year_range_label, parent=the_years_node)
            self.add_year_range_story_nodes(tree, year_range_node, title_lists[range_str])

    def add_year_range_story_nodes(
        self, tree, year_range_node, title_list: List[FantaComicBookInfo]
    ):
        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=year_range_node)

    def add_dda_story_nodes(self, tree, dda_node):
        title_list = self.filtered_title_lists.get_title_lists()["Donald Duck Adventures"]

        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=dda_node)

    def get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
        title_node = TitleTreeViewNode(full_fanta_info)

        title_node.num_label.text = str(full_fanta_info.fanta_chronological_number)
        title_node.num_label.bind(on_press=self.main_screen.title_row_button_pressed)

        title_node.num_label.color_selected = (0, 0, 1, 1)

        title_node.title_label.text = get_display_title(full_fanta_info)
        title_node.title_label.bind(on_press=self.main_screen.title_row_button_pressed)

        issue_info = (
            f"{get_short_formatted_first_published_str(full_fanta_info)}"
            f"  [{get_short_formatted_submitted_date(full_fanta_info)}]"
        )

        title_node.issue_label.text = issue_info
        title_node.issue_label.bind(on_press=self.main_screen.title_row_button_pressed)

        return title_node


if __name__ == "__main__":
    # TODO(glk): Some issue with type checking inspection?
    # noinspection PyTypeChecker
    cmd_args = CmdArgs("Fantagraphics source files")
    args_ok, error_msg = cmd_args.args_are_valid()
    if not args_ok:
        logging.error(error_msg)
        sys.exit(1)

    setup_logging(cmd_args.get_log_level())

    comics_database = cmd_args.get_comics_database()

    BarksReaderApp(comics_database).run()
