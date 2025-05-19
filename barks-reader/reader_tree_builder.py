import logging
from typing import List, Callable

from kivy.uix.treeview import TreeViewNode

from barks_fantagraphics.barks_tags import (
    TagCategories,
    BARKS_TAG_CATEGORIES,
    Tags,
    TagGroups,
    BARKS_TAG_GROUPS_TITLES,
    get_tagged_titles,
)
from barks_fantagraphics.barks_titles import BARKS_TITLES, Titles
from barks_fantagraphics.comics_utils import (
    get_short_formatted_first_published_str,
    get_short_formatted_submitted_date,
)
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo, SERIES_CS, SERIES_DDA
from barks_fantagraphics.title_search import BarksTitleSearch
from filtered_title_lists import FilteredTitleLists
from main_screen import MainScreen
from reader_formatter import get_markup_text_with_num_titles, get_bold_markup_text
from reader_ui_classes import (
    ReaderTreeView,
    MainTreeViewNode,
    TitleSearchBoxTreeViewNode,
    TagSearchBoxTreeViewNode,
    StoryGroupTreeViewNode,
    YearRangeTreeViewNode,
    TitleTreeViewNode,
)


class ReaderTreeBuilder:
    def __init__(
        self,
        filtered_title_lists: FilteredTitleLists,
        title_search: BarksTitleSearch,
        main_screen: MainScreen,
    ):
        self.__filtered_title_lists = filtered_title_lists
        self.__title_search = title_search
        self.__main_screen = main_screen

    def build_main_screen_tree(self):
        tree: ReaderTreeView = self.__main_screen.reader_tree_view

        tree.bind(on_node_expand=self.__main_screen.on_node_expanded)

        self.__add_intro_node(tree)
        self.__add_the_stories_node(tree)
        self.__add_search_node(tree)
        self.__add_appendix_node(tree)
        self.__add_index_node(tree)

        tree.bind(minimum_height=tree.setter("height"))

    def __add_intro_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="Introduction")
        label.bind(on_press=self.__main_screen.on_intro_pressed)
        tree.add_node(label)

    def __add_the_stories_node(self, tree: ReaderTreeView):
        label = MainTreeViewNode(text="The Stories")
        label.bind(on_press=self.__main_screen.on_the_stories_pressed)
        new_node = tree.add_node(label)
        self.__add_story_nodes(tree, new_node)

    def __add_search_node(self, tree: ReaderTreeView):
        node = MainTreeViewNode(text="Search")
        node.bind(on_press=self.__main_screen.on_search_pressed)
        search_node = tree.add_node(node)

        node = TitleSearchBoxTreeViewNode(self.__title_search)
        node.bind(on_title_search_box_pressed=self.__main_screen.on_title_search_box_pressed)
        node.bind(
            on_title_search_box_title_changed=self.__main_screen.on_title_search_box_title_changed
        )
        tree.add_node(node, parent=search_node)

        node = TagSearchBoxTreeViewNode(self.__title_search)
        node.bind(on_tag_search_box_pressed=self.__main_screen.on_tag_search_box_pressed)
        node.bind(on_tag_search_box_text_changed=self.__main_screen.on_tag_search_box_text_changed)
        node.bind(on_tag_search_box_tag_changed=self.__main_screen.on_tag_search_box_tag_changed)
        node.bind(
            on_tag_search_box_title_changed=self.__main_screen.on_tag_search_box_title_changed
        )
        tree.add_node(node, parent=search_node)

    def __add_appendix_node(self, tree: ReaderTreeView):
        node = MainTreeViewNode(text="Appendix")
        node.bind(on_press=self.__main_screen.on_appendix_pressed)
        tree.add_node(node)

    def __add_index_node(self, tree: ReaderTreeView):
        node = MainTreeViewNode(text="Index")
        node.bind(on_press=self.__main_screen.on_index_pressed)
        tree.add_node(node)

    def __add_story_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        node = StoryGroupTreeViewNode(text=get_bold_markup_text("Chronological"))
        node.bind(on_press=self.__main_screen.on_chrono_pressed)
        new_node = tree.add_node(node, parent=parent_node)
        self.__add_year_range_nodes(tree, new_node)

        node = StoryGroupTreeViewNode(text=get_bold_markup_text("Series"))
        node.bind(on_press=self.__main_screen.on_series_pressed)
        new_node = tree.add_node(node, parent=parent_node)
        self.__add_series_nodes(tree, new_node)

        node = StoryGroupTreeViewNode(text=get_bold_markup_text("Categories"))
        node.bind(on_press=self.__main_screen.on_categories_pressed)
        new_node = tree.add_node(node, parent=parent_node)
        self.__add_categories_nodes(tree, new_node)

    def __add_year_range_nodes(self, tree: ReaderTreeView, parent_node: TreeViewNode):
        for year_range in self.__filtered_title_lists.year_ranges:
            year_range_str = f"{year_range[0]} - {year_range[1]}"
            year_range_titles = self.__main_screen.title_lists[year_range_str]
            year_range_text = get_markup_text_with_num_titles(
                year_range_str, len(year_range_titles)
            )
            node = YearRangeTreeViewNode(text=year_range_text)
            node.bind(on_press=self.__main_screen.on_year_range_pressed)

            new_node = tree.add_node(node, parent=parent_node)
            self.__add_year_range_story_nodes(tree, new_node, year_range_titles)

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
            node = StoryGroupTreeViewNode(text=get_bold_markup_text(category.value))
            node.bind(on_press=self.__main_screen.on_category_pressed)

            new_node = tree.add_node(node, parent=parent_node)
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
        node = StoryGroupTreeViewNode(text=get_markup_text_with_num_titles(tag.value, len(titles)))
        self.__add_tagged_story_nodes(tree, titles, node)
        tree.add_node(node, parent=parent_node)

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
        title_list = self.__main_screen.title_lists[series]
        series_text = get_markup_text_with_num_titles(series, len(title_list))

        node = StoryGroupTreeViewNode(text=series_text)
        node.bind(on_press=on_pressed)
        self.__add_series_story_nodes(tree, title_list, node)
        tree.add_node(node, parent=parent_node)

    def __add_series_story_nodes(
        self,
        tree: ReaderTreeView,
        title_list: List[FantaComicBookInfo],
        parent_node: TreeViewNode,
    ) -> None:
        for title_info in title_list:
            tree.add_node(self.__get_title_tree_view_node(title_info), parent=parent_node)

    def __get_title_tree_view_node(self, full_fanta_info: FantaComicBookInfo) -> TitleTreeViewNode:
        title_node = TitleTreeViewNode(full_fanta_info)

        title_node.num_label.text = str(full_fanta_info.fanta_chronological_number)
        title_node.num_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        title_node.num_label.color_selected = (0, 0, 1, 1)

        title_node.title_label.text = full_fanta_info.comic_book_info.get_display_title()
        title_node.title_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        issue_info = (
            f"{get_short_formatted_first_published_str(full_fanta_info.comic_book_info)}"
            f"  [{get_short_formatted_submitted_date(full_fanta_info.comic_book_info)}]"
        )

        title_node.issue_label.text = issue_info
        title_node.issue_label.bind(on_press=self.__main_screen.on_title_row_button_pressed)

        return title_node
