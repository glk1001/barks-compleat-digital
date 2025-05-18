import logging
import sys
from typing import List, Union, Dict, Callable

import kivy.core.text
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewNode

from background_views import BackgroundViews, ViewStates
from barks_fantagraphics.barks_tags import (
    Tags,
    TagCategories,
    BARKS_TAG_CATEGORIES,
    BARKS_TAG_CATEGORIES_DICT,
    BARKS_TAG_GROUPS_TITLES,
    TagGroups,
    get_tagged_titles,
)
from barks_fantagraphics.barks_titles import Titles, ComicBookInfo, BARKS_TITLES, get_title_dict
from barks_fantagraphics.comics_cmd_args import CmdArgs
from barks_fantagraphics.comics_database import ComicsDatabase
from barks_fantagraphics.comics_utils import (
    setup_logging,
    get_short_formatted_submitted_date,
    get_short_formatted_first_published_str,
    get_dest_comic_zip_file_stem,
)
from barks_fantagraphics.fanta_comics_info import (
    FantaComicBookInfo,
    SERIES_CS,
    SERIES_DDA,
    ALL_LISTS,
    get_all_fanta_comic_book_info,
)
from barks_fantagraphics.title_search import BarksTitleSearch, unique_extend
from file_paths import (
    get_mcomix_python_bin_path,
    get_mcomix_path,
    get_mcomix_barks_reader_config_path,
    get_the_comic_zips_dir,
    get_comic_inset_file,
)
from filtered_title_lists import FilteredTitleLists
from mcomix_reader import ComicReader
from random_title_images import get_random_title_image
from reader_formatter import ReaderFormatter

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


class TitleSearchBoxTreeViewNode(FloatLayout, TreeViewNode):
    name = "Title Search Box"
    text = StringProperty("")
    SELECTED_COLOR = (0, 0, 0, 0.0)
    TEXT_COLOR = (1, 1, 1, 1)
    TEXT_BACKGROUND_COLOR = (0.5, 0.5, 0.5, 0.8)
    SPINNER_TEXT_COLOR = (1, 1, 0, 1)
    SPINNER_BACKGROUND_COLOR = (0, 0, 1, 1)
    NODE_SIZE = (dp(100), dp(30))

    on_title_search_box_pressed = None
    on_title_search_box_title_pressed = None

    def on_touch_down(self, touch):
        if self.title_search_box.collide_point(*touch.pos):
            self.on_title_search_box_pressed(self)
            return super().on_touch_down(touch)
        if self.title_spinner.collide_point(*touch.pos):
            self.on_title_search_box_title_pressed(self)
            return super().on_touch_down(touch)
        return False


class TagSearchBoxTreeViewNode(FloatLayout, TreeViewNode):
    name = "Tag Search Box"
    text = StringProperty("")
    SELECTED_COLOR = (0, 0, 0, 0.0)
    TAG_LABEL_COLOR = (1, 1, 1, 1)
    TAG_LABEL_BACKGROUND_COLOR = (0.5, 0.5, 0.5, 0.8)
    TAG_TEXT_COLOR = (1, 1, 1, 1)
    TAG_TEXT_BACKGROUND_COLOR = (0.5, 0.5, 0.5, 0.8)
    TAG_SPINNER_TEXT_COLOR = (0, 1, 0, 1)
    TAG_SPINNER_BACKGROUND_COLOR = (1, 0, 1, 1)
    TAG_TITLE_SPINNER_TEXT_COLOR = (1, 1, 0, 1)
    TAG_TITLE_SPINNER_BACKGROUND_COLOR = (0, 0, 1, 1)
    NODE_SIZE = (dp(100), dp(60))

    on_tag_search_box_pressed = None
    on_tag_search_box_tag_pressed = None
    on_tag_search_box_title_pressed = None

    def on_touch_down(self, touch):
        if self.tag_search_box.collide_point(*touch.pos):
            self.on_tag_search_box_pressed(self)
            return super().on_touch_down(touch)
        if self.tag_spinner.collide_point(*touch.pos):
            self.on_tag_search_box_tag_pressed(self)
            return super().on_touch_down(touch)
        if self.tag_title_spinner.collide_point(*touch.pos):
            self.on_tag_search_box_title_pressed(self)
            return super().on_touch_down(touch)
        return False


