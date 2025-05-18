from typing import Union, Dict, List

from kivy.core.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeViewNode

from background_views import BackgroundViews, ViewStates
from barks_fantagraphics.barks_tags import (
    Tags,
    BARKS_TAG_CATEGORIES_DICT,
    TagGroups,
)
from barks_fantagraphics.barks_titles import ComicBookInfo, Titles, get_title_dict
from barks_fantagraphics.comics_utils import get_dest_comic_zip_file_stem
from barks_fantagraphics.fanta_comics_info import (
    FantaComicBookInfo,
    get_all_fanta_comic_book_info,
    SERIES_CS,
    SERIES_DDA,
    ALL_LISTS,
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
from reader_ui_classes import ReaderTreeView, YearRangeTreeViewNode, StoryGroupTreeViewNode


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
        self.update_title(title_str)

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
