import logging
from typing import Union, Dict, List

from kivy.clock import Clock
from kivy.metrics import sp
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import TreeViewNode

from background_views import BackgroundViews, ViewStates
from barks_fantagraphics.barks_tags import (
    BARKS_TAG_CATEGORIES_DICT,
)
from barks_fantagraphics.barks_titles import ComicBookInfo, Titles, get_title_dict, BARKS_TITLES
from barks_fantagraphics.comics_utils import get_dest_comic_zip_file_stem
from barks_fantagraphics.fanta_comics_info import (
    FantaComicBookInfo,
    get_all_fanta_comic_book_info,
    SERIES_CS,
    SERIES_DDA,
)
from barks_fantagraphics.title_search import BarksTitleSearch
from file_paths import (
    get_mcomix_python_bin_path,
    get_mcomix_path,
    get_mcomix_barks_reader_config_path,
    get_the_comic_zips_dir,
    get_comic_inset_file,
    get_barks_reader_app_icon_file,
)
from filtered_title_lists import FilteredTitleLists
from mcomix_reader import ComicReader
from random_title_images import get_random_title_image, ALL_BUT_ORIGINAL_ART
from reader_formatter import ReaderFormatter, get_clean_text_without_num_titles
from reader_ui_classes import (
    ReaderTreeView,
    YearRangeTreeViewNode,
    StoryGroupTreeViewNode,
    TitleSearchBoxTreeViewNode,
    TagSearchBoxTreeViewNode,
)


