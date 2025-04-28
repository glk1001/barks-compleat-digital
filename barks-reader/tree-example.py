from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
from kivy.uix.label import Label
import kivy.core.text


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class TreeViewRow(BoxLayout, TreeViewNode):
    pass


class TreeViewButton(Button, TreeViewNode):
    pass


class TreeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_height = 30
        self.intro_text = None
        Window.size = (1200, 700)

    def pressed(self, button: Button):
        if button.text == "Introduction":
            self.intro_text.opacity = 1.0
        else:
            self.intro_text.opacity = 0.0
        print(f'Button "{button.text}" pressed.')

    def build(self):
        intro_text = TextInput(
            text="hello line 1\nhello line 2\nhello line 3\n",
            multiline=True,
            readonly = True,
            size_hint = (0.7, 1),
            pos_hint={"x": 0.3, "top": 1.0},
            opacity = 0.0,
        )

        left_box = BoxLayout(orientation="vertical", size_hint=(0.3, 1))
        left_box.add_widget(self.build_tree(intro_text))

        lo = BoxLayout(orientation="horizontal", size_hint=(1, 1))
        lo.add_widget(left_box)
        lo.add_widget(intro_text)

        return lo

    def build_tree(self, intro_text):
        self.intro_text = intro_text

        tree = TreeView(hide_root=True)
        # tree.root.text = 'X'

        intro_label = TreeViewButton(
            text="Introduction",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Introduction") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        intro_label.bind(size=intro_label.setter("text_size"))
        intro_label.bind(on_press=self.pressed)
        intro_node = tree.add_node(intro_label)

        the_stories_label = TreeViewButton(
            text="The Stories",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("The Stories") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        the_stories_label.bind(size=the_stories_label.setter("text_size"))
        the_stories_label.bind(on_press=self.pressed)
        the_stories_node = tree.add_node(the_stories_label)

        self.add_story_nodes(tree, the_stories_node)

        tag_search_label = TreeViewButton(
            text="Tag Search",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Tag Search") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        tag_search_label.bind(size=tag_search_label.setter("text_size"))
        tag_search_label.bind(on_press=self.pressed)
        tag_search_node = tree.add_node(tag_search_label)

        appendix_label = TreeViewButton(
            text="Appendix",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Appendix") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        appendix_label.bind(size=appendix_label.setter("text_size"))
        appendix_label.bind(on_press=self.pressed)
        appendix_node = tree.add_node(appendix_label)

        index_label = TreeViewButton(
            text="Index",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Index") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        index_label.bind(size=index_label.setter("text_size"))
        index_label.bind(on_press=self.pressed)
        index_node = tree.add_node(index_label)

        return tree

    def add_story_nodes(self, tree, the_stories_node):
        by_year_label = TreeViewButton(
            text="Chronological by Year",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Chronological by Year") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        by_year_label.bind(size=by_year_label.setter("text_size"))
        by_year_label.bind(on_press=self.pressed)
        self.add_year_nodes(tree, by_year_label)
        tree.add_node(by_year_label, parent=the_stories_node)

        dda_label = TreeViewButton(
            text="Donald Duck Adventures",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Donald Duck Adventures") + 30, self.label_height),
            halign="left",
            valign="middle",
        )
        dda_label.bind(size=dda_label.setter("text_size"))
        dda_label.bind(on_press=self.pressed)
        self.add_dda_story_nodes(tree, dda_label)
        tree.add_node(dda_label, parent=the_stories_node)

    def add_year_nodes(self, tree, the_years_node):
        child_node_1 = TreeViewButton(
            text="1942",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("1942") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        child_node_1.bind(size=child_node_1.setter("text_size"))
        child_node_1.bind(on_press=self.pressed)
        tree.add_node(child_node_1, parent=the_years_node)

        child_node_2 = TreeViewButton(
            text="1943",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("1942") + 20, self.label_height),
            halign="left",
            valign="middle",
        )
        child_node_2.bind(size=child_node_2.setter("text_size"))
        child_node_2.bind(on_press=self.pressed)
        tree.add_node(child_node_2, parent=the_years_node)

    def add_dda_story_nodes(self, tree, dda_node):
        child_node_1 = TreeViewButton(
            text="Donald Duck and The Mummy's Ring",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Donald Duck and The Mummy's Ring") + 70, self.label_height),
            halign="left",
            valign="middle",
        )
        child_node_1.bind(size=child_node_1.setter("text_size"))
        child_node_1.bind(on_press=self.pressed)
        tree.add_node(child_node_1, parent=dda_node)

        child_node_2 = TreeViewButton(
            text="Frozen Gold",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Frozen Gold") + 40, self.label_height),
            halign="left",
            valign="middle",
        )
        child_node_2.bind(size=child_node_2.setter("text_size"))
        child_node_2.bind(on_press=self.pressed)
        tree.add_node(child_node_2, parent=dda_node)


if __name__ == "__main__":
    TreeApp().run()
