import collections
import csv
import os
from dataclasses import dataclass
from datetime import date
from typing import Dict, OrderedDict

from .comics_consts import PUBLICATION_INFO_SUBDIR, STORIES_INFO_FILENAME

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
    fantagraphics_volume: str = ""
    number_in_series: int = -1
    chronological_number: int = -1

    def get_issue_title(self):
        short_issue_name = SHORT_ISSUE_NAME[self.issue_name]
        return f"{short_issue_name} {self.issue_number}"


ComicBookInfoDict = OrderedDict[str, ComicBookInfo]


def get_all_comic_book_info(story_info_dir: str) -> ComicBookInfoDict:
    stories_filename = os.path.join(story_info_dir, PUBLICATION_INFO_SUBDIR, STORIES_INFO_FILENAME)

    current_number_in_series = SERIES_INFO_START_NUMBERS.copy()
    all_info: ComicBookInfoDict = collections.OrderedDict()

    chronological_number = 1
    with open(stories_filename, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in reader:
            title = row[0]
            if title not in SERIES_INFO:
                continue

            colorist = SERIES_INFO[title].colorist
            series_name = SERIES_INFO[title].series_name
            fantagraphics_volume = SERIES_INFO[title].fanta_volume

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
                fantagraphics_volume,
                current_number_in_series[series_name],
                chronological_number,
            )

            all_info[title] = comic_book_info

            current_number_in_series[series_name] += 1
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


@dataclass
class SourceBook:
    title: str
    pub: str
    volume: int
    year: int
    num_pages: int


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

SRC_SALEM = "(Salem-Empire)"
SRC_DIGI = "(Digital-Empire)"
SRC_BEAN = "(Bean-Empire)"

ISSUE_NAME_AS_TITLE = {
    US: "Uncle\nScrooge",
    FG: "Firestone\nGiveaway",
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
}

FANTAGRAPHICS = "Fantagraphics"
FANTAGRAPHICS_DIRNAME = FANTAGRAPHICS + "-original"
FANTAGRAPHICS_UPSCAYLED_DIRNAME = FANTAGRAPHICS + "-upscayled"
FANTAGRAPHICS_RESTORED_DIRNAME = FANTAGRAPHICS + "-restored"
FANTAGRAPHICS_RESTORED_UPSCAYLED_DIRNAME = FANTAGRAPHICS_RESTORED_DIRNAME + "-upscayled"
FANTAGRAPHICS_RESTORED_SVG_DIRNAME = FANTAGRAPHICS_RESTORED_DIRNAME + "-svg"
FANTAGRAPHICS_RESTORED_OCR_DIRNAME = FANTAGRAPHICS_RESTORED_DIRNAME + "-ocr"
FANTAGRAPHICS_FIXES_DIRNAME = FANTAGRAPHICS + "-fixes-and-additions"
FANTAGRAPHICS_FIXES_SCRAPS_DIRNAME = FANTAGRAPHICS_FIXES_DIRNAME + "-scraps"
FANTAGRAPHICS_UPSCAYLED_FIXES_DIRNAME = FANTAGRAPHICS_UPSCAYLED_DIRNAME + "-fixes-and-additions"
FANTAGRAPHICS_RESTORED_FIXES_DIRNAME = FANTAGRAPHICS_RESTORED_DIRNAME + "-fixes-and-additions"
FANTAGRAPHICS_PANEL_SEGMENTS_DIRNAME = FANTAGRAPHICS_RESTORED_DIRNAME + "-panel-segments"

JPG_FILE_EXT = ".jpg"
PNG_FILE_EXT = ".png"
SVG_FILE_EXT = ".svg"
JSON_FILE_EXT = ".json"
TEXT_FILE_EXT = ".txt"

