from enum import IntEnum, auto


class Issues(IntEnum):
    CH = 0
    CID = auto()
    CP = auto()
    CS = auto()
    DD = auto()
    DIBP = auto()
    FC = auto()
    FG = auto()
    KI = auto()
    MC = auto()
    MMA = auto()
    SF = auto()
    US = auto()
    USGTD = auto()
    VP = auto()
    EXTRAS = auto()


SHORT_ISSUE_NAME = [
    "CG",
    "CID",
    "CP",
    "WDCS",
    "DD",
    "DIBP",
    "FC",
    "FG",
    "KG",
    "MOC",
    "MMA",
    "SF",
    "US",
    "USGTD",
    "VP",
    "EX",
]

ISSUE_NAME = [
    "Cheerios Giveaway",
    "Christmas in Disneyland",
    "Christmas Parade",
    "Comics and Stories",
    "Donald Duck",
    "Disneyland Birthday Party",
    "Four Color",
    "Firestone Giveaway",
    "Kites Giveaway",
    "Boys' and Girls' March of Comics",
    "Mickey Mouse Almanac",
    "Summer Fun",
    "Uncle Scrooge",
    "Uncle Scrooge Goes to Disneyland",
    "Vacation Parade",
    "Extras (Non-Barks)",
]

ISSUE_NAME_WRAPPED = {
    Issues.US: "Uncle\nScrooge",
    Issues.FG: "Firestone\nGiveaway",
    Issues.USGTD: "Uncle Scrooge\nGoes to\nDisneyland",
    Issues.CID: "Christmas\nin\nDisneyland",
}
