import logging
from typing import List, Callable, Tuple, Dict

from kivy.uix.treeview import TreeViewNode
from kivy.utils import escape_markup

from barks_fantagraphics.barks_tags import (
    TagCategories,
    BARKS_TAG_CATEGORIES,
    Tags,
    TagGroups,
    BARKS_TAG_GROUPS_TITLES,
    get_tagged_titles,
)
from barks_fantagraphics.barks_titles import BARKS_TITLES, Titles, ComicBookInfo
from barks_fantagraphics.comics_utils import (
    get_short_formatted_first_published_str,
    get_short_submitted_day_and_month,
)
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo, SERIES_CS, SERIES_DDA
from filtered_title_lists import FilteredTitleLists
from main_screen import MainScreen
from reader_formatter import (
    get_markup_text_with_num_titles,
    get_bold_markup_text,
    get_markup_text_with_extra,
)
from reader_ui_classes import (
    ReaderTreeView,
    MainTreeViewNode,
    TitleSearchBoxTreeViewNode,
    TagSearchBoxTreeViewNode,
    StoryGroupTreeViewNode,
    YearRangeTreeViewNode,
    CsYearRangeTreeViewNode,
    TitleTreeViewNode,
)


class ReaderTreeBuilder:
    def __init__(
        self,
        main_screen: MainScreen,
    ):
        self.__main_screen = main_screen

        self.year_range_nodes: Dict[Tuple[int, int], TreeViewNode] = {}

    def build_main_screen_tree(self):
        tree: ReaderTreeView = self.__main_screen.ids.reader_tree_view

        tree.bind(on_node_expand=self.__main_screen.on_node_expanded)

        self.__add_intro_node(tree)
        self.__add_the_stories_node(tree)
        self.__add_search_node(tree)
        self.__add_appendix_node(tree)
        self.__add_index_node(tree)

        tree.bind(minimum_height=tree.setter("height"))

    def __add_intro_node(self, tree: ReaderTreeView):
        self.__create_and_add_simple_node(tree, "Introduction", self.__main_screen.on_intro_pressed)

    def __add_the_stories_node(self, tree: ReaderTreeView):
        new_node = self.__create_and_add_simple_node(
            tree, "The Stories", self.__main_screen.on_the_stories_pressed
        )
        self.__add_story_nodes(tree, new_node)

    def __add_search_node(self, tree: ReaderTreeView):
        search_node = self.__create_and_add_simple_node(
            tree, "Search", self.__main_screen.on_search_pressed
        )

        self.__create_and_add_title_search_box_node(tree, search_node)
        self.__create_and_add_tag_search_box_node(tree, search_node)

    def __add_appendix_node(self, tree: ReaderTreeView):
        self.__create_and_add_simple_node(tree, "Appendix", self.__main_screen.on_appendix_pressed)

    def __add_index_node(self, tree: ReaderTreeView):
        self.__create_and_add_simple_node(tree, "Index", self.__main_screen.on_index_pressed)

    def __add_story_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        new_node = self.__create_and_add_simple_node(
            tree,
            "Chronological",
            self.__main_screen.on_chrono_pressed,
            True,
            StoryGroupTreeViewNode,
            parent_node,
        )
        self.__add_year_range_nodes(tree, new_node)

        new_node = self.__create_and_add_simple_node(
            tree,
            "Series",
            self.__main_screen.on_series_pressed,
            True,
            StoryGroupTreeViewNode,
            parent_node,
        )
        self.__add_series_nodes(tree, new_node)

        new_node = self.__create_and_add_simple_node(
            tree,
            "Categories",
            self.__main_screen.on_categories_pressed,
            True,
            StoryGroupTreeViewNode,
            parent_node,
        )
        self.__add_categories_nodes(tree, new_node)

    def __add_year_range_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for year_range in self.__main_screen.filtered_title_lists.chrono_year_ranges:
            new_node, year_range_titles = self.__add_year_range_node(tree, year_range, parent_node)
            self.__add_year_range_story_nodes(tree, year_range_titles, new_node)

            self.year_range_nodes[year_range] = new_node

    def __add_year_range_node(
        self, tree: ReaderTreeView, year_range: Tuple[int, int], parent_node: TreeViewNode
    ) -> Tuple[TreeViewNode, List[FantaComicBookInfo]]:
        return self.__create_and_add_year_range_node(
            tree,
            year_range,
            self.__main_screen.on_year_range_pressed,
            lambda x: x,
            self.__get_year_range_extra_text,
            YearRangeTreeViewNode,
            parent_node,
        )

    @staticmethod
    def __get_year_range_extra_text(title_list: List[FantaComicBookInfo]) -> str:
        return str(len(title_list))

    def __add_year_range_story_nodes(
        self, tree: ReaderTreeView, title_list: List[FantaComicBookInfo], parent_node: TreeViewNode
    ):
        self.__add_fanta_info_story_nodes(tree, title_list, parent_node)

    def __add_categories_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for category in TagCategories:
            new_node = self.__create_and_add_simple_node(
                tree,
                category.value,
                self.__main_screen.on_category_pressed,
                True,
                StoryGroupTreeViewNode,
                parent_node,
            )
            self.__add_category_node(tree, category, new_node)

    def __add_category_node(
        self, tree: ReaderTreeView, category: TagCategories, parent_node: TreeViewNode
    ):
        for tag_or_group in BARKS_TAG_CATEGORIES[category]:
            if type(tag_or_group) == Tags:
                self.__add_tag_node(tree, tag_or_group, parent_node)
            else:
                assert type(tag_or_group) == TagGroups
                titles = BARKS_TAG_GROUPS_TITLES[tag_or_group]
                tag_group_node = self.__add_tag_group_node(tree, tag_or_group, titles, parent_node)
                self.__add_title_nodes(tree, titles, tag_group_node)

    def __add_tag_node(self, tree: ReaderTreeView, tag: Tags, parent_node: TreeViewNode):
        titles = get_tagged_titles(tag)
        new_node = StoryGroupTreeViewNode(
            text=get_markup_text_with_num_titles(tag.value, len(titles))
        )
        self.__add_tagged_story_nodes(tree, titles, new_node)
        tree.add_node(new_node, parent=parent_node)

    @staticmethod
    def __add_tag_group_node(
        tree: ReaderTreeView, tag_group: TagGroups, titles: List[Titles], parent_node: TreeViewNode
    ):
        node = StoryGroupTreeViewNode(
            text=get_markup_text_with_num_titles(tag_group.value, len(titles))
        )
        return tree.add_node(node, parent=parent_node)

    def __add_tagged_story_nodes(
        self, tree: ReaderTreeView, titles: List[Titles], parent_node: TreeViewNode
    ) -> None:
        self.__add_title_nodes(tree, titles, parent_node)

    def __add_title_nodes(
        self, tree: ReaderTreeView, titles: List[Titles], parent_node: TreeViewNode
    ) -> None:
        for title in titles:
            # TODO: Very roundabout way to get fanta info
            title_str = BARKS_TITLES[title]
            if title_str not in self.__main_screen.all_fanta_titles:
                logging.debug(f'Skipped unconfigured title "{title_str}".')
                continue
            title_info = self.__main_screen.all_fanta_titles[title_str]
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __add_series_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        self.__add_series_node(tree, SERIES_CS, self.__main_screen.cs_pressed, parent_node)
        self.__add_series_node(tree, SERIES_DDA, self.__main_screen.dda_pressed, parent_node)

    def __add_series_node(
        self, tree: ReaderTreeView, series: str, on_pressed: Callable, parent_node: TreeViewNode
    ) -> None:
        if series == SERIES_CS:
            self.__add_cs_node(tree, on_pressed, parent_node)
        else:
            title_list = self.__main_screen.title_lists[series]
            series_text = get_markup_text_with_num_titles(series, len(title_list))

            new_node = StoryGroupTreeViewNode(text=series_text)
            new_node.bind(on_press=on_pressed)
            self.__add_series_story_nodes(tree, title_list, new_node)

            tree.add_node(new_node, parent=parent_node)

    def __add_cs_node(
        self, tree: ReaderTreeView, on_pressed: Callable, parent_node: TreeViewNode
    ) -> None:
        title_list = self.__main_screen.title_lists[SERIES_CS]

        series_text = get_markup_text_with_num_titles(SERIES_CS, len(title_list))
        series_node = StoryGroupTreeViewNode(text=series_text)
        series_node.bind(on_press=on_pressed)

        for year_range in self.__main_screen.filtered_title_lists.cs_year_ranges:
            new_node, year_range_titles = self.__add_cs_year_range_node(
                tree, year_range, series_node
            )
            self.__add_year_range_story_nodes(tree, year_range_titles, new_node)

        tree.add_node(series_node, parent=parent_node)

    def __add_cs_year_range_node(
        self, tree: ReaderTreeView, year_range: Tuple[int, int], parent_node: TreeViewNode
    ) -> Tuple[TreeViewNode, List[FantaComicBookInfo]]:
        return self.__create_and_add_year_range_node(
            tree,
            year_range,
            self.__main_screen.on_cs_year_range_pressed,
            FilteredTitleLists.get_cs_range_str_from_str,
            self.__get_cs_year_range_extra_text,
            CsYearRangeTreeViewNode,
            parent_node,
        )

    @staticmethod
    def __get_cs_year_range_extra_text(title_list: List[FantaComicBookInfo]) -> str:
        first_issue = min(
            title_list, key=lambda x: x.comic_book_info.issue_number
        ).comic_book_info.issue_number
        last_issue = max(
            title_list, key=lambda x: x.comic_book_info.issue_number
        ).comic_book_info.issue_number

        return f"WDCS {first_issue}-{last_issue}"

    def __add_series_story_nodes(
        self,
        tree: ReaderTreeView,
        title_list: List[FantaComicBookInfo],
        parent_node: TreeViewNode,
    ) -> None:
        self.__add_fanta_info_story_nodes(tree, title_list, parent_node)

    def __add_fanta_info_story_nodes(
        self,
        tree: ReaderTreeView,
        title_info_list: List[FantaComicBookInfo],
        parent_node: TreeViewNode,
    ):
        for title_info in title_info_list:
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
        title_node = TitleTreeViewNode(full_fanta_info)

        title_node.ids.num_label.text = str(full_fanta_info.fanta_chronological_number)
        title_node.ids.num_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        title_node.ids.num_label.color_selected = (0, 0, 1, 1)

        title_node.ids.title_label.text = full_fanta_info.comic_book_info.get_display_title()
        title_node.ids.title_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        first_published = get_short_formatted_first_published_str(full_fanta_info.comic_book_info)
        submitted_date = self.get_formatted_submitted_str(full_fanta_info.comic_book_info)
        issue_info = f"[i]{first_published}" f"{submitted_date}[/i]"

        title_node.ids.issue_label.text = issue_info
        title_node.ids.issue_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        return title_node

    @staticmethod
    def get_formatted_submitted_str(comic_book_info: ComicBookInfo) -> str:
        left_sq_bracket = escape_markup("[")
        right_sq_bracket = escape_markup("]")

        return (
            f" {left_sq_bracket}"
            f"{get_short_submitted_day_and_month(comic_book_info)}"
            f" [b][color={TitleTreeViewNode.ISSUE_LABEL_SUBMITTED_YEAR_COLOR}]"
            f" [b]"
            f"{comic_book_info.submitted_year}"
            f"[/color][/b]"
            f"[/b]"
            f"{right_sq_bracket}"
        )

    @staticmethod
    def __create_and_add_simple_node(
        tree: ReaderTreeView,
        text: str,
        on_press_handler: Callable,
        is_bold: bool = False,
        node_class: type = MainTreeViewNode,
        parent_node: TreeViewNode = None,
    ) -> TreeViewNode:
        node_text = get_bold_markup_text(text) if is_bold else text

        new_node = node_class(text=node_text)
        new_node.bind(on_press=on_press_handler)

        return tree.add_node(new_node, parent=parent_node)

    def __create_and_add_title_search_box_node(
        self, tree: ReaderTreeView, parent_node: TreeViewNode
    ):
        new_node = TitleSearchBoxTreeViewNode(self.__main_screen.title_search)

        new_node.bind(on_title_search_box_pressed=self.__main_screen.on_title_search_box_pressed)
        new_node.bind(
            on_title_search_box_title_changed=self.__main_screen.on_title_search_box_title_changed
        )

        return tree.add_node(new_node, parent=parent_node)

    def __create_and_add_tag_search_box_node(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        new_node = TagSearchBoxTreeViewNode(self.__main_screen.title_search)

        new_node.bind(on_tag_search_box_pressed=self.__main_screen.on_tag_search_box_pressed)
        new_node.bind(
            on_tag_search_box_text_changed=self.__main_screen.on_tag_search_box_text_changed
        )
        new_node.bind(
            on_tag_search_box_tag_changed=self.__main_screen.on_tag_search_box_tag_changed
        )
        new_node.bind(
            on_tag_search_box_title_changed=self.__main_screen.on_tag_search_box_title_changed
        )

        return tree.add_node(new_node, parent=parent_node)

    def __create_and_add_year_range_node(
        self,
        tree: ReaderTreeView,
        year_range: Tuple[int, int],
        on_press_handler: Callable,
        get_title_key_func: Callable[[str], str],
        get_year_range_extra_text_func: Callable[[List[FantaComicBookInfo]], str],
        node_class: type,
        parent_node: TreeViewNode,
    ) -> Tuple[TreeViewNode, List[FantaComicBookInfo]]:
        year_range_str = FilteredTitleLists.get_range_str(year_range)
        year_range_key = get_title_key_func(year_range_str)
        year_range_titles = self.__main_screen.title_lists[year_range_key]

        year_range_extra_text = get_year_range_extra_text_func(year_range_titles)
        year_range_text = get_markup_text_with_extra(year_range_str, year_range_extra_text)

        new_node = node_class(text=year_range_text)
        new_node.bind(on_press=on_press_handler)

        new_node = tree.add_node(new_node, parent=parent_node)

        return new_node, year_range_titles