class StoryGroupTreeViewNode(Button, TreeViewNode):
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


class MainScreen(BoxLayout):
    MAIN_TITLE_BACKGROUND_COLOR = (1, 1, 1, 0.05)
    MAIN_TITLE_COLOR = (1, 1, 0, 1)
    TITLE_INFO_LABEL_COLOR = (1.0, 0.99, 0.9, 1.0)
    TITLE_EXTRA_INFO_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)
    DEBUG_BACKGROUND_OPACITY = 0

    BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG = (1, 0, 0, 1)
    BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG = (1, 0, 0, 0)
    BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG = (1, 0, 0, 0.5)
    BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG = (0, 0, 0, 0)

    reader_contents: ScrollView = ObjectProperty()
    reader_tree_view: ReaderTreeView = ObjectProperty()
    intro_text: TextInput = ObjectProperty()
    main_title = ObjectProperty()
    title_info = ObjectProperty()
    extra_title_info = ObjectProperty()
    title_page_image = ObjectProperty()
    title_page_button = ObjectProperty()

    top_view_image: Image = ObjectProperty()
    bottom_view: AnchorLayout = ObjectProperty()

    def __init__(self, filtered_title_lists: FilteredTitleLists, **kwargs):
        super().__init__(**kwargs)

        self.formatter = ReaderFormatter()
        self.fanta_info: Union[FantaComicBookInfo, None] = None

        self.title_lists: Dict[str, List[FantaComicBookInfo]] = (
            filtered_title_lists.get_title_lists()
        )
        self.title_dict: Dict[str, Titles] = get_title_dict()
        self.title_search = BarksTitleSearch()
        self.all_fanta_titles = get_all_fanta_comic_book_info()

        self.comic_reader = ComicReader(
            get_mcomix_python_bin_path(),
            get_mcomix_path(),
            get_mcomix_barks_reader_config_path(),
            get_the_comic_zips_dir(),
        )

        self.background_views = BackgroundViews(self.title_lists)
        self.top_view_image.color = (1, 1, 1, 0.5)
        self.bottom_view.before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG

        self.tag_search_box_title_spinner = None

        self.update_background_views(ViewStates.INITIAL)

    def node_expanded(self, _tree: ReaderTreeView, node: TreeViewNode):
        if isinstance(node, YearRangeTreeViewNode):
            self.update_background_views(ViewStates.ON_YEAR_RANGE_NODE, year_range=node.text)
        elif isinstance(node, StoryGroupTreeViewNode):
            if node.text == SERIES_CS:
                self.update_background_views(ViewStates.ON_CS_NODE)
            elif node.text == SERIES_DDA:
                self.update_background_views(ViewStates.ON_DDA_NODE)
            elif node.text in BARKS_TAG_CATEGORIES_DICT:
                self.update_background_views(ViewStates.ON_CATEGORY_NODE, category=node.text)

    def intro_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_INTRO_NODE)

        self.intro_text.text = "hello line 1\nhello line 2\nhello line 3\n"

    def the_stories_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_THE_STORIES_NODE)

    def search_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_SEARCH_NODE)

    def title_search_box_pressed(self, instance):
        print("Title search box pressed", instance)

        if not instance.title_search_box.text:
            instance.title_spinner.text = ""
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

    def title_search_box_title_pressed(self, instance):
        print("Title search box title pressed", instance)

        self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

        instance.title_spinner.text = ""

    def title_search_box_text_changed(self, instance, value):
        print("Title search box text changed", instance, "text:", value)

        self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

        if len(value) <= 1:
            instance.title_spinner.text = ""
            instance.title_spinner.is_open = False
        else:
            titles = self.get_titles_matching_search_title_str(str(value))
            if titles:
                instance.title_spinner.values = titles
                instance.title_spinner.text = titles[0]
                instance.title_spinner.is_open = True
                self.title_search_box_spinner_value_changed(
                    instance.title_spinner, instance.title_spinner.text
                )
            else:
                instance.title_spinner.values = []
                instance.title_spinner.text = ""
                instance.title_spinner.is_open = False

    def title_search_box_spinner_value_changed(self, _spinner: Spinner, title_str: str):
        print(f'Title search box spinner value changed: "{title_str}".')
        self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE)
        self.update_title(title_str)

    def get_titles_matching_search_title_str(self, value: str) -> List[str]:
        title_list = self.title_search.get_titles_matching_prefix(value)
        if len(value) > 2:
            unique_extend(title_list, self.title_search.get_titles_containing(value))

        return self.title_search.get_titles_as_strings(title_list)

    def tag_search_box_pressed(self, instance):
        print("Tag search box pressed", instance)

        self.tag_search_box_title_spinner = instance.tag_title_spinner

        if not instance.tag_search_box.text:
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)
            instance.tag_spinner.text = ""
            instance.tag_title_spinner.text = ""

    def tag_search_box_tag_spinner_pressed(self, instance):
        print("Tag search box tag spinner pressed", instance)

        # TODO: Is this correct?
        self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

        instance.tag_title_spinner.text = ""

    def tag_search_box_title_spinner_pressed(self, instance):
        print("Tag search box title spinner pressed", instance)

        # TODO: Is this correct?
        self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

        instance.tag_title_spinner.text = ""
        #
        # if instance.tag_spinner.text and not instance.tag_title_spinner.text:
        #     self.tag_search_box_tag_spinner_value_changed(
        #         instance.tag_spinner, instance.tag_spinner.text
        #     )

    def tag_search_box_text_changed(self, instance, value):
        print("Tag search box text changed", instance, "text:", value)

        self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

        if len(value) <= 1:
            instance.tag_spinner.text = ""
            instance.tag_spinner.is_open = False
            instance.tag_title_spinner.values = []
            instance.tag_title_spinner.text = ""
            instance.tag_title_spinner.is_open = False
        else:
            tags = self.get_tags_matching_search_tag_str(str(value))
            if tags:
                instance.tag_spinner.values = sorted([str(t.value) for t in tags])
                instance.tag_spinner.is_open = True
            else:
                instance.tag_spinner.values = []
                instance.tag_spinner.text = ""
                instance.tag_spinner.is_open = False
                instance.tag_title_spinner.values = []
                instance.tag_title_spinner.text = ""
                instance.tag_title_spinner.is_open = False

    def tag_search_box_tag_spinner_value_changed(self, _spinner: Spinner, tag_str: str):
        print(f'Tag search box tag spinner value changed: "{tag_str}".')
        if not tag_str:
            return

        titles = self.title_search.get_titles_from_alias_tag(tag_str.lower())

        if not titles:
            self.tag_search_box_title_spinner.values = []
            self.tag_search_box_title_spinner.text = ""
            self.tag_search_box_title_spinner.is_open = False
            return

        self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

        self.tag_search_box_title_spinner.values = self.title_search.get_titles_as_strings(titles)
        self.tag_search_box_title_spinner.text = self.tag_search_box_title_spinner.values[0]
        self.tag_search_box_title_spinner.is_open = True

    def tag_search_box_title_spinner_value_changed(self, _spinner: Spinner, title_str: str):
        print(f'Tag search box title spinner value changed: "{title_str}".')
        self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE)

    def get_tags_matching_search_tag_str(self, value: str) -> List[Union[Tags, TagGroups]]:
        tag_list = self.title_search.get_tags_matching_prefix(value)
        # if len(value) > 2:
        #     unique_extend(title_list, self.title_search.get_titles_containing(value))

        return tag_list

    def update_title(self, title_str: str):
        if not title_str:
            return

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            return

        self.fanta_info = self.all_fanta_titles[title_str]
        self.set_title()

    def get_fanta_info_from_title(self, title_str) -> FantaComicBookInfo:
        all_titles = self.title_lists[ALL_LISTS]
        return all_titles[self.title_dict[title_str]]

    def appendix_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_APPENDIX_NODE)

    def index_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_INDEX_NODE)

    def chrono_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CHRONO_BY_YEAR_NODE)

    def year_range_pressed(self, button: Button):
        self.update_background_views(ViewStates.ON_YEAR_RANGE_NODE, year_range=button.text)

    def series_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_SERIES_NODE)

    def cs_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CS_NODE)

    def dda_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_DDA_NODE)

    def categories_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CATEGORIES_NODE)

    def category_pressed(self, button: Button):
        self.update_background_views(ViewStates.ON_CATEGORY_NODE, category=button.text)

    def title_row_button_pressed(self, button: Button):
        self.update_background_views(ViewStates.ON_TITLE_NODE)

        self.fanta_info = button.parent.fanta_info
        self.set_title()

    def update_background_views(
        self, tree_node: ViewStates, category: str = "", year_range: str = ""
    ) -> None:
        self.background_views.set_current_category(category)
        self.background_views.set_current_year_range(year_range)

        self.background_views.set_view_state(tree_node)

        self.intro_text.opacity = 0.0

        self.top_view_image.opacity = self.background_views.get_top_view_image_opacity()
        self.top_view_image.source = self.background_views.get_top_view_image_file()
        self.top_view_image.color = self.background_views.get_top_view_image_color()

        self.bottom_view.opacity = self.background_views.get_bottom_view_image_opacity()
        self.bottom_view.after_image.source = (
            self.background_views.get_bottom_view_after_image_file()
        )
        self.bottom_view.after_image.color = (
            self.background_views.get_bottom_view_after_image_color()
        )
        self.bottom_view.before_image.source = (
            self.background_views.get_bottom_view_before_image_file()
        )
        self.bottom_view.before_image.color = (
            self.background_views.get_bottom_view_before_image_color()
        )

    def set_title(self) -> None:
        print(f'Setting title = "{self.fanta_info.comic_book_info.get_title_str()}".')

        comic_inset_file = get_comic_inset_file(self.fanta_info.comic_book_info.title)
        title_info_image = get_random_title_image(self.fanta_info.comic_book_info.get_title_str())

        self.main_title.text = self.get_main_title_str()
        self.title_info.text = self.formatter.get_title_info(self.fanta_info)
        self.extra_title_info.text = self.formatter.get_extra_title_info(self.fanta_info)
        self.title_page_image.source = comic_inset_file
        self.bottom_view.before_image.source = title_info_image

    def get_main_title_str(self):
        if self.fanta_info.comic_book_info.is_barks_title:
            return self.fanta_info.comic_book_info.get_title_str()

        return self.fanta_info.comic_book_info.get_title_from_issue_name()

    def image_pressed(self):
        if self.fanta_info is None:
            print(f'Image "{self.title_page_image.source}" pressed. But no title selected.')
            return

        if self.comic_reader.reader_is_running:
            print(f'Image "{self.title_page_image.source}" pressed. But already reading comic.')
            return

        comic_file_stem = get_dest_comic_zip_file_stem(
            self.fanta_info.comic_book_info.get_title_str(),
            self.fanta_info.fanta_chronological_number,
            self.fanta_info.get_short_issue_title(),
        )

        print(f'Image "{self.title_page_image.source}" pressed. Want to run "{comic_file_stem}".')

        self.comic_reader.show_comic(comic_file_stem)

        print(f"Exited image press.")


