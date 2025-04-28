import logging
import sys
from dataclasses import dataclass
from typing import List, Tuple

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import escape_markup

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging
from mcomix_reader import ComicReader


@dataclass
class ComicTitleInfo:
    chronological_number: int
    title: str
    issue_title: str
    filename: str


def get_all_comic_titles(titles: List[str]) -> Tuple[List[ComicTitleInfo], int]:
    titles_with_issue_nums = []
    max_title_len = 0
    for title in titles:
        comic_book = comics_database.get_comic_book(title)
        title_with_issue_num = comic_book.get_title_with_issue_num()
        max_title_len = max(max_title_len, len(title_with_issue_num))
        titles_with_issue_nums.append(
            ComicTitleInfo(
                comic_book.chronological_number,
                title,
                comic_book.get_comic_issue_title(),
                title_with_issue_num,
            )
        )

    return titles_with_issue_nums, max_title_len


class ScrollableLabelList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.do_scroll_x = False
        self.do_scroll_y = True
        self.always_overscroll = False
        self.effect_cls = "ScrollEffect"

        self.bar_color = (0.8, 0.8, 0.8, 1)
        self.bar_inactive_color = (0.8, 0.8, 0.8, 0.8)
        self.bar_width = 5

        self.layout = GridLayout(
            cols=3, padding=10, spacing=[15, 20], pos=(0, 0), size_hint_x=0.5, size_hint_y=None
        )
        self.add_widget(self.layout)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.comic_reader = ComicReader()

    def add_item(self, num: int, title: str, issue_title: str, comic_filename: str):
        num_label = Label(
            text=f"{num}",
            size_hint=(None, 1.0),
            width=35,
            markup=False,
            underline=False,
            halign="right",
            valign="middle",
        )
        num_label.bind(size=num_label.setter("text_size"))
        self.layout.add_widget(num_label)

        esc_filename = escape_markup(comic_filename)
        text_label = Label(
            text=f"[ref={esc_filename}]{title}[/ref]",
            size_hint=(None, 1.0),
            width=300,
            markup=True,
            underline=False,
            halign="left",
            valign="middle",
        )
        text_label.bind(on_ref_press=self.comic_reader.show_comic)
        text_label.bind(size=text_label.setter("text_size"))
        self.layout.add_widget(text_label)

        issue_label = Label(
            text=f"[{issue_title}]",
            size_hint=(None, 1.0),
            width=100,
            markup=False,
            underline=False,
            halign="left",
            valign="middle",
        )
        issue_label.bind(size=issue_label.setter("text_size"))
        self.layout.add_widget(issue_label)

    def on_request_close(self):
        return self.comic_reader.on_app_request_close()


class MyApp(App):
    def __init__(self, title_with_issues: List[ComicTitleInfo], max_title_len: int, **kwargs):
        super().__init__(**kwargs)

        self.title_with_issues = title_with_issues

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.title = "The Compleat Barks Reader"

        label_list = ScrollableLabelList()
        for title_info in self.title_with_issues:
            label_list.add_item(title_info.chronological_number, title_info.title,
                                title_info.issue_title, title_info.filename)
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
    all_comic_titles, max_comic_title_len = get_all_comic_titles(cmd_args.get_titles())

    MyApp(all_comic_titles, max_comic_title_len).run()
