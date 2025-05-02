import logging
import os
import subprocess
import threading

from kivy.clock import Clock

HOME_DIR = os.environ.get("HOME")

MCOMIX_PYTHON_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/.venv/bin/python")
MCOMIX_PATH = os.path.join(HOME_DIR, "Prj/github/mcomix-git-glk1001/mcomixstarter.py")

THE_COMICS_DIR = os.path.join(HOME_DIR, "Books/Carl Barks/The Comics/Chronological")
BARKS_READER_CONFIG_PATH = os.path.join(
    HOME_DIR, "Prj/github/barks-compleat-digital/barks-reader/mcomix-barks-ui-desc.xml"
)


class ComicReader:
    def __init__(self):
        self.reader_is_running = False
        self.comic_name: str = ""
        self.comic_path: str = ""

    def on_app_request_close(self):
        if self.reader_is_running:
            logging.debug(f"ComicReader: on_request_close event triggered but reader is running.")
            return True

        return False  # Returning False allows the app to close now

    def show_comic(self, value: str):
        self.comic_name = value

        Clock.schedule_once(lambda dt: self.run_reader(), 0.1)

    def run_reader(self):
        self.comic_path = os.path.join(THE_COMICS_DIR, self.comic_name + ".cbz")

        threading.Thread(target=self.run_comic_reader, daemon=True).start()

    def run_comic_reader(self) -> None:
        ui_desc_path = BARKS_READER_CONFIG_PATH

        run_args = [
            MCOMIX_PYTHON_PATH,
            MCOMIX_PATH,
            "--ui-desc-file",
            ui_desc_path,
            self.comic_path,
        ]
        logging.info(f"Running mcomix: {' '.join(run_args)}.")

        process = subprocess.Popen(run_args, text=True)
        self.reader_is_running = True
        result = process.wait()
        logging.info(f"mcomix return code = {result}.")

        self.reader_is_running = False
