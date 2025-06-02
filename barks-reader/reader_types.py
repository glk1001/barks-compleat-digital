from typing import Tuple

INTRO_NODE_TEXT = "Introduction"
THE_STORIES_NODE_TEXT = "The Stories"
CHRONOLOGICAL_NODE_TEXT = "Chronological"
SERIES_NODE_TEXT = "Series"
CATEGORIES_NODE_TEXT = "Categories"
SEARCH_NODE_TEXT = "Search"
APPENDIX_NODE_TEXT = "Appendix"
INDEX_NODE_TEXT = "Index"

Color = Tuple[float, float, float, float]


def get_formatted_color(color: Color) -> str:
    color_strings = [f"{c:04.2f}" for c in color]
    return f'({", ".join(color_strings)})'
