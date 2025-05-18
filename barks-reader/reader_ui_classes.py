from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.treeview import TreeView, TreeViewNode

from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo

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
