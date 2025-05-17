from barks_fantagraphics.barks_extra_info import BARKS_EXTRA_INFO
from barks_fantagraphics.comic_issues import ISSUE_NAME, Issues
from barks_fantagraphics.comics_utils import (
    get_formatted_first_published_str,
    get_long_formatted_submitted_date,
)
from barks_fantagraphics.fanta_comics_info import FantaComicBookInfo, FANTA_SOURCE_COMICS, FAN


class ReaderFormatter:
    def __init__(self):
        # Use a custom issue_name here to display slightly shorter names.
        self.title_info_issue_name = ISSUE_NAME.copy()
        self.title_info_issue_name[Issues.CS] = "Comics & Stories"
        self.title_info_issue_name[Issues.MC] = "March of Comics"

    def get_title_info(self, fanta_info: FantaComicBookInfo) -> str:
        # TODO: Clean this up.
        issue_info = get_formatted_first_published_str(
            fanta_info.comic_book_info, self.title_info_issue_name
        )
        submitted_info = get_long_formatted_submitted_date(fanta_info.comic_book_info)
        fanta_book = FANTA_SOURCE_COMICS[fanta_info.fantagraphics_volume]
        source = f"{FAN} CBDL, Vol {fanta_book.volume}, {fanta_book.year}"
        return (
            f"[i]1st Issue:[/i]   [b]{issue_info}[/b]\n"
            f"[i]Submitted:[/i] [b]{submitted_info}[/b]\n"
            f"[i]Source:[/i]       [b]{source}[/b]"
        )

    def get_extra_title_info(self, fanta_info: FantaComicBookInfo) -> str:
        title = fanta_info.comic_book_info.title
        if title not in BARKS_EXTRA_INFO:
            return ""

        return f"{BARKS_EXTRA_INFO[title]}"
