import logging
import sys
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

        self.layout = GridLayout(cols=1, spacing=5, pos=(0, 0), size_hint_x=0.5, size_hint_y=None)
        self.add_widget(self.layout)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.comic_reader = ComicReader()

    def add_item(self, text):
        esc_text = escape_markup(text)
        label = Label(
            text=f"[ref={esc_text}]{text}[/ref]",
            size_hint_y=None,
            height=20,
            markup=True,
            underline=False,
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        label.bind(on_ref_press=self.comic_reader.show_comic)
        self.layout.add_widget(label)

    def on_request_close(self):
        return self.comic_reader.on_app_request_close()


class MyApp(App):
    def __init__(self, title_with_issues: List[Tuple[int, str, str]], max_title_len: int, **kwargs):
        super().__init__(**kwargs)

        self.title_with_issues = title_with_issues

    def build(self):
        Window.bind(on_request_close=self.on_request_close_window)

        self.title = "The Compleat Barks Reader"

        label_list = ScrollableLabelList()
        for chronological_num, title, issue_title in self.title_with_issues:
            label_list.add_item(f"{chronological_num:3} {title} {issue_title}")
        return label_list

    def on_request_close_window(self, *args):
        return self.root.on_request_close()


def get_all_comic_titles(titles: List[str]) -> Tuple[List[Tuple[int, str, str]], int]:
    titles_with_issue_nums = []
    max_title_len = 0
    for title in titles:
        comic_book = comics_database.get_comic_book(title)
        title_with_issue_num = comic_book.get_title_with_issue_num()
        max_title_len = max(max_title_len, len(title_with_issue_num))
        titles_with_issue_nums.append(
                (comic_book.chronological_number, title, comic_book.get_comic_issue_title()))

    return titles_with_issue_nums, max_title_len


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
