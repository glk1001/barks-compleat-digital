import logging
import os
from enum import Enum, auto
from random import randrange
from typing import Dict, List

from kivy.clock import Clock

from barks_fantagraphics.barks_titles import Titles
from barks_fantagraphics.fanta_comics_info import (
    FantaComicBookInfo,
    ALL_LISTS,
    SERIES_CS,
    SERIES_DDA,
)
from file_paths import get_comic_inset_file
from random_title_images import get_random_image, get_random_color
from reader_types import Color, get_formatted_color


class ViewStates(Enum):
    INITIAL = auto()
    ON_INTRO_NODE = auto()
    ON_THE_STORIES_NODE = auto()
    ON_SEARCH_NODE = auto()
    ON_APPENDIX_NODE = auto()
    ON_INDEX_NODE = auto()
    ON_CHRONO_BY_YEAR_NODE = auto()
    ON_YEAR_RANGE_NODE = auto()
    ON_SERIES_NODE = auto()
    ON_CS_NODE = auto()
    ON_DDA_NODE = auto()
    ON_CATEGORIES_NODE = auto()
    ON_CATEGORY_NODE = auto()
    ON_TITLE_NODE = auto()
    ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TITLE_SEARCH_BOX_NODE = auto()
    ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TAG_SEARCH_BOX_NODE = auto()


