import collections
import logging
from dataclasses import dataclass
from typing import Dict, OrderedDict

from .comics_info import ComicBookInfo, get_all_comic_book_info, CS, DD, US

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
class FantaComicBookInfo:
    comic_book_info: ComicBookInfo
    colorist: str
    series_name: str = ""
    fantagraphics_volume: str = ""
    number_in_series: int = -1
    fanta_chronological_number: int = -1

    def get_issue_title(self):
        return self.comic_book_info.get_issue_title()


FantaComicBookInfoDict = OrderedDict[str, FantaComicBookInfo]


def get_all_fanta_comic_book_info() -> FantaComicBookInfoDict:
    current_number_in_series = SERIES_INFO_START_NUMBERS.copy()
    all_fanta_info: FantaComicBookInfoDict = collections.OrderedDict()

    all_info = get_all_comic_book_info()
    fanta_chronological_number = 1
    for title in all_info:
        if title not in SERIES_INFO:
            logging.debug(f'Title "{title}" not in SERIES_INFO.')
            continue

        colorist = SERIES_INFO[title].colorist
        series_name = SERIES_INFO[title].series_name
        fantagraphics_volume = SERIES_INFO[title].fanta_volume

        comic_book_info = FantaComicBookInfo(
            all_info[title],
            colorist=colorist,
            series_name=series_name,
            fantagraphics_volume=fantagraphics_volume,
            number_in_series=current_number_in_series[series_name],
            fanta_chronological_number = fanta_chronological_number,
        )

        all_fanta_info[title] = comic_book_info

        current_number_in_series[series_name] += 1
        fanta_chronological_number += 1

    return all_fanta_info


def get_fanta_volume_str(volume: int) -> str:
    return f"FANTA_{volume:02}"


@dataclass
class FantaBook:
    title: str
    pub: str
    volume: int
    year: int
    num_pages: int


FAN = "Fantagraphics"
CB = "Carl Barks"

