import logging
import os.path
from dataclasses import dataclass
from enum import Enum, auto
from random import randrange
from typing import List, Callable, Union, Set, Tuple

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
    get_app_splash_images_dir,
)
from reader_utils import prob_rand_less_equal


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
APP_SPLASH_IMAGES = [
    "006.png",
]

ALL_TYPES = {t for t in FileTypes}
ALL_BUT_ORIGINAL_ART = {t for t in FileTypes if t != FileTypes.ORIGINAL_ART}

FIT_MODE_CONTAIN = "contain"
FIT_MODE_COVER = "cover"


@dataclass
class ImageInfo:
    filename: str = ""
    from_title: Titles = Titles.GOOD_NEIGHBORS
    fit_mode: str = FIT_MODE_COVER


def get_random_search_image() -> ImageInfo:
    title_index = randrange(0, len(SEARCH_TITLES))
    title = SEARCH_TITLES[title_index]

    return ImageInfo(
        __get_random_comic_file(BARKS_TITLES[title], get_comic_search_files, False),
        title,
        FIT_MODE_COVER,
    )


def get_random_app_splash_image() -> str:
    index = randrange(0, len(APP_SPLASH_IMAGES))
    return os.path.join(get_app_splash_images_dir(), APP_SPLASH_IMAGES[index])


def get_random_image_file(
    title_list: List[FantaComicBookInfo], file_types: Union[Set[FileTypes], None] = None
) -> str:
    return get_random_image(title_list, file_types=file_types).filename


def get_random_image_for_title(
    title: str, file_types: Set[FileTypes], use_edited: bool = False
) -> str:
    title_image = __get_random_image_for_title(title, file_types, use_edited)
    if title_image:
        return title_image[0]

    return get_comic_inset_file(EMERGENCY_INSET_FILE)


def get_random_image(
    title_list: List[FantaComicBookInfo],
    use_random_fit_mode=False,
    file_types: Union[Set[FileTypes], None] = None,
    use_edited: bool = False,
) -> ImageInfo:
    title_index = randrange(0, len(title_list))

    comic_book_info = title_list[title_index].comic_book_info
    title = comic_book_info.title
    fit_mode = FIT_MODE_COVER if not use_random_fit_mode else __get_random_fit_mode()

    title_image = __get_random_image_for_title(
        comic_book_info.get_title_str(), file_types, use_edited
    )

    if title_image:
        image_file = title_image[0]
        file_type = title_image[1]
        if file_type == FileTypes.COVER:
            fit_mode = FIT_MODE_CONTAIN
        return ImageInfo(image_file, title, fit_mode)

    return ImageInfo(get_comic_inset_file(title), title, fit_mode)


def __get_random_fit_mode() -> str:
    if prob_rand_less_equal(50):
        return FIT_MODE_COVER

    return FIT_MODE_CONTAIN


def __get_random_image_for_title(
    title_str: str, file_types: Union[Set[FileTypes], None], use_edited: bool
) -> Union[Tuple[str, FileTypes], None]:
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
                image_file = __get_comic_file(title_str, file_type, use_edited)
                if image_file:
                    return image_file, file_type
                logging.debug(f'"{title_str}": No images of type {file_type.name}.')
                percent[file_type] = -1

        if max(percent.values()) < 0:
            break

    return None


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
