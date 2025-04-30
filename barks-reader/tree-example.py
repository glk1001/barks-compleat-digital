import logging
import sys
from typing import Tuple, List

import kivy.core.text
from django.utils.termcolors import background
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import setup_logging
from barks_fantagraphics.fanta_comics_info import get_filtered_title_lists, FantaComicBookInfo


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class TreeViewRow(BoxLayout, TreeViewNode):
    pass


class TreeViewButton(Button, TreeViewNode):
    pass


class TreeApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.label_height = 30
        self.intro_text = None
        Window.size = (1500, 800)
        Window.left = 300
        Window.top = 200

    def pressed(self, button: Button):
        if button.text == "Introduction":
            self.intro_text.opacity = 1.0
        else:
            self.intro_text.opacity = 0.0
        print(f'Button "{button.text}" pressed.')

    def build(self):
        intro_text = TextInput(
            text="hello line 1\nhello line 2\nhello line 3\n",
            multiline=True,
            readonly=True,
            size_hint=(0.7, 1),
            pos_hint={"x": 0.3, "top": 1.0},
            opacity=0.0,
        )

        # left_box = BoxLayout(orientation="vertical", size_hint=(0.3, 1))
        # left_box.add_widget(self.build_tree(intro_text))

        scroll_view = ScrollView(size_hint=(0.3, 1))
        scroll_view.do_scroll_x = False
        scroll_view.do_scroll_y = True
        scroll_view.always_overscroll = False
        scroll_view.effect_cls = "ScrollEffect"
        scroll_view.scroll_type = ["bars", "content"]

        scroll_view.bar_color = (0.8, 0.8, 0.8, 1)
        scroll_view.bar_inactive_color = (0.8, 0.8, 0.8, 0.8)
        scroll_view.bar_width = 5

        scroll_view.add_widget(self.build_tree(intro_text))

        lo = BoxLayout(orientation="horizontal", size_hint=(1, 1))
        lo.add_widget(scroll_view)
        lo.add_widget(intro_text)

        return lo

    def build_tree(self, intro_text):
        self.intro_text = intro_text

        tree = TreeView(hide_root=True, indent_level="40dp")

        tree.size_hint = 1, None
        tree.bind(minimum_height=tree.setter("height"))

        intro_label = TreeViewButton(
            text="Introduction",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Introduction") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        intro_label.bind(size=intro_label.setter("text_size"))
        intro_label.bind(on_press=self.pressed)
        intro_node = tree.add_node(intro_label)

        the_stories_label = TreeViewButton(
            text="The Stories",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("The Stories") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        the_stories_label.bind(size=the_stories_label.setter("text_size"))
        the_stories_label.bind(on_press=self.pressed)
        the_stories_node = tree.add_node(the_stories_label)

        self.add_story_nodes(tree, the_stories_node)

        tag_search_label = TreeViewButton(
            text="Tag Search",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Tag Search") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        tag_search_label.bind(size=tag_search_label.setter("text_size"))
        tag_search_label.bind(on_press=self.pressed)
        tag_search_node = tree.add_node(tag_search_label)

        appendix_label = TreeViewButton(
            text="Appendix",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Appendix") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        appendix_label.bind(size=appendix_label.setter("text_size"))
        appendix_label.bind(on_press=self.pressed)
        appendix_node = tree.add_node(appendix_label)

        index_label = TreeViewButton(
            text="Index",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Index") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        index_label.bind(size=index_label.setter("text_size"))
        index_label.bind(on_press=self.pressed)
        index_node = tree.add_node(index_label)

        return tree

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
        by_year_label.bind(on_press=self.pressed)
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
        dda_label.bind(on_press=self.pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_range_nodes(self, tree, the_years_node):
        year_ranges = [
            (1942, 1945),
            (1946, 1949),
            (1950, 1953),
            (1954, 1957),
            (1958, 1961),
        ]

        def create_range_lamba(year_range: Tuple[int, int]):
            return (
                lambda info: year_range[0] <= info.comic_book_info.submitted_year <= year_range[1]
            )

        filters = {}
        for year_range in year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            filters[range_str] = create_range_lamba(year_range)

        titles = get_filtered_title_lists(filters)

        for year_range in year_ranges:
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
            year_range_label.bind(on_press=self.pressed)
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
                height=f"{NUM_LABEL_HEIGHT + TITLE_LABEL_HEIGHT}dp",
            )

            num_label = TreeViewButton(
                text=f"{fanta_info.fanta_chronological_number}",
                bold=True,
                color=TITLE_NUM_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=f"{NUM_LABEL_HEIGHT}dp",
                width=f'{get_str_pixel_width("999")+20}dp',
                halign="right",
                valign="middle",
            )
            num_label.text_size = (num_label.width, num_label.height)
            num_label.bind(on_press=self.pressed)
            box1.add_widget(num_label)

            issue_label = TreeViewButton(
                text=f"{fanta_info.comic_book_info.get_issue_title()}",
                color=ISSUE_TITLE_LABEL_COLOR,
                size_hint=(None, None),
                background_color=LABEL_BACKGROUND_COLOR,
                height=f"{NUM_LABEL_HEIGHT}dp",
                width=f'{get_str_pixel_width("WDCS 500") + 50}dp',
                halign="left",
                valign="middle",
            )
            issue_label.text_size = (issue_label.width, issue_label.height)
            issue_label.bind(on_press=self.pressed)
            box1.add_widget(issue_label)

            empty_label = TreeViewButton(
                text="   ",
                color=TITLE_NUM_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=f"{TITLE_LABEL_HEIGHT}dp",
                width=f'{get_str_pixel_width("999")+20}dp',
                halign="right",
                valign="middle",
            )
            empty_label.text_size = (empty_label.width, empty_label.height)
            empty_label.bind(on_press=self.pressed)
            box2.add_widget(empty_label)

            text_label = TreeViewButton(
                text=display_title,
                font_size=TITLE_FONT_SIZE,
                color=TITLE_LABEL_COLOR,
                background_color=LABEL_BACKGROUND_COLOR,
                size_hint=(None, None),
                height=f"{TITLE_LABEL_HEIGHT}dp",
                #                width=f"{get_str_pixel_width(title[0]) + 50}dp",
                width=f"{TITLE_LABEL_WIDTH}dp",
                halign="left",
                valign="middle",
            )
            text_label.text_size = (text_label.width, text_label.height)
            text_label.bind(on_press=self.pressed)
            box2.add_widget(text_label)

            box1.minimum_height = box1.height
            box2.minimum_height = box2.height

            box_node.add_widget(box1)
            box_node.add_widget(box2)
            box_node.minimum_height = box_node.height

            tree.add_node(box_node, parent=year_range_node)

    def add_dda_story_nodes(self, tree, dda_node):
        story_node_1 = TreeViewButton(
            text="Donald Duck and The Mummy's Ring",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Donald Duck and The Mummy's Ring") + 70, self.label_height),
            halign="left",
            valign="middle",
        )
        story_node_1.bind(size=story_node_1.setter("text_size"))
        story_node_1.bind(on_press=self.pressed)
        tree.add_node(story_node_1, parent=dda_node)

        story_node_2 = TreeViewButton(
            text="Frozen Gold",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Frozen Gold") + 40, self.label_height),
            halign="left",
            valign="middle",
        )
        story_node_2.bind(size=story_node_2.setter("text_size"))
        story_node_2.bind(on_press=self.pressed)
        tree.add_node(story_node_2, parent=dda_node)


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

    TreeApp(comics_database).run()
