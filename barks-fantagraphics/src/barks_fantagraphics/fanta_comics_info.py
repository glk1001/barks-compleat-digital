import collections
import logging
from dataclasses import dataclass
from typing import Dict, OrderedDict

from . import barks_titles as bt
from .barks_titles import ComicBookInfo, get_all_comic_book_info, CS, DD, US


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

    all_comic_book_info = get_all_comic_book_info()
    fanta_chronological_number = 1
    for title in all_comic_book_info:
        if title not in SERIES_INFO:
            logging.debug(f'Title "{title}" not in SERIES_INFO.')
            continue

        colorist = SERIES_INFO[title].colorist
        series_name = SERIES_INFO[title].series_name
        fantagraphics_volume = SERIES_INFO[title].fanta_volume

        fanta_info = FantaComicBookInfo(
            comic_book_info=all_comic_book_info[title],
            colorist=colorist,
            series_name=series_name,
            fantagraphics_volume=fantagraphics_volume,
            number_in_series=current_number_in_series[series_name],
            fanta_chronological_number=fanta_chronological_number,
        )

        all_fanta_info[title] = fanta_info

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

FANTA_01 = "FANTA_01"
FANTA_02 = "FANTA_02"
FANTA_03 = "FANTA_03"
FANTA_04 = "FANTA_04"
FANTA_05 = "FANTA_05"
FANTA_06 = "FANTA_06"
FANTA_07 = "FANTA_07"
FANTA_08 = "FANTA_08"
FANTA_09 = "FANTA_09"
FANTA_10 = "FANTA_10"
FANTA_11 = "FANTA_11"
FANTA_12 = "FANTA_12"
FANTA_13 = "FANTA_13"
FANTA_14 = "FANTA_14"
FANTA_15 = "FANTA_15"
FANTA_16 = "FANTA_16"
FANTA_17 = "FANTA_17"
FANTA_18 = "FANTA_18"
FANTA_19 = "FANTA_19"
FANTA_20 = "FANTA_20"
FANTA_21 = "FANTA_21"

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

CENSORED_TITLES = [bt.SILENT_NIGHT, bt.MILKMAN_THE]
SILENT_NIGHT_PUBLICATION_ISSUE = "Gemstone's Christmas Parade, No.3, 2005"