class BackgroundViews:
    BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG = (1, 0, 0, 1)
    BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG = (1, 0, 0, 0)
    BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG = (1, 0, 0, 0.5)
    BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG = (0, 0, 0, 0)
    TOP_VIEW_EVENT_TIMEOUT_SECS = 1000.0
    BOTTOM_VIEW_EVENT_TIMEOUT_SECS = 1000.0

    def __init__(self, title_lists: Dict[str, List[FantaComicBookInfo]]):
        self.title_lists = title_lists

        self.__top_view_image_file = ""
        self.__top_view_image_color: Color = (0, 0, 0, 0)
        self.__top_view_image_opacity = 1.0
        self.__top_view_change_event = None

        self.__bottom_view_image_opacity = 0.0

        self.__bottom_view_after_image_file = ""
        self.__bottom_view_after_image_color: Color = (0, 0, 0, 0)
        self.__bottom_view_change_after_event = None

        self.__bottom_view_before_image_file = ""
        self.__bottom_view_before_image_color: Color = (0, 0, 0, 0)

        self.__current_year_range = ""
        self.__current_category = ""

        self.__view_state = ViewStates.INITIAL

    def get_view_state(self) -> ViewStates:
        return self.__view_state

    def get_top_view_image_opacity(self) -> float:
        return self.__top_view_image_opacity

    def get_top_view_image_color(self) -> Color:
        return self.__top_view_image_color

    def get_top_view_image_file(self) -> str:
        return self.__top_view_image_file

    def get_bottom_view_image_opacity(self) -> float:
        return self.__bottom_view_image_opacity

    def get_bottom_view_after_image_color(self) -> Color:
        return self.__bottom_view_after_image_color

    def get_bottom_view_after_image_file(self) -> str:
        return self.__bottom_view_after_image_file

    def get_bottom_view_before_image_color(self) -> Color:
        return self.__bottom_view_before_image_color

    def get_bottom_view_before_image_file(self) -> str:
        return self.__bottom_view_before_image_file

    def set_current_category(self, cat: str) -> None:
        self.__current_category = cat

    def set_current_year_range(self, year_range: str) -> None:
        self.__current_year_range = year_range

    def set_bottom_view_before_image(self, image_file: str) -> None:
        self.__bottom_view_before_image_file = image_file

    def set_view_state(self, view_state: ViewStates) -> None:
        self.__view_state = view_state
        self.__update_visibilities()

    def __set_top_view_image(self) -> None:
        # noinspection PyUnreachableCode
        match self.__view_state:
            case ViewStates.INITIAL:
                self.__top_view_image_file = get_comic_inset_file(Titles.COLD_BARGAIN_A)
            case ViewStates.ON_INTRO_NODE:
                self.__top_view_image_file = get_comic_inset_file(Titles.ADVENTURE_DOWN_UNDER)
            case ViewStates.ON_THE_STORIES_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[ALL_LISTS])
            case (
                ViewStates.ON_SEARCH_NODE
                | ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewStates.ON_TITLE_SEARCH_BOX_NODE
                | ViewStates.ON_TAG_SEARCH_BOX_NODE
            ):
                self.__top_view_image_file = get_comic_inset_file(Titles.TRACKING_SANDY)
            case ViewStates.ON_APPENDIX_NODE:
                self.__top_view_image_file = get_comic_inset_file(
                    Titles.FABULOUS_PHILOSOPHERS_STONE_THE
                )
            case ViewStates.ON_INDEX_NODE:
                self.__top_view_image_file = get_comic_inset_file(Titles.TRUANT_OFFICER_DONALD)
            case (
                ViewStates.ON_CHRONO_BY_YEAR_NODE
                | ViewStates.ON_SERIES_NODE
                | ViewStates.ON_CATEGORIES_NODE
            ):
                self.__top_view_image_file = get_random_image(self.title_lists[ALL_LISTS])
            case ViewStates.ON_CS_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[SERIES_CS])
            case ViewStates.ON_DDA_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[SERIES_DDA])
            case ViewStates.ON_CATEGORY_NODE:
                logging.debug(f"Current category: '{self.__current_category}'")
                if not self.__current_category:
                    self.__top_view_image_file = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.__top_view_image_file = get_random_image(
                        self.title_lists[self.__current_category]
                    )
            case ViewStates.ON_YEAR_RANGE_NODE:
                logging.debug(f"Year range: '{self.__current_year_range}'")
                if not self.__current_year_range:
                    self.__top_view_image_file = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.__top_view_image_file = get_random_image(
                        self.title_lists[self.__current_year_range]
                    )
            case ViewStates.ON_TITLE_NODE:
                pass
            case _:
                assert False

        self.__set_top_view_image_color()
        self.__schedule_top_view_event()

        logging.debug(
            f"Set top view:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__top_view_image_file)}',"
            f" Color: {get_formatted_color(self.__top_view_image_color)},"
            f" Opacity: {self.__top_view_image_opacity}."
        )

    def __set_top_view_image_color(self):
        self.__top_view_image_color = get_random_color()

    def __set_bottom_view_after_image(self) -> None:
        if self.__view_state in [
            ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewStates.ON_TITLE_SEARCH_BOX_NODE,
            ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewStates.ON_TAG_SEARCH_BOX_NODE,
            ViewStates.ON_TITLE_NODE,
        ]:
            return

        self.__bottom_view_after_image_file = get_random_image(self.title_lists[ALL_LISTS])
        self.__set_bottom_view_after_image_color()
        self.__schedule_bottom_view_after_event()

        logging.debug(
            f"Set Bottom view after image:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__bottom_view_after_image_file)}',"
            f" Color: {get_formatted_color(self.__bottom_view_after_image_color)},"
            f" Opacity: {self.__bottom_view_image_opacity}."
        )

    def __set_bottom_view_after_image_color(self):
        if randrange(0, 100) < 20:
            rand_color = [1, 1, 1, 1]
        else:
            rand_index = randrange(0, 3)
            rgb_val = 0.5 if rand_index == 2 else 0.1
            rand_color_val = randrange(230, 255) / 255.0
            rand_color = [rgb_val, rgb_val, rgb_val, self.__bottom_view_after_image_color[3]]
            rand_color[rand_index] = rand_color_val

        self.__bottom_view_after_image_color = tuple(rand_color)

    def __schedule_top_view_event(self):
        if self.__top_view_change_event:
            self.__top_view_change_event.cancel()

        self.__top_view_change_event = Clock.schedule_interval(
            lambda dt: self.__set_top_view_image(), self.TOP_VIEW_EVENT_TIMEOUT_SECS
        )

    def __schedule_bottom_view_after_event(self):
        if self.__bottom_view_change_after_event:
            self.__bottom_view_change_after_event.cancel()

        self.__bottom_view_change_after_event = Clock.schedule_interval(
            lambda dt: self.__set_bottom_view_after_image(), self.BOTTOM_VIEW_EVENT_TIMEOUT_SECS
        )

    def __update_visibilities(self):
        if self.__view_state == ViewStates.ON_INTRO_NODE:
            self.__bottom_view_image_opacity = 0.0
            self.__bottom_view_after_image_color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.__bottom_view_before_image_color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG
        elif self.__view_state in [
            ViewStates.ON_TITLE_SEARCH_BOX_NODE,
            ViewStates.ON_TITLE_NODE,
            ViewStates.ON_TAG_SEARCH_BOX_NODE,
        ]:
            self.__bottom_view_image_opacity = 1.0
            self.__bottom_view_after_image_color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.__bottom_view_before_image_color = self.BOTTOM_VIEW_BEFORE_IMAGE_ENABLED_BG
        else:
            self.__bottom_view_image_opacity = 1.0
            self.__bottom_view_after_image_color = self.BOTTOM_VIEW_AFTER_IMAGE_ENABLED_BG
            self.__bottom_view_before_image_color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG

        self.__set_top_view_image()
        self.__set_bottom_view_after_image()

        logging.debug(
            f"Set Bottom view before image:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__bottom_view_before_image_file)}',"
            f" Color: {get_formatted_color(self.__bottom_view_before_image_color)},"
            f" Opacity: {self.__bottom_view_image_opacity}."
        )
