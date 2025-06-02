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
from filtered_title_lists import FilteredTitleLists
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
    ON_CS_YEAR_RANGE_NODE = auto()
    ON_DDA_NODE = auto()
    ON_CATEGORIES_NODE = auto()
    ON_CATEGORY_NODE = auto()
    ON_TITLE_NODE = auto()
    ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TITLE_SEARCH_BOX_NODE = auto()
    ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET = auto()
    ON_TAG_SEARCH_BOX_NODE = auto()


class BackgroundViews:
    TOP_VIEW_EVENT_TIMEOUT_SECS = 1000.0
    BOTTOM_VIEW_EVENT_TIMEOUT_SECS = 1000.0

    def __init__(self, title_lists: Dict[str, List[FantaComicBookInfo]]):
        self.title_lists = title_lists

        self.__top_view_image_opacity = 1.0
        self.__top_view_image_title = None
        self.__top_view_image_file = ""
        self.__top_view_image_color: Color = (0, 0, 0, 0)
        self.__top_view_change_event = None

        self.__bottom_view_title_opacity = 0.0

        self.__bottom_view_fun_image_opacity = 0.0
        self.__bottom_view_fun_image_title = None
        self.__bottom_view_fun_image_file = ""
        self.__bottom_view_fun_image_color: Color = (0, 0, 0, 0)
        self.__bottom_view_change_fun_image_event = None

        self.__bottom_view_title_image_file = ""
        self.__bottom_view_title_image_color: Color = (0, 0, 0, 0)

        self.__current_year_range = ""
        self.__current_cs_year_range = ""
        self.__current_category = ""

        self.__view_state = ViewStates.INITIAL

    def get_view_state(self) -> ViewStates:
        return self.__view_state

    def get_top_view_image_opacity(self) -> float:
        return self.__top_view_image_opacity

    def get_top_view_image_color(self) -> Color:
        return self.__top_view_image_color

    def get_top_view_image_title(self) -> Titles:
        return self.__top_view_image_title

    def get_top_view_image_file(self) -> str:
        return self.__top_view_image_file

    def get_bottom_view_title_opacity(self) -> float:
        return self.__bottom_view_title_opacity

    def get_bottom_view_fun_image_opacity(self) -> float:
        return self.__bottom_view_fun_image_opacity

    def get_bottom_view_fun_image_color(self) -> Color:
        return self.__bottom_view_fun_image_color

    def get_bottom_view_fun_image_title(self) -> Titles:
        return self.__bottom_view_fun_image_title

    def get_bottom_view_fun_image_file(self) -> str:
        return self.__bottom_view_fun_image_file

    def get_bottom_view_title_image_color(self) -> Color:
        return self.__bottom_view_title_image_color

    def get_bottom_view_title_image_file(self) -> str:
        return self.__bottom_view_title_image_file

    def get_current_category(self) -> str:
        return self.__current_category

    def set_current_category(self, cat: str) -> None:
        self.__current_category = cat

    def get_current_year_range(self) -> str:
        return self.__current_year_range

    def set_current_year_range(self, year_range: str) -> None:
        self.__current_year_range = year_range

    def get_current_cs_year_range(self) -> str:
        return self.__current_cs_year_range

    def set_current_cs_year_range(self, year_range: str) -> None:
        self.__current_cs_year_range = year_range

    def set_view_state(self, view_state: ViewStates) -> None:
        self.__view_state = view_state
        self.__update_views()

    def __update_views(self):
        if self.__view_state == ViewStates.ON_INTRO_NODE:
            self.__bottom_view_fun_image_opacity = 0.0
            self.__bottom_view_title_opacity = 0.0
            return

        if self.__view_state in [
            ViewStates.ON_TITLE_SEARCH_BOX_NODE,
            ViewStates.ON_TITLE_NODE,
            ViewStates.ON_TAG_SEARCH_BOX_NODE,
        ]:
            self.__bottom_view_fun_image_opacity = 0.0
            self.__bottom_view_title_opacity = 1.0
        else:
            self.__bottom_view_fun_image_opacity = 1.0
            self.__bottom_view_title_opacity = 0.0

        self.__set_top_view_image()
        self.__set_bottom_view_fun_image()
        self.__set_bottom_view_title_image_color()

    def __set_top_view_image(self) -> None:
        # noinspection PyUnreachableCode
        match self.__view_state:
            case ViewStates.INITIAL:
                self.__set_initial_top_view_image()
            case ViewStates.ON_INTRO_NODE:
                self.__set_top_view_image_for_intro()
            case (
                ViewStates.ON_THE_STORIES_NODE
                | ViewStates.ON_CHRONO_BY_YEAR_NODE
                | ViewStates.ON_SERIES_NODE
                | ViewStates.ON_CATEGORIES_NODE
            ):
                self.__set_top_view_image_for_stories()
            case ViewStates.ON_CS_NODE:
                self.__set_top_view_image_for_cs()
            case ViewStates.ON_CS_YEAR_RANGE_NODE:
                self.__set_top_view_image_for_cs_year_range()
            case ViewStates.ON_DDA_NODE:
                self.__set_top_view_image_for_dda()
            case ViewStates.ON_YEAR_RANGE_NODE:
                self.__set_top_view_image_for_year_range()
            case ViewStates.ON_CATEGORY_NODE:
                self.__set_top_view_image_for_category()
            case ViewStates.ON_TITLE_NODE:
                pass
            case (
                ViewStates.ON_SEARCH_NODE
                | ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewStates.ON_TITLE_SEARCH_BOX_NODE
                | ViewStates.ON_TAG_SEARCH_BOX_NODE
            ):
                self.__set_top_view_image_for_search()
            case ViewStates.ON_APPENDIX_NODE:
                self.__set_top_view_image_for_appendix()
            case ViewStates.ON_INDEX_NODE:
                self.__set_top_view_image_for_index()
            case _:
                assert False

        self.__set_top_view_image_color()
        self.__schedule_top_view_event()

        logging.debug(
            f"Top view image:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__top_view_image_file)}',"
            f" Color: {get_formatted_color(self.__top_view_image_color)},"
            f" Opacity: {self.__top_view_image_opacity}."
        )

    def __set_initial_top_view_image(self):
        self.__top_view_image_title = Titles.COLD_BARGAIN_A
        self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)

    def __set_top_view_image_for_intro(self):
        self.__top_view_image_title = Titles.ADVENTURE_DOWN_UNDER
        self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)

    def __set_top_view_image_for_stories(self):
        self.__top_view_image_file, self.__top_view_image_title = get_random_image(
            self.title_lists[ALL_LISTS], use_edited=True
        )

    def __set_top_view_image_for_cs(self):
        self.__top_view_image_file, self.__top_view_image_title = get_random_image(
            self.title_lists[SERIES_CS], use_edited=True
        )

    def __set_top_view_image_for_dda(self):
        self.__top_view_image_file, self.__top_view_image_title = get_random_image(
            self.title_lists[SERIES_DDA], use_edited=True
        )

    def __set_top_view_image_for_category(self):
        logging.debug(f"Current category: '{self.__current_category}'.")
        if not self.__current_category:
            self.__top_view_image_title = Titles.GOOD_NEIGHBORS
            self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)
        else:
            self.__top_view_image_file, self.__top_view_image_title = get_random_image(
                self.title_lists[self.__current_category], use_edited=True
            )

    def __set_top_view_image_for_year_range(self):
        logging.debug(f"Year range: '{self.__current_year_range}'.")
        if not self.__current_year_range:
            self.__top_view_image_title = Titles.GOOD_NEIGHBORS
            self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)
        else:
            self.__top_view_image_file, self.__top_view_image_title = get_random_image(
                self.title_lists[self.__current_year_range], use_edited=True
            )

    def __set_top_view_image_for_cs_year_range(self):
        logging.debug(f"CS Year range: '{self.__current_cs_year_range}'.")
        if not self.__current_cs_year_range:
            self.__top_view_image_title = Titles.GOOD_NEIGHBORS
            self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)
        else:
            cs_range = FilteredTitleLists.get_cs_range_str_from_str(self.__current_cs_year_range)
            logging.debug(f"CS Year range key: '{cs_range}'.")
            self.__top_view_image_file, self.__top_view_image_title = get_random_image(
                self.title_lists[cs_range], use_edited=True
            )

    def __set_top_view_image_for_search(self):
        self.__top_view_image_title = Titles.TRACKING_SANDY
        self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)

    def __set_top_view_image_for_appendix(self):
        self.__top_view_image_title = Titles.FABULOUS_PHILOSOPHERS_STONE_THE
        self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)

    def __set_top_view_image_for_index(self):
        self.__top_view_image_title = Titles.TRUANT_OFFICER_DONALD
        self.__top_view_image_file = get_comic_inset_file(self.__top_view_image_title)

    def __set_top_view_image_color(self):
        self.__top_view_image_color = get_random_color()

    def __set_bottom_view_fun_image(self) -> None:
        if self.__view_state in [
            ViewStates.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewStates.ON_TITLE_SEARCH_BOX_NODE,
            ViewStates.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewStates.ON_TAG_SEARCH_BOX_NODE,
            ViewStates.ON_TITLE_NODE,
        ]:
            return

        self.__bottom_view_fun_image_file, self.__bottom_view_fun_image_title = get_random_image(
            self.title_lists[ALL_LISTS]
        )
        self.__set_bottom_view_fun_image_color()
        self.__schedule_bottom_view_fun_image_event()

        logging.debug(
            f"Bottom view fun image:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__bottom_view_fun_image_file)}',"
            f" Color: {get_formatted_color(self.__bottom_view_fun_image_color)},"
            f" Opacity: {self.__bottom_view_fun_image_opacity}."
        )

    # TODO: Rationalize image color setters
    def __set_bottom_view_fun_image_color(self):
        if randrange(0, 100) < 20:
            rand_color = [1, 1, 1, 1]
        else:
            alpha = randrange(130, 230) / 255.0

            rand_index = randrange(0, 3)
            rgb_val = 0.5 if rand_index == 2 else 0.1
            rand_color_val = randrange(230, 255) / 255.0
            rand_color = [rgb_val, rgb_val, rgb_val, alpha]
            rand_color[rand_index] = rand_color_val

        self.__bottom_view_fun_image_color = tuple(rand_color)

    def set_bottom_view_title_image_file(self, image_file: str) -> None:
        self.__bottom_view_title_image_file = image_file
        self.__log_bottom_view_title_state()

    def __set_bottom_view_title_image_color(self):
        if randrange(0, 100) < 20:
            rand_color = [1, 1, 1, 0.5]
        else:
            alpha = randrange(130, 200) / 255.0

            rand_index = randrange(0, 3)
            rgb_val = 0.5 if rand_index == 2 else 0.1
            rand_color_val = randrange(230, 255) / 255.0
            rand_color = [rgb_val, rgb_val, rgb_val, alpha]
            rand_color[rand_index] = rand_color_val

        self.__bottom_view_title_image_color = tuple(rand_color)

        self.__log_bottom_view_title_state()

    def __log_bottom_view_title_state(self):
        logging.debug(
            f"Bottom view title image:"
            f" State: {self.__view_state},"
            f" Image: '{os.path.basename(self.__bottom_view_title_image_file)}',"
            f" Color: {get_formatted_color(self.__bottom_view_title_image_color)},"
            f" Opacity: {self.__bottom_view_title_opacity}."
        )

    def __schedule_top_view_event(self):
        if self.__top_view_change_event:
            self.__top_view_change_event.cancel()

        self.__top_view_change_event = Clock.schedule_interval(
            lambda dt: self.__set_top_view_image(), self.TOP_VIEW_EVENT_TIMEOUT_SECS
        )

    def __schedule_bottom_view_fun_image_event(self):
        if self.__bottom_view_change_fun_image_event:
            self.__bottom_view_change_fun_image_event.cancel()

        self.__bottom_view_change_fun_image_event = Clock.schedule_interval(
            lambda dt: self.__set_bottom_view_fun_image(), self.BOTTOM_VIEW_EVENT_TIMEOUT_SECS
        )
