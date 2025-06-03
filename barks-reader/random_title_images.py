from enum import Enum, auto
from random import randrange
from typing import List, Tuple, Callable, Union, Set

from barks_fantagraphics.barks_titles import Titles, BARKS_TITLES
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo
from file_paths import (
    EMERGENCY_INSET_FILE,
    get_comic_inset_file,
    get_comic_cover_file,
    get_comic_splash_files,
    get_comic_silhouette_files,
    get_comic_censorship_files,
    get_comic_favourite_files,
    get_comic_original_art_files,
    get_comic_search_files,
)
from reader_types import Color


def get_random_color() -> Color:
    return (
        randrange(100, 255) / 255.0,
        randrange(100, 255) / 255.0,
        randrange(100, 255) / 255.0,
        randrange(220, 250) / 255.0,
    )


class FileTypes(Enum):
    COVER = auto()
    SILHOUETTE = auto()
    SPLASH = auto()
    CENSORSHIP = auto()
    FAVOURITE = auto()
    ORIGINAL_ART = auto()


SEARCH_TITLES = [
    Titles.BACK_TO_LONG_AGO,
    Titles.TRACKING_SANDY,
    Titles.SEARCH_FOR_THE_CUSPIDORIA,
]

ALL_TYPES = {t for t in FileTypes}
ALL_BUT_ORIGINAL_ART = {t for t in FileTypes if t != FileTypes.ORIGINAL_ART}


def get_random_search_image() -> Tuple[str, Titles]:
    title_index = randrange(0, len(SEARCH_TITLES))
    title = SEARCH_TITLES[title_index]

    return __get_random_comic_file(BARKS_TITLES[title], get_comic_search_files, False), title


def get_random_image(
    title_list: List[FantaComicBookInfo],
    file_types: Union[Set[FileTypes], None] = None,
    use_edited: bool = False,
) -> Tuple[str, Titles]:
    title_index = randrange(0, len(title_list))

    comic_book_info = title_list[title_index].comic_book_info
    title = comic_book_info.title

    title_image_file = __get_random_title_image_file(
        comic_book_info.get_title_str(), file_types, use_edited
    )
    if title_image_file:
        return title_image_file, title

    return get_comic_inset_file(title), title


def get_random_image_file(
    title_list: List[FantaComicBookInfo], file_types: Union[Set[FileTypes], None] = None
) -> str:
    return get_random_image(title_list, file_types)[0]


def get_random_title_image(title: str, file_types: Set[FileTypes], use_edited: bool = False) -> str:
    title_image_file = __get_random_title_image_file(title, file_types, use_edited)
    if title_image_file:
        return title_image_file

    return get_comic_inset_file(EMERGENCY_INSET_FILE)


def __get_random_title_image_file(
    title_str: str, file_types: Union[Set[FileTypes], None], use_edited: bool
) -> str:
    if file_types is None:
        file_types: Set[FileTypes] = ALL_TYPES

    num_categories = len(file_types)

    percent = {}
    n = 1
    for file_type in file_types:
        percent[file_type] = n * int(round(100 / num_categories))
        n += 1

    for num_attempts in range(10):
        rand_percent = randrange(0, 100)
        # print(f"Attempt {num_attempts}: rand percent = {rand_percent}.")

        for file_type in percent:
            if rand_percent <= percent[file_type]:
                title_file = __get_comic_file(title_str, file_type, use_edited)
                if title_file:
                    return title_file
                percent[file_type] = -1

        if max(percent.values()) < 0:
            break

    return ""


def __get_comic_file(title_str: str, file_type: FileTypes, use_edited: bool) -> str:
    if file_type == FileTypes.COVER:
        return get_comic_cover_file(title_str, use_edited)
    if file_type == FileTypes.SILHOUETTE:
        return __get_random_comic_file(title_str, get_comic_silhouette_files, use_edited)
    if file_type == FileTypes.SPLASH:
        return __get_random_comic_file(title_str, get_comic_splash_files, use_edited)
    if file_type == FileTypes.CENSORSHIP:
        return __get_random_comic_file(title_str, get_comic_censorship_files, use_edited)
    if file_type == FileTypes.FAVOURITE:
        return __get_random_comic_file(title_str, get_comic_favourite_files, use_edited)
    if file_type == FileTypes.ORIGINAL_ART:
        return __get_random_comic_file(title_str, get_comic_original_art_files, use_edited)

    return ""


def __get_random_comic_file(
    title_str: str, get_file_func: Callable[[str, bool], List[str]], use_edited: bool
) -> str:
    title_files = get_file_func(title_str, use_edited)
    if title_files:
        index = randrange(0, len(title_files))
        return title_files[index]

    return ""
