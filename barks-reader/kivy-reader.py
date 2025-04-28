import logging
import sys
from typing import List

import kivy.core.text
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import escape_markup

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging
from comic_book_info import ComicTitleInfo, get_all_comic_titles
from mcomix_reader import ComicReader

APP_TITLE = "The Compleat Barks Reader"

TITLE_NUM_COLOR = (1.0, 1.0, 1.0, 1.0)
TITLE_LABEL_COLOR = (1.0, 1.0, 0.0, 1.0)
ISSUE_TITLE_LABEL_COLOR = (1.0, 1.0, 1.0, 0.8)


def get_str_pixel_width(text: str, **kwargs) -> int:
    return kivy.core.text.Label(**kwargs).get_extents(text)[0]


class ScrollableLabelList(ScrollView):
    def __init__(self, max_title_width: int, **kwargs):
        super().__init__(**kwargs)

        self.max_title_width = max_title_width + 60
        self.max_num_width = get_str_pixel_width("999") + 5
        self.max_issue_title_width = get_str_pixel_width("[WDCS 500]") + 20

        self.size_hint = (1, None)
        self.size = (Window.width, Window.height)

        self.do_scroll_x = False
        self.do_scroll_y = True
        self.always_overscroll = False
        self.effect_cls = "ScrollEffect"
        self.scroll_type = ["bars", "content"]

        self.bar_color = (0.8, 0.8, 0.8, 1)
        self.bar_inactive_color = (0.8, 0.8, 0.8, 0.8)
        self.bar_width = 5

        self.layout = GridLayout(cols=3, padding=20, spacing=[15, 20], size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.add_widget(self.layout)

        self.comic_reader = ComicReader()

    def add_item(self, comic_info: ComicTitleInfo):
        esc_filename = escape_markup(comic_info.filename)

        num_label = Label(
            text=f"[ref={esc_filename}]{comic_info.chronological_number}[/ref]",
            color=TITLE_NUM_COLOR,
            size_hint=(None, 1.0),
            width=self.max_num_width,
            markup=True,
            halign="right",
            valign="middle",
        )
        num_label.bind(size=num_label.setter("text_size"))
        num_label.bind(on_ref_press=self.comic_reader.show_comic)
        self.layout.add_widget(num_label)

        text_label = Label(
            text=f"[ref={esc_filename}]{comic_info.title}[/ref]",
            color=TITLE_LABEL_COLOR,
            size_hint=(None, 1.0),
            width=self.max_title_width,
            markup=True,
            halign="left",
            valign="middle",
        )
        text_label.bind(on_ref_press=self.comic_reader.show_comic)
        text_label.bind(size=text_label.setter("text_size"))
        self.layout.add_widget(text_label)

        issue_label = Label(
            text=f"[ref={esc_filename}][{comic_info.issue_title}][/ref]",
            color=ISSUE_TITLE_LABEL_COLOR,
            size_hint=(None, 1.0),
            width=self.max_issue_title_width,
            markup=True,
            halign="left",
            valign="middle",
        )
        issue_label.bind(on_ref_press=self.comic_reader.show_comic)
        issue_label.bind(size=issue_label.setter("text_size"))
        self.layout.add_widget(issue_label)

    def on_request_close(self):
        return self.comic_reader.on_app_request_close()


class MyApp(App):
    def __init__(self, all_comics_info: List[ComicTitleInfo], longest_title: str, **kwargs):
        super().__init__(**kwargs)

        self.all_comics_info = all_comics_info
        self.max_title_width = get_str_pixel_width(longest_title)

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.title = APP_TITLE

        label_list = ScrollableLabelList(self.max_title_width)
        for comic_info in self.all_comics_info:
            label_list.add_item(comic_info)

        return label_list

    def on_request_close_window(self, *args):
        return self.root.on_request_close()


if __name__ == "__main__":
    # TODO(glk): Some issue with type checking inspection?
    # noinspection PyTypeChecker
    cmd_args = CmdArgs("Fantagraphics source files", CmdArgNames.TITLE | CmdArgNames.VOLUME)
    args_ok, error_msg = cmd_args.args_are_valid()
    if not args_ok:
        logging.error(error_msg)
        sys.exit(1)

    setup_logging(cmd_args.get_log_level())

    comics_database = cmd_args.get_comics_database()
    all_comic_book_info, longest_comic_title = get_all_comic_titles(
        comics_database, cmd_args.get_titles()
    )

    MyApp(all_comic_book_info, longest_comic_title).run()
