from random import randrange
from typing import List

from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo
from file_paths import (
    EMERGENCY_INSET_FILE,
    get_comic_inset_file,
    get_comic_cover_file,
    get_comic_splash_files,
    get_comic_silhouette_files,
    get_comic_censorship_files,
)


def get_random_image(title_list: List[FantaComicBookInfo]) -> str:
    title_index = randrange(0, len(title_list))

    title_image_file = __get_random_title_image(title_list[title_index].comic_book_info.title_str)
    if title_image_file:
        return title_image_file

    return get_comic_inset_file(title_list[title_index].comic_book_info.title)


def __get_random_title_image(title: str) -> str:
    num_categories = 4
    silhouette_percent = int(round(100 / num_categories))
    splashes_percent = 2 * int(round(100 / num_categories))
    censorship_percent = 3 * int(round(100 / num_categories))
    covers_percent = 4 * int(round(100 / num_categories))

    for num_attempts in range(10):
        rand_percent = randrange(0, 100)
        print(f"Attempt {num_attempts}: rand percent = {rand_percent}.")

        if rand_percent <= silhouette_percent:
            title_files = get_comic_silhouette_files(title)
            if title_files:
                index = randrange(0, len(title_files))
                return title_files[index]
            silhouette_percent = -1
            print(f"No silhouettes.")

        if rand_percent <= splashes_percent:
            title_files = get_comic_splash_files(title)
            if title_files:
                index = randrange(0, len(title_files))
                return title_files[index]
            splashes_percent = -1
            print(f"No splashes.")

        if rand_percent <= censorship_percent:
            title_files = get_comic_censorship_files(title)
            if title_files:
                index = randrange(0, len(title_files))
                return title_files[index]
            censorship_percent = -1
            print(f"No censorship files.")

        if rand_percent <= covers_percent:
            title_file = get_comic_cover_file(title)
            if title_file:
                return title_file
            covers_percent = -1
            print(f"No covers.")

        if (
            silhouette_percent == -1
            and splashes_percent == -1
            and censorship_percent == -1
            and covers_percent == -1
        ):
            break

    return ""


def get_random_title_image(title: str) -> str:
    title_image_file = __get_random_title_image(title)
    if title_image_file:
        return title_image_file

    return get_comic_inset_file(EMERGENCY_INSET_FILE)