SERIES_INFO: Dict[str, FantaSeriesInfo] = {
    # DDA
    bt.DONALD_DUCK_FINDS_PIRATE_GOLD: FantaSeriesInfo("?", SERIES_DDA, FANTA_01),
    bt.DONALD_DUCK_AND_THE_MUMMYS_RING: FantaSeriesInfo("?", SERIES_DDA, FANTA_01),
    bt.TOO_MANY_PETS: FantaSeriesInfo(GLEA, SERIES_DDA, FANTA_02),
    bt.FROZEN_GOLD: FantaSeriesInfo(GLEA, SERIES_DDA, FANTA_02),
    bt.MYSTERY_OF_THE_SWAMP: FantaSeriesInfo(BIGD, SERIES_DDA, FANTA_03),
    bt.FIREBUG_THE: FantaSeriesInfo(DIGI, SERIES_DDA, FANTA_03),
    bt.TERROR_OF_THE_RIVER_THE: FantaSeriesInfo(SLEA, SERIES_DDA, FANTA_04),
    bt.MAHARAJAH_DONALD: FantaSeriesInfo(GLEA, SERIES_DDA, FANTA_04),
    bt.VOLCANO_VALLEY: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_05),
    bt.ADVENTURE_DOWN_UNDER: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_05),
    bt.GHOST_OF_THE_GROTTO_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_05),
    bt.CHRISTMAS_ON_BEAR_MOUNTAIN: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_05),
    bt.DARKEST_AFRICA: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_06),
    bt.OLD_CASTLES_SECRET_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_06),
    bt.SHERIFF_OF_BULLET_VALLEY: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_06),
    bt.GOLDEN_CHRISTMAS_TREE_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_07),
    bt.LOST_IN_THE_ANDES: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_07),
    bt.RACE_TO_THE_SOUTH_SEAS: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_07),
    bt.VOODOO_HOODOO: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_07),
    bt.LETTER_TO_SANTA: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_08),
    bt.LUCK_OF_THE_NORTH: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_08),
    bt.TRAIL_OF_THE_UNICORN: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_08),
    bt.LAND_OF_THE_TOTEM_POLES: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_08),
    bt.IN_ANCIENT_PERSIA: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.VACATION_TIME: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.PIXILATED_PARROT_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.MAGIC_HOURGLASS_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.BIG_TOP_BEDLAM: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.YOU_CANT_GUESS: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_09),
    bt.DANGEROUS_DISGUISE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_10),
    bt.NO_SUCH_VARMINT: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_10),
    bt.IN_OLD_CALIFORNIA: FantaSeriesInfo(JRC, SERIES_DDA, FANTA_10),
    bt.CHRISTMAS_FOR_SHACKTOWN_A: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_11),
    bt.GOLDEN_HELMET_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_11),
    bt.GILDED_MAN_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_11),
    bt.TRICK_OR_TREAT: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_13),
    bt.SECRET_OF_HONDORICA: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_17),
    bt.FORBIDDEN_VALLEY: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_19),
    bt.TITANIC_ANTS_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_19),
    # US
    bt.ONLY_A_POOR_OLD_MAN: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.BACK_TO_THE_KLONDIKE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.HORSERADISH_STORY_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.MENEHUNE_MYSTERY_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.SECRET_OF_ATLANTIS_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.TRALLA_LA: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_12),
    bt.SEVEN_CITIES_OF_CIBOLA_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.MYSTERIOUS_STONE_RAY_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.LEMMING_WITH_THE_LOCKET_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.FABULOUS_PHILOSOPHERS_STONE_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.GREAT_STEAMBOAT_RACE_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.RICHES_RICHES_EVERYWHERE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.GOLDEN_FLEECING_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_14),
    bt.LAND_BENEATH_THE_GROUND: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.LOST_CROWN_OF_GENGHIS_KHAN_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.SECOND_RICHEST_DUCK_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.BACK_TO_LONG_AGO: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.COLD_BARGAIN_A: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.LAND_OF_THE_PYGMY_INDIANS: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.FANTASTIC_RIVER_RACE_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_16),
    bt.BLACK_PEARLS_OF_TABU_YAMA_THE: FantaSeriesInfo(RTOM, SERIES_DDA, FANTA_19),
    bt.MINES_OF_KING_SOLOMON_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_20),
    bt.CITY_OF_GOLDEN_ROOFS: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_20),
    bt.MONEY_WELL_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_20),
    bt.GOLDEN_RIVER_THE: FantaSeriesInfo(RTOM, SERIES_USA, FANTA_20),
    # WDCS
    bt.VICTORY_GARDEN_THE: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.RABBITS_FOOT_THE: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.LIFEGUARD_DAZE: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.GOOD_DEEDS: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.LIMBER_W_GUEST_RANCH_THE: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.MIGHTY_TRAPPER_THE: FantaSeriesInfo("?", SERIES_CS, FANTA_01),
    bt.GOOD_NEIGHBORS: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_02),
    bt.SALESMAN_DONALD: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_02),
    bt.SNOW_FUN: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_02),
    bt.DUCK_IN_THE_IRON_PANTS_THE: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_02),
    bt.KITE_WEATHER: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_02),
    bt.THREE_DIRTY_LITTLE_DUCKS: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_02),
    bt.MAD_CHEMIST_THE: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_02),
    bt.RIVAL_BOATMEN: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_02),
    bt.CAMERA_CRAZY: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_02),
    bt.FARRAGUT_THE_FALCON: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_02),
    bt.PURLOINED_PUTTY_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_02),
    bt.HIGH_WIRE_DAREDEVILS: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_02),
    bt.TEN_CENTS_WORTH_OF_TROUBLE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_02),
    bt.DONALDS_BAY_LOT: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_02),
    bt.THIEVERY_AFOOT: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_02),
    bt.TRAMP_STEAMER_THE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.LONG_RACE_TO_PUMPKINBURG_THE: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_03),
    bt.WEBFOOTED_WRANGLER: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_03),
    bt.ICEBOX_ROBBER_THE: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_03),
    bt.PECKING_ORDER: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_03),
    bt.TAMING_THE_RAPIDS: FantaSeriesInfo(BIGD, SERIES_CS, FANTA_03),
    bt.EYES_IN_THE_DARK: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.DAYS_AT_THE_LAZY_K: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.THUG_BUSTERS: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.GREAT_SKI_RACE_THE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.TEN_DOLLAR_DITHER: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.SILENT_NIGHT: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_03),
    bt.DONALD_TAMES_HIS_TEMPER: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.SINGAPORE_JOE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_03),
    bt.MASTER_ICE_FISHER: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_03),
    bt.JET_RESCUE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_03),
    bt.DONALDS_MONSTER_KITE: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_03),
    bt.BICEPS_BLUES: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_04),
    bt.SMUGSNORKLE_SQUATTIE_THE: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_04),
    bt.SWIMMING_SWINDLERS: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_04),
    bt.PLAYIN_HOOKEY: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.GOLD_FINDER_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.TURKEY_RAFFLE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_04),
    bt.BILL_COLLECTORS_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.CANTANKEROUS_CAT_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.GOING_BUGGY: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.JAM_ROBBERS: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.PICNIC_TRICKS: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_04),
    bt.DONALDS_POSY_PATCH: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.DONALD_MINES_HIS_OWN_BUSINESS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.MAGICAL_MISERY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.VACATION_MISERY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.WALTZ_KING_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.MASTERS_OF_MELODY_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.FIREMAN_DONALD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.TERRIBLE_TURKEY_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_05),
    bt.WINTERTIME_WAGER: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.WATCHING_THE_WATCHMAN: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.WIRED: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.GOING_APE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.SPOIL_THE_ROD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.ROCKET_RACE_TO_THE_MOON: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.DONALD_OF_THE_COAST_GUARD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.GLADSTONE_RETURNS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.LINKS_HIJINKS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.PEARLS_OF_WISDOM: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.FOXY_RELATIONS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_06),
    bt.CRAZY_QUIZ_SHOW_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.TRUANT_OFFICER_DONALD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.DONALD_DUCKS_WORST_NIGHTMARE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.PIZEN_SPRING_DUDE_RANCH: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.RIVAL_BEACHCOMBERS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.SUNKEN_YACHT_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.MANAGING_THE_ECHO_SYSTEM: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.PLENTY_OF_PETS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_07),
    bt.SUPER_SNOOPER: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.DOWSING_DUCKS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.GOLDILOCKS_GAMBIT_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.DONALDS_LOVE_LETTERS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.RIP_VAN_DONALD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.SERUM_TO_CODFISH_COVE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_08),
    bt.WILD_ABOUT_FLOWERS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_09),
    bt.BILLIONS_TO_SNEEZE_AT: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.OPERATION_ST_BERNARD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.FINANCIAL_FABLE_A: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.APRIL_FOOLERS_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.KNIGHTLY_RIVALS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.POOL_SHARKS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.TROUBLE_WITH_DIMES_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.GLADSTONES_LUCK: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.TEN_STAR_GENERALS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.TRUANT_NEPHEWS_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.TERROR_OF_THE_BEAGLE_BOYS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_10),
    bt.BIG_BIN_ON_KILLMOTOR_HILL_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.GLADSTONES_USUAL_VERY_GOOD_YEAR: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.SCREAMING_COWBOY_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.STATUESQUE_SPENDTHRIFTS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.ROCKET_WING_SAVES_THE_DAY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.GLADSTONES_TERRIBLE_SECRET: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.THINK_BOX_BOLLIX_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.HOUSEBOAT_HOLIDAY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.GEMSTONE_HUNTERS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.SPENDING_MONEY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_11),
    bt.HYPNO_GUN_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.OMELET: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.CHARITABLE_CHORE_A: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.TURKEY_WITH_ALL_THE_SCHEMINGS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.FLIP_DECISION: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.MY_LUCKY_VALENTINE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.EASTER_ELECTION_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.TALKING_DOG_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.MUCH_ADO_ABOUT_QUACKLY_HALL: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.WORM_WEARY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.SOME_HEIR_OVER_THE_RAINBOW: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.MASTER_RAINMAKER_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.MONEY_STAIRS_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.BEE_BUMBLES: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_13),
    bt.WISPY_WILLIE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.HAMMY_CAMEL_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.TURKEY_TROT_AT_ONE_WHISTLE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.RAFFLE_REVERSAL: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.FIX_UP_MIX_UP: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.FLOUR_FOLLIES: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.PRICE_OF_FAME_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.MIDGETS_MADNESS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.SALMON_DERBY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.CHELTENHAMS_CHOICE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.RANTS_ABOUT_ANTS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.TRAVELLING_TRUANTS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.TOO_SAFE_SAFE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.SEARCH_FOR_THE_CUSPIDORIA: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.NEW_YEARS_REVOLUTIONS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.ICEBOAT_TO_BEAVER_ISLAND: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.DAFFY_TAFFY_PULL_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.GHOST_SHERIFF_OF_LAST_GASP_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.DESCENT_INTERVAL_A: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_15),
    bt.DONALDS_RAUCOUS_ROLE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.GOOD_CANOES_AND_BAD_CANOES: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.CHICKADEE_CHALLENGE_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.UNORTHODOX_OX_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.TROUBLE_INDEMNITY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.CUSTARD_GUN_THE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.THREE_UN_DUCKS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.SECRET_RESOLUTIONS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_17),
    bt.ICE_TAXIS_THE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.SEARCHING_FOR_A_SUCCESSOR: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.OLYMPIC_HOPEFUL_THE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.GOPHER_GOOF_UPS: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.IN_THE_SWIM: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.CAMPING_CONFUSION: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_17),
    bt.MASTER_THE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_18),
    bt.WHALE_OF_A_STORY_A: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.SMOKE_WRITER_IN_THE_SKY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.RUNAWAY_TRAIN_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.STATUES_OF_LIMITATIONS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.BORDERLINE_HERO: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.FEARSOME_FLOWERS: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.KNIGHT_IN_SHINING_ARMOR: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.DONALDS_PET_SERVICE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.IN_KAKIMAW_COUNTRY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.LOSING_FACE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_18),
    bt.DAY_DUCKBURG_GOT_DYED_THE: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_18),
    bt.GYROS_IMAGINATION_INVENTION: FantaSeriesInfo(TOZ, SERIES_CS, FANTA_18),
    bt.RED_APPLE_SAP: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.SPECIAL_DELIVERY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.CODE_OF_DUCKBURG_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_18),
    bt.SAGMORE_SPRINGS_HOTEL: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_19),
    bt.TENDERFOOT_TRAP_THE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_19),
    bt.ROCKET_RACE_AROUND_THE_WORLD: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_19),
    bt.WISHING_STONE_ISLAND: FantaSeriesInfo(SLEA, SERIES_CS, FANTA_19),
    bt.HALF_BAKED_BAKER_THE: FantaSeriesInfo(GLEA, SERIES_CS, FANTA_19),
    bt.DODGING_MISS_DAISY: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_19),
    bt.MILKMAN_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_19),
    bt.PERSISTENT_POSTMAN_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_19),
    bt.MOCKING_BIRD_RIDGE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_19),
    bt.OLD_FROGGIE_CATAPULT: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_19),
    bt.DRAMATIC_DONALD: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_21),
    bt.NOBLE_PORPOISES: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_21),
    bt.TRACKING_SANDY: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.LITTLEST_CHICKEN_THIEF_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.BEACHCOMBERS_PICNIC_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.MASTER_MOVER_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.ROCKET_ROASTED_CHRISTMAS_TURKEY: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.SPRING_FEVER: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.LOVELORN_FIREMAN_THE: FantaSeriesInfo(RTOM, SERIES_CS, FANTA_21),
    bt.FLOATING_ISLAND_THE: FantaSeriesInfo(DIGI, SERIES_CS, FANTA_21),
    bt.BLACK_FOREST_RESCUE_THE: FantaSeriesInfo(EROS, SERIES_CS, FANTA_21),
    # DD SHORTS
    bt.HARD_LOSER_THE: FantaSeriesInfo(SLEA, SERIES_DDS, FANTA_02),
    bt.SEALS_ARE_SO_SMART: FantaSeriesInfo(GLEA, SERIES_DDS, FANTA_04),
    bt.PEACEFUL_HILLS_THE: FantaSeriesInfo(SLEA, SERIES_DDS, FANTA_04),
    bt.DONALD_DUCKS_BEST_CHRISTMAS: FantaSeriesInfo(DIGI, SERIES_DDS, FANTA_03),
    bt.SANTAS_STORMY_VISIT: FantaSeriesInfo(SLEA, SERIES_DDS, FANTA_04),
    bt.DONALD_DUCKS_ATOM_BOMB: FantaSeriesInfo(SLEA, SERIES_DDS, FANTA_04),
    bt.THREE_GOOD_LITTLE_DUCKS: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_05),
    bt.TOYLAND: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_07),
    bt.NEW_TOYS: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_08),
    bt.HOBBLIN_GOBLINS: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_13),
    bt.DOGCATCHER_DUCK: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_17),
    bt.LOST_PEG_LEG_MINE_THE: FantaSeriesInfo(TOZ, SERIES_DDS, FANTA_18),
    bt.WATER_SKI_RACE: FantaSeriesInfo(RTOM, SERIES_DDS, FANTA_19),
    # US SHORTS
    bt.SOMETHIN_FISHY_HERE: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_12),
    bt.ROUND_MONEY_BIN_THE: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_12),
    bt.MILLION_DOLLAR_PIGEON: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_14),
    bt.OUTFOXED_FOX: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_12),
    bt.CAMPAIGN_OF_NOTE_A: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_14),
    bt.TUCKERED_TIGER_THE: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_14),
    bt.HEIRLOOM_WATCH: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_14),
    bt.FAULTY_FORTUNE: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_16),
    bt.MIGRATING_MILLIONS: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_16),
    bt.COLOSSALEST_SURPRISE_QUIZ_SHOW_THE: FantaSeriesInfo(RTOM, SERIES_USS, FANTA_16),
    bt.SEPTEMBER_SCRIMMAGE: FantaSeriesInfo(GLEA, SERIES_USS, FANTA_20),
    # GG
    bt.TRAPPED_LIGHTNING: FantaSeriesInfo(TOZ, SERIES_GG, FANTA_20),
    bt.INVENTOR_OF_ANYTHING: FantaSeriesInfo(RTOM, SERIES_GG, FANTA_20),
    bt.CAT_BOX_THE: FantaSeriesInfo(RTOM, SERIES_GG, FANTA_20),
    bt.GRANDMAS_PRESENT: FantaSeriesInfo(GLEA, SERIES_GG, FANTA_20),
    bt.FORECASTING_FOLLIES: FantaSeriesInfo(RTOM, SERIES_GG, FANTA_20),
    bt.FISHING_MYSTERY: FantaSeriesInfo(RTOM, SERIES_GG, FANTA_20),
    bt.PICNIC: FantaSeriesInfo(SLEA, SERIES_GG, FANTA_20),
    bt.SURE_FIRE_GOLD_FINDER_THE: FantaSeriesInfo(SLEA, SERIES_GG, FANTA_20),
    bt.GYRO_BUILDS_A_BETTER_HOUSE: FantaSeriesInfo(RTOM, SERIES_GG, FANTA_20),
    bt.AUGUST_ACCIDENT: FantaSeriesInfo(GLEA, SERIES_GG, FANTA_20),
    bt.ROSCOE_THE_ROBOT: FantaSeriesInfo(GLEA, SERIES_GG, FANTA_20),
    bt.GETTING_THOR: FantaSeriesInfo(SLEA, SERIES_GG, FANTA_20),
    bt.KNOW_IT_ALL_MACHINE_THE: FantaSeriesInfo(SLEA, SERIES_GG, FANTA_20),
    # MISC
    bt.RIDDLE_OF_THE_RED_HAT_THE: FantaSeriesInfo(GLEA, SERIES_MISC, FANTA_03),
    bt.DONALD_DUCK_TELLS_ABOUT_KITES: FantaSeriesInfo(RTOM, SERIES_MISC, FANTA_15),
    bt.CHRISTMAS_IN_DUCKBURG: FantaSeriesInfo(RTOM, SERIES_MISC, FANTA_21),
    bt.JUNGLE_HI_JINKS: FantaSeriesInfo(GLEA, SERIES_MISC, FANTA_21),
    bt.FLYING_FARMHAND_THE: FantaSeriesInfo(RTOM, SERIES_MISC, FANTA_21),
    bt.HONEY_OF_A_HEN_A: FantaSeriesInfo(DIGI, SERIES_MISC, FANTA_21),
    bt.WEATHER_WATCHERS_THE: FantaSeriesInfo(DIGI, SERIES_MISC, FANTA_21),
    bt.SHEEPISH_COWBOYS_THE: FantaSeriesInfo(DIGI, SERIES_MISC, FANTA_21),
}
