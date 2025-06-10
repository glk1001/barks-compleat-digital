# You might need 'pip install rarfile' and the 'unrar' executable for .cbr support
# import rarfile
import io
import logging
import threading
import zipfile
from pathlib import Path
from threading import Thread
from typing import Callable, IO, Dict, Tuple

from PIL import Image as PilImage, ImageOps
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.actionbar import ActionBar, ActionButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from screeninfo import get_monitors

from barks_fantagraphics.comics_consts import PNG_FILE_EXT, JPG_FILE_EXT, PageType
from file_paths import (
    get_barks_reader_action_bar_background_file,
    get_barks_reader_close_icon_file,
    get_barks_reader_fullscreen_icon_file,
    get_barks_reader_app_icon_file,
    get_barks_reader_next_icon_file,
    get_barks_reader_previous_icon_file,
    get_barks_reader_goto_start_icon_file,
    get_barks_reader_goto_end_icon_file,
    get_barks_reader_fullscreen_exit_icon_file,
    get_barks_reader_action_bar_group_background_file,
    get_barks_reader_goto_icon_file,
)
from reader_consts_and_types import ACTION_BAR_SIZE_Y

GOTO_PAGE_DROPDOWN_FRAC_OF_HEIGHT = 0.97
GOTO_PAGE_BUTTON_HEIGHT = dp(25)
GOTO_PAGE_BUTTON_BODY_COLOR = (0, 1, 1, 1)
GOTO_PAGE_BUTTON_NONBODY_COLOR = (0, 0.5, 0.5, 1)
GOTO_PAGE_BUTTON_CURRENT_PAGE_COLOR = (1, 1, 0, 1)


