import logging
import sys
from typing import Tuple, List

import kivy.core.text
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp, sp
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


class MainScreen(BoxLayout):
    intro_text = ObjectProperty()
    reader_contents = ObjectProperty()

    def pressed(self, button: Button):
        if button.text == "Introduction":
            self.intro_text.opacity = 1.0
        else:
            self.intro_text.opacity = 0.0
        print(f'Button "{button.text}" pressed.')


class ReaderTreeView(TreeView):
    pass


class TreeViewRow(BoxLayout, TreeViewNode):
    pass


class TreeViewButton(Button, TreeViewNode):
    pass


class MainTreeViewNode(Button, TreeViewNode):
    pass


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

        index_label = MainTreeViewNode(text="Introduction")
        index_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(index_label)

        index_label = MainTreeViewNode(text="The Stories")
        index_label.bind(on_press=self.main_screen.pressed)
        the_stories_node = tree.add_node(index_label)
        self.add_story_nodes(tree, the_stories_node)

        index_label = MainTreeViewNode(text="Search")
        index_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(index_label)

        index_label = MainTreeViewNode(text="Appendix")
        index_label.bind(on_press=self.main_screen.pressed)
        tree.add_node(index_label)

        index_label = MainTreeViewNode(text="Index")
        index_label.bind(on_press=self.main_screen.pressed)
        index_node = tree.add_node(index_label)

        tree.bind(minimum_height=tree.setter("height"))

    def add_story_nodes(self, tree, the_stories_node):
        by_year_label = TreeViewButton(
            text="Chronological by Year",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Chronological by Year") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        by_year_label.bind(size=by_year_label.setter("text_size"))
        by_year_label.bind(on_press=self.main_screen.pressed)
        self.add_year_range_nodes(tree, by_year_label)
        the_years_node = tree.add_node(by_year_label, parent=the_stories_node)
        self.add_year_range_nodes(tree, the_years_node)

        dda_label = TreeViewButton(
            text="Donald Duck Adventures",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Donald Duck Adventures") + 30, self.label_height),
            halign="left",
            valign="middle",
        )
        dda_label.bind(size=dda_label.setter("text_size"))
        dda_label.bind(on_press=self.main_screen.pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_range_nodes(self, tree, the_years_node):
        titles = self.filtered_title_lists.get_title_lists()

        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            year_range_label = TreeViewButton(
                text=range_str,
                color=(1.0, 0.0, 0.0, 1.0),
                background_color=(0.0, 0.0, 0.0, 1.0),
                size_hint=(None, None),
                size=(get_str_pixel_width(range_str) + 20, self.label_height),
                halign="left",
                valign="middle",
            )
            year_range_label.bind(size=year_range_label.setter("text_size"))
            year_range_label.bind(on_press=self.main_screen.pressed)
            year_range_node = tree.add_node(year_range_label, parent=the_years_node)
            self.add_year_range_story_nodes(tree, year_range_node, titles[range_str])

    def add_year_range_story_nodes(
        self, tree, year_range_node, titles: List[Tuple[str, FantaComicBookInfo]]
    ):
        TITLE_NUM_COLOR = (1.0, 1.0, 1.0, 1.0)
        TITLE_LABEL_COLOR = (1.0, 1.0, 0.0, 1.0)
        ISSUE_TITLE_LABEL_COLOR = (1.0, 1.0, 1.0, 0.8)
        LABEL_BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)
        NUM_LABEL_HEIGHT = 20
        TITLE_LABEL_WIDTH = 400
        TITLE_LABEL_HEIGHT = 35
        TITLE_FONT_SIZE = 18

        for title in titles:
            fanta_info = title[1]
            display_title = (
                title[0] if fanta_info.comic_book_info.is_barks_title else f"({title[0]})"
            )

            box1 = TreeViewRow(orientation="horizontal", spacing=20)
            box2 = TreeViewRow(orientation="horizontal", spacing=20)
            box_node = TreeViewRow(
                orientation="vertical",
                spacing=5,
                size_hint_y=None,
                height=dp(NUM_LABEL_HEIGHT + TITLE_LABEL_HEIGHT),
            )

            num_label = TreeViewButton(
                text=f"{fanta_info.fanta_chronological_number}",
                bold=True,
                color=TITLE_NUM_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=dp(NUM_LABEL_HEIGHT),
                width=dp(get_str_pixel_width("999") + 20),
                halign="right",
                valign="middle",
            )
            num_label.text_size = (num_label.width, num_label.height)
            num_label.bind(on_press=self.main_screen.pressed)
            box1.add_widget(num_label)

            issue_label = TreeViewButton(
                text=f"{fanta_info.comic_book_info.get_issue_title()}",
                color=ISSUE_TITLE_LABEL_COLOR,
                size_hint=(None, None),
                background_color=LABEL_BACKGROUND_COLOR,
                height=dp(NUM_LABEL_HEIGHT),
                width=dp(get_str_pixel_width("WDCS 500") + 50),
                halign="left",
                valign="middle",
            )
            issue_label.text_size = (issue_label.width, issue_label.height)
            issue_label.bind(on_press=self.main_screen.pressed)
            box1.add_widget(issue_label)

            empty_label = TreeViewButton(
                text="   ",
                color=TITLE_NUM_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=dp(TITLE_LABEL_HEIGHT),
                width=dp(get_str_pixel_width("999") + 20),
                halign="right",
                valign="middle",
            )
            empty_label.text_size = (empty_label.width, empty_label.height)
            empty_label.bind(on_press=self.main_screen.pressed)
            box2.add_widget(empty_label)

            text_label = TreeViewButton(
                text=display_title,
                font_size=sp(TITLE_FONT_SIZE),
                color=TITLE_LABEL_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=dp(TITLE_LABEL_HEIGHT),
                #                width=f"{get_str_pixel_width(title[0]) + 50}dp",
                width=dp(TITLE_LABEL_WIDTH),
                halign="left",
                valign="middle",
            )
            text_label.text_size = (text_label.width, text_label.height)
            text_label.bind(on_press=self.main_screen.pressed)
            box2.add_widget(text_label)

            box1.minimum_height = box1.height
            box2.minimum_height = box2.height

            box_node.add_widget(box1)
            box_node.add_widget(box2)
            box_node.minimum_height = box_node.height

            tree.add_node(box_node, parent=year_range_node)

    def add_dda_story_nodes(self, tree, dda_node):
        titles = self.filtered_title_lists.get_title_lists()
        for title in titles["Donald Duck Adventures"]:
            story_node_1 = TreeViewButton(
                text=title[0],
                color=(1.0, 0.0, 0.0, 1.0),
                background_color=(0.0, 0.0, 0.0, 1.0),
                size_hint=(None, None),
                size=(get_str_pixel_width(title[0]) + 70, self.label_height),
                halign="left",
                valign="middle",
            )
            story_node_1.bind(size=story_node_1.setter("text_size"))
            story_node_1.bind(on_press=self.main_screen.pressed)
            tree.add_node(story_node_1, parent=dda_node)


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
