import collections
import csv
import os

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import OrderedDict

# Sort these out
# "News from Afar","M","Uncle Scrooge",25,1959,3,-1,-1,-1
# "Rainbow's End","M","Donald Duck",71,1960,5,-1,-1,-1
# "The Homey Touch","M","Uncle Scrooge",32,1960,12,-1,-1,-1
# "Turnabout","M","Uncle Scrooge",32,1960,12,-1,-1,-1
# "Pawns of the Loup Garou","M","Donald Duck",117,1968,1,-1,-1,-1

DD = "Donald Duck"
US = "Uncle Scrooge"

CS = "Comics and Stories"
FC = "Four Color"
CP = "Christmas Parade"
VP = "Vacation Parade"
MC = "Boys' and Girls' March of Comics"
FG = "Firestone Giveaway"
CH = "Cheerios Giveaway"
KI = "Kites Giveaway"
USGTD = "Uncle Scrooge Goes to Disneyland"
CID = "Christmas in Disneyland"
MMA = "Mickey Mouse Almanac"
SF = "Summer Fun"

ISSUE_NAME_AS_TITLE = {
    US: "Uncle\nScrooge",
    FG: "Firestone\nGiveaway",
    USGTD: "Uncle Scrooge\nGoes to\nDisneyland",
    CID: "Christmas\nin\nDisneyland",
}
SHORT_ISSUE_NAME = {
    DD: "DD",
    US: "US",
    CS: "WDCS",
    FC: "FC",
    CP: "CP",
    VP: "VP",
    MC: "MOC",
    FG: "FG",
    CH: "CG",
    KI: "KG",
    USGTD: "USGTD",
    CID: "CID",
    MMA: "MMA",
    SF: "SF",
}

PUBLICATION_INFO_SUBDIR = "story-indexes"
SUBMISSION_DATES_SUBDIR = "story-indexes"
STORIES_INFO_FILENAME = "the-stories.csv"


@dataclass
class ComicBookInfo:
    is_barks_title: bool
    issue_name: str
    issue_number: int
    issue_year: int
    issue_month: int
    submitted_year: int
    submitted_month: int
    submitted_day: int
    chronological_number: int

    def get_issue_title(self):
        short_issue_name = SHORT_ISSUE_NAME[self.issue_name]
        return f"{short_issue_name} {self.issue_number}"


ComicBookInfoDict = OrderedDict[str, ComicBookInfo]


def get_all_comic_book_info() -> ComicBookInfoDict:
    story_info_dir = str(Path(__file__).parent.parent.parent.absolute())

    stories_filename = os.path.join(story_info_dir, PUBLICATION_INFO_SUBDIR, STORIES_INFO_FILENAME)

    all_info: ComicBookInfoDict = collections.OrderedDict()

    chronological_number = 1
    with open(stories_filename, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in reader:
            title = row[0]

            comic_book_info = ComicBookInfo(
                is_barks_title=row[1] == "T",
                issue_name=row[2],
                issue_number=int(row[3]),
                issue_year=int(row[4]),
                issue_month=int(row[5]),
                submitted_year=int(row[6]),
                submitted_month=int(row[7]),
                submitted_day=int(row[8]),
                chronological_number=chronological_number,
            )

            all_info[title] = comic_book_info

            chronological_number += 1

    check_story_submitted_order(all_info)

    return all_info


def check_story_submitted_order(stories: ComicBookInfoDict):
    prev_chronological_number = -1
    prev_title = ""
    prev_submitted_date = date(1940, 1, 1)
    for story in stories:
        title = story.title()
        if not 1 <= stories[story].submitted_month <= 12:
            raise Exception(
                f'"{title}": Invalid submission month: {stories[story].submitted_month}.'
            )
        submitted_day = 1 if stories[story].submitted_day == -1 else stories[story].submitted_day
        submitted_date = date(
            stories[story].submitted_year,
            stories[story].submitted_month,
            submitted_day,
        )
        if prev_submitted_date > submitted_date:
            raise Exception(
                f'"{title}": Out of order submitted date {submitted_date}.'
                f' Previous entry: "{prev_title}" - {prev_submitted_date}.'
            )
        chronological_number = stories[story].chronological_number
        if prev_chronological_number > chronological_number:
            raise Exception(
                f'"{title}": Out of order chronological number {chronological_number}.'
                f' Previous entry: "{prev_title}" - {prev_chronological_number}.'
            )
        prev_title = title
        prev_submitted_date = submitted_date