class ComicBookReader(BoxLayout):
    """Main layout for the comic reader."""

    current_page_index = NumericProperty(0)
    current_comic_path = StringProperty("")

    MAX_WINDOW_WIDTH = get_monitors()[0].width
    MAX_WINDOW_HEIGHT = get_monitors()[0].height

    def __init__(self, close_reader_func: Callable[[], None], goto_page_widget: Widget, **kwargs):
        super().__init__(**kwargs)

        self.root = None
        self.action_bar = None
        self.close_reader_func = close_reader_func
        self.goto_page_widget = goto_page_widget

        self.orientation = "vertical"

        self.comic_image = Image()
        self.comic_image.fit_mode = "contain"
        self.comic_image.mipmap = False
        self.add_widget(self.comic_image)

        self.images = []
        self.image_names = []
        self.image_loaded_events = []
        self.first_page_index = -1
        self.last_page_index = -1
        self.all_loaded = False
        self.page_to_index_map = None

        # Bind property changes to update the display
        self.bind(current_page_index=self.show_page)

        self.x_mid = -1
        self.y_top_margin = -1
        self.fullscreen_left_margin = -1
        self.fullscreen_right_margin = -1

        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, _window, width, height):
        self.x_mid = round(width / 2 - self.x)
        self.y_top_margin = round(height - self.y - (0.09 * height))

        logging.debug(
            f"Resize event: x,y = {self.x},{self.y},"
            f" width = {width}, height = {height},"
            f" self.width = {self.width}, self.height = {self.height}."
        )
        logging.debug(f"Resize event: x_mid = {self.x_mid}, y_top_margin = {self.y_top_margin}.")

        self.fullscreen_left_margin = round(self.MAX_WINDOW_WIDTH / 4.0)
        self.fullscreen_right_margin = self.MAX_WINDOW_WIDTH - self.fullscreen_left_margin
        logging.debug(
            f"Resize event: fullscreen_left_margin = {self.fullscreen_left_margin},"
            f" fullscreen_right_margin = {self.fullscreen_right_margin}."
        )

    def close(self, fullscreen_button: ActionButton):
        self.exit_fullscreen(fullscreen_button)

        self.images.clear()
        self.images = []
        self.image_names = []
        self.first_page_index = -1
        self.last_page_index = -1

        self.close_reader_func()

    def set_action_bar(self, action_bar: ActionBar):
        self.action_bar = action_bar

    def on_touch_down(self, touch):
        logging.debug(
            f"Touch down event: self.x,self.y = {self.x},{self.y},"
            f" touch.x,touch.y = {round(touch.x)},{round(touch.y)},"
            f" width = {round(self.width)}, height = {round(self.height)}."
            f" x_mid = {self.x_mid}, y_top_margin = {self.y_top_margin}."
        )

        x_rel = round(touch.x - self.x)
        y_rel = round(touch.y - self.y)

        if self.is_in_top_margin(x_rel, y_rel):
            logging.debug(f"Top margin pressed: x_rel,y_rel = {x_rel},{y_rel}.")
            if Window.fullscreen:
                self.toggle_action_bar()
        elif self.is_in_left_margin(x_rel, y_rel):
            logging.debug(f"Left margin pressed: x_rel,y_rel = {x_rel},{y_rel}.")
            self.prev_page(None)
        elif self.is_in_right_margin(x_rel, y_rel):
            logging.debug(f"Right margin pressed: x_rel,y_rel = {x_rel},{y_rel}.")
            self.next_page(None)
        else:
            logging.debug(
                f"Dead zone: x_rel,y_rel = {x_rel},{y_rel},"
                f" Windows.fullscreen = {Window.fullscreen}."
            )

        return super().on_touch_down(touch)

    def is_in_top_margin(self, x: int, y: int) -> bool:
        if y <= self.y_top_margin:
            return False

        if not Window.fullscreen:
            return True

        return self.fullscreen_left_margin < x <= self.fullscreen_right_margin

    def is_in_left_margin(self, x: int, y: int) -> bool:
        return (x < self.x_mid) and (y <= self.y_top_margin)

    def is_in_right_margin(self, x: int, y: int) -> bool:
        return (x >= self.x_mid) and (y <= self.y_top_margin)

    def read_comic(
        self, title_str: str, comic_path: str, page_to_index_map: Dict[str, Tuple[int, PageType]]
    ):
        self.action_bar.action_view.action_previous.title = title_str
        self.current_comic_path = comic_path
        self.page_to_index_map = page_to_index_map
        self.load_current_comic_path()

    def load_current_comic_path(self):
        self.all_loaded = False

        self.load_image_names()
        self.init_load_events()

        t = Thread(target=self.load_comic, args=[self.current_comic_path])
        t.daemon = True
        t.start()

    def init_load_events(self):
        self.image_loaded_events = []
        for _name in self.image_names:
            self.image_loaded_events.append(threading.Event())

    def load_image_names(self):
        if not self.current_comic_path.lower().endswith((".cbz", ".zip")):
            raise Exception("Expected '.cbz' or '.zip' file.")

        try:
            with zipfile.ZipFile(self.current_comic_path, "r") as archive:
                # Get image file names, sorted alphabetically
                self.image_names = sorted(
                    [f for f in archive.namelist() if f.lower().endswith((".png", ".jpg"))]
                )

            self.first_page_index = 0
            self.last_page_index = len(self.image_names) - 1

        except FileNotFoundError:
            logging.error(f'Comic file not found: "{self.current_comic_path}".')
            # Optionally show an error message to the user
        except zipfile.BadZipFile:
            logging.error(f'Bad zip file: "{self.current_comic_path}".')
            # Optionally show an error message to the user
        # except rarfile.BadRarFile:
        #      Logger.error(f"Bad rar file: {self.current_comic_path}")
        #      # Optionally show an error message to the user
        except Exception as e:
            logging.error(f'Error loading comic "{self.current_comic_path}": {e}')
            # Optionally show a generic error message

    def load_comic(self, comic_path):
        """Loads images from the comic archive."""
        self.images = []  # Clear previous images
        self.current_page_index = -1  # Reset page index

        try:
            with zipfile.ZipFile(comic_path, "r") as archive:
                first_loaded = False
                for i, name in enumerate(self.image_names):
                    with archive.open(name) as file:
                        ext = Path(name).suffix
                        self.images.append(self.get_image_data(file, ext))
                    self.image_loaded_events[i].set()
                    if not first_loaded:
                        first_loaded = True
                        Clock.schedule_once(self.first_image_loaded, 0)

            self.all_loaded = True
            logging.info(f"Loaded {len(self.images)} images from {comic_path}.")

            # Add .cbr support if rarfile is installed
            # elif comic_path.lower().endswith(('.cbr', '.rar')):
            #     with rarfile.RarFile(comic_path, 'r') as archive:
            #         image_names = sorted([
            #             f for f in archive.namelist()
            #             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
            #         ])
            #         for name in image_names:
            #             with archive.open(name) as file:
            #                 img_data = io.BytesIO(file.read())
            #                 self.images.append(img_data)
            #     Logger.info(f"Loaded {len(self.images)} images from {comic_path}")

        except FileNotFoundError:
            logging.error(f'Comic file not found: "{comic_path}".')
            # Optionally show an error message to the user
        except zipfile.BadZipFile:
            logging.error(f'Bad zip file: "{comic_path}".')
            # Optionally show an error message to the user
        # except rarfile.BadRarFile:
        #      Logger.error(f"Bad rar file: {comic_path}")
        #      # Optionally show an error message to the user
        except Exception as e:
            logging.error(f'Error loading comic "{comic_path}": {e}')
            # Optionally show a generic error message

    def first_image_loaded(self, _dt):
        self.current_page_index = 0
        logging.debug(f"First image loaded: current page index = {self.current_page_index}.")

    @staticmethod
    def get_image_format(ext: str) -> str:
        return "jpeg" if ext == JPG_FILE_EXT else PNG_FILE_EXT

    def get_image_data(self, file: IO[bytes], ext: str) -> io.BytesIO:
        assert ext in [PNG_FILE_EXT, JPG_FILE_EXT]

        img_data = PilImage.open(io.BytesIO(file.read()))
        img_data = ImageOps.contain(
            img_data,
            (self.MAX_WINDOW_HEIGHT, self.MAX_WINDOW_WIDTH),
            PilImage.Resampling.LANCZOS,
        )

        data = io.BytesIO()
        img_data.save(data, format=self.get_image_format(ext))

        return data

    def show_page(self, _instance, _value):
        """Displays the image for the current_page_index."""
        if self.current_page_index == -1:
            return

        logging.debug(
            f"Display image {self.current_page_index}:"
            f' "{self.image_names[self.current_page_index]}".'
        )

        self.wait_for_image_to_load()

        assert self.images
        assert self.first_page_index <= self.current_page_index <= self.last_page_index

        try:
            # Kivy Image widget can load from BytesIO
            self.comic_image.texture = None  # Clear previous texture
            self.comic_image.source = ""  # Clear previous source
            self.comic_image.reload()  # Ensure reload if source was same BytesIO object

            # Reset stream position before loading
            self.images[self.current_page_index].seek(0)
            self.comic_image.texture = CoreImage(
                self.images[self.current_page_index], ext="jpeg"
            ).texture
        except Exception as e:
            logging.error(f"Error displaying image with index {self.current_page_index}: {e}")
            # Optionally display a placeholder image or error message

    def goto_start_page(self, _instance):
        """Goes to the first page."""
        if self.current_page_index == self.first_page_index:
            logging.info(f"Already on the first page: current index = {self.current_page_index}.")
        else:
            logging.info(f"Goto start page requested: requested index = {self.first_page_index}.")
            self.current_page_index = self.first_page_index

    def goto_last_page(self, _instance):
        """Goes to the last page."""
        if self.current_page_index == self.last_page_index:
            logging.info(f"Already on the last page: current index = {self.current_page_index}.")
        else:
            logging.info(f"Last page requested: requested index = {self.last_page_index}.")
            self.current_page_index = self.last_page_index

    def next_page(self, _instance):
        """Goes to the next page."""
        if self.current_page_index >= self.last_page_index:
            logging.info(f"Already on the last page: current index = {self.current_page_index}.")
        else:
            logging.info(f"Next page requested: requested index = {self.current_page_index + 1}")
            self.current_page_index += 1

    def prev_page(self, _instance):
        """Goes to the previous page."""
        if self.current_page_index == self.first_page_index:
            logging.info(f"Already on the first page: current index = {self.current_page_index}.")
        else:
            logging.info(f"Prev page requested: requested index = {self.current_page_index - 1}")
            self.current_page_index -= 1

        return True

    def goto_page(self, _instance):
        """Goes to user requested page."""

        max_dropdown_height = round(GOTO_PAGE_DROPDOWN_FRAC_OF_HEIGHT * self.height)
        dropdown = DropDown(
            auto_dismiss=True,
            dismiss_on_select=True,
            on_select=self.on_page_selected,
            max_height=max_dropdown_height,
        )

        selected_button = None
        for page, (page_index, page_type) in self.page_to_index_map.items():
            page_num_button = Button(
                text=str(page),
                size_hint_y=None,
                height=GOTO_PAGE_BUTTON_HEIGHT,
                bold=page_type == PageType.BODY,
                background_color=(
                    GOTO_PAGE_BUTTON_BODY_COLOR
                    if page_type == PageType.BODY
                    else GOTO_PAGE_BUTTON_NONBODY_COLOR
                ),
            )
            page_num_button.bind(on_press=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(page_num_button)

            if page_index == self.current_page_index:
                selected_button = page_num_button
                selected_button.background_color = GOTO_PAGE_BUTTON_CURRENT_PAGE_COLOR

        dropdown.open(self.goto_page_widget)
        dropdown.scroll_to(selected_button)

    def on_page_selected(self, _instance, page: str):
        self.current_page_index = self.page_to_index_map[page][0]

    def wait_for_image_to_load(self):
        if self.all_loaded:
            return

        logging.info(f"Waiting for image with index {self.current_page_index} to finish loading.")
        while not self.image_loaded_events[self.current_page_index].wait(timeout=1):
            logging.info(
                f"Still waiting for image with index {self.current_page_index} to finish loading."
            )
        logging.info(f"Finished waiting for image with index {self.current_page_index} to load.")

    def toggle_fullscreen(self, button: ActionButton):
        """Toggles fullscreen mode."""
        if Window.fullscreen:
            Window.fullscreen = False
            self.show_action_bar()
            button.text = "Fullscreen"
            button.icon = self.root.ACTION_BAR_FULLSCREEN_ICON
            logging.info("Exiting fullscreen.")
        else:
            self.hide_action_bar()
            button.text = "Windowed"
            button.icon = self.root.ACTION_BAR_FULLSCREEN_EXIT_ICON
            Window.fullscreen = "auto"  # Use 'auto' for best platform behavior
            logging.info("Entering fullscreen.")

    def hide_action_bar(self):
        self.action_bar.height = 0
        self.action_bar.opacity = 0

    def show_action_bar(self):
        self.action_bar.height = ACTION_BAR_SIZE_Y
        self.action_bar.opacity = 1

    def exit_fullscreen(self, button: ActionButton):
        if not Window.fullscreen:
            return

        Window.fullscreen = False
        self.show_action_bar()
        button.text = "Fullscreen"
        logging.info("Exiting fullscreen.")

    def toggle_action_bar(self) -> None:
        """Toggles the visibility of the action bar."""
        logging.debug(
            f"On toggle action bar entry:" f" self.action_bar.height = {self.action_bar.height}"
        )

        if self.action_bar.height <= 0.1:
            self.show_action_bar()
        else:
            self.hide_action_bar()

        logging.debug(
            f"On toggle action bar exit: self.action_bar.height = {self.action_bar.height}"
        )


class ComicBookReaderScreen(BoxLayout, Screen):
    APP_ICON_FILE = get_barks_reader_app_icon_file()
    ACTION_BAR_HEIGHT = ACTION_BAR_SIZE_Y
    ACTION_BAR_BACKGROUND_PATH = get_barks_reader_action_bar_background_file()
    ACTION_BAR_GROUP_BACKGROUND_PATH = get_barks_reader_action_bar_group_background_file()
    ACTION_BAR_BACKGROUND_COLOR = (0.6, 0.7, 0.2, 1)
    ACTION_BUTTON_BACKGROUND_COLOR = (0.6, 1.0, 0.2, 1)
    ACTION_BAR_CLOSE_ICON = get_barks_reader_close_icon_file()
    ACTION_BAR_FULLSCREEN_ICON = get_barks_reader_fullscreen_icon_file()
    ACTION_BAR_FULLSCREEN_EXIT_ICON = get_barks_reader_fullscreen_exit_icon_file()
    ACTION_BAR_NEXT_ICON = get_barks_reader_next_icon_file()
    ACTION_BAR_PREV_ICON = get_barks_reader_previous_icon_file()
    ACTION_BAR_GOTO_ICON = get_barks_reader_goto_icon_file()
    ACTION_BAR_GOTO_START_ICON = get_barks_reader_goto_start_icon_file()
    ACTION_BAR_GOTO_END_ICON = get_barks_reader_goto_end_icon_file()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comic_book_reader_widget = None

    def add_reader_widget(self, comic_book_reader_widget: ComicBookReader):
        self.comic_book_reader_widget = comic_book_reader_widget
        self.add_widget(self.comic_book_reader_widget)


KV_FILE = Path(__file__).stem + ".kv"


def get_barks_comic_reader(screen_name: str, close_reader_func: Callable[[], None]):
    Builder.load_file(KV_FILE)

    root = ComicBookReaderScreen(name=screen_name)

    comic_book_reader_widget = ComicBookReader(close_reader_func, root.ids.goto_page_button)

    comic_book_reader_widget.root = root
    comic_book_reader_widget.set_action_bar(root.ids.comic_action_bar)

    root.add_reader_widget(comic_book_reader_widget)

    return root
