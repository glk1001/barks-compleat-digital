import csv
import functools
from dataclasses import dataclass
from typing import Dict, List, Tuple

import comics_info
from comics_info import (
    ComicBookInfo,
    MONTH_AS_SHORT_STR,
    CH,
    CP,
    CS,
    DD,
    FC,
    FG,
    KI,
    MC,
    US,
    VP,
)
from create_clean_comic import get_formatted_submitted_date
from read_stories import get_all_stories, StoryInfo
from read_sub_dates import get_all_submitted_info, SubmittedInfoDict

MONTH_AS_INT: Dict[str, int] = {
    "<none>": -1,
    "January": comics_info.JAN,
    "February": comics_info.FEB,
    "March": comics_info.MAR,
    "April": comics_info.APR,
    "May": comics_info.MAY,
    "June": comics_info.JUN,
    "July": comics_info.JUL,
    "August": comics_info.AUG,
    "September": comics_info.SEP,
    "October": comics_info.OCT,
    "November": comics_info.NOV,
    "December": comics_info.DEC,
}

COMICS_AND_STORIES_ISSUE_NAME = "W WDC"
COMICS_AND_STORIES_FILENAME = "sub-dates-cs-cleaned.txt"
FOUR_COLOR_ISSUE_NAME = "W OS"
FOUR_COLOR_FILENAME = "sub-dates-os-cleaned.txt"
DONALD_DUCK_ISSUE_NAME = "W DD"
DONALD_DUCK_FILENAME = "sub-dates-dd-cleaned.txt"
UNCLE_SCROOGE_ISSUE_NAME = "W US"
UNCLE_SCROOGE_FILENAME = "sub-dates-us-cleaned.txt"
CHRISTMAS_PARADE_ISSUE_NAME = "W CP"
CHRISTMAS_PARADE_FILENAME = "sub-dates-cp-cleaned.txt"
VACATION_PARADE_ISSUE_NAME = "W VP"
VACATION_PARADE_FILENAME = "sub-dates-vp-cleaned.txt"
FIRESTONE_GIVEAWAYS_FILENAME = "sub-dates-fg-cleaned.txt"
FIRESTONE_GIVEAWAYS_ISSUE_NAME = "W FGW"
KITES_GIVEAWAYS_FILENAME = "sub-dates-ki-cleaned.txt"
KITES_GIVEAWAYS_ISSUE_NAME = "W KGA"
MARCH_OF_COMICS_GIVEAWAYS_FILENAME = "sub-dates-moc-cleaned.txt"
MARCH_OF_COMICS_GIVEAWAYS_ISSUE_NAME = "W MOC"
CHEERIOS_GIVEAWAYS_FILENAME = "sub-dates-ch-cleaned.txt"
CHEERIOS_GIVEAWAYS_ISSUE_NAME = "W CGW"


@dataclass
class ComicBookInfo:
    issue_name: str
    issue_number: int
    issue_year: int
    issue_month: int
    submitted_year: int
    submitted_month: int
    submitted_day: int


all_stories: List[StoryInfo] = get_all_stories()
all_cs_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    COMICS_AND_STORIES_FILENAME, COMICS_AND_STORIES_ISSUE_NAME
)
all_fc_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    FOUR_COLOR_FILENAME, FOUR_COLOR_ISSUE_NAME
)
all_dd_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    DONALD_DUCK_FILENAME, DONALD_DUCK_ISSUE_NAME
)
all_us_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    UNCLE_SCROOGE_FILENAME, UNCLE_SCROOGE_ISSUE_NAME
)
all_moc_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    MARCH_OF_COMICS_GIVEAWAYS_FILENAME, MARCH_OF_COMICS_GIVEAWAYS_ISSUE_NAME
)
all_cp_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    CHRISTMAS_PARADE_FILENAME, CHRISTMAS_PARADE_ISSUE_NAME
)
all_vp_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    VACATION_PARADE_FILENAME, VACATION_PARADE_ISSUE_NAME
)
all_fg_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    FIRESTONE_GIVEAWAYS_FILENAME, FIRESTONE_GIVEAWAYS_ISSUE_NAME
)
all_ch_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    CHEERIOS_GIVEAWAYS_FILENAME, CHEERIOS_GIVEAWAYS_ISSUE_NAME
)
all_ki_sub_dates: SubmittedInfoDict = get_all_submitted_info(
    KITES_GIVEAWAYS_FILENAME, KITES_GIVEAWAYS_ISSUE_NAME
)


