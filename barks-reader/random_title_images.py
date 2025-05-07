from random import randrange

from file_paths import (
    get_comic_inset_file,
    get_comic_cover_file,
    get_comic_splash_files,
    get_comic_silhouette_files,
    EMERGENCY_INSET_FILE,
)
from filtered_title_lists import FilteredTitleLists


def get_random_image(filtered_title_lists: FilteredTitleLists, title_category: str) -> str:
    titles = filtered_title_lists.get_title_lists()[title_category]
    title_index = randrange(0, len(titles))
    title_image = get_comic_inset_file(titles[title_index].comic_book_info.title)

    return title_image


def get_random_title_image(title: str) -> str:
    num_categories = 3
    silhouette_percent = int(round(100 / num_categories))
    splashes_percent = 2 * int(round(100 / num_categories))
    covers_percent = 3 * int(round(100 / num_categories))

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

        if rand_percent <= covers_percent:
            title_file = get_comic_cover_file(title)
            if title_file:
                return title_file
            covers_percent = -1
            print(f"No covers.")

        if silhouette_percent == -1 and splashes_percent == -1 and covers_percent == -1:
            break

    return get_comic_inset_file(EMERGENCY_INSET_FILE)
