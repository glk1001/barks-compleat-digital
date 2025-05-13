import logging
import os.path
import sys
from enum import Enum, auto
from random import randrange
from typing import List, Union, Dict, Callable

import kivy.core.text
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.barks_extra_info import BARKS_EXTRA_INFO
from barks_fantagraphics.barks_tags import (
    Tags,
    TagCategories,
    BARKS_TAGGED_TITLES,
    BARKS_TAG_CATEGORIES,
    BARKS_TAG_CATEGORIES_DICT,
    BARKS_TAG_ALIASES,
)
from barks_fantagraphics.barks_titles import Titles, ComicBookInfo, BARKS_TITLES, get_title_dict
from barks_fantagraphics.comic_issues import Issues, ISSUE_NAME
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
from barks_fantagraphics.fanta_comics_info import (
    FantaComicBookInfo,
    FAN,
    FANTA_SOURCE_COMICS,
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
from random_title_images import get_random_title_image, get_random_image

APP_TITLE = "The Compleat Barks Reader"

Builder.load_file("tree-example.kv")


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

    on_pressed = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_pressed(self)
            return super().on_touch_down(touch)
        return False


class TagSearchBoxTreeViewNode(FloatLayout, TreeViewNode):
    name = "Tag Search Box"
    text = StringProperty("")
    SELECTED_COLOR = (0, 0, 0, 0.0)
    TEXT_COLOR = (1, 1, 1, 1)
    TEXT_BACKGROUND_COLOR = (0.5, 0.5, 0.5, 0.8)
    SPINNER_TEXT_COLOR = (1, 1, 0, 1)
    SPINNER_BACKGROUND_COLOR = (0, 0, 1, 1)
    NODE_SIZE = (dp(100), dp(60))

    on_tag_search_box_pressed = None

    def on_touch_down(self, touch):
        if self.tag_search_box.collide_point(*touch.pos):
            self.on_tag_search_box_pressed(self)
            return super().on_touch_down(touch)
        if self.tag_spinner.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self.tag_title_spinner.collide_point(*touch.pos):
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


class TreeNodes(Enum):
    INITIAL = auto()
    ON_INTRO_NODE = auto()
    ON_THE_STORIES_NODE = auto()
    ON_SEARCH_NODE = auto()
    ON_APPENDIX_NODE = auto()
    ON_INDEX_NODE = auto()
    ON_CHRONO_BY_YEAR_NODE = auto()
    ON_YEAR_RANGE_NODE = auto()
    ON_SERIES_NODE = auto()
    ON_CS_NODE = auto()
    ON_DDA_NODE = auto()
    ON_CATEGORIES_NODE = auto()
    ON_CATEGORY_NODE = auto()
    ON_TITLE_NODE = auto()
    ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TITLE_SEARCH_BOX_NODE = auto()
    ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TAG_SEARCH_BOX_NODE = auto()


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

    top_view_image = ObjectProperty()
    bottom_view = ObjectProperty()
    reader_contents = ObjectProperty()
    intro_text = ObjectProperty()
    main_title = ObjectProperty()
    title_info = ObjectProperty()
    extra_title_info = ObjectProperty()
    title_page_image = ObjectProperty()
    title_page_button = ObjectProperty()

    def __init__(self, filtered_title_lists: FilteredTitleLists, **kwargs):
        super().__init__(**kwargs)

        # Use a custom issue_name here to display slightly shorter names.
        self.title_info_issue_name = ISSUE_NAME.copy()
        self.title_info_issue_name[Issues.CS] = "Comics & Stories"
        self.title_info_issue_name[Issues.MC] = "March of Comics"

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

        self.top_view_image.color = (1, 1, 1, 0.5)
        self.bottom_view_before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG

        self.current_tree_node = TreeNodes.INITIAL
        self.current_year_range = ""
        self.current_category = ""
        self.tag_search_box_title_spinner = None

        self.top_view_change_event = None
        self.bottom_view_change_after_event = None

        self.update_visibilities()

    def node_expanded(self, tree: ReaderTreeView, node: TreeViewNode):
        if isinstance(node, YearRangeTreeViewNode):
            self.current_tree_node = TreeNodes.ON_YEAR_RANGE_NODE
            self.current_year_range = node.text
            self.set_next_top_view_image()
            self.set_next_bottom_view_image()
        elif isinstance(node, StoryGroupTreeViewNode):
            if node.text == SERIES_CS:
                self.current_tree_node = TreeNodes.ON_CS_NODE
                self.set_next_top_view_image()
                self.set_next_bottom_view_image()
            elif node.text == SERIES_DDA:
                self.current_tree_node = TreeNodes.ON_DDA_NODE
                self.set_next_top_view_image()
                self.set_next_bottom_view_image()
            elif node.text in BARKS_TAG_CATEGORIES_DICT:
                self.current_tree_node = TreeNodes.ON_CATEGORY_NODE
                self.current_category = node.text
                self.set_next_top_view_image()
                self.set_next_bottom_view_image()

    def intro_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_INTRO_NODE
        self.update_visibilities()

        self.intro_text.text = "hello line 1\nhello line 2\nhello line 3\n"

    def the_stories_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_THE_STORIES_NODE
        self.update_visibilities()

    def search_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_SEARCH_NODE
        self.update_visibilities()

    def title_search_box_pressed(self, instance):
        print("Title search box pressed", instance)

        self.current_tree_node = TreeNodes.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET
        self.update_visibilities()

        instance.spinner.text = ""

    def title_search_box_text_changed(self, instance, value):
        print("Title search box text changed", instance, "text:", value)

        self.current_tree_node = TreeNodes.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET
        self.update_visibilities()

        if len(value) <= 1:
            instance.spinner.text = ""
            instance.spinner.is_open = False
        else:
            titles = self.get_titles_matching_search_title_str(str(value))
            if titles:
                instance.spinner.values = titles
                instance.spinner.text = titles[0]
                instance.spinner.is_open = True
                print(f'Spinner text set to "{instance.spinner.text}".')
                self.title_search_box_value_changed(instance.spinner, instance.spinner.text)
            else:
                instance.spinner.values = []
                instance.spinner.text = ""
                instance.spinner.is_open = False

    def get_titles_matching_search_title_str(self, value: str) -> List[str]:
        title_list = self.title_search.get_titles_matching_prefix(value)
        if len(value) > 2:
            unique_extend(title_list, self.title_search.get_titles_containing(value))

        return self.title_search.get_titles_as_strings(title_list)

    def title_search_box_value_changed(self, spinner: Spinner, title_str: str):
        print(f'Title spinner value changed: "{title_str}".')
        if not title_str:
            return

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            return

        self.current_tree_node = TreeNodes.ON_TITLE_SEARCH_BOX_NODE
        self.update_visibilities()

        self.fanta_info = self.all_fanta_titles[title_str]
        print(f'New fanta_info: "{self.fanta_info.comic_book_info.get_title_str()}".')
        self.set_title()

    def tag_search_box_pressed(self, instance):
        print("Tag search box pressed", instance)

        self.current_tree_node = TreeNodes.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
        self.update_visibilities()

        instance.tag_spinner.text = ""
        instance.tag_title_spinner.text = ""
        self.tag_search_box_title_spinner = instance.tag_title_spinner

    def tag_search_box_text_changed(self, instance, value):
        print("Tag search box text changed", instance, "text:", value)

        self.current_tree_node = TreeNodes.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
        self.update_visibilities()

        self.tag_search_box_title_spinner.values = []
        self.tag_search_box_title_spinner.text = ""
        self.tag_search_box_title_spinner.is_open = False

        if len(value) <= 1:
            instance.tag_spinner.text = ""
            instance.tag_spinner.is_open = False
        else:
            tags = self.get_tags_matching_search_tag_str(str(value))
            if tags:
                instance.tag_spinner.values = sorted([t.value for t in tags])
                # instance.tag_spinner.text = tags[0].value
                instance.tag_spinner.is_open = True
                print(f'tag_spinner text set to "{instance.tag_spinner.text}".')
                self.title_search_box_value_changed(instance.tag_spinner, instance.tag_spinner.text)
            else:
                instance.tag_spinner.values = []
                instance.tag_spinner.text = ""
                instance.tag_spinner.is_open = False

    def tag_search_box_value_changed(self, spinner: Spinner, tag_str: str):
        print(f'Tag spinner tag value changed: "{tag_str}".')
        if not tag_str:
            return

        tag = BARKS_TAG_ALIASES[tag_str.lower()]

        if tag not in BARKS_TAGGED_TITLES:
            self.tag_search_box_title_spinner.values = []
            self.tag_search_box_title_spinner.text = ""
            self.tag_search_box_title_spinner.is_open = False
            return

        self.current_tree_node = TreeNodes.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
        self.update_visibilities()

        titles = [t[0] for t in BARKS_TAGGED_TITLES[tag]]

        self.tag_search_box_title_spinner.values = self.title_search.get_titles_as_strings(titles)
        self.tag_search_box_title_spinner.text = self.tag_search_box_title_spinner.values[0]
        self.tag_search_box_title_spinner.is_open = True

    def tag_search_box_title_value_changed(self, spinner: Spinner, title_str: str):
        print(f'Tag spinner title value changed: "{title_str}".')
        if not title_str:
            return

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            return

        self.current_tree_node = TreeNodes.ON_TAG_SEARCH_BOX_NODE
        self.update_visibilities()

        self.fanta_info = self.all_fanta_titles[title_str]
        print(f'New fanta_info: "{self.fanta_info.comic_book_info.get_title_str()}".')
        self.set_title()

    def get_tags_matching_search_tag_str(self, value: str) -> List[Tags]:
        tag_list = self.title_search.get_tags_matching_prefix(value)
        # if len(value) > 2:
        #     unique_extend(title_list, self.title_search.get_titles_containing(value))

        return tag_list

    def get_fanta_info_from_title(self, title_str) -> FantaComicBookInfo:
        all_titles = self.title_lists[ALL_LISTS]
        return all_titles[self.title_dict[title_str]]

    def appendix_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_APPENDIX_NODE
        self.update_visibilities()

    def index_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_INDEX_NODE
        self.update_visibilities()

    def chrono_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_CHRONO_BY_YEAR_NODE
        self.update_visibilities()

    def year_range_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_YEAR_RANGE_NODE
        self.update_visibilities()

        self.current_year_range = button.text

    def series_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_SERIES_NODE
        self.update_visibilities()

    def cs_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_CS_NODE
        self.update_visibilities()

    def dda_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_DDA_NODE
        self.update_visibilities()

    def categories_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_CATEGORIES_NODE
        self.update_visibilities()

    def category_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_CATEGORY_NODE
        self.update_visibilities()

        self.current_category = button.text

    def title_row_button_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_TITLE_NODE
        self.update_visibilities()

        self.fanta_info = button.parent.fanta_info
        self.set_title()

    def set_title(self) -> None:
        print(f'Setting title = "{self.fanta_info.comic_book_info.get_title_str()}".')

        comic_inset_file = get_comic_inset_file(self.fanta_info.comic_book_info.title)
        title_info_image = get_random_title_image(self.fanta_info.comic_book_info.get_title_str())

        self.main_title.text = self.get_main_title_str()
        self.title_info.text = self.get_title_info()
        self.extra_title_info.text = self.get_extra_title_info()
        self.title_page_image.source = comic_inset_file
        self.bottom_view_before_image.source = title_info_image

    def get_main_title_str(self):
        if self.fanta_info.comic_book_info.is_barks_title:
            return self.fanta_info.comic_book_info.get_title_str()

        return self.fanta_info.comic_book_info.get_title_from_issue_name()

    def image_pressed(self):
        if self.fanta_info is None:
            print(f'Image "{self.title_page_image.source}" pressed. No title selected.')
            return

        if self.comic_reader.reader_is_running:
            print(f'Image "{self.title_page_image.source}" pressed. Already reading comic.')
            return

        comic_file_stem = get_dest_comic_zip_file_stem(
            self.fanta_info.comic_book_info.get_title_str(),
            self.fanta_info.fanta_chronological_number,
            self.fanta_info.get_short_issue_title(),
        )

        print(f'Image "{self.title_page_image.source}" pressed. Want to run "{comic_file_stem}".')

        self.comic_reader.show_comic(comic_file_stem)

        print(f"Exited image press.")

    def get_title_info(self) -> str:
        # TODO: Clean this up.
        issue_info = get_formatted_first_published_str(
            self.fanta_info.comic_book_info, self.title_info_issue_name
        )
        submitted_info = get_long_formatted_submitted_date(self.fanta_info.comic_book_info)
        fanta_book = FANTA_SOURCE_COMICS[self.fanta_info.fantagraphics_volume]
        source = f"{FAN} CBDL, Vol {fanta_book.volume}, {fanta_book.year}"
        return (
            f"[i]1st Issue:[/i]   [b]{issue_info}[/b]\n"
            f"[i]Submitted:[/i] [b]{submitted_info}[/b]\n"
            f"[i]Source:[/i]       [b]{source}[/b]"
        )

    def get_extra_title_info(self) -> str:
        title = self.fanta_info.comic_book_info.title
        if title not in BARKS_EXTRA_INFO:
            return ""

        return f"{BARKS_EXTRA_INFO[title]}"

    def update_visibilities(self):
        if self.current_tree_node == TreeNodes.ON_INTRO_NODE:
            self.bottom_view.opacity = 0.0
            self.intro_text.opacity = 1.0
            self.bottom_view_after_image.color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.bottom_view_before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG
        elif self.current_tree_node in [
            TreeNodes.ON_TITLE_SEARCH_BOX_NODE,
            TreeNodes.ON_TITLE_NODE,
            TreeNodes.ON_TAG_SEARCH_BOX_NODE,
        ]:
            self.bottom_view.opacity = 1.0
            self.intro_text.opacity = 0.0
            self.bottom_view_after_image.color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.bottom_view_before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG
        else:
            self.bottom_view.opacity = 1.0
            self.intro_text.opacity = 0.0
            self.bottom_view_after_image.color = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG
            self.bottom_view_before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG

        self.set_next_top_view_image()
        self.set_next_bottom_view_image()

    def set_next_top_view_image(self):
        match self.current_tree_node:
            case TreeNodes.INITIAL:
                self.top_view_image.source = get_comic_inset_file(Titles.COLD_BARGAIN_A)
            case TreeNodes.ON_INTRO_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.ADVENTURE_DOWN_UNDER)
            case TreeNodes.ON_THE_STORIES_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[ALL_LISTS])
            case TreeNodes.ON_SEARCH_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_TITLE_SEARCH_BOX_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_TAG_SEARCH_BOX_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_APPENDIX_NODE:
                self.top_view_image.source = get_comic_inset_file(
                    Titles.FABULOUS_PHILOSOPHERS_STONE_THE
                )
            case TreeNodes.ON_INDEX_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRUANT_OFFICER_DONALD)
            case TreeNodes.ON_CHRONO_BY_YEAR_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[ALL_LISTS])
            case TreeNodes.ON_SERIES_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[ALL_LISTS])
            case TreeNodes.ON_CS_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[SERIES_CS])
            case TreeNodes.ON_DDA_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[SERIES_DDA])
            case TreeNodes.ON_CATEGORIES_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[ALL_LISTS])
            case TreeNodes.ON_CATEGORY_NODE:
                print(f"Current category: '{self.current_category}'")
                if not self.current_category:
                    self.top_view_image.source = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.top_view_image.source = get_random_image(
                        self.title_lists[self.current_category]
                    )
            case TreeNodes.ON_YEAR_RANGE_NODE:
                print(f"Year range: '{self.current_year_range}'")
                if not self.current_year_range:
                    self.top_view_image.source = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.top_view_image.source = get_random_image(
                        self.title_lists[self.current_year_range]
                    )
            case TreeNodes.ON_TITLE_NODE:
                pass
            case _:
                assert False

        print(
            f"Set top view. Category: {self.current_tree_node}."
            f" Image: '{os.path.basename(self.top_view_image.source)}'."
        )

        self.set_next_top_view_image_bg()
        self.schedule_top_view_event()

    def set_next_top_view_image_bg(self):
        random_color = (
            randrange(100, 255) / 255.0,
            randrange(100, 255) / 255.0,
            randrange(100, 255) / 255.0,
            randrange(220, 250) / 255.0,
        )
        self.top_view_image.color = random_color
        print(f"Top view image bg = {self.top_view_image.color}")

    def set_next_bottom_view_image(self):
        if self.current_tree_node in [
            TreeNodes.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET,
            TreeNodes.ON_TITLE_SEARCH_BOX_NODE,
            TreeNodes.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET,
            TreeNodes.ON_TAG_SEARCH_BOX_NODE,
            TreeNodes.ON_TITLE_NODE,
        ]:
            return

        self.bottom_view_after_image.source = get_random_image(self.title_lists[ALL_LISTS])
        print(
            f"Bottom view after image: '{os.path.basename(self.bottom_view_after_image.source)}'."
        )

        self.set_next_bottom_view_after_image_bg()
        self.schedule_bottom_view_after_event()

    def set_next_bottom_view_after_image_bg(self):
        if randrange(0, 100) < 20:
            rand_color = [1, 1, 1, 1]
        else:
            rand_index = randrange(0, 3)
            rand_color_val = randrange(230, 255) / 255.0
            rand_color = [0.1, 0.1, 0.1, self.bottom_view_after_image.color[3]]
            rand_color[rand_index] = rand_color_val

        self.bottom_view_after_image.color = tuple(rand_color)
        print(f"Bottom view after image bg = {self.bottom_view_after_image.color}")

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
        tree: ReaderTreeView = self.main_screen.reader_contents_tree

        tree.bind(on_node_expand=self.main_screen.node_expanded)

        self.add_intro_node(tree)
        self.add_the_stories_node(tree)
        self.add_search_node(tree)
        self.add_appendix_node(tree)
        self.add_index_node(tree)

        tree.bind(minimum_height=tree.setter("height"))

    def add_intro_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Introduction")
        label.bind(on_press=self.main_screen.intro_pressed)
        tree.add_node(label)

    def add_the_stories_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="The Stories")
        label.bind(on_press=self.main_screen.the_stories_pressed)
        new_node = tree.add_node(label)
        self.add_story_nodes(tree, new_node)

    def add_search_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Search")
        label.bind(on_press=self.main_screen.search_pressed)
        search_node = tree.add_node(label)

        label = TitleSearchBoxTreeViewNode()
        label.on_pressed = self.main_screen.title_search_box_pressed
        label.bind(text=self.main_screen.title_search_box_text_changed)
        label.spinner.bind(text=self.main_screen.title_search_box_value_changed)
        tree.add_node(label, parent=search_node)

        label = TagSearchBoxTreeViewNode()
        label.on_tag_search_box_pressed = self.main_screen.tag_search_box_pressed
        label.bind(text=self.main_screen.tag_search_box_text_changed)
        label.tag_spinner.bind(text=self.main_screen.tag_search_box_value_changed)
        label.tag_title_spinner.bind(text=self.main_screen.title_search_box_value_changed)
        tree.add_node(label, parent=search_node)

    def add_appendix_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Appendix")
        label.bind(on_press=self.main_screen.appendix_pressed)
        tree.add_node(label)

    def add_index_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Index")
        label.bind(on_press=self.main_screen.index_pressed)
        tree.add_node(label)

    def add_story_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        label = StoryGroupTreeViewNode(text="Chronological")
        label.bind(on_press=self.main_screen.chrono_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.add_year_range_nodes(tree, new_node)

        label = StoryGroupTreeViewNode(text="Series")
        label.bind(on_press=self.main_screen.series_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.add_series_nodes(tree, new_node)

        label = StoryGroupTreeViewNode(text="Categories")
        label.bind(on_press=self.main_screen.categories_pressed)
        new_node = tree.add_node(label, parent=parent_node)
        self.add_categories_nodes(tree, new_node)

    def add_year_range_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            label = YearRangeTreeViewNode(text=range_str)
            label.bind(on_press=self.main_screen.year_range_pressed)

            new_node = tree.add_node(label, parent=parent_node)
            self.add_year_range_story_nodes(tree, new_node, self.main_screen.title_lists[range_str])

    def add_year_range_story_nodes(
        self,
        tree: ReaderTreeView,
        parent_node: TreeViewNode,
        title_list: List[FantaComicBookInfo],
    ):
        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=parent_node)

    def add_categories_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for category in TagCategories:
            label = StoryGroupTreeViewNode(text=category.value)
            label.bind(on_press=self.main_screen.category_pressed)

            new_node = tree.add_node(label, parent=parent_node)
            self.add_category_node(tree, category, new_node)

    def add_category_node(
        self, tree: ReaderTreeView, category: TagCategories, parent_node: TreeViewNode
    ):
        for tag in BARKS_TAG_CATEGORIES[category]:
            label = StoryGroupTreeViewNode(text=tag.value)
            # TODO: What to do when a category is pressed?
            # label.bind(on_press=self.category_pressed)
            self.add_tagged_story_nodes(tree, tag, label)
            tree.add_node(label, parent=parent_node)

    def add_tagged_story_nodes(self, tree: ReaderTreeView, tag: Tags, parent_node: TreeViewNode):
        for title in BARKS_TAGGED_TITLES[tag]:
            # TODO: Very roundabout way to get fanta info
            title_str = BARKS_TITLES[title[0]]
            if title_str not in self.main_screen.all_fanta_titles:
                print(f'Skipped unconfigured title "{title_str}".')
                continue
            title_info = self.main_screen.all_fanta_titles[title_str]
            tree.add_node(self.get_title_tree_view_node(title_info), parent=parent_node)

    def add_series_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        self.add_series_node(tree, SERIES_CS, self.main_screen.cs_pressed, parent_node)
        self.add_series_node(tree, SERIES_DDA, self.main_screen.dda_pressed, parent_node)

    def add_series_node(
        self, tree: ReaderTreeView, series: str, on_pressed: Callable, parent_node: TreeViewNode
    ):
        label = StoryGroupTreeViewNode(text=series)
        label.bind(on_press=on_pressed)
        self.add_series_story_nodes(tree, series, label)
        tree.add_node(label, parent=parent_node)

    def add_series_story_nodes(self, tree: ReaderTreeView, series: str, parent_node: TreeViewNode):
        title_list = self.main_screen.title_lists[series]

        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=parent_node)

    def get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
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
