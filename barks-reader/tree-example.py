import logging
import os.path
import sys
from enum import Enum, auto
from random import randrange
from typing import List, Union, Dict

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

from barks_fantagraphics.barks_titles import Titles, get_title_dict, ComicBookInfo
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


class SearchBoxTreeViewNode(FloatLayout, TreeViewNode):
    name = "Search Box"
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


class TreeNodes(Enum):
    INITIAL = auto()
    ON_INTRO_NODE = auto()
    ON_THE_STORIES_NODE = auto()
    ON_SEARCH_NODE = auto()
    ON_APPENDIX_NODE = auto()
    ON_INDEX_NODE = auto()
    ON_CHRONO_BY_YEAR_NODE = auto()
    ON_YEAR_RANGE_NODE = auto()
    ON_DDA_NODE = auto()
    ON_TITLE_NODE = auto()
    ON_SEARCH_BOX_NODE_NO_TITLE = auto()
    ON_SEARCH_BOX_NODE = auto()


class MainScreen(BoxLayout):
    MAIN_TITLE_BACKGROUND_COLOR = (1, 1, 1, 0.05)
    MAIN_TITLE_COLOR = (1, 1, 0, 1)
    TITLE_INFO_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)
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
    title_page_image = ObjectProperty()
    title_page_button = ObjectProperty()

    def __init__(self, filtered_title_lists: FilteredTitleLists, **kwargs):
        super().__init__(**kwargs)

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

        self.top_view_change_event = None
        self.bottom_view_change_after_event = None

        self.update_visibilities()

    def node_expanded(self, tree: ReaderTreeView, node: TreeViewNode):
        if isinstance(node, YearRangeTreeViewNode):
            self.current_tree_node = TreeNodes.ON_YEAR_RANGE_NODE
            self.current_year_range = node.text
            self.set_next_top_view_image()
            self.set_next_bottom_view_image()
        elif isinstance(node, CategoryTreeViewNode):
            if node.text == SERIES_DDA:
                self.current_tree_node = TreeNodes.ON_DDA_NODE
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

    def search_box_pressed(self, instance):
        print("Search box pressed", instance)

        self.current_tree_node = TreeNodes.ON_SEARCH_BOX_NODE_NO_TITLE
        self.update_visibilities()

        instance.spinner.text = ""

    def search_box_text_changed(self, instance, value):
        print("Search box text changed", instance, "text:", value)

        self.current_tree_node = TreeNodes.ON_SEARCH_BOX_NODE_NO_TITLE
        self.update_visibilities()

        if len(value) <= 1:
            instance.spinner.text = ""
            instance.spinner.is_open = False
        else:
            titles = self.get_matching_titles(str(value))
            if titles:
                instance.spinner.values = titles
                instance.spinner.text = titles[0]
                instance.spinner.is_open = True
                print(f'Spinner text set to "{instance.spinner.text}".')
                self.search_box_value_changed(instance.spinner, instance.spinner.text)
            else:
                instance.spinner.values = []
                instance.spinner.text = ""
                instance.spinner.is_open = False

    def get_matching_titles(self, value: str) -> List[str]:
        title_list = self.title_search.get_titles(value)
        if len(value) > 2:
            unique_extend(title_list, self.title_search.get_titles_containing(value))

        return self.title_search.get_titles_as_strings(title_list)

    def search_box_value_changed(self, spinner: Spinner, title_str: str):
        print(f'Spinner value changed: "{title_str}".')
        if not title_str:
            return

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            return

        self.current_tree_node = TreeNodes.ON_SEARCH_BOX_NODE
        self.update_visibilities()

        self.fanta_info = self.all_fanta_titles[title_str]
        print(f'New fanta_info: "{self.fanta_info.comic_book_info.title_str}".')
        self.set_title()

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

    def dda_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_DDA_NODE
        self.update_visibilities()

    def title_row_button_pressed(self, button: Button):
        self.current_tree_node = TreeNodes.ON_TITLE_NODE
        self.update_visibilities()

        self.fanta_info = button.parent.fanta_info
        self.set_title()

    def set_title(self) -> None:
        print(f'Setting title = "{self.fanta_info.comic_book_info.title_str}".')

        comic_inset_file = get_comic_inset_file(self.fanta_info.comic_book_info.title)
        title_info_image = get_random_title_image(self.fanta_info.comic_book_info.title_str)

        self.main_title.text = self.fanta_info.comic_book_info.get_display_title()
        self.title_info.text = self.get_title_info()
        self.title_page_image.source = comic_inset_file
        self.bottom_view_before_image.source = title_info_image

    def image_pressed(self):
        if self.fanta_info is None:
            print(f'Image "{self.title_page_image.source}" pressed. No title selected.')
            return

        if self.comic_reader.reader_is_running:
            print(f'Image "{self.title_page_image.source}" pressed. Already reading comic.')
            return

        comic_file_stem = get_dest_comic_zip_file_stem(
            self.fanta_info.comic_book_info.title_str,
            self.fanta_info.fanta_chronological_number,
            self.fanta_info.get_short_issue_title(),
        )

        print(f'Image "{self.title_page_image.source}" pressed. Want to run "{comic_file_stem}".')

        self.comic_reader.show_comic(comic_file_stem)

        print(f"Exited image press.")

    def get_title_info(self) -> str:
	    # TODO: Clean this up.
        issue_info = get_formatted_first_published_str(self.fanta_info).replace("Comics and Stories", "Comics & Stories")
        submitted_info = get_long_formatted_submitted_date(self.fanta_info)
        fanta_book = FANTA_SOURCE_COMICS[self.fanta_info.fantagraphics_volume]
        source = f"{FAN} CBDL, Vol {fanta_book.volume}, {fanta_book.year}"
        return (
            f"[i]1st Issue:[/i]   [b]{issue_info}[/b]\n"
            f"[i]Submitted:[/i] [b]{submitted_info}[/b]\n"
            f"[i]Source:[/i]       [b]{source}[/b]"
        )

    def update_visibilities(self):
        if self.current_tree_node == TreeNodes.ON_INTRO_NODE:
            self.bottom_view.opacity = 0.0
            self.intro_text.opacity = 1.0
            self.bottom_view_after_image.color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.bottom_view_before_image.color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG
        elif self.current_tree_node in [TreeNodes.ON_SEARCH_BOX_NODE, TreeNodes.ON_TITLE_NODE]:
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
            case TreeNodes.ON_SEARCH_BOX_NODE_NO_TITLE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_SEARCH_BOX_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRACKING_SANDY)
            case TreeNodes.ON_APPENDIX_NODE:
                self.top_view_image.source = get_comic_inset_file(
                    Titles.FABULOUS_PHILOSOPHERS_STONE_THE
                )
            case TreeNodes.ON_INDEX_NODE:
                self.top_view_image.source = get_comic_inset_file(Titles.TRUANT_OFFICER_DONALD)
            case TreeNodes.ON_CHRONO_BY_YEAR_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[ALL_LISTS])
            case TreeNodes.ON_DDA_NODE:
                self.top_view_image.source = get_random_image(self.title_lists[SERIES_DDA])
            case TreeNodes.ON_YEAR_RANGE_NODE:
                print(f"Year range: {self.current_year_range}")
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
            f"Category: {self.current_tree_node}."
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
            TreeNodes.ON_SEARCH_BOX_NODE_NO_TITLE,
            TreeNodes.ON_SEARCH_BOX_NODE,
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
        search_node = tree.add_node(search_label)
        search_box_label = SearchBoxTreeViewNode()
        search_box_label.on_pressed = self.main_screen.search_box_pressed
        search_box_label.bind(text=self.main_screen.search_box_text_changed)
        search_box_label.spinner.bind(text=self.main_screen.search_box_value_changed)
        tree.add_node(search_box_label, parent=search_node)

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

        dda_label = CategoryTreeViewNode(text=SERIES_DDA)
        dda_label.bind(on_press=self.main_screen.dda_pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_range_nodes(self, tree, the_years_node):
        for year_range in self.filtered_title_lists.year_ranges:
            range_str = f"{year_range[0]} - {year_range[1]}"
            year_range_label = YearRangeTreeViewNode(text=range_str)
            year_range_label.bind(on_press=self.main_screen.year_range_pressed)

            year_range_node = tree.add_node(year_range_label, parent=the_years_node)
            self.add_year_range_story_nodes(
                tree, year_range_node, self.main_screen.title_lists[range_str]
            )

    def add_year_range_story_nodes(
        self, tree, year_range_node, title_list: List[FantaComicBookInfo]
    ):
        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=year_range_node)

    def add_dda_story_nodes(self, tree, dda_node):
        title_list = self.main_screen.title_lists[SERIES_DDA]

        for title_info in title_list:
            tree.add_node(self.get_title_tree_view_node(title_info), parent=dda_node)

    def get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
        title_node = TitleTreeViewNode(full_fanta_info)

        title_node.num_label.text = str(full_fanta_info.fanta_chronological_number)
        title_node.num_label.bind(on_press=self.main_screen.title_row_button_pressed)

        title_node.num_label.color_selected = (0, 0, 1, 1)

        title_node.title_label.text = full_fanta_info.comic_book_info.get_display_title()
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
