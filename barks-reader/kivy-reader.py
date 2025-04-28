import logging
import os.path
import subprocess
import sys
from typing import List

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import escape_markup

from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging


def run_comic_reader(comic_book_filename: str) -> None:
    python_path = "/home/greg/Prj/github/mcomix-git-glk1001/.venv/bin/python"
    mcomix_path = "/home/greg/Prj/github/mcomix-git-glk1001/mcomixstarter.py"
    ui_desc_path = (
        "/home/greg/Prj/github/barks-compleat-digital/barks-reader/mcomix-barks-ui-desc.xml"
    )

    run_args = [python_path, mcomix_path, "--ui-desc-file", ui_desc_path, comic_book_filename]
    print(f"Running mcomix: {' '.join(run_args)}.")
    logging.debug(f"Running mcomix: {' '.join(run_args)}.")

    result = subprocess.run(
        run_args,
        capture_output=True,
        text=True,
        check=True,
    )
    print(result.stdout)
    print(result.stderr)

    # process = subprocess.Popen(run_args, stdout=subprocess.PIPE, text=True)
    # return process

class ComicReader:
    def __init__(self):
        self.old_color = None
        self.reader_is_running = False

    def run_reader(self, instance, value):
        the_comics_dir = "/home/greg/Books/Carl Barks/The Comics/Chronological"
        comic_name = value.replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]")

        self.reader_is_running = True
        run_comic_reader(os.path.join(the_comics_dir, comic_name + ".cbz"))
        self.reader_is_running = False

        instance.color = self.old_color

    def show_comic(self, label, value):
        self.old_color = label.color
        label.color = (0.0, 1.0, 0.0, 1)
        Clock.schedule_once(lambda dt: self.run_reader(label, value), 0.1)

    def on_request_close(self):
        print(f"ComicReader: on_request_close event triggered. reader_is_running = {self.reader_is_running}")
        return self.reader_is_running  # Returning False allows the app to close


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
            underline=True,
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        label.bind(on_ref_press=self.comic_reader.show_comic)
        self.layout.add_widget(label)

    def on_request_close(self, *args):
        print("ScrollableLabelList: on_request_close event triggered.")
        return self.comic_reader.on_request_close()


class MyApp(App):
    def __init__(self, ttls: List[str], max_ttl_len: int, **kwargs):
        super().__init__(**kwargs)
        self.titles = ttls

    def build(self):
        self.title = "Scrollable Label List with Refs"

        Window.bind(on_request_close=self.on_request_close_window)  # Bind the event

        label_list = ScrollableLabelList()
        for ttl in self.titles:
            label_list.add_item(f"{ttl}")
        return label_list

    def on_request_close_window(self, *args):
        print("MyApp: on_request_close event triggered.")
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

    titles = cmd_args.get_titles()

    titles_with_issue_nums = []
    max_title_len = 0
    for title in titles:
        comic_book = comics_database.get_comic_book(title)

        title_with_issue_num = comic_book.get_title_with_issue_num()
        if max_title_len < len(title_with_issue_num):
            max_title_len = len(title_with_issue_num)

        titles_with_issue_nums.append(title_with_issue_num)

    MyApp(titles_with_issue_nums, max_title_len).run()