SRC_SALEM = "(Salem-Empire)"
SRC_DIGI = "(Digital-Empire)"
SRC_BEAN = "(Bean-Empire)"

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
VOLUME_18 = f"{CB} Vol. 18 - {DD} - The Lost Peg Leg Mine {SRC_DIGI}"
VOLUME_19 = f"{CB} Vol. 19 - {DD} - The Black Pearls of Tabu Yama {SRC_BEAN}"
VOLUME_20 = f"{CB} Vol. 20 - {US} - The Mines of King Solomon {SRC_BEAN}"
VOLUME_21 = f"{CB} Vol. 21 - {DD} - Christmas in Duckburg {SRC_BEAN}"
VOLUME_22 = f"{CB} Vol. 22 - {US} - The Twenty-Four Carat Moon {SRC_BEAN}"
VOLUME_23 = f"{CB} Vol. 23 - {US} - Under the Polar Ice {SRC_BEAN}"
VOLUME_24 = f"{CB} Vol. 24 - {US} - Island in the Sky"
VOLUME_25 = f"{CB} Vol. 25 - {US} - Balloonatics {SRC_SALEM}"
VOLUME_26 = f"{CB} Vol. 26 - {US} - The Golden Nugget Boat {SRC_SALEM}"
VOLUME_27 = f"{CB} Vol. 27 - {US} - Duck Luck {SRC_SALEM}"
VOLUME_28 = f"{CB} Vol. 28 - {US} - Cave of Ali Baba {SRC_SALEM}"
FANTA_SOURCE_COMICS = {
    f"{get_fanta_volume_str(1)}": FantaBook(VOLUME_01, FAN, 1, 2025, 0),
    f"{get_fanta_volume_str(2)}": FantaBook(VOLUME_02, FAN, 2, 2024, 245),
    f"{get_fanta_volume_str(3)}": FantaBook(VOLUME_03, FAN, 3, 2024, 248),
    f"{get_fanta_volume_str(4)}": FantaBook(VOLUME_04, FAN, 4, 2023, 225),
    f"{get_fanta_volume_str(5)}": FantaBook(VOLUME_05, FAN, 5, 2013, 216),
    f"{get_fanta_volume_str(6)}": FantaBook(VOLUME_06, FAN, 6, 2013, 232),
    f"{get_fanta_volume_str(7)}": FantaBook(VOLUME_07, FAN, 7, 2011, 239),
    f"{get_fanta_volume_str(8)}": FantaBook(VOLUME_08, FAN, 8, 2014, 223),
    f"{get_fanta_volume_str(9)}": FantaBook(VOLUME_09, FAN, 9, 2015, 215),
    f"{get_fanta_volume_str(10)}": FantaBook(VOLUME_10, FAN, 10, 2016, 231),
    f"{get_fanta_volume_str(11)}": FantaBook(VOLUME_11, FAN, 11, 2012, 240),
    f"{get_fanta_volume_str(12)}": FantaBook(VOLUME_12, FAN, 12, 2012, 248),
    f"{get_fanta_volume_str(13)}": FantaBook(VOLUME_13, FAN, 13, 2015, 227),
    f"{get_fanta_volume_str(14)}": FantaBook(VOLUME_14, FAN, 14, 2014, 240),
    f"{get_fanta_volume_str(15)}": FantaBook(VOLUME_15, FAN, 15, 2016, 248),
    f"{get_fanta_volume_str(16)}": FantaBook(VOLUME_16, FAN, 16, 2017, 234),
    f"{get_fanta_volume_str(17)}": FantaBook(VOLUME_17, FAN, 17, 2017, 201),
    f"{get_fanta_volume_str(18)}": FantaBook(VOLUME_18, FAN, 18, 2018, 202),
    f"{get_fanta_volume_str(19)}": FantaBook(VOLUME_19, FAN, 19, 2018, 201),
    f"{get_fanta_volume_str(20)}": FantaBook(VOLUME_20, FAN, 20, 2019, 209),
    f"{get_fanta_volume_str(21)}": FantaBook(VOLUME_21, FAN, 21, 2019, 201),
    f"{get_fanta_volume_str(22)}": FantaBook(VOLUME_22, FAN, 22, 2020, 201),
    f"{get_fanta_volume_str(23)}": FantaBook(VOLUME_23, FAN, 23, 2020, 201),
    f"{get_fanta_volume_str(24)}": FantaBook(VOLUME_24, FAN, 24, 2021, 211),
    f"{get_fanta_volume_str(25)}": FantaBook(VOLUME_25, FAN, 25, 2021, 211),
    f"{get_fanta_volume_str(26)}": FantaBook(VOLUME_26, FAN, 26, 2022, 209),
    f"{get_fanta_volume_str(27)}": FantaBook(VOLUME_27, FAN, 27, 2022, 203),
    f"{get_fanta_volume_str(28)}": FantaBook(VOLUME_28, FAN, 28, 2023, 209),
}

FIRST_VOLUME_NUMBER = 2
LAST_VOLUME_NUMBER = len(FANTA_SOURCE_COMICS)

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
TOZ = "Tom Ziuko"
EROS = "Erik Rosengarten"


@dataclass
class FantaSeriesInfo:
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
THE_MILKMAN = "The Milkman"
CENSORED_TITLES = [SILENT_NIGHT, THE_MILKMAN]

SILENT_NIGHT_PUBLICATION_ISSUE = "Gemstone's Christmas Parade, No.3, 2005"

