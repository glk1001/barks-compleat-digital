import logging
import sys
from typing import Tuple, List

import kivy.core.text
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo
from filtered_title_lists import FilteredTitleLists

Builder.load_file("tree-example.kv")


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


def get_display_title(title: Tuple[str, FantaComicBookInfo]) -> str:
    return title[0] if title[1].comic_book_info.is_barks_title else f"({title[0]})"


class MainScreen(BoxLayout):
    intro_text = ObjectProperty(text="hello line 1\nhello line 2\nhello line 3\n")
    reader_contents = ObjectProperty()

    def pressed(self, button: Button):
        if button.text == "Introduction":
            self.intro_text.opacity = 1.0
        else:
            self.intro_text.opacity = 0.0

        print(f'"{type(button)}" "{button.text}" pressed.')

    def title_row_button_pressed(self, button: Button):
        self.intro_text.opacity = 0.0

        print(
            f'Title row button "{button.text}" pressed.'
            f" num = {button.parent.num_label.text},"
            f' title = "{button.parent.title_label.text}".'
            f' issue = "{button.parent.issue_label.text}"'
        )


class ReaderTreeView(TreeView):
    TREE_VIEW_INDENT_LEVEL = dp(40)


class MainTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = (1.0, 0.0, 0.0, 1.0)
    BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)
    NODE_SIZE = (dp(100), dp(30))


class CategoryTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = (1.0, 0.0, 0.0, 1.0)
    BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)
    NODE_WIDTH = dp(170)
    NODE_HEIGHT = dp(30)


class YearRangeTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = (1.0, 0.0, 0.0, 1.0)
    BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)
    NODE_WIDTH = dp(100)
    NODE_HEIGHT = dp(30)


class TreeViewButton(Button):
    pass


class TitleTreeViewLabel(Button):
    pass


class TitleTreeViewNode(BoxLayout, TreeViewNode):
    LABEL_BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)
    LABEL_HEIGHT = dp(30)


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.filtered_title_lists = FilteredTitleLists()

        self.main_screen = None

        self.label_height = 30
        self.main_screen_label_width = 90

        Window.size = (1500, 800)
        Window.left = 300
        Window.top = 200

    def build(self):
        self.main_screen = MainScreen()

        self.build_main_screen_tree()

        return self.main_screen

    def build_main_screen_tree(self):
        tree = self.main_screen.reader_contents_tree

        intro_label = MainTreeViewNode(text="Introduction")
        intro_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(intro_label)

        the_stories_label = MainTreeViewNode(text="The Stories")
        the_stories_label.bind(on_press=self.main_screen.pressed)
        the_stories_node = tree.add_node(the_stories_label)
        self.add_story_nodes(tree, the_stories_node)

        search_label = MainTreeViewNode(text="Search")
        search_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(search_label)

        appendix_label = MainTreeViewNode(text="Appendix")
        appendix_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(appendix_label)

        index_label = MainTreeViewNode(text="Index")
        index_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(index_label)

        tree.bind(minimum_height=tree.setter("height"))

    def add_story_nodes(self, tree, the_stories_node):
        by_year_label = CategoryTreeViewNode(text="Chronological by Year")
        by_year_label.bind(on_press=self.main_screen.pressed)
        self.add_year_range_nodes(tree, by_year_label)
        the_years_node = tree.add_node(by_year_label, parent=the_stories_node)
        self.add_year_range_nodes(tree, the_years_node)

        dda_label = CategoryTreeViewNode(text="Donald Duck Adventures")
        dda_label.bind(on_press=self.main_screen.pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_range_nodes(self, tree, the_years_node):
        titles = self.filtered_title_lists.get_title_lists()

        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            year_range_label = YearRangeTreeViewNode(text=range_str)
            year_range_label.bind(on_press=self.main_screen.pressed)

            year_range_node = tree.add_node(year_range_label, parent=the_years_node)
            self.add_year_range_story_nodes(tree, year_range_node, titles[range_str])

    def add_year_range_story_nodes(
        self, tree, year_range_node, titles: List[Tuple[str, FantaComicBookInfo]]
    ):
        for title in titles:
            tree.add_node(self.get_title_tree_view_node(title), parent=year_range_node)

    def add_dda_story_nodes(self, tree, dda_node):
        titles = self.filtered_title_lists.get_title_lists()

        for title in titles["Donald Duck Adventures"]:
            tree.add_node(self.get_title_tree_view_node(title), parent=dda_node)

    def get_title_tree_view_node(self, title: Tuple[str, FantaComicBookInfo]) -> TitleTreeViewNode:
        fanta_info = title[1]

        title_node = TitleTreeViewNode()

        title_node.num_label.text = str(fanta_info.fanta_chronological_number)
        title_node.num_label.bind(on_press=self.main_screen.title_row_button_pressed)

        title_node.issue_label.text = fanta_info.comic_book_info.get_issue_title()
        title_node.issue_label.bind(on_press=self.main_screen.title_row_button_pressed)

        title_node.title_label.text = get_display_title(title)
        title_node.title_label.bind(on_press=self.main_screen.title_row_button_pressed)

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
