import os
from enum import Enum, auto
from typing import Dict, List

from barks_fantagraphics.barks_titles import Titles
from barks_fantagraphics.fanta_comics_info import (
    ALL_LISTS,
    SERIES_CS,
    SERIES_DDA,
    FantaComicBookInfo,
)
from file_paths import get_comic_inset_file
from random_title_images import get_random_image
from reader_types import Color


class ViewState(Enum):
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

    def __init__(self, title_lists: Dict[str, List[FantaComicBookInfo]]):
        self.title_lists = title_lists

        self.__top_view_image_file = ""
        self.__top_view_image_color: Color = (0, 0, 0, 0)
        self.__top_view_image_opacity = 0.0

        self.__bottom_view_image_opacity = 0.0

        self.__bottom_view_after_image_file = ""
        self.__bottom_view_after_image_color: Color = (0, 0, 0, 0)

        self.__bottom_view_before_image_file = ""
        self.__bottom_view_before_image_color: Color = (0, 0, 0, 0)

        self.__current_year_range = ""
        self.__current_category = ""

        self.__view_state = ViewState.INITIAL

    def get_view_state(self) -> ViewState:
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

    def set_view_state(self, view_state: ViewState) -> None:
        self.__view_state = view_state

    def __set_top_view_image(self) -> None:
        # noinspection PyUnreachableCode
        match self.__view_state:
            case ViewState.INITIAL:
                self.__top_view_image_file = get_comic_inset_file(Titles.COLD_BARGAIN_A)
            case ViewState.ON_INTRO_NODE:
                self.__top_view_image_file = get_comic_inset_file(Titles.ADVENTURE_DOWN_UNDER)
            case ViewState.ON_THE_STORIES_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[ALL_LISTS])
            case (
                ViewState.ON_SEARCH_NODE
                | ViewState.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewState.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET
                | ViewState.ON_TITLE_SEARCH_BOX_NODE
                | ViewState.ON_TAG_SEARCH_BOX_NODE
            ):
                self.__top_view_image_file = get_comic_inset_file(Titles.TRACKING_SANDY)
            case ViewState.ON_APPENDIX_NODE:
                self.__top_view_image_file = get_comic_inset_file(
                    Titles.FABULOUS_PHILOSOPHERS_STONE_THE
                )
            case ViewState.ON_INDEX_NODE:
                self.__top_view_image_file = get_comic_inset_file(Titles.TRUANT_OFFICER_DONALD)
            case (
                ViewState.ON_CHRONO_BY_YEAR_NODE
                | ViewState.ON_SERIES_NODE
                | ViewState.ON_CATEGORIES_NODE
            ):
                self.__top_view_image_file = get_random_image(self.title_lists[ALL_LISTS])
            case ViewState.ON_CS_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[SERIES_CS])
            case ViewState.ON_DDA_NODE:
                self.__top_view_image_file = get_random_image(self.title_lists[SERIES_DDA])
            case ViewState.ON_CATEGORY_NODE:
                print(f"Current category: '{self.__current_category}'")
                if not self.__current_category:
                    self.__top_view_image_file = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.__top_view_image_file = get_random_image(
                        self.title_lists[self.__current_category]
                    )
            case ViewState.ON_YEAR_RANGE_NODE:
                print(f"Year range: '{self.__current_year_range}'")
                if not self.__current_year_range:
                    self.__top_view_image_file = get_comic_inset_file(Titles.GOOD_NEIGHBORS)
                else:
                    self.__top_view_image_file = get_random_image(
                        self.title_lists[self.__current_year_range]
                    )
            case ViewState.ON_TITLE_NODE:
                pass
            case _:
                assert False

        print(
            f"Set top view. State: {self.__view_state}."
            f" Image: '{os.path.basename(self.__top_view_image_file)}'."
        )

    def __set_bottom_view_after_image(self) -> None:
        if self.__view_state in [
            ViewState.ON_TITLE_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewState.ON_TITLE_SEARCH_BOX_NODE,
            ViewState.ON_TAG_SEARCH_BOX_NODE_NO_TITLE_YET,
            ViewState.ON_TAG_SEARCH_BOX_NODE,
            ViewState.ON_TITLE_NODE,
        ]:
            return

        self.__bottom_view_after_image_file = get_random_image(self.title_lists[ALL_LISTS])
        print(
            f"Bottom view after image: '{os.path.basename(self.__bottom_view_after_image_file)}'."
        )

    def __update_visibilities(self):
        if self.__view_state == ViewState.ON_INTRO_NODE:
            self.__bottom_view_image_opacity = 0.0
            self.__bottom_view_after_image_color = self.BOTTOM_VIEW_AFTER_IMAGE_DISABLED_BG
            self.__bottom_view_before_image_color = self.BOTTOM_VIEW_BEFORE_IMAGE_DISABLED_BG
        elif self.__view_state in [
            ViewState.ON_TITLE_SEARCH_BOX_NODE,
            ViewState.ON_TITLE_NODE,
            ViewState.ON_TAG_SEARCH_BOX_NODE,
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