SERIES_INFO: Dict[str, FantaSeriesInfo] = {
    # DDA
    "Donald Duck Finds Pirate Gold": FantaSeriesInfo("?", SERIES_DDA, "FANTA_01"),
    "Donald Duck and the Mummy's Ring": FantaSeriesInfo("?", SERIES_DDA, "FANTA_01"),
    "Too Many Pets": FantaSeriesInfo(GLEA, SERIES_DDA, "FANTA_02"),
    "Frozen Gold": FantaSeriesInfo(GLEA, SERIES_DDA, "FANTA_02"),
    "Mystery of the Swamp": FantaSeriesInfo(BIGD, SERIES_DDA, "FANTA_03"),
    "The Firebug": FantaSeriesInfo(DIGI, SERIES_DDA, "FANTA_03"),
    "The Terror of the River!!": FantaSeriesInfo(SLEA, SERIES_DDA, "FANTA_04"),
    "Maharajah Donald": FantaSeriesInfo(GLEA, SERIES_DDA, "FANTA_04"),
    "Volcano Valley": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Adventure Down Under": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "The Ghost of the Grotto": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Christmas on Bear Mountain": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_05"),
    "Darkest Africa": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "The Old Castle's Secret": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "Sheriff of Bullet Valley": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_06"),
    "The Golden Christmas Tree": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Lost in the Andes!": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Race to the South Seas!": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Voodoo Hoodoo": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_07"),
    "Letter to Santa": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Luck of the North": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Trail of the Unicorn": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "Land of the Totem Poles": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_08"),
    "In Ancient Persia": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Vacation Time": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "The Pixilated Parrot": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "The Magic Hourglass": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Big-Top Bedlam": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "You Can't Guess!": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_09"),
    "Dangerous Disguise": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_10"),
    "No Such Varmint": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_10"),
    "In Old California!": FantaSeriesInfo(JRC, SERIES_DDA, "FANTA_10"),
    "A Christmas for Shacktown": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "The Golden Helmet": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "The Gilded Man": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_11"),
    "Trick or Treat": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_13"),
    "Secret of Hondorica": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_17"),
    "Forbidden Valley": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_19"),
    "The Titanic Ants!": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_19"),
    # US
    "Only a Poor Old Man": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "Back to the Klondike": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Horseradish Story": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Menehune Mystery": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Secret of Atlantis": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "Tralla La": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_12"),
    "The Seven Cities of Cibola": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Mysterious Stone Ray": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Lemming with the Locket": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Fabulous Philosopher's Stone": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Great Steamboat Race": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "Riches, Riches, Everywhere!": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "The Golden Fleecing": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_14"),
    "Land Beneath the Ground!": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Lost Crown of Genghis Khan!": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Second-Richest Duck": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "Back to Long Ago!": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "A Cold Bargain": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "Land of the Pygmy Indians": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Fantastic River Race": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_16"),
    "The Black Pearls of Tabu Yama": FantaSeriesInfo(RTOM, SERIES_DDA, "FANTA_19"),
    "The Mines of King Solomon": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_20"),
    "City of Golden Roofs": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_20"),
    "The Money Well": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_20"),
    "The Golden River": FantaSeriesInfo(RTOM, SERIES_USA, "FANTA_20"),
    # WDCS
    "The Victory Garden": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Rabbit's Foot": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Lifeguard Daze": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Good Deeds": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Limber W. Guest Ranch": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "The Mighty Trapper": FantaSeriesInfo("?", SERIES_CS, "FANTA_01"),
    "Good Neighbors": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Salesman Donald": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Snow Fun": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "The Duck in the Iron Pants": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "Kite Weather": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Three Dirty Little Ducks": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_02"),
    "The Mad Chemist": FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_02"),
    "Rival Boatmen": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Camera Crazy": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Farragut the Falcon": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "The Purloined Putty": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "High-wire Daredevils": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_02"),
    "Ten Cents' Worth of Trouble": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Donald's Bay Lot": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "Thievery Afoot": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_02"),
    "The Tramp Steamer": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "The Long Race to Pumpkinburg": FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_03"),
    "Webfooted Wrangler": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "The Icebox Robber": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Pecking Order": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Taming the Rapids": FantaSeriesInfo(BIGD, SERIES_CS, "FANTA_03"),
    "Eyes in the Dark": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Days at the Lazy K": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Thug Busters": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "The Great Ski Race": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Ten-Dollar Dither": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Donald Tames His Temper": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Singapore Joe": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_03"),
    "Master Ice Fisher": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_03"),
    "Jet Rescue": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_03"),
    "Donald's Monster Kite": FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_03"),
    "Biceps Blues": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "The Smugsnorkle Squattie": FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_04"),
    "Swimming Swindlers": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "Playin' Hookey": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "The Gold-Finder": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Turkey Raffle": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_04"),
    "The Bill Collectors": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "The Cantankerous Cat": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Going Buggy": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Jam Robbers": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Picnic Tricks": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_04"),
    "Donald's Posy Patch": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Donald Mines His Own Business": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Magical Misery": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Vacation Misery": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Waltz King": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Masters of Melody": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Fireman Donald": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "The Terrible Turkey": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_05"),
    "Wintertime Wager": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Watching the Watchman": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Wired": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Going Ape": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Spoil the Rod": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Rocket Race to the Moon": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Donald of the Coast Guard": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Gladstone Returns": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Links Hijinks": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Pearls of Wisdom": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "Foxy Relations": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_06"),
    "The Crazy Quiz Show": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Truant Officer Donald": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Donald Duck's Worst Nightmare": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Pizen Spring Dude Ranch": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Rival Beachcombers": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "The Sunken Yacht": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Managing the Echo System": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Plenty of Pets": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_07"),
    "Super Snooper": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "The Great Duckburg Frog-Jumping Contest": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Dowsing Ducks": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "The Goldilocks Gambit": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Donald's Love Letters": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Rip Van Donald": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Serum to Codfish Cove": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_08"),
    "Wild about Flowers": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_09"),
    "Billions to Sneeze At": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Operation St. Bernard": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "A Financial Fable": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The April Foolers": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Knightly Rivals": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Pool Sharks": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Trouble With Dimes": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Gladstone's Luck": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Ten-Star Generals": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Truant Nephews": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "Terror of the Beagle Boys": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_10"),
    "The Big Bin on Killmotor Hill": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gladstone's Usual Very Good Year": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Screaming Cowboy": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Statuesque Spendthrifts": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Rocket Wing Saves the Day": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gladstone's Terrible Secret": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Think Box Bollix": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Houseboat Holiday": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Gemstone Hunters": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "Spending Money": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_11"),
    "The Hypno-Gun": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Omelet": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "A Charitable Chore": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Turkey with All the Schemings": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Flip Decision": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "My Lucky Valentine": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Easter Election": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Talking Dog": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Much Ado about Quackly Hall": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Worm Weary": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Some Heir Over the Rainbow": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Master Rainmaker": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "The Money Stairs": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Bee Bumbles": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_13"),
    "Wispy Willie": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "The Hammy Camel": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Turkey Trot at One Whistle": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Raffle Reversal": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Fix-up Mix-up": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Flour Follies": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "The Price of Fame": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Midgets Madness": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Salmon Derby": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Cheltenham's Choice": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Rants About Ants": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Travelling Truants": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Too Safe Safe": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Search for the Cuspidoria": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "New Year's Revolutions": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Iceboat to Beaver Island": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "The Daffy Taffy Pull": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "The Ghost Sheriff of Last Gasp": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "A Descent Interval": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_15"),
    "Donald's Raucous Role": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "Good Canoes and Bad Canoes": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "The Chickadee Challenge": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "The Unorthodox Ox": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "Trouble Indemnity": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "The Custard Gun": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "Three Un-Ducks": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "Secret Resolutions": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_17"),
    "The Ice Taxis": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "Searching for a Successor": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "The Olympic Hopeful": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "Gopher Goof-Ups": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "In the Swim": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "Camping Confusion": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_17"),
    "The Master": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_18"),
    "A Whale of a Story": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Smoke Writer in the Sky": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "The Runaway Train": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Statues of Limitations": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Borderline Hero": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Fearsome Flowers": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Knight in Shining Armor": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Donald's Pet Service": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "In Kakimaw Country": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Losing Face": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_18"),
    "The Day Duckburg Got Dyed": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_18"),
    "Gyro's Imagination Invention": FantaSeriesInfo(TOZ, SERIES_CS, "FANTA_18"),
    "Red Apple Sap": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Special Delivery": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "The Code of Duckburg": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_18"),
    "Sagmore Springs Hotel": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_19"),
    "The Tenderfoot Trap": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_19"),
    "Rocket Race Around the World": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_19"),
    "Wishing Stone Island": FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_19"),
    "Dodging Miss Daisy": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_19"),
    "The Half-Baked Baker": FantaSeriesInfo(GLEA, SERIES_CS, "FANTA_19"),
    "The Persistent Postman": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_19"),
    "Mocking Bird Ridge": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_19"),
    "Old Froggie Catapult": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_19"),
    "Dramatic Donald": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_21"),
    "Noble Porpoises": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_21"),
    "Tracking Sandy": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "The Littlest Chicken Thief": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "The Beachcombers' Picnic": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "The Master Mover": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "Rocket-Roasted Christmas Turkey": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "Spring Fever": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "The Lovelorn Fireman": FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_21"),
    "The Floating Island": FantaSeriesInfo(DIGI, SERIES_CS, "FANTA_21"),
    "The Black Forest Rescue": FantaSeriesInfo(EROS, SERIES_CS, "FANTA_21"),
    # DD SHORTS
    "The Hard Loser": FantaSeriesInfo(SLEA, SERIES_DDS, "FANTA_02"),
    "Seals Are So Smart!": FantaSeriesInfo(GLEA, SERIES_DDS, "FANTA_04"),
    "The Peaceful Hills": FantaSeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Donald Duck's Best Christmas": FantaSeriesInfo(DIGI, SERIES_DDS, "FANTA_03"),
    "Santa's Stormy Visit": FantaSeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Donald Duck's Atom Bomb": FantaSeriesInfo(SLEA, SERIES_DDS, "FANTA_04"),
    "Three Good Little Ducks": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_05"),
    "Toyland": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_07"),
    "New Toys": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_08"),
    "Hobblin' Goblins": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_13"),
    "Dogcatcher Duck": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_17"),
    "The Lost Peg Leg Mine": FantaSeriesInfo(TOZ, SERIES_DDS, "FANTA_18"),
    "Water Ski Race": FantaSeriesInfo(RTOM, SERIES_DDS, "FANTA_19"),
    # US SHORTS
    "Somethin' Fishy Here": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "The Round Money Bin": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "Million Dollar Pigeon": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Outfoxed Fox": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_12"),
    "A Campaign of Note": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "The Tuckered Tiger": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Heirloom Watch": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_14"),
    "Faulty Fortune": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_16"),
    "Migrating Millions": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_16"),
    "The Colossalest Surprise Quiz Show": FantaSeriesInfo(RTOM, SERIES_USS, "FANTA_16"),
    "September Scrimmage": FantaSeriesInfo(GLEA, SERIES_USS, "FANTA_20"),
    # GG
    "Trapped Lightning": FantaSeriesInfo(TOZ, SERIES_GG, "FANTA_20"),
    "Inventor of Anything": FantaSeriesInfo(RTOM, SERIES_GG, "FANTA_20"),
    "The Cat Box": FantaSeriesInfo(RTOM, SERIES_GG, "FANTA_20"),
    "Grandma's Present": FantaSeriesInfo(GLEA, SERIES_GG, "FANTA_20"),
    "Forecasting Follies": FantaSeriesInfo(RTOM, SERIES_GG, "FANTA_20"),
    "Fishing Mystery": FantaSeriesInfo(RTOM, SERIES_GG, "FANTA_20"),
    "Picnic": FantaSeriesInfo(SLEA, SERIES_GG, "FANTA_20"),
    "The Sure-Fire Gold Finder": FantaSeriesInfo(SLEA, SERIES_GG, "FANTA_20"),
    "Gyro Builds a Better House": FantaSeriesInfo(RTOM, SERIES_GG, "FANTA_20"),
    "August Accident": FantaSeriesInfo(GLEA, SERIES_GG, "FANTA_20"),
    "Roscoe the Robot": FantaSeriesInfo(GLEA, SERIES_GG, "FANTA_20"),
    "Getting Thor": FantaSeriesInfo(SLEA, SERIES_GG, "FANTA_20"),
    "The Know-It-All Machine": FantaSeriesInfo(SLEA, SERIES_GG, "FANTA_20"),
    # MISC
    SILENT_NIGHT: FantaSeriesInfo(SLEA, SERIES_CS, "FANTA_03"),
    THE_MILKMAN: FantaSeriesInfo(RTOM, SERIES_CS, "FANTA_19"),
    "The Riddle of the Red Hat": FantaSeriesInfo(GLEA, SERIES_MISC, "FANTA_03"),
    "Donald Duck Tells About Kites": FantaSeriesInfo(RTOM, SERIES_MISC, "FANTA_15"),
    "Christmas in Duckburg": FantaSeriesInfo(RTOM, SERIES_MISC, "FANTA_21"),
    "Jungle Hi-Jinks": FantaSeriesInfo(GLEA, SERIES_MISC, "FANTA_21"),
    "The Flying Farmhand": FantaSeriesInfo(RTOM, SERIES_MISC, "FANTA_21"),
    "A Honey of a Hen": FantaSeriesInfo(DIGI, SERIES_MISC, "FANTA_21"),
    "The Weather Watchers": FantaSeriesInfo(DIGI, SERIES_MISC, "FANTA_21"),
    "The Sheepish Cowboys": FantaSeriesInfo(DIGI, SERIES_MISC, "FANTA_21"),
}
