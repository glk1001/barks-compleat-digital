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
        self.filtered_title_lists = filtered_title_lists
        self.title_search = title_search
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

        label = TitleSearchBoxTreeViewNode(self.title_search)
        label.on_title_search_box_pressed = self.main_screen.on_title_search_box_pressed
        label.on_title_search_box_title_pressed = self.main_screen.on_title_search_box_title_pressed
        label.title_spinner.bind(text=self.main_screen.on_title_search_box_title_changed)
        tree.add_node(label, parent=search_node)

        label = TagSearchBoxTreeViewNode(self.title_search)
        label.bind(on_tag_search_box_pressed=self.main_screen.on_tag_search_box_pressed)
        label.bind(on_tag_search_box_tag_pressed=self.main_screen.on_tag_search_box_tag_pressed)
        label.bind(on_tag_search_box_title_pressed=self.main_screen.on_tag_search_box_title_pressed)
        label.bind(on_tag_search_box_text_changed=self.main_screen.on_tag_search_box_text_changed)
        label.bind(on_tag_search_box_tag_changed=self.main_screen.on_tag_search_box_tag_changed)
        label.bind(on_tag_search_box_title_changed=self.main_screen.on_tag_search_box_title_changed)
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
                logging.debug(f'Skipped unconfigured title "{title_str}".')
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
