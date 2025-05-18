import logging
from typing import List, Union

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.barks_tags import Tags, TagGroups
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo
from barks_fantagraphics.title_search import unique_extend, BarksTitleSearch

TREE_VIEW_NODE_TEXT_COLOR = (1, 1, 1, 1)
TREE_VIEW_NODE_SELECTED_COLOR = (1, 0, 1, 0.8)
TREE_VIEW_NODE_BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)


class ReaderTreeView(TreeView):
    TREE_VIEW_INDENT_LEVEL = dp(30)


class MainTreeViewNode(Button, TreeViewNode):
    TEXT_COLOR = TREE_VIEW_NODE_TEXT_COLOR
    SELECTED_COLOR = TREE_VIEW_NODE_SELECTED_COLOR
    BACKGROUND_COLOR = TREE_VIEW_NODE_BACKGROUND_COLOR
    NODE_SIZE = (dp(100), dp(30))


class TitlePageImage(ButtonBehavior, Image):
    TITLE_IMAGE_X_FRAC_OF_PARENT = 0.98
    TITLE_IMAGE_Y_FRAC_OF_PARENT = 0.98 * 0.97


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

    def __init__(self, title_search: BarksTitleSearch):
        super().__init__()
        self.title_search = title_search
        self.bind(text=self.search_box_text_changed)

    def on_touch_down(self, touch):
        if self.title_search_box.collide_point(*touch.pos):
            self.on_title_search_box_pressed(self)
            return super().on_touch_down(touch)
        if self.title_spinner.collide_point(*touch.pos):
            self.on_title_search_box_title_pressed(self)
            return super().on_touch_down(touch)
        return False

    def search_box_text_changed(self, instance, value: str):
        logging.debug(f'**Title search box text changed: {instance}, text: "{value}".')

        if len(value) <= 1:
            instance.set_empty_title_spinner_text()
        else:
            titles = self.get_titles_matching_search_title_str(str(value))
            instance.set_title_spinner_values(titles)

    def get_titles_matching_search_title_str(self, value: str) -> List[str]:
        title_list = self.title_search.get_titles_matching_prefix(value)
        if len(value) > 2:
            unique_extend(title_list, self.title_search.get_titles_containing(value))

        return self.title_search.get_titles_as_strings(title_list)

    def set_empty_title_spinner_text(self):
        self.title_spinner.text = ""
        self.title_spinner.is_open = False

    def set_empty_title_spinner_values(self):
        self.title_spinner.values = []
        self.title_spinner.text = ""
        self.title_spinner.is_open = False

    def set_title_spinner_values(self, titles: List[str]):
        if not titles:
            self.set_empty_title_spinner_values()
        else:
            self.title_spinner.values = titles
            self.title_spinner.text = titles[0]
            self.title_spinner.is_open = True


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

    on_tag_search_box_text_changed = None
    on_tag_search_box_tag_spinner_value_changed = None
    on_tag_search_box_title_spinner_value_changed = None

    def __init__(self, title_search: BarksTitleSearch):
        super().__init__()
        self.title_search = title_search
        self.bind(text=self.tag_search_box_text_changed)
        self.tag_spinner.bind(text=self.tag_search_box_tag_spinner_value_changed)
        self.tag_title_spinner.bind(text=self.tag_search_box_title_spinner_value_changed)

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

    def tag_search_box_text_changed(self, instance, value):
        logging.debug(f'**Tag search box text changed: {instance}, text: "{value}".')

        self.on_tag_search_box_text_changed(instance, value)

        if len(value) <= 1:
            instance.set_empty_tag_spinner_values()
            instance.set_empty_title_spinner_values()
        else:
            tags = self.get_tags_matching_search_tag_str(str(value))
            if tags:
                instance.set_tag_spinner_values(sorted([str(t.value) for t in tags]))
            else:
                instance.set_empty_tag_spinner_values()
                instance.set_empty_title_spinner_values()

    def tag_search_box_tag_spinner_value_changed(self, spinner: Spinner, tag_str: str):
        logging.debug(f'**Tag search box tag spinner text changed: {spinner}, text: "{tag_str}".')

        self.on_tag_search_box_tag_spinner_value_changed(spinner, tag_str)

        if not tag_str:
            return

        titles = self.title_search.get_titles_from_alias_tag(tag_str.lower())

        if not titles:
            spinner.parent.set_empty_title_spinner_values()
            return

        spinner.parent.set_title_spinner_values(self.title_search.get_titles_as_strings(titles))

    def tag_search_box_title_spinner_value_changed(self, spinner: Spinner, title_str: str) -> None:
        logging.debug(
            f'**Tag search box tag title spinner text changed: {spinner}, text: "{title_str}".'
        )
        self.on_tag_search_box_title_spinner_value_changed(spinner, title_str)

    def get_tags_matching_search_tag_str(self, value: str) -> List[Union[Tags, TagGroups]]:
        tag_list = self.title_search.get_tags_matching_prefix(value)
        # if len(value) > 2:
        #     unique_extend(title_list, self.title_search.get_titles_containing(value))

        return tag_list

    def set_empty_tag_spinner_text(self):
        self.tag_spinner.text = ""
        self.tag_spinner.is_open = False

    def set_empty_tag_spinner_values(self):
        self.tag_spinner.values = []
        self.tag_spinner.text = ""
        self.tag_spinner.is_open = False

    def set_tag_spinner_values(self, titles: List[str]):
        if not titles:
            self.set_empty_tag_spinner_values()
        else:
            self.tag_spinner.values = titles
            self.tag_spinner.text = titles[0]
            self.tag_spinner.is_open = True

    def set_empty_title_spinner_text(self):
        self.tag_title_spinner.text = ""
        self.tag_title_spinner.is_open = False

    def set_empty_title_spinner_values(self):
        self.tag_title_spinner.values = []
        self.tag_title_spinner.text = ""
        self.tag_title_spinner.is_open = False

    def set_title_spinner_values(self, titles: List[str]):
        if not titles:
            self.set_empty_title_spinner_values()
        else:
            self.tag_title_spinner.values = titles
            self.tag_title_spinner.text = titles[0]
            self.tag_title_spinner.is_open = True


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