class MainScreen(BoxLayout):
    MAIN_TITLE_BACKGROUND_COLOR = (1, 1, 1, 0.05)
    MAIN_TITLE_COLOR = (1, 1, 0, 1)
    MAIN_TITLE_FONT_NAME = "Carl Barks Script"
    MAIN_TITLE_FONT_SIZE = sp(28)
    main_title_text = StringProperty()

    TITLE_INFO_LABEL_COLOR = (1.0, 0.99, 0.9, 1.0)
    TITLE_EXTRA_INFO_LABEL_COLOR = (1.0, 1.0, 1.0, 1.0)
    title_info_text = StringProperty()
    extra_title_info_text = StringProperty()
    title_page_image_source = StringProperty()
    app_icon_file = StringProperty(get_barks_reader_app_icon_file())

    DEBUG_BACKGROUND_OPACITY = 0

    reader_tree_view: ReaderTreeView = ObjectProperty()

    intro_text = StringProperty()
    intro_text_opacity = NumericProperty(0.0)

    top_view_image_source = StringProperty()
    top_view_image_color = ColorProperty()
    top_view_image_opacity = NumericProperty(1.0)

    bottom_view_title_opacity = NumericProperty(0.0)
    bottom_view_title_image_source = StringProperty()
    bottom_view_title_image_color = ColorProperty()
    bottom_view_fun_image_opacity = NumericProperty(1.0)
    bottom_view_fun_image_source = StringProperty()
    bottom_view_fun_image_color = ColorProperty()

    def __init__(self, filtered_title_lists: FilteredTitleLists, **kwargs):
        super().__init__(**kwargs)

        self.formatter = ReaderFormatter()
        self.fanta_info: Union[FantaComicBookInfo, None] = None
        self.year_range_nodes = None

        self.filtered_title_lists: FilteredTitleLists = filtered_title_lists
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

        self.top_view_image_title = None
        self.bottom_view_fun_image_title = None

        self.background_views = BackgroundViews(self.title_lists)
        self.update_background_views(ViewStates.INITIAL)

    def on_action_bar_collapse(self):
        print(f"Action bar collapse pressed.")
        something_was_open = False
        for node in self.reader_tree_view.iterate_open_nodes():
            if node.is_open:
                self.reader_tree_view.toggle_node(node)
                self.close_open_nodes(node)
                something_was_open = True

        if something_was_open:
            self.update_background_views(ViewStates.INITIAL)

    def close_open_nodes(self, start_node: TreeViewNode) -> None:
        for node in start_node.nodes:
            if node.is_open:
                self.reader_tree_view.toggle_node(node)
                self.close_open_nodes(node)

    def on_action_bar_change_view_images(self):
        print(f"Action bar change pics pressed.")
        self.change_background_views()

    def on_action_bar_goto(self, button: Button):
        print(f"Action bar goto pressed: '{button.text}'")
        node = self.find_node(self.reader_tree_view.root, button.text)
        if node:
            print(f"Found node '{node.text}'.")
            self.close_open_nodes(self.reader_tree_view.root)
            self.open_all_parent_nodes(node)
            self.goto_node(node)
            # TODO: Need on_press to be called

    @staticmethod
    def find_node(start_node: TreeViewNode, node_text: str):
        nodes_to_visit = start_node.nodes.copy()

        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            if not hasattr(current_node, "text"):
                continue
            current_node_text = get_clean_text_without_num_titles(current_node.text)
            if current_node_text == node_text:
                return current_node
            nodes_to_visit.extend(current_node.nodes)

        return None

    def on_action_bar_pressed(self, button: Button):
        print(f"Action bar pressed: '{button.text}'")

    def on_goto_top_view_title(self) -> None:
        print("Pressed goto top view title.")

        self.goto_chrono_title(self.top_view_image_title, self.top_view_image_source)

    def on_goto_fun_view_title(self, _button: Button) -> None:
        print("Pressed goto bottom view title.")

        self.goto_chrono_title(self.bottom_view_fun_image_title, self.bottom_view_fun_image_source)

    def goto_chrono_title(self, title: Titles, image_source: str) -> None:
        title_fanta_info = self.get_fanta_info(title)

        year_nodes = self.year_range_nodes[
            self.filtered_title_lists.get_year_range_from_info(title_fanta_info)
        ]
        self.open_all_parent_nodes(year_nodes)

        title_node = self.find_title_node(year_nodes, title)
        self.goto_node(title_node, scroll_to=True)

        self.title_row_selected(title_fanta_info, image_source)

    def goto_node(self, node: TreeViewNode, scroll_to=False) -> None:
        def show_node(n):
            self.reader_tree_view.select_node(n)
            if scroll_to:
                self.ids.scroll_view.scroll_to(n)

        Clock.schedule_once(lambda dt, item=node: show_node(item))

    def get_fanta_info(self, title: Titles) -> FantaComicBookInfo:
        # TODO: Very roundabout way to get fanta info
        title_str = BARKS_TITLES[title]
        return self.all_fanta_titles[title_str]

    @staticmethod
    def find_title_node(start_node: TreeViewNode, target_title: Titles):
        nodes_to_visit = start_node.nodes.copy()

        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            node_title = current_node.get_title()
            if node_title == target_title:
                return current_node
            nodes_to_visit.extend(current_node.nodes)

        return None

    def title_row_selected(self, new_fanta_info: FantaComicBookInfo, title_image_file: str):
        self.fanta_info = new_fanta_info
        self.set_title(title_image_file)

        self.update_background_views(ViewStates.ON_TITLE_NODE)

    def open_all_parent_nodes(self, node: TreeViewNode) -> None:
        parent_node = node
        while parent_node and isinstance(parent_node, TreeViewNode):
            if not parent_node.is_open:
                self.reader_tree_view.toggle_node(parent_node)
            parent_node = parent_node.parent_node

    def on_node_expanded(self, _tree: ReaderTreeView, node: TreeViewNode):
        if isinstance(node, YearRangeTreeViewNode):
            self.update_background_views(ViewStates.ON_YEAR_RANGE_NODE, year_range=node.text)
        elif isinstance(node, StoryGroupTreeViewNode):
            if node.text == SERIES_CS:
                self.update_background_views(ViewStates.ON_CS_NODE)
            elif node.text == SERIES_DDA:
                self.update_background_views(ViewStates.ON_DDA_NODE)
            elif node.text in BARKS_TAG_CATEGORIES_DICT:
                self.update_background_views(ViewStates.ON_CATEGORY_NODE, category=node.text)

    def on_intro_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_INTRO_NODE)

        self.intro_text = "hello line 1\nhello line 2\nhello line 3\n"

    def on_the_stories_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_THE_STORIES_NODE)

    def on_search_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_SEARCH_NODE)

    def on_title_search_box_pressed(self, instance: TitleSearchBoxTreeViewNode):
        logging.debug(f"Title search box pressed: {instance}.")

        if not instance.get_current_title():
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_title_search_box_title_changed(self, _spinner: Spinner, title_str: str):
        logging.debug(f'Title search box title changed: "{title_str}".')

        if not title_str:
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)
        elif self.update_title(title_str):
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE)
        else:
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_pressed(self, instance: TagSearchBoxTreeViewNode):
        logging.debug(f"Tag search box pressed: {instance}.")

        if not instance.get_current_tag():
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_text_changed(self, instance: TagSearchBoxTreeViewNode, text: str):
        logging.debug(f'Tag search box text changed: text: "{text}".')

        if not instance.get_current_title():
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_tag_changed(self, instance: TagSearchBoxTreeViewNode, tag_str: str):
        logging.debug(f'Tag search box tag changed: "{tag_str}".')

        if not tag_str:
            return

        if not instance.get_current_title():
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_title_changed(self, _instance, title_str: str):
        logging.debug(f'Tag search box title changed: "{title_str}".')

        if not title_str:
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)
        elif self.update_title(title_str):
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE)
        else:
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def update_title(self, title_str: str) -> bool:
        logging.debug(f'Update title: "{title_str}".')
        assert title_str != ""

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            logging.debug(f'Update title: Not configured yet: "{title_str}".')
            return False

        self.fanta_info = self.all_fanta_titles[title_str]
        self.set_title()
        return True

    def on_appendix_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_APPENDIX_NODE)

    def on_index_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_INDEX_NODE)

    def on_chrono_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CHRONO_BY_YEAR_NODE)

    def on_year_range_pressed(self, button: Button):
        self.update_background_views(ViewStates.ON_YEAR_RANGE_NODE, year_range=button.text)

    def on_series_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_SERIES_NODE)

    def cs_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CS_NODE)

    def dda_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_DDA_NODE)

    def on_categories_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_CATEGORIES_NODE)

    def on_category_pressed(self, button: Button):
        self.update_background_views(ViewStates.ON_CATEGORY_NODE, category=button.text)

    def on_title_row_button_pressed(self, button: Button):
        self.fanta_info = button.parent.fanta_info
        self.set_title()

        self.update_background_views(ViewStates.ON_TITLE_NODE)

    def change_background_views(self) -> None:
        self.update_background_views(
            self.background_views.get_view_state(),
            self.background_views.get_current_category(),
            self.background_views.get_current_year_range(),
        )

    def update_background_views(
        self, tree_node: ViewStates, category: str = "", year_range: str = ""
    ) -> None:
        self.background_views.set_current_category(category)
        self.background_views.set_current_year_range(get_clean_text_without_num_titles(year_range))

        self.background_views.set_view_state(tree_node)

        self.intro_text_opacity = 0.0

        self.top_view_image_title = self.background_views.get_top_view_image_title()
        self.top_view_image_opacity = self.background_views.get_top_view_image_opacity()
        self.top_view_image_source = self.background_views.get_top_view_image_file()
        self.top_view_image_color = self.background_views.get_top_view_image_color()

        self.bottom_view_fun_image_opacity = (
            self.background_views.get_bottom_view_fun_image_opacity()
        )
        self.bottom_view_fun_image_title = self.background_views.get_bottom_view_fun_image_title()
        self.bottom_view_fun_image_source = self.background_views.get_bottom_view_fun_image_file()
        self.bottom_view_fun_image_color = self.background_views.get_bottom_view_fun_image_color()
        self.bottom_view_title_opacity = self.background_views.get_bottom_view_title_opacity()
        self.bottom_view_title_image_source = (
            self.background_views.get_bottom_view_title_image_file()
        )
        self.bottom_view_title_image_color = (
            self.background_views.get_bottom_view_title_image_color()
        )

    def set_title(self, title_image_file: str = "") -> None:
        logging.debug(f'Setting title to "{self.fanta_info.comic_book_info.get_title_str()}".')

        if not title_image_file:
            title_image_file = get_random_title_image(
                self.fanta_info.comic_book_info.get_title_str(), ALL_BUT_ORIGINAL_ART
            )
        self.background_views.set_bottom_view_title_image_file(title_image_file)

        self.main_title_text = self.get_main_title_str()
        self.title_info_text = self.formatter.get_title_info(self.fanta_info)
        self.extra_title_info_text = self.formatter.get_extra_title_info(self.fanta_info)
        self.title_page_image_source = get_comic_inset_file(
            self.fanta_info.comic_book_info.title, use_edited=True
        )

    def get_main_title_str(self):
        if self.fanta_info.comic_book_info.is_barks_title:
            return self.fanta_info.comic_book_info.get_title_str()

        return self.fanta_info.comic_book_info.get_title_from_issue_name()

    def on_image_pressed(self):
        if self.fanta_info is None:
            logging.debug(f'Image "{self.title_page_image_source}" pressed. But no title selected.')
            return

        if self.comic_reader.reader_is_running:
            logging.debug(
                f'Image "{self.title_page_image_source}" pressed. But already reading comic.'
            )
            return

        comic_file_stem = get_dest_comic_zip_file_stem(
            self.fanta_info.comic_book_info.get_title_str(),
            self.fanta_info.fanta_chronological_number,
            self.fanta_info.get_short_issue_title(),
        )

        logging.debug(
            f'Image "{self.title_page_image_source}" pressed. Want to run "{comic_file_stem}".'
        )

        self.comic_reader.show_comic(comic_file_stem)

        logging.debug(f"Comic reader is running.")
