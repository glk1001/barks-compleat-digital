import collections
from dataclasses import dataclass
from datetime import date
from typing import Dict, OrderedDict, Tuple

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

MONTH_AS_STR: Dict[int, str] = {
    JAN: 'January',
    FEB: 'February',
    MAR: 'March',
    APR: 'April',
    MAY: 'May',
    JUN: 'June',
    JUL: 'July',
    AUG: 'August',
    SEP: 'September',
    OCT: 'October',
    NOV: 'November',
    DEC: 'December',
}


@dataclass
class ComicBookInfo:
    issue_name: str
    issue_number: int
    issue_month: int
    issue_year: int
    submitted_month: int
    submitted_day: int
    submitted_year: int
    colorist: str
    series_name: str = ""
    number_in_series: int = -1


def check_story_submission_order(stories: OrderedDict[str, ComicBookInfo]):
    prev_submission_date = date(1940, 1, 1)
    for story in stories:
        submitted_month_str = stories[story].submitted_month
        if submitted_month_str == "<none>":
            continue
        submission_date = date(
            stories[story].submitted_year,
            stories[story].submitted_month,
            stories[story].submitted_day,
        )
        if prev_submission_date > submission_date:
            raise Exception(f"{story}: Out of order submission date {submission_date}.")
        prev_submission_date = submission_date


def get_comic_book_series(title: str) -> Tuple[str, OrderedDict[str, ComicBookInfo]]:
    if title in DONALD_DUCK_LONG_STORIES:
        return SERIES_DDA, DONALD_DUCK_LONG_STORIES
    if title in UNCLE_SCROOGE_LONG_STORIES:
        return SERIES_US, UNCLE_SCROOGE_LONG_STORIES
    if title in COMICS_AND_STORIES:
        return SERIES_CS, COMICS_AND_STORIES

    raise Exception(f"Unknown title: '{title}'.")


@dataclass
class SourceBook:
    title: str
    pub: str
    year: int


FAN = "Fantagraphics"
CB = "Carl Barks"
DD = "Donald Duck"
US = "Uncle Scrooge"

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


CS = "Comics and Stories"
FC = "Four Color"
CP = "Christmas Parade"
MC = "Boys' and Girls' March of Comics"
VP = "Vacation Parade"
DD = "Donald Duck"
FG = "Firestone Giveaway"
CH = "Cheerios Giveaway"
KI = "Kites Giveaway"

SERIES_DDA = "Donald Duck Adventures"
SERIES_US = US
SERIES_CS = CS

RTOM = "Rich Tommaso"
GLEA = "Gary Leach"
SLEA = "Susan Daigle-Leach"


# fmt: off
DONALD_DUCK_LONG_STORIES = collections.OrderedDict([
        ('Donald Duck Finds Pirate Gold', ComicBookInfo(FC, 9, SEP, 1942, MAY, 21, 1942, '?')),
        ('The Mummy\'s Ring', ComicBookInfo(FC, 29, SEP, 1943, MAY, 10, 1943, '?')),
        ('The Hard Loser', ComicBookInfo(FC, 29, SEP, 1943, MAY, 10, 1943, '?')),
        ('Too Many Pets', ComicBookInfo(FC, 29, SEP, 1943, MAY, 29, 1943, '?')),
        ('Frozen Gold', ComicBookInfo(FC, 62, JAN, 1945, AUG, 9, 1944, '?')),
        ('The Mystery of the Swamp', ComicBookInfo(FC, 62, JAN, 1945, SEP, 23, 1944, '?')),
        ('The Firebug', ComicBookInfo(FC, 108, MAY, 1946, JUL, 19, 1945, '?')),
        ('The Terror of the River!!', ComicBookInfo(FC, 108, MAY, 1946, JAN, 25, 1946, SLEA)),
        ('Seals Are So Smart!', ComicBookInfo(FC, 108, MAY, 1946, JAN, 25, 1946, GLEA)),
        ('Maharajah Donald', ComicBookInfo(MC, 4, MAY, 1947, AUG, 13, 1946, GLEA)),
        ('Volcano Valley', ComicBookInfo(FC, 159, MAY, 1947, DEC, 9, 1946, RTOM)),
        ('Adventure "Down Under"', ComicBookInfo(FC, 159, AUG, 1947, APR, 4, 1947, RTOM)),
        ('The Ghost of the Grotto', ComicBookInfo(FC, 159, AUG, 1947, APR, 15, 1947, RTOM)),
        ('Christmas on Bear Mountain', ComicBookInfo(FC, 178, DEC, 1947, JUL, 22, 1947, RTOM)),
        ('Darkest Africa', ComicBookInfo(MC, 20, APR, 1948, SEP, 26, 1947, RTOM)),
        ('The Old Castle\'s Secret', ComicBookInfo(FC, 189, JUN, 1948, DEC, 3, 1947, RTOM)),
        ('Sheriff of Bullet Valley', ComicBookInfo(FC, 199, OCT, 1948, MAR, 16, 1948, RTOM)),
        ('The Golden Christmas Tree', ComicBookInfo(FC, 203, DEC, 1948, JUN, 30, 1948, RTOM)),
        ('Lost in the Andes', ComicBookInfo(FC, 223, APR, 1949, OCT, 21, 1948, RTOM)),
        ('Race to the South Seas', ComicBookInfo(MC, 41, FEB, 1949, DEC, 15, 1948, RTOM)),
        ('Voodoo Hoodoo', ComicBookInfo(FC, 238, AUG, 1949, MAR, 3, 1949, RTOM)),
        ('Letter to Santa', ComicBookInfo(CP, 1, NOV, 1949, JUN, 1, 1949, RTOM)),
        ('Luck of the North', ComicBookInfo(FC, 256, DEC, 1949, JUN, 29, 1949, RTOM)),
        ('Trail of the Unicorn', ComicBookInfo(FC, 263, FEB, 1950, SEP, 8, 1949, RTOM)),
        ('Land of the Totem Poles', ComicBookInfo(FC, 263, FEB, 1950, SEP, 29, 1949, RTOM)),
        ('In Ancient Persia', ComicBookInfo(FC, 275, MAY, 1950, NOV, 23, 1949, RTOM)),
        ('Vacation Time', ComicBookInfo(VP, 1, JUL, 1950, JAN, 5, 1950, RTOM)),
        ('The Pixilated Parrot', ComicBookInfo(FC, 282, JUL, 1950, FEB, 23, 1950, RTOM)),
        ('The Magic Hourglass', ComicBookInfo(FC, 291, SEP, 1950, MAR, 16, 1950, RTOM)),
        ('Big-top Bedlam', ComicBookInfo(FC, 300, NOV, 1950, APR, 20, 1950, RTOM)),
])
# fmt: on
check_story_submission_order(DONALD_DUCK_LONG_STORIES)

# fmt: off
UNCLE_SCROOGE_LONG_STORIES = collections.OrderedDict([
        ('Only a Poor Old Man', ComicBookInfo(FC, 386, MAR, 1952, SEP, 27, 1951, RTOM)),
])
# fmt: on
check_story_submission_order(UNCLE_SCROOGE_LONG_STORIES)

# fmt: off
COMICS_AND_STORIES = collections.OrderedDict([
        ('Managing the Echo System', ComicBookInfo(CS, 105, JUN, 1949, JAN, 13, 1949, RTOM)),
        ('Plenty of Pets', ComicBookInfo(CS, 106, JUL, 1949, JAN, 27, 1949, RTOM)),
])
# fmt: on
check_story_submission_order(COMICS_AND_STORIES)
