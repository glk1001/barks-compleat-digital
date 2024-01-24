import collections
import csv
from dataclasses import dataclass
from datetime import date
from typing import Dict, OrderedDict

JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

MONTH_AS_LONG_STR: Dict[int, str] = {
    JAN: "January",
    FEB: "February",
    MAR: "March",
    APR: "April",
    MAY: "May",
    JUN: "June",
    JUL: "July",
    AUG: "August",
    SEP: "September",
    OCT: "October",
    NOV: "November",
    DEC: "December",
}
MONTH_AS_SHORT_STR: Dict[int, str] = {
    -1: "   ",
    JAN: "Jan",
    FEB: "Feb",
    MAR: "Mar",
    APR: "Apr",
    MAY: "May",
    JUN: "Jun",
    JUL: "Jul",
    AUG: "Aug",
    SEP: "Sep",
    OCT: "Oct",
    NOV: "Nov",
    DEC: "Dec",
}


@dataclass
class ComicBookInfo:
    issue_name: str
    issue_number: int
    issue_year: int
    issue_month: int
    submitted_year: int
    submitted_month: int
    submitted_day: int
    colorist: str
    series_name: str = ""
    number_in_series: int = -1


ComicBookInfoDict = OrderedDict[str, ComicBookInfo]


def get_all_comic_book_info(stories_filename: str) -> ComicBookInfoDict:
    current_number_in_series = SERIES_INFO_START_NUMBERS.copy()
    all_info: ComicBookInfoDict = collections.OrderedDict()

    with open(stories_filename, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in reader:
            title = row[0]
            if title not in SERIES_INFO:
                continue

            colorist = SERIES_INFO[title].colorist
            series_name = SERIES_INFO[title].series_name

            comic_book_info = ComicBookInfo(
                row[1],
                int(row[2]),
                int(row[3]),
                int(row[4]),
                int(row[5]),
                int(row[6]),
                int(row[7]),
                colorist,
                series_name,
                current_number_in_series[series_name],
            )

            all_info[title] = comic_book_info

            current_number_in_series[series_name] += 1

    return all_info


def check_story_submitted_order(stories: ComicBookInfoDict):
    prev_title = ""
    prev_submitted_date = date(1940, 1, 1)
    for story in stories:
        submitted_month_str = stories[story].submitted_month
        if submitted_month_str == "<none>":
            continue
        submitted_day = (
            1 if stories[story].submitted_day == -1 else stories[story].submitted_day
        )
        title = story.title()
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
        prev_title = title
        prev_submitted_date = submitted_date


@dataclass
class SourceBook:
    title: str
    pub: str
    year: int


FAN = "Fantagraphics"
CB = "Carl Barks"

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

# fmt: off
SOURCE_COMICS = {
        'FANTA_04': SourceBook( f"{CB} Vol. 4 - {DD} - Maharajah Donald (Lil Salem-Empire)", FAN, 2023),
        'FANTA_05': SourceBook( f"{CB} Vol. 5 - {DD} - Christmas on Bear Mountain (Digital-Empire)", FAN, 2013),
        'FANTA_06': SourceBook( f"{CB} Vol. 6 - {DD} - The Old Castle's Secret (Digital-Empire)", FAN, 2013),
        'FANTA_07': SourceBook( f"{CB} Vol. 7 - {DD} - Lost in the Andes (Digital-Empire)", FAN, 2011),
        'FANTA_08': SourceBook( f"{CB} Vol. 8 - {DD} - Trail of the Unicorn (Digital-Empire)", FAN, 2014),
        'FANTA_09': SourceBook( f"{CB} Vol. 9 - {DD} - The Pixilated Parrot (Digital-Empire)", FAN, 2015),
        'FANTA_10': SourceBook(f"{CB} Vol. 10 - {DD} - Terror of the Beagle Boys (Digital-Empire)", FAN, 2016),
        'FANTA_11': SourceBook(f"{CB} Vol. 11 - {DD} - A Christmas for Shacktown (Digital-Empire)", FAN, 2012),
        'FANTA_12': SourceBook(f"{CB} Vol. 12 - {US} - Only a Poor Old Man (Digital-Empire)", FAN, 2012),
        'FANTA_13': SourceBook(f"{CB} Vol. 13 - {DD} - Trick or Treat (Digital-Empire)", FAN, 2015),
        'FANTA_14': SourceBook(f"{CB} Vol. 14 - {US} - The Seven Cities of Gold (Digital-Empire)", FAN, 2014),
        'FANTA_15': SourceBook(f"{CB} Vol. 15 - {DD} - The Ghost Sheriff of Last Gasp (Digital-Empire)", FAN, 2016),
        'FANTA_16': SourceBook(f"{CB} Vol. 16 - {US} - The Lost Crown of Genghis Khan (Digital-Empire)", FAN, 2017),
        'FANTA_17': SourceBook(f"{CB} Vol. 17 - {DD} - The Secret of Hondorica (Digital-Empire)", FAN, 2017),
        'FANTA_18': SourceBook(f"{CB} Vol. 18 - {DD} - The Lost Peg Leg Mine (Digital-Empire)", FAN, 2018),
        'FANTA_19': SourceBook(f"{CB} Vol. 19 - {DD} - The Black Pearls of Tabu Yama (Bean-Empire)", FAN, 2018),
        'FANTA_20': SourceBook(f"{CB} Vol. 20 - {US} - The Mines of King Solomon (Bean-Empire)", FAN, 2019),
}
# fmt: on

SERIES_DDA = DD + " Adventures"
SERIES_USA = US + " Adventures"
SERIES_DDS = DD + " Short Stories"
SERIES_USS = US + " Short Stories"
SERIES_CS = CS
SERIES_GG = "Gyro Gearloose"
SERIES_MISC = "Misc"

ALL_SERIES = [
    SERIES_DDA,
    SERIES_USA,
    SERIES_DDS,
    SERIES_USS,
    SERIES_CS,
    SERIES_GG,
    SERIES_MISC,
]

RTOM = "Rich Tommaso"
GLEA = "Gary Leach"
SLEA = "Susan Daigle-Leach"
DIGI = "Digikore Studios"


@dataclass
class SeriesInfo:
    colorist: str
    series_name: str
    number_in_series: int = -1


SERIES_INFO_START_NUMBERS: Dict[str, int] = {
    SERIES_DDA: 1,
    SERIES_USA: 1,
    SERIES_DDS: 1,
    SERIES_USS: 1,
    SERIES_CS: 73, # wrong
    SERIES_GG: 1,
    SERIES_MISC: 1,
}

# fmt: off
SERIES_INFO: Dict[str, SeriesInfo] = {
    "Donald Duck Finds Pirate Gold": SeriesInfo("?", SERIES_DDA),
    "Donald Duck and the Mummy's Ring": SeriesInfo("?", SERIES_DDA),
    "The Hard Loser": SeriesInfo("?", SERIES_DDA),
    "Too Many Pets": SeriesInfo("?", SERIES_DDA),
    "Frozen Gold": SeriesInfo("?", SERIES_DDA),
    "Mystery of the Swamp": SeriesInfo("?", SERIES_DDA),
    "The Firebug": SeriesInfo("?", SERIES_DDA),
    "The Terror of the River!!": SeriesInfo(SLEA, SERIES_DDA),
    "Maharajah Donald": SeriesInfo(GLEA, SERIES_DDA),
    "Volcano Valley": SeriesInfo(RTOM, SERIES_DDA),
    "Adventure Down Under": SeriesInfo(RTOM, SERIES_DDA),
    "The Ghost of the Grotto": SeriesInfo(RTOM, SERIES_DDA),
    "Christmas on Bear Mountain": SeriesInfo(RTOM, SERIES_DDA),
    "Darkest Africa": SeriesInfo(RTOM, SERIES_DDA),
    "The Old Castle's Secret": SeriesInfo(RTOM, SERIES_DDA),
    "Sheriff of Bullet Valley": SeriesInfo(RTOM, SERIES_DDA),
    "The Golden Christmas Tree": SeriesInfo(RTOM, SERIES_DDA),
    "Lost in the Andes!": SeriesInfo(RTOM, SERIES_DDA),
    "Race to the South Seas!": SeriesInfo(RTOM, SERIES_DDA),
    "Voodoo Hoodoo": SeriesInfo(RTOM, SERIES_DDA),
    "Letter to Santa": SeriesInfo(RTOM, SERIES_DDA),
    "Luck of the North": SeriesInfo(RTOM, SERIES_DDA),
    "Trail of the Unicorn": SeriesInfo(RTOM, SERIES_DDA),
    "Land of the Totem Poles": SeriesInfo(RTOM, SERIES_DDA),
    "In Ancient Persia": SeriesInfo(RTOM, SERIES_DDA),
    "Vacation Time": SeriesInfo(RTOM, SERIES_DDA),
    "The Pixilated Parrot": SeriesInfo(RTOM, SERIES_DDA),
    "The Magic Hourglass": SeriesInfo(RTOM, SERIES_DDA),
    "Big-Top Bedlam": SeriesInfo(RTOM, SERIES_DDA),
    "Dangerous Disguise": SeriesInfo(RTOM, SERIES_DDA),
    "No Such Varmint": SeriesInfo(RTOM, SERIES_DDA),
    "In Old California!": SeriesInfo(RTOM, SERIES_DDA),
    "A Christmas for Shacktown": SeriesInfo(RTOM, SERIES_DDA),
    "The Golden Helmet": SeriesInfo(RTOM, SERIES_DDA),
    "The Gilded Man": SeriesInfo(RTOM, SERIES_DDA),
    "Trick or Treat": SeriesInfo(RTOM, SERIES_DDA),
    "Secret of Hondorica": SeriesInfo(RTOM, SERIES_DDA),
    "Forbidden Valley": SeriesInfo(RTOM, SERIES_DDA),

    "Only a Poor Old Man": SeriesInfo(RTOM, SERIES_USA),
    "Back to the Klondike": SeriesInfo(RTOM, SERIES_USA),
    "The Horseradish Story": SeriesInfo(RTOM, SERIES_USA),
    "The Menehune Mystery": SeriesInfo(RTOM, SERIES_USA),
    "The Secret of Atlantis": SeriesInfo(RTOM, SERIES_USA),
    "Tralla La": SeriesInfo(RTOM, SERIES_USA),
    "The Seven Cities of Cibola": SeriesInfo(RTOM, SERIES_USA),
    "The Mysterious Stone Ray": SeriesInfo(RTOM, SERIES_USA),
    "The Lemming with the Locket": SeriesInfo(RTOM, SERIES_USA),
    "The Fabulous Philosopher's Stone": SeriesInfo(RTOM, SERIES_USA),
    "The Great Steamboat Race": SeriesInfo(RTOM, SERIES_USA),
    "Riches, Riches, Everywhere!": SeriesInfo(RTOM, SERIES_USA),
    "The Golden Fleecing": SeriesInfo(RTOM, SERIES_USA),
    "Land Beneath the Ground!": SeriesInfo(RTOM, SERIES_USA),
    "The Lost Crown of Genghis Khan!": SeriesInfo(RTOM, SERIES_USA),
    "The Second-Richest Duck": SeriesInfo(RTOM, SERIES_USA),
    "Back to Long Ago!": SeriesInfo(RTOM, SERIES_USA),
    "A Cold Bargain": SeriesInfo(RTOM, SERIES_USA),

    "The Bill Collectors": SeriesInfo(DIGI, SERIES_CS),
    "Managing the Echo System": SeriesInfo(RTOM, SERIES_CS),
    "Plenty of Pets": SeriesInfo(RTOM, SERIES_CS),

    "Seals Are So Smart!": SeriesInfo(GLEA, SERIES_DDS),
    "The Peaceful Hills": SeriesInfo(SLEA, SERIES_DDS),

    "Somethin' Fishy Here": SeriesInfo(RTOM, SERIES_USS),
}
# fmt: on