VOLUME_01 = f"{CB} Vol. 1 - {DD} - Pirate Gold {SRC_SALEM}"
VOLUME_02 = f"{CB} Vol. 2 - {DD} - Frozen Gold {SRC_SALEM}"
VOLUME_03 = f"{CB} Vol. 3 - {DD} - Mystery of the Swamp {SRC_SALEM}"
VOLUME_04 = f"{CB} Vol. 4 - {DD} - Maharajah Donald {SRC_SALEM}"
VOLUME_05 = f"{CB} Vol. 5 - {DD} - Christmas on Bear Mountain {SRC_DIGI}"
VOLUME_06 = f"{CB} Vol. 6 - {DD} - The Old Castle's Secret {SRC_DIGI}"
VOLUME_07 = f"{CB} Vol. 7 - {DD} - Lost in the Andes {SRC_DIGI}"
VOLUME_08 = f"{CB} Vol. 8 - {DD} - Trail of the Unicorn {SRC_DIGI}"
VOLUME_09 = f"{CB} Vol. 9 - {DD} - The Pixilated Parrot {SRC_DIGI}"
VOLUME_10 = f"{CB} Vol. 10 - {DD} - Terror of the Beagle Boys {SRC_DIGI}"
VOLUME_11 = f"{CB} Vol. 11 - {DD} - A Christmas for Shacktown {SRC_DIGI}"
VOLUME_12 = f"{CB} Vol. 12 - {US} - Only a Poor Old Man {SRC_DIGI}"
VOLUME_13 = f"{CB} Vol. 13 - {DD} - Trick or Treat {SRC_DIGI}"
VOLUME_14 = f"{CB} Vol. 14 - {US} - The Seven Cities of Gold {SRC_DIGI}"
VOLUME_15 = f"{CB} Vol. 15 - {DD} - The Ghost Sheriff of Last Gasp {SRC_DIGI}"
VOLUME_16 = f"{CB} Vol. 16 - {US} - The Lost Crown of Genghis Khan {SRC_DIGI}"
VOLUME_17 = f"{CB} Vol. 17 - {DD} - The Secret of Hondorica {SRC_DIGI}"
VOLUME_18 = f"{CB} Vol. 18 - {DD} - The Lost Peg Leg Mine ({SRC_DIGI}"
VOLUME_19 = f"{CB} Vol. 19 - {DD} - The Black Pearls of Tabu Yama {SRC_BEAN}"
VOLUME_20 = f"{CB} Vol. 20 - {US} - The Mines of King Solomon {SRC_BEAN}"
SOURCE_COMICS = {
    "FANTA_01": SourceBook(VOLUME_01, FAN, 1, 2025, 0),
    "FANTA_02": SourceBook(VOLUME_02, FAN, 2, 2024, 245),
    "FANTA_03": SourceBook(VOLUME_03, FAN, 3, 2024, 248),
    "FANTA_04": SourceBook(VOLUME_04, FAN, 4, 2023, 225),
    "FANTA_05": SourceBook(VOLUME_05, FAN, 5, 2013, 216),
    "FANTA_06": SourceBook(VOLUME_06, FAN, 6, 2013, 232),
    "FANTA_07": SourceBook(VOLUME_07, FAN, 7, 2011, 239),
    "FANTA_08": SourceBook(VOLUME_08, FAN, 8, 2014, 223),
    "FANTA_09": SourceBook(VOLUME_09, FAN, 9, 2015, 215),
    "FANTA_10": SourceBook(VOLUME_10, FAN, 10, 2016, 231),
    "FANTA_11": SourceBook(VOLUME_11, FAN, 11, 2012, 240),
    "FANTA_12": SourceBook(VOLUME_12, FAN, 12, 2012, 248),
    "FANTA_13": SourceBook(VOLUME_13, FAN, 13, 2015, 227),
    "FANTA_14": SourceBook(VOLUME_14, FAN, 14, 2014, 240),
    "FANTA_15": SourceBook(VOLUME_15, FAN, 15, 2016, 248),
    "FANTA_16": SourceBook(VOLUME_16, FAN, 16, 2017, 234),
    "FANTA_17": SourceBook(VOLUME_17, FAN, 17, 2017, 201),
    "FANTA_18": SourceBook(VOLUME_18, FAN, 18, 2018, 202),
    "FANTA_19": SourceBook(VOLUME_19, FAN, 19, 2018, 201),
    "FANTA_20": SourceBook(VOLUME_20, FAN, 20, 2019, 209),
}

FIRST_VOLUME_NUMBER = 2
LAST_VOLUME_NUMBER = len(SOURCE_COMICS)

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
BIGD = "Big Doors Studios"
JRC = "Joseph Robert Cowles"


@dataclass
class SeriesInfo:
    colorist: str
    series_name: str
    fanta_volume: str
    number_in_series: int = -1


SERIES_INFO_START_NUMBERS: Dict[str, int] = {
    SERIES_DDA: 1,
    SERIES_USA: 1,
    SERIES_DDS: 1,
    SERIES_USS: 1,
    SERIES_CS: 1,
    SERIES_GG: 1,
    SERIES_MISC: 1,
}

SILENT_NIGHT = "Silent Night"
CENSORED_TITLES = [SILENT_NIGHT]

