from typing import Tuple, List, Dict

from barks_fantagraphics.barks_tags import TagCategories, BARKS_TAG_CATEGORIES_TITLES
from barks_fantagraphics.fanta_comics_info import (
    get_filtered_title_lists,
    FantaComicBookInfo,
    SERIES_CS,
    SERIES_DDA,
    SERIES_DDS,
    SERIES_GG,
    SERIES_MISC,
    SERIES_USA,
    SERIES_USS,
)


class FilteredTitleLists:
    def __init__(self):
        self.year_ranges = [
            (1942, 1945),
            (1946, 1949),
            (1950, 1953),
            (1954, 1957),
            (1958, 1961),
        ]
        self.series_names = [
            SERIES_CS,
            SERIES_DDA,
            SERIES_DDS,
            SERIES_GG,
            SERIES_MISC,
            SERIES_USA,
            SERIES_USS,
        ]
        self.categories = list(TagCategories)

    @staticmethod
    def get_range_str(year_range: Tuple[int, int]):
        return f"{year_range[0]} - {year_range[1]}"

    def get_title_lists(self) -> Dict[str, List[FantaComicBookInfo]]:

        def create_range_lamba(yr_range: Tuple[int, int]):
            return lambda info: yr_range[0] <= info.comic_book_info.submitted_year <= yr_range[1]

        def create_series_lamba(series_name: str):
            return lambda info: info.series_name == series_name

        def create_category_lamba(cat: TagCategories):
            return lambda info: info.comic_book_info.title in BARKS_TAG_CATEGORIES_TITLES[cat]

        filters = {}
        for year_range in self.year_ranges:
            filters[self.get_range_str(year_range)] = create_range_lamba(year_range)
        for name in self.series_names:
            filters[name] = create_series_lamba(name)
        for category in self.categories:
            filters[category.name] = create_category_lamba(category)

        return get_filtered_title_lists(filters)
