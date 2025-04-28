import logging
import os
import subprocess
import threading
from typing import Union

from kivy.clock import Clock
from kivy.uix.label import Label

IN_USE_LABEL_COLOR = (1.0, 0.0, 0.0, 1.0)

HOME_DIR = os.environ.get("HOME")

MCOMIX_PYTHON_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/.venv/bin/python")
MCOMIX_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/mcomixstarter.py")

THE_COMICS_DIR = os.path.join(HOME_DIR, "Books/Carl Barks/The Comics/Chronological")
BARKS_READER_CONFIG_PATH = os.path.join(
    HOME_DIR, "Prj/github/barks-compleat-digital/barks-reader/mcomix-barks-ui-desc.xml"
)


def run_comic_reader(comic_book_filename: str) -> None:
    ui_desc_path = BARKS_READER_CONFIG_PATH

    run_args = [
        MCOMIX_PYTHON_PATH,
        MCOMIX_PATH,
        "--ui-desc-file",
        ui_desc_path,
        comic_book_filename,
    ]
    logging.info(f"Running mcomix: {' '.join(run_args)}.")

    result = subprocess.run(
        run_args,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout:
        logging.info(result.stdout)
    if result.stderr:
        logging.info(result.stderr)


class ComicReader:
    def __init__(self):
        self.old_color = None
        self.reader_is_running = False
        self.comic_name: str = ""
        self.comic_path: str = ""
        self.label: Union[Label, None] = None

    def show_comic(self, label, value):
        self.label = label
        self.old_color = label.color
        self.label.color = IN_USE_LABEL_COLOR

        self.comic_name = value.replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]")

        Clock.schedule_once(lambda dt: self.run_reader(), 0.1)

    def run_reader(self):
        self.comic_path = os.path.join(THE_COMICS_DIR, self.comic_name + ".cbz")

        threading.Thread(target=self.run_reader_process, daemon=True).start()

    def run_reader_process(self):
        self.reader_is_running = True
        run_comic_reader(self.comic_path)
        self.reader_is_running = False

        self.label.color = self.old_color

    def on_app_request_close(self):
        if self.reader_is_running:
            logging.debug(f"ComicReader: on_request_close event triggered but reader is running.")
            return True

        return False  # Returning False allows the app to close now
