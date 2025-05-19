import logging
from typing import Union, Dict, List

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
from barks_fantagraphics.barks_titles import ComicBookInfo, Titles, get_title_dict
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
)
from filtered_title_lists import FilteredTitleLists
from mcomix_reader import ComicReader
from random_title_images import get_random_title_image
from reader_formatter import ReaderFormatter
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

    DEBUG_BACKGROUND_OPACITY = 0

    reader_tree_view: ReaderTreeView = ObjectProperty()

    intro_text = StringProperty()
    intro_text_opacity = NumericProperty(0.0)

    top_view_image_source = StringProperty()
    top_view_image_color = ColorProperty()
    top_view_image_opacity = NumericProperty(1.0)

    bottom_view_opacity = NumericProperty(1.0)
    bottom_view_after_image_source = StringProperty()
    bottom_view_after_image_color = ColorProperty()
    bottom_view_before_image_source = StringProperty()
    bottom_view_before_image_color = ColorProperty()

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

        self.intro_text = "hello line 1\nhello line 2\nhello line 3\n"

    def the_stories_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_THE_STORIES_NODE)

    def search_pressed(self, _button: Button):
        self.update_background_views(ViewStates.ON_SEARCH_NODE)

    def on_title_search_box_pressed(self, instance: TitleSearchBoxTreeViewNode):
        logging.debug(f"Title search box pressed: {instance}.")

        if not instance.title_search_box.text:
            instance.set_empty_title_spinner_text()
            self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_title_search_box_title_pressed(self, instance: TitleSearchBoxTreeViewNode):
        logging.debug(f"Title search box tite pressed: {instance}.")

        self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET)

        instance.set_empty_title_spinner_text()

    def on_title_search_box_title_changed(self, _spinner: Spinner, title_str: str):
        logging.debug(f'Title search box spinner value changed: title_str: "{title_str}".')
        if not title_str:
            return

        self.update_title(title_str)
        self.update_background_views(ViewStates.ON_TITLE_SEARCH_BOX_NODE)

    def on_tag_search_box_pressed(self, instance: TagSearchBoxTreeViewNode):
        logging.debug(f"Tag search box pressed: {instance}.")

        if not instance.tag_search_box.text:
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_tag_pressed(self, instance: TagSearchBoxTreeViewNode):
        logging.debug(f"Tag search box tag spinner pressed: {instance}.")

        if not instance.get_current_title():
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

    def on_tag_search_box_title_pressed(self, instance: TagSearchBoxTreeViewNode):
        logging.debug(f"Tag search box tag title spinner pressed: {instance}.")

        if not instance.get_current_title():
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET)

        #
        # if instance.tag_spinner.text and not instance.tag_title_spinner.text:
        #     self.tag_search_box_tag_spinner_value_changed(
        #         instance.tag_spinner, instance.tag_spinner.text
        #     )

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
        else:
            self.update_title(title_str)
            self.update_background_views(ViewStates.ON_TAG_SEARCH_BOX_NODE)

    def update_title(self, title_str: str):
        logging.debug(f'Update title: "{title_str}".')
        assert title_str != ""

        title_str = ComicBookInfo.get_title_str_from_display_title(title_str)

        if title_str not in self.all_fanta_titles:
            return

        self.fanta_info = self.all_fanta_titles[title_str]
        self.set_title()

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

        self.intro_text_opacity = 0.0

        self.top_view_image_opacity = self.background_views.get_top_view_image_opacity()
        self.top_view_image_source = self.background_views.get_top_view_image_file()
        self.top_view_image_color = self.background_views.get_top_view_image_color()

        self.bottom_view_opacity = self.background_views.get_bottom_view_image_opacity()
        self.bottom_view_after_image_source = (
            self.background_views.get_bottom_view_after_image_file()
        )
        self.bottom_view_after_image_color = (
            self.background_views.get_bottom_view_after_image_color()
        )
        self.bottom_view_before_image_source = (
            self.background_views.get_bottom_view_before_image_file()
        )
        self.bottom_view_before_image_color = (
            self.background_views.get_bottom_view_before_image_color()
        )

    def set_title(self) -> None:
        logging.debug(f'Setting title to "{self.fanta_info.comic_book_info.get_title_str()}".')

        comic_inset_file = get_comic_inset_file(self.fanta_info.comic_book_info.title)
        self.background_views.set_bottom_view_before_image(
            get_random_title_image(self.fanta_info.comic_book_info.get_title_str())
        )

        self.main_title_text = self.get_main_title_str()
        self.title_info_text = self.formatter.get_title_info(self.fanta_info)
        self.extra_title_info_text = self.formatter.get_extra_title_info(self.fanta_info)
        self.title_page_image_source = comic_inset_file

    def get_main_title_str(self):
        if self.fanta_info.comic_book_info.is_barks_title:
            return self.fanta_info.comic_book_info.get_title_str()

        return self.fanta_info.comic_book_info.get_title_from_issue_name()

    def image_pressed(self):
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