SILENT_NIGHT_PUBLICATION_ISSUE = "Gemstone's Christmas Parade, No.3, 2005"

SERIES_INFO: Dict[str, SeriesInfo] = {
    # DDA
    "Donald Duck Finds Pirate Gold": SeriesInfo("?", SERIES_DDA, "FANTA_01"),
    "Donald Duck and the Mummy's Ring": SeriesInfo("?", SERIES_DDA, "FANTA_01"),
    "Too Many Pets": SeriesInfo(GLEA, SERIES_DDA, "FANTA_02"),
    "Frozen Gold": SeriesInfo(GLEA, SERIES_DDA, "FANTA_02"),
    "Mystery of the Swamp": SeriesInfo(BIGD, SERIES_DDA, "FANTA_03"),
    "The Terror of the River!!": SeriesInfo(SLEA, SERIES_DDA, "FANTA_04"),
    "Maharajah Donald": SeriesInfo(GLEA, SERIES_DDA, "FANTA_04"),
    "Volcano Valley": SeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Adventure Down Under": SeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "The Ghost of the Grotto": SeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Christmas on Bear Mountain": SeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Darkest Africa": SeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "The Old Castle's Secret": SeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "Sheriff of Bullet Valley": SeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "The Golden Christmas Tree": SeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Lost in the Andes!": SeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Race to the South Seas!": SeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Voodoo Hoodoo": SeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Letter to Santa": SeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Luck of the North": SeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Trail of the Unicorn": SeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Land of the Totem Poles": SeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "In Ancient Persia": SeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Vacation Time": SeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "The Pixilated Parrot": SeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "The Magic Hourglass": SeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Big-Top Bedlam": SeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Dangerous Disguise": SeriesInfo(RTOM, SERIES_DDA, "FANTA_10"),
    "No Such Varmint": SeriesInfo(RTOM, SERIES_DDA, "FANTA_10"),
    "In Old California!": SeriesInfo(JRC, SERIES_DDA, "FANTA_10"),
    "A Christmas for Shacktown": SeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "The Golden Helmet": SeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "The Gilded Man": SeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "Trick or Treat": SeriesInfo(RTOM, SERIES_DDA, "FANTA_13"),
    "Secret of Hondorica": SeriesInfo(RTOM, SERIES_DDA, "FANTA_17"),
    "Forbidden Valley": SeriesInfo(RTOM, SERIES_DDA, "FANTA_19"),
    # US
    "Only a Poor Old Man": SeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "Back to the Klondike": SeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Horseradish Story": SeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Menehune Mystery": SeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Secret of Atlantis": SeriesInfo(RTOM, SERIES_USA, "FANTA_?"),
    "Tralla La": SeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Seven Cities of Cibola": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Mysterious Stone Ray": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Lemming with the Locket": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Fabulous Philosopher's Stone": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Great Steamboat Race": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "Riches, Riches, Everywhere!": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Golden Fleecing": SeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "Land Beneath the Ground!": SeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Lost Crown of Genghis Khan!": SeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Second-Richest Duck": SeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "Back to Long Ago!": SeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "A Cold Bargain": SeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    # WDCS
    "The Victory Garden": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Rabbit's Foot": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Lifeguard Daze": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Good Deeds": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Limber W. Guest Ranch": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Mighty Trapper": SeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Good Neighbors": SeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Salesman Donald": SeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Snow Fun": SeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "The Duck in the Iron Pants": SeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Kite Weather": SeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Three Dirty Little Ducks": SeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "The Mad Chemist": SeriesInfo(SLEA, SERIES_CS, "FANTA_02"),
    "Rival Boatmen": SeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Camera Crazy": SeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Farragut the Falcon": SeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "The Purloined Putty": SeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "High-wire Daredevils": SeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Ten Cents' Worth of Trouble": SeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Donald's Bay Lot": SeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Thievery Afoot": SeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "The Tramp Steamer": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "The Long Race to Pumpkinburg": SeriesInfo(SLEA, SERIES_CS, "FANTA_03"),
    "Webfooted Wrangler": SeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "The Icebox Robber": SeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Pecking Order": SeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Taming the Rapids": SeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Eyes in the Dark": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Days at the Lazy K": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Thug Busters": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "The Great Ski Race": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Ten-Dollar Dither": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Donald Tames His Temper": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Singapore Joe": SeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Master Ice Fisher": SeriesInfo(DIGI, SERIES_CS, "FANTA_03"),
    "Jet Rescue": SeriesInfo(DIGI, SERIES_CS, "FANTA_03"),
    "Donald's Monster Kite": SeriesInfo(SLEA, SERIES_CS, "FANTA_03"),
    "Biceps Blues": SeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "The Smugsnorkle Squattie": SeriesInfo(SLEA, SERIES_CS, "FANTA_04"),
    "Swimming Swindlers": SeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "Playin' Hookey": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "The Gold-Finder": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Turkey Raffle": SeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "The Bill Collectors": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "The Cantankerous Cat": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Going Buggy": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Jam Robbers": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Picnic Tricks": SeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Donald's Posy Patch": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Donald Mines His Own Business": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Magical Misery": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Vacation Misery": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Waltz King": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Masters of Melody": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Fireman Donald": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Terrible Turkey": SeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Wintertime Wager": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Watching the Watchman": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Wired": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Going Ape": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Spoil the Rod": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Rocket Race to the Moon": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Donald of the Coast Guard": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Gladstone Returns": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Links Hijinks": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Pearls of Wisdom": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Foxy Relations": SeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "The Crazy Quiz Show": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Truant Officer Donald": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Donald Duck's Worst Nightmare": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Pizen Spring Dude Ranch": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Rival Beachcombers": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "The Sunken Yacht": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Managing the Echo System": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Plenty of Pets": SeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Super Snooper": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "The Great Duckburg Frog-Jumping Contest": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Dowsing Ducks": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "The Goldilocks Gambit": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Donald's Love Letters": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Rip Van Donald": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Serum to Codfish Cove": SeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Wild about Flowers": SeriesInfo(RTOM, SERIES_CS, "FANTA_09"),
    "Billions to Sneeze At": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Operation St. Bernard": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "A Financial Fable": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The April Foolers": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Knightly Rivals": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Pool Sharks": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Trouble With Dimes": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Gladstone's Luck": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Ten-Star Generals": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Truant Nephews": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Terror of the Beagle Boys": SeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Big Bin on Killmotor Hill": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gladstone's Usual Very Good Year": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Screaming Cowboy": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Statuesque Spendthrifts": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Rocket Wing Saves the Day": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gladstone's Terrible Secret": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Think Box Bollix": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Houseboat Holiday": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gemstone Hunters": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Spending Money": SeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Easter Election": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Talking Dog": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Worm Weary": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Much Ado about Quackly Hall": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Some Heir Over the Rainbow": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Master Rainmaker": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Money Stairs": SeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    # DD SHORTS
    "The Hard Loser": SeriesInfo(SLEA, SERIES_DDS, "FANTA_02"),
    "The Firebug": SeriesInfo(DIGI, SERIES_DDS, "FANTA_03"),
    "Seals Are So Smart!": SeriesInfo(GLEA, SERIES_DDS, "FANTA_04"),
    "The Peaceful Hills": SeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Donald Duck's Best Christmas": SeriesInfo(DIGI, SERIES_DDS, "FANTA_03"),
    "Santa's Stormy Visit": SeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Donald Duck's Atom Bomb": SeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Three Good Little Ducks": SeriesInfo(RTOM, SERIES_DDS, "FANTA_05"),
    "Toyland": SeriesInfo(RTOM, SERIES_DDS, "FANTA_07"),
    "New Toys": SeriesInfo(RTOM, SERIES_DDS, "FANTA_08"),
    "Hobblin' Goblins": SeriesInfo(RTOM, SERIES_DDS, "FANTA_13"),
    # US SHORTS
    "Somethin' Fishy Here": SeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "The Round Money Bin": SeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "Billion Dollar Pigeon": SeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Outfoxed Fox": SeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "A Campaign of Note": SeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "The Tuckered Tiger": SeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Heirloom Watch": SeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Faulty Fortune": SeriesInfo(RTOM, SERIES_USS, "FANTA_16"),
    # GG
    "Trapped Lightning": SeriesInfo(RTOM, SERIES_GG, "FANTA_?"),
    "Inventor of Anything": SeriesInfo(RTOM, SERIES_GG, "FANTA_?"),
    # MISC
    SILENT_NIGHT: SeriesInfo(SLEA, SERIES_CS, "FANTA_?"),
    "The Riddle of the Red Hat": SeriesInfo(GLEA, SERIES_MISC, "FANTA_03"),
}


def get_formatted_day(day: int) -> str:
    if day == 1 or day == 31:
        day_str = str(day) + "st"
    elif day == 2 or day == 22:
        day_str = str(day) + "nd"
    elif day == 3 or day == 23:
        day_str = str(day) + "rd"
    else:
        day_str = str(day) + "th"

    return day_str
