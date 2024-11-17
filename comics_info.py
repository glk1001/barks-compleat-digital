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
    chronological_number: int = -1


ComicBookInfoDict = OrderedDict[str, ComicBookInfo]


def get_all_comic_book_info(stories_filename: str) -> ComicBookInfoDict:
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
    subdir: str
    srce_file_ext: str


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

FAN_DIR1 = "Fantagraphics"
FAN_DIR2 = "Fantagraphics-restored"

PNG_FILE_EXT = ".png"
JPG_FILE_EXT = ".jpg"

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
    "FANTA_01": SourceBook(VOLUME_01, FAN, 1, 2025, FAN_DIR2, PNG_FILE_EXT),
    "FANTA_02": SourceBook(VOLUME_02, FAN, 2, 2024, FAN_DIR2, PNG_FILE_EXT),
    "FANTA_03": SourceBook(VOLUME_03, FAN, 3, 2024, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_04": SourceBook(VOLUME_04, FAN, 4, 2023, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_05": SourceBook(VOLUME_05, FAN, 5, 2013, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_06": SourceBook(VOLUME_06, FAN, 6, 2013, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_07": SourceBook(VOLUME_07, FAN, 7, 2011, FAN_DIR2, PNG_FILE_EXT),
    "FANTA_08": SourceBook(VOLUME_08, FAN, 8, 2014, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_09": SourceBook(VOLUME_09, FAN, 9, 2015, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_10": SourceBook(VOLUME_10, FAN, 10, 2016, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_11": SourceBook(VOLUME_11, FAN, 11, 2012, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_12": SourceBook(VOLUME_12, FAN, 12, 2012, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_13": SourceBook(VOLUME_13, FAN, 13, 2015, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_14": SourceBook(VOLUME_14, FAN, 14, 2014, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_15": SourceBook(VOLUME_15, FAN, 15, 2016, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_16": SourceBook(VOLUME_16, FAN, 16, 2017, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_17": SourceBook(VOLUME_17, FAN, 17, 2017, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_18": SourceBook(VOLUME_18, FAN, 18, 2018, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_19": SourceBook(VOLUME_19, FAN, 19, 2018, FAN_DIR1, JPG_FILE_EXT),
    "FANTA_20": SourceBook(VOLUME_20, FAN, 20, 2019, FAN_DIR1, JPG_FILE_EXT),
}

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
    "Donald Duck Finds Pirate Gold": SeriesInfo("?", SERIES_DDA),
    "Donald Duck and the Mummy's Ring": SeriesInfo("?", SERIES_DDA),
    "Too Many Pets": SeriesInfo(GLEA, SERIES_DDA),
    "Frozen Gold": SeriesInfo(GLEA, SERIES_DDA),
    "Mystery of the Swamp": SeriesInfo(BIGD, SERIES_DDA),
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
    "In Old California!": SeriesInfo(JRC, SERIES_DDA),
    "A Christmas for Shacktown": SeriesInfo(RTOM, SERIES_DDA),
    "The Golden Helmet": SeriesInfo(RTOM, SERIES_DDA),
    "The Gilded Man": SeriesInfo(RTOM, SERIES_DDA),
    "Trick or Treat": SeriesInfo(RTOM, SERIES_DDA),
    "Secret of Hondorica": SeriesInfo(RTOM, SERIES_DDA),
    "Forbidden Valley": SeriesInfo(RTOM, SERIES_DDA),
    # US
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
    # WDCS
    "The Victory Garden": SeriesInfo("?", SERIES_CS),
    "The Rabbit's Foot": SeriesInfo("?", SERIES_CS),
    "Lifeguard Daze": SeriesInfo("?", SERIES_CS),
    "Good Deeds": SeriesInfo("?", SERIES_CS),
    "The Limber W. Guest Ranch": SeriesInfo("?", SERIES_CS),
    "The Mighty Trapper": SeriesInfo("?", SERIES_CS),
    "Good Neighbors": SeriesInfo(BIGD, SERIES_CS),
    "Salesman Donald": SeriesInfo("?", SERIES_CS),
    "Snow Fun": SeriesInfo("?", SERIES_CS),
    "The Duck in the Iron Pants": SeriesInfo("?", SERIES_CS),
    "Kite Weather": SeriesInfo("?", SERIES_CS),
    "Three Dirty Little Ducks": SeriesInfo("?", SERIES_CS),
    "The Mad Chemist": SeriesInfo("?", SERIES_CS),
    "Rival Boatmen": SeriesInfo("?", SERIES_CS),
    "Camera Crazy": SeriesInfo("?", SERIES_CS),
    "Farragut the Falcon": SeriesInfo("?", SERIES_CS),
    "The Purloined Putty": SeriesInfo("?", SERIES_CS),
    "High-wire Daredevils": SeriesInfo("?", SERIES_CS),
    "Ten Cents' Worth of Trouble": SeriesInfo("?", SERIES_CS),
    "Donald's Bay Lot": SeriesInfo("?", SERIES_CS),
    "Thievery Afoot": SeriesInfo("?", SERIES_CS),
    "The Tramp Steamer": SeriesInfo(GLEA, SERIES_CS),
    "The Long Race to Pumpkinburg": SeriesInfo(SLEA, SERIES_CS),
    "Webfooted Wrangler": SeriesInfo(BIGD, SERIES_CS),
    "The Icebox Robber": SeriesInfo(BIGD, SERIES_CS),
    "Pecking Order": SeriesInfo(BIGD, SERIES_CS),
    "Taming the Rapids": SeriesInfo(BIGD, SERIES_CS),
    "Eyes in the Dark": SeriesInfo(GLEA, SERIES_CS),
    "Days at the Lazy K": SeriesInfo(GLEA, SERIES_CS),
    "Thug Busters": SeriesInfo(GLEA, SERIES_CS),
    "The Great Ski Race": SeriesInfo(GLEA, SERIES_CS),
    "Ten-Dollar Dither": SeriesInfo(GLEA, SERIES_CS),
    "Donald Tames His Temper": SeriesInfo(GLEA, SERIES_CS),
    "Singapore Joe": SeriesInfo(GLEA, SERIES_CS),
    "Master Ice Fisher": SeriesInfo(DIGI, SERIES_CS),
    "Jet Rescue": SeriesInfo(DIGI, SERIES_CS),
    "Donald's Monster Kite": SeriesInfo(SLEA, SERIES_CS),
    "Biceps Blues": SeriesInfo(GLEA, SERIES_CS),
    "The Smugsnorkle Squattie": SeriesInfo(SLEA, SERIES_CS),
    "Swimming Swindlers": SeriesInfo(GLEA, SERIES_CS),
    "Playin' Hookey": SeriesInfo(DIGI, SERIES_CS),
    "The Gold-Finder": SeriesInfo(DIGI, SERIES_CS),
    "Turkey Raffle": SeriesInfo(GLEA, SERIES_CS),
    "The Bill Collectors": SeriesInfo(DIGI, SERIES_CS),
    "The Cantankerous Cat": SeriesInfo(DIGI, SERIES_CS),
    "Going Buggy": SeriesInfo(DIGI, SERIES_CS),
    "Jam Robbers": SeriesInfo(DIGI, SERIES_CS),
    "Picnic Tricks": SeriesInfo(DIGI, SERIES_CS),
    "Donald's Posy Patch": SeriesInfo(RTOM, SERIES_CS),
    "Donald Mines His Own Business": SeriesInfo(RTOM, SERIES_CS),
    "Magical Misery": SeriesInfo(RTOM, SERIES_CS),
    "Vacation Misery": SeriesInfo(RTOM, SERIES_CS),
    "The Waltz King": SeriesInfo(RTOM, SERIES_CS),
    "The Masters of Melody": SeriesInfo(RTOM, SERIES_CS),
    "Fireman Donald": SeriesInfo(RTOM, SERIES_CS),
    "The Terrible Turkey": SeriesInfo(RTOM, SERIES_CS),
    "Wintertime Wager": SeriesInfo(RTOM, SERIES_CS),
    "Watching the Watchman": SeriesInfo(RTOM, SERIES_CS),
    "Wired": SeriesInfo(RTOM, SERIES_CS),
    "Going Ape": SeriesInfo(RTOM, SERIES_CS),
    "Spoil the Rod": SeriesInfo(RTOM, SERIES_CS),
    "Rocket Race to the Moon": SeriesInfo(RTOM, SERIES_CS),
    "Donald of the Coast Guard": SeriesInfo(RTOM, SERIES_CS),
    "Gladstone Returns": SeriesInfo(RTOM, SERIES_CS),
    "Links Hijinks": SeriesInfo(RTOM, SERIES_CS),
    "Pearls of Wisdom": SeriesInfo(RTOM, SERIES_CS),
    "Foxy Relations": SeriesInfo(RTOM, SERIES_CS),
    "The Crazy Quiz Show": SeriesInfo(RTOM, SERIES_CS),
    "Truant Officer Donald": SeriesInfo(RTOM, SERIES_CS),
    "Donald Duck's Worst Nightmare": SeriesInfo(RTOM, SERIES_CS),
    "Pizen Spring Dude Ranch": SeriesInfo(RTOM, SERIES_CS),
    "Rival Beachcombers": SeriesInfo(RTOM, SERIES_CS),
    "The Sunken Yacht": SeriesInfo(RTOM, SERIES_CS),
    "Managing the Echo System": SeriesInfo(RTOM, SERIES_CS),
    "Plenty of Pets": SeriesInfo(RTOM, SERIES_CS),
    "Super Snooper": SeriesInfo(RTOM, SERIES_CS),
    "The Great Duckburg Frog-Jumping Contest": SeriesInfo(RTOM, SERIES_CS),
    "Dowsing Ducks": SeriesInfo(RTOM, SERIES_CS),
    "The Goldilocks Gambit": SeriesInfo(RTOM, SERIES_CS),
    "Donald's Love Letters": SeriesInfo(RTOM, SERIES_CS),
    "Rip Van Donald": SeriesInfo(RTOM, SERIES_CS),
    "Serum to Codfish Cove": SeriesInfo(RTOM, SERIES_CS),
    "Wild about Flowers": SeriesInfo(RTOM, SERIES_CS),
    "Billions to Sneeze At": SeriesInfo(RTOM, SERIES_CS),
    "Operation St. Bernard": SeriesInfo(RTOM, SERIES_CS),
    "A Financial Fable": SeriesInfo(RTOM, SERIES_CS),
    "The April Foolers": SeriesInfo(RTOM, SERIES_CS),
    "Knightly Rivals": SeriesInfo(RTOM, SERIES_CS),
    "Pool Sharks": SeriesInfo(RTOM, SERIES_CS),
    "The Trouble With Dimes": SeriesInfo(RTOM, SERIES_CS),
    "Gladstone's Luck": SeriesInfo(RTOM, SERIES_CS),
    "Ten-Star Generals": SeriesInfo(RTOM, SERIES_CS),
    "The Truant Nephews": SeriesInfo(RTOM, SERIES_CS),
    "Terror of the Beagle Boys": SeriesInfo(RTOM, SERIES_CS),
    "The Big Bin on Killmotor Hill": SeriesInfo(RTOM, SERIES_CS),
    "Gladstone's Usual Very Good Year": SeriesInfo(RTOM, SERIES_CS),
    "The Screaming Cowboy": SeriesInfo(RTOM, SERIES_CS),
    "Statuesque Spendthrifts": SeriesInfo(RTOM, SERIES_CS),
    "Rocket Wing Saves the Day": SeriesInfo(RTOM, SERIES_CS),
    "Gladstone's Terrible Secret": SeriesInfo(RTOM, SERIES_CS),
    "The Think Box Bollix": SeriesInfo(RTOM, SERIES_CS),
    "Houseboat Holiday": SeriesInfo(RTOM, SERIES_CS),
    "Gemstone Hunters": SeriesInfo(RTOM, SERIES_CS),
    "Spending Money": SeriesInfo(RTOM, SERIES_CS),
    "The Easter Election": SeriesInfo(RTOM, SERIES_CS),
    "The Talking Dog": SeriesInfo(RTOM, SERIES_CS),
    "Worm Weary": SeriesInfo(RTOM, SERIES_CS),
    "Much Ado about Quackly Hall": SeriesInfo(RTOM, SERIES_CS),
    "Some Heir Over the Rainbow": SeriesInfo(RTOM, SERIES_CS),
    "The Master Rainmaker": SeriesInfo(RTOM, SERIES_CS),
    "The Money Stairs": SeriesInfo(RTOM, SERIES_CS),
    # DD SHORTS
    "The Hard Loser": SeriesInfo(SLEA, SERIES_DDS),
    "The Firebug": SeriesInfo(DIGI, SERIES_DDS),
    "Seals Are So Smart!": SeriesInfo(GLEA, SERIES_DDS),
    "The Peaceful Hills": SeriesInfo(SLEA, SERIES_DDS),
    "Donald Duck's Best Christmas": SeriesInfo(DIGI, SERIES_DDS),
    "Santa's Stormy Visit": SeriesInfo(SLEA, SERIES_DDS),
    "Donald Duck's Atom Bomb": SeriesInfo(SLEA, SERIES_DDS),
    "Three Good Little Ducks": SeriesInfo(RTOM, SERIES_DDS),
    "Toyland": SeriesInfo(RTOM, SERIES_DDS),
    "New Toys": SeriesInfo(RTOM, SERIES_DDS),
    "Hobblin' Goblins": SeriesInfo(RTOM, SERIES_DDS),
    # US SHORTS
    "Somethin' Fishy Here": SeriesInfo(RTOM, SERIES_USS),
    "The Round Money Bin": SeriesInfo(RTOM, SERIES_USS),
    "Billion Dollar Pigeon": SeriesInfo(RTOM, SERIES_USS),
    "Outfoxed Fox": SeriesInfo(RTOM, SERIES_USS),
    "A Campaign of Note": SeriesInfo(RTOM, SERIES_USS),
    "The Tuckered Tiger": SeriesInfo(RTOM, SERIES_USS),
    "Heirloom Watch": SeriesInfo(RTOM, SERIES_USS),
    "Faulty Fortune": SeriesInfo(RTOM, SERIES_USS),
    # GG
    "Trapped Lightning": SeriesInfo(RTOM, SERIES_GG),
    "Inventor of Anything": SeriesInfo(RTOM, SERIES_GG),
    # MISC
    SILENT_NIGHT: SeriesInfo(SLEA, SERIES_CS),
    "The Riddle of the Red Hat": SeriesInfo(GLEA, SERIES_MISC),
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