class ReaderTreeBuilder:
    def __init__(self, filtered_title_lists: FilteredTitleLists, main_screen: MainScreen):
        self.filtered_title_lists = filtered_title_lists
        self.main_screen = main_screen

    def build_main_screen_tree(self):
        tree: ReaderTreeView = self.main_screen.reader_tree_view

        tree.bind(on_node_expand=self.main_screen.node_expanded)

        self.__add_intro_node(tree)
        self.__add_the_stories_node(tree)
        self.__add_search_node(tree)
        self.__add_appendix_node(tree)
        self.__add_index_node(tree)

        tree.bind(minimum_height=tree.setter("height"))

    def __add_intro_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Introduction")
        label.bind(on_press=self.main_screen.intro_pressed)
        tree.add_node(label)

    def __add_the_stories_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="The Stories")
        label.bind(on_press=self.main_screen.the_stories_pressed)
        new_node = tree.add_node(label)
        self.__add_story_nodes(tree, new_node)

    def __add_search_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Search")
        label.bind(on_press=self.main_screen.search_pressed)
        search_node = tree.add_node(label)

        label = TitleSearchBoxTreeViewNode()
        label.on_title_search_box_pressed = self.main_screen.title_search_box_pressed
        label.on_title_search_box_title_pressed = self.main_screen.title_search_box_title_pressed
        label.bind(text=self.main_screen.title_search_box_text_changed)
        label.title_spinner.bind(text=self.main_screen.title_search_box_spinner_value_changed)
        tree.add_node(label, parent=search_node)

        label = TagSearchBoxTreeViewNode()
        label.on_tag_search_box_pressed = self.main_screen.tag_search_box_pressed
        label.on_tag_search_box_tag_pressed = self.main_screen.tag_search_box_tag_spinner_pressed
        label.on_tag_search_box_title_pressed = (
            self.main_screen.tag_search_box_title_spinner_pressed
        )
        label.bind(text=self.main_screen.tag_search_box_text_changed)
        label.tag_spinner.bind(text=self.main_screen.tag_search_box_tag_spinner_value_changed)
        label.tag_title_spinner.bind(
            text=self.main_screen.tag_search_box_title_spinner_value_changed
        )
        tree.add_node(label, parent=search_node)

    def __add_appendix_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Appendix")
        label.bind(on_press=self.main_screen.appendix_pressed)
        tree.add_node(label)

    def __add_index_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Index")
        label.bind(on_press=self.main_screen.index_pressed)
        tree.add_node(label)

    def __add_story_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        label = StoryGroupTreeViewNode(text="Chronological")
        label.bind(on_press=self.main_screen.chrono_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.__add_year_range_nodes(tree, new_node)

        label = StoryGroupTreeViewNode(text="Series")
        label.bind(on_press=self.main_screen.series_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.__add_series_nodes(tree, new_node)

        label = StoryGroupTreeViewNode(text="Categories")
        label.bind(on_press=self.main_screen.categories_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.__add_categories_nodes(tree, new_node)

    def __add_year_range_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            label = YearRangeTreeViewNode(text=range_str)
            label.bind(on_press=self.main_screen.year_range_pressed)

            new_node = tree.add_node(label, parent=parent_node)
            self.__add_year_range_story_nodes(
                tree, new_node, self.main_screen.title_lists[range_str]
            )

    def __add_year_range_story_nodes(
        self,
        tree: ReaderTreeView,
        parent_node: TreeViewNode,
        title_list: List[FantaComicBookInfo],
    ):
        for title_info in title_list:
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __add_categories_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for category in TagCategories:
            label = StoryGroupTreeViewNode(text=category.value)
            label.bind(on_press=self.main_screen.category_pressed)

            new_node = tree.add_node(label, parent=parent_node)
            self.__add_category_node(tree, category, new_node)

    def __add_category_node(
        self, tree: ReaderTreeView, category: TagCategories, parent_node: TreeViewNode
    ):
        for tag_or_group in BARKS_TAG_CATEGORIES[category]:
            if type(tag_or_group) == Tags:
                self.__add_tag_node(tree, tag_or_group, parent_node)
            else:
                assert type(tag_or_group) == TagGroups
                tag_group_node = self.__add_tag_group_node(tree, tag_or_group, parent_node)
                titles = BARKS_TAG_GROUPS_TITLES[tag_or_group]
                self.__add_title_nodes(tree, titles, tag_group_node)

    def __add_tag_node(self, tree: ReaderTreeView, tag: Tags, parent_node: TreeViewNode):
        label = StoryGroupTreeViewNode(text=tag.value)
        self.__add_tagged_story_nodes(tree, tag, label)
        tree.add_node(label, parent=parent_node)

    @staticmethod
    def __add_tag_group_node(tree: ReaderTreeView, tag_group: TagGroups, parent_node: TreeViewNode):
        label = StoryGroupTreeViewNode(text=tag_group.value)
        return tree.add_node(label, parent=parent_node)

    def __add_tagged_story_nodes(
        self, tree: ReaderTreeView, tag: Tags, parent_node: TreeViewNode
    ) -> None:
        titles = get_tagged_titles(tag)
        self.__add_title_nodes(tree, titles, parent_node)

    def __add_title_nodes(
        self, tree: ReaderTreeView, titles: List[Titles], parent_node: TreeViewNode
    ) -> None:
        for title in titles:
            # TODO: Very roundabout way to get fanta info
            title_str = BARKS_TITLES[title]
            if title_str not in self.main_screen.all_fanta_titles:
                print(f'Skipped unconfigured title "{title_str}".')
                continue
            title_info = self.main_screen.all_fanta_titles[title_str]
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __add_series_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        self.__add_series_node(tree, SERIES_CS, self.main_screen.cs_pressed, parent_node)
        self.__add_series_node(tree, SERIES_DDA, self.main_screen.dda_pressed, parent_node)

    def __add_series_node(
        self, tree: ReaderTreeView, series: str, on_pressed: Callable, parent_node: TreeViewNode
    ) -> None:
        label = StoryGroupTreeViewNode(text=series)
        label.bind(on_press=on_pressed)
        self.__add_series_story_nodes(tree, series, label)
        tree.add_node(label, parent=parent_node)

    def __add_series_story_nodes(
        self, tree: ReaderTreeView, series: str, parent_node: TreeViewNode
    ) -> None:
        title_list = self.main_screen.title_lists[series]

        for title_info in title_list:
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
        title_node = TitleTreeViewNode(full_fanta_info)

        title_node.num_label.text = str(full_fanta_info.fanta_chronological_number)
        title_node.num_label.bind(on_press=self.main_screen.title_row_button_pressed)

        title_node.num_label.color_selected = (0, 0, 1, 1)

        title_node.title_label.text = full_fanta_info.comic_book_info.get_display_title()
        title_node.title_label.bind(on_press=self.main_screen.title_row_button_pressed)

        issue_info = (
            f"{get_short_formatted_first_published_str(full_fanta_info.comic_book_info)}"
            f"  [{get_short_formatted_submitted_date(full_fanta_info.comic_book_info)}]"
        )

        title_node.issue_label.text = issue_info
        title_node.issue_label.bind(on_press=self.main_screen.title_row_button_pressed)

        return title_node


class BarksReaderApp(App):
    def __init__(self, comics_db: ComicsDatabase, **kwargs):
        super().__init__(**kwargs)

        self.comics_database = comics_db
        self.filtered_title_lists = FilteredTitleLists()

        self.main_screen: Union[MainScreen, None] = None

        Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        Window.left = DEFAULT_LEFT_POS
        Window.top = DEFAULT_TOP_POS

    def on_request_close_window(self, *_args):
        return self.main_screen.comic_reader.on_app_request_close()

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.main_screen = MainScreen(self.filtered_title_lists)

        tree_builder = ReaderTreeBuilder(self.filtered_title_lists, self.main_screen)
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

    setup_logging(cmd_args.get_log_level())

    comics_database = cmd_args.get_comics_database()

    BarksReaderApp(comics_database).run()
