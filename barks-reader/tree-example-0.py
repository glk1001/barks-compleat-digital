from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
from kivy.uix.label import Label
import kivy.core.text

def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class TreeViewRow(BoxLayout, TreeViewNode):
    pass


class TreeViewButton(Button, TreeViewNode):
    pass


def pressed(button: Button):
    print(f'Button "{button.text}" pressed.')


class TreeApp(App):
    def build(self):
        tree = TreeView(hide_root=True)
        #tree.root.text = 'X'

        label_height = 30
        label_size = (70, label_height)
        button_size = (100, label_height)

        intro_label = TreeViewButton(
            text="Introduction",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Introduction") + 20, label_height),
            halign="left",
            valign="middle",
        )
        intro_label.bind(size=intro_label.setter("text_size"))
        intro_label.bind(on_press=pressed)
        intro_node = tree.add_node(intro_label)

        the_stories_label = TreeViewButton(
            text="The Stories",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("The Stories") + 20, label_height),
            halign="left",
            valign="middle",
        )
        the_stories_label.bind(size=the_stories_label.setter("text_size"))
        the_stories_label.bind(on_press=pressed)
        the_stories_node = tree.add_node(the_stories_label)

        child_node_1 = TreeViewRow(spacing=0, orientation="horizontal")
        btn1 = Button(
            text="Hello",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=button_size,
            halign="left",
            valign="middle",
        )
        btn2 = Button(
            text="World 1",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=button_size,
            halign="left",
            valign="middle",
        )
        child_node_1.bind(minimum_height=child_node_1.setter("height"))
        child_node_1.add_widget(btn1)
        child_node_1.add_widget(btn2)
        tree.add_node(child_node_1, parent=the_stories_node)

        child_node_2 = TreeViewRow(spacing=0, orientation="horizontal")
        btn1 = Button(
            text="Hello",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=button_size,
            halign="left",
            valign="middle",
        )
        btn2 = Button(
            text="World 2",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=button_size,
            halign="left",
            valign="middle",
        )
        child_node_2.bind(minimum_height=child_node_2.setter("height"))
        child_node_2.add_widget(btn1)
        child_node_2.add_widget(btn2)
        tree.add_node(child_node_2, parent=the_stories_node)

        tag_search_label = TreeViewButton(
            text="Tag Search",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Tag Search") + 20, label_height),
            halign="left",
            valign="middle",
        )
        tag_search_label.bind(size=tag_search_label.setter("text_size"))
        tag_search_node = tree.add_node(tag_search_label)

        appendix_label = TreeViewButton(
            text="Appendix",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Appendix") + 20, label_height),
            halign="left",
            valign="middle",
        )
        appendix_label.bind(size=appendix_label.setter("text_size"))
        appendix_node = tree.add_node(appendix_label)

        index_label = TreeViewButton(
            text="Index",
            color=(1.0, 0.0, 0.0, 1.0),
            background_color=(0.0, 0.0, 0.0, 1.0),
            size_hint=(None, None),
            size=(get_str_pixel_width("Index") + 20, label_height),
            halign="left",
            valign="middle",
        )
        index_label.bind(size=index_label.setter("text_size"))
        index_node = tree.add_node(index_label)

        return tree


if __name__ == "__main__":
    TreeApp().run()