def get_comic_book_info(story: StoryInfo) -> ComicBookInfo:
    if story.issue_name == "Walt Disney's Comics and Stories":
        sub_info = all_cs_sub_dates[(COMICS_AND_STORIES_ISSUE_NAME, story.issue_num)]
        issue_name = CS
    elif story.issue_name == "Donald Duck Four Color":
        issue_name = FC
        sub_info = all_fc_sub_dates[(FOUR_COLOR_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Mickey Mouse Four Color":
        issue_name = FC
        sub_info = all_fc_sub_dates[(FOUR_COLOR_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Uncle Scrooge Four Color":
        issue_name = FC
        sub_info = all_fc_sub_dates[(FOUR_COLOR_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Donald Duck":
        issue_name = DD
        sub_info = all_dd_sub_dates[(DONALD_DUCK_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Uncle Scrooge":
        issue_name = US
        sub_info = all_us_sub_dates[(UNCLE_SCROOGE_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Walt Disney's Christmas Parade":
        issue_name = CP
        sub_info = all_cp_sub_dates[(CHRISTMAS_PARADE_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Walt Disney's Vacation Parade":
        issue_name = VP
        sub_info = all_vp_sub_dates[(VACATION_PARADE_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Boys' and Girls' March of Comics":
        issue_name = MC
        sub_info = all_moc_sub_dates[
            (MARCH_OF_COMICS_GIVEAWAYS_ISSUE_NAME, story.issue_num)
        ]
    elif story.issue_name == "Firestone Giveaway":
        issue_name = FG
        sub_info = all_fg_sub_dates[(FIRESTONE_GIVEAWAYS_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Cheerios Giveaway":
        issue_name = CH
        sub_info = all_ch_sub_dates[(CHEERIOS_GIVEAWAYS_ISSUE_NAME, story.issue_num)]
    elif story.issue_name == "Kites Giveaway":
        issue_name = KI
        sub_info = all_ki_sub_dates[(KITES_GIVEAWAYS_ISSUE_NAME, story.issue_num)]
    else:
        issue_name = ""
        sub_info = None
        print(f"Unknown story: {story.title}, {story.issue_name}")

    if not sub_info:
        return None
    if sub_info.submitted_day == "<none>":
        return None

    return ComicBookInfo(
        issue_name,
        int(story.issue_num),
        int(story.issue_year),
        MONTH_AS_INT[story.issue_month],
        int(sub_info.submitted_year),
        MONTH_AS_INT[sub_info.submitted_month],
        int(sub_info.submitted_day),
    )


all_comic_book_info: List[Tuple[str, ComicBookInfo]] = []
for story in all_stories:
    comic_book_info = get_comic_book_info(story)
    if comic_book_info:
        all_comic_book_info.append((story.title, comic_book_info))


def compare(info1: Tuple[str, ComicBookInfo], info2: Tuple[str, ComicBookInfo]) -> int:
    cb_info1 = info1[1]
    cb_info2 = info2[1]
    if cb_info1.submitted_year < cb_info2.submitted_year:
        return -1
    if cb_info1.submitted_year > cb_info2.submitted_year:
        return +1
    if cb_info1.submitted_month < cb_info2.submitted_month:
        return -1
    if cb_info1.submitted_month > cb_info2.submitted_month:
        return +1
    if cb_info1.submitted_day < cb_info2.submitted_day:
        return -1
    if cb_info1.submitted_day > cb_info2.submitted_day:
        return +1
    return 0


all_comic_book_info = sorted(all_comic_book_info, key=functools.cmp_to_key(compare))

# Now dump the sorted comc book info to a csv.
output_file = "/tmp/barks-stories.csv"
with open(output_file, "w") as f:
    for info in all_comic_book_info:
        title = info[0]
        comic_book_info = info[1]
        f.write(
            f'"{title}","{comic_book_info.issue_name}",{comic_book_info.issue_number},'
            f"{comic_book_info.issue_year},{comic_book_info.issue_month},"
            f"{comic_book_info.submitted_year},"
            f"{comic_book_info.submitted_month},"
            f"{comic_book_info.submitted_day}\n"
        )

# Now retrieve and print the formatted csv as a check.
with open(output_file) as csv_file:
    all_comic_book_info: List[Tuple[str, ComicBookInfo]] = []
    reader = csv.reader(csv_file, delimiter=",", quotechar='"')

    max_title_len = 0
    max_issue_name = 0
    for row in reader:
        title = row[0]
        issue_name = row[1]
        all_comic_book_info.append(
            (
                title,
                ComicBookInfo(
                    issue_name,
                    int(row[2]),
                    int(row[3]),
                    int(row[4]),
                    int(row[5]),
                    int(row[6]),
                    int(row[7]),
                ),
            )
        )

        if len(title) > max_title_len:
            max_title_len = len(title)
        if len(issue_name) > max_issue_name:
            max_issue_name = len(issue_name)

    for info in all_comic_book_info:
        title = info[0]
        comic_book_info = info[1]
        print(
            f'"{title:<{max_title_len}}", "{comic_book_info.issue_name:<{max_issue_name}}",'
            f" {comic_book_info.issue_number:>4},"
            f" {MONTH_AS_SHORT_STR[comic_book_info.issue_month]:>3}"
            f" {comic_book_info.issue_year:>4},"
            f" {get_formatted_submitted_date(comic_book_info):<19}"
        )
