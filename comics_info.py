import collections
from dataclasses import dataclass
from typing import OrderedDict, Tuple


@dataclass
class ComicBookInfo:
    first_published: str
    first_submitted: str
    colorist: str
    series_name: str = ""
    number_in_series: int = -1


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
CB = 'Carl Barks'
DD = 'Donald Duck'
US = 'Uncle Scrooge'

SOURCE_COMICS = {
        'FANTA_04': SourceBook(f"{CB} Vol. 4 - {DD} - Maharajah Donald (Lil Salem-Empire)", FAN, 2023),
        'FANTA_05': SourceBook(f"{CB} Vol. 5 - {DD} - Christmas on Bear Mountain (Digital-Empire)", FAN, 2013),
        'FANTA_06': SourceBook(f"{CB} Vol. 6 - {DD} - The Old Castle's Secret (Digital-Empire)", FAN, 2013),
        'FANTA_07': SourceBook(f"{CB} Vol. 7 - {DD} - Lost in the Andes (Digital-Empire)", FAN, 2011),
        'FANTA_08': SourceBook(f"{CB} Vol. 8 - {DD} - Trail of the Unicorn (Digital-Empire)", FAN, 2014),
        'FANTA_09': SourceBook(f"{CB} Vol. 9 - {DD} - The Pixilated Parrot (Digital-Empire)", FAN, 2015),
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


CS = "Comics and Stories"
FC = "Four Color"
CP = "Christmas Parade"
MC = "Boys' and Girls' March of Comics"
VP = "Vacation Parade"

SERIES_DDA = "Donald Duck Adventures"
SERIES_US = US
SERIES_CS = CS

RTOM = 'Rich Tommaso'
GLEA = 'Gary Leach'
SLEA = 'Susan Daigle-Leach'

DONALD_DUCK_LONG_STORIES = collections.OrderedDict([
        ('Donald Duck Finds Pirate Gold', ComicBookInfo(f'{FC} #9, September 1942', '', '?')),
        ('The Mummy\'s Ring', ComicBookInfo(f'{FC} #29, September 1943', 'May 10th, 1943', '?')),
        ('The Hard Loser', ComicBookInfo(f'{FC} #29, September 1943', 'May 10th, 1943', '?')),
        ('Too Many Pets', ComicBookInfo(f'{FC} #29, September 1943', 'May 29th, 1943', '?')),
        ('Frozen Gold', ComicBookInfo(f'{FC} #62, January 1945', 'August 9th, 1944', '?')),
        ('The Mystery of the Swamp', ComicBookInfo(f'{FC} #62, January 1945', 'September 23rd, 1944', '?')),
        ('The Firebug', ComicBookInfo(f'{FC} #108, May 1946', 'July 19th, 1945', '?')),
        ('The Terror of the River!!', ComicBookInfo(f'{FC} #108, May 1946', 'January 25th, 1946', SLEA)),
        ('Seals Are So Smart!', ComicBookInfo(f'{FC} #108, May 1946', 'January 25th, 1946', GLEA)),
        ('Maharajah Donald', ComicBookInfo(f'{MC} #4, May 1947', 'August 13th, 1946', GLEA)),
        ('Volcano Valley', ComicBookInfo(f'{FC} #159, May 1947', 'December 9th, 1946', RTOM)),
        ('Adventure "Down Under"', ComicBookInfo(f'{FC} #159, August 1947', 'April 4th, 1947', RTOM)),
        ('The Ghost of the Grotto', ComicBookInfo(f'{FC} #159, August 1947', 'April 15th, 1947', RTOM)),
        ('Christmas on Bear Mountain', ComicBookInfo(f'{FC} #178, December 1947', 'July 22nd, 1947', RTOM)),
        ('Darkest Africa', ComicBookInfo(f'{MC} #20, April 1948', 'September 26th, 1947', RTOM)),
        ('The Old Castle\'s Secret', ComicBookInfo(f'{FC} #189, June 1948', 'December 3rd, 1947', RTOM)),
        ('Sheriff of Bullet Valley', ComicBookInfo(f'{FC} #199, October 1948', 'March 16th, 1948', RTOM)),
        ('The Golden Christmas Tree', ComicBookInfo(f'{FC} #203, December 1948', 'June 30th, 1948', RTOM)),
        ('Lost in the Andes', ComicBookInfo(f'{FC} #223, April 1949', 'October 21st, 1948', RTOM)),
        ('Race to the South Seas', ComicBookInfo(f'{MC} #41, February 1949', 'December 15th, 1948', RTOM)),
        ('Voodoo Hoodoo', ComicBookInfo(f'{FC} #238, August 1949', 'March 3rd, 1949', RTOM)),
        ('Letter to Santa', ComicBookInfo(f'{CP} #1, November 1949', 'June 1st, 1949', RTOM)),
        ('Luck of the North', ComicBookInfo(f'{FC} #256, December 1949', 'June 29th, 1949', RTOM)),
        ('Trail of the Unicorn', ComicBookInfo(f'{FC} #263, February 1950', 'September 8th, 1949', RTOM)),
        ('Land of the Totem Poles', ComicBookInfo(f'{FC} #263, February 1950', 'September 29th, 1949', RTOM)),
        ('In Ancient Persia', ComicBookInfo(f'{FC} #275, May 1950', 'November 23rd, 1949', RTOM)),
        ('Vacation Time', ComicBookInfo(f'{VP} #1, July 1950', 'January 5th, 1950', RTOM)),
        ('The Pixilated Parrot', ComicBookInfo(f'{FC} #282, July 1950', 'February 23rd, 1950', RTOM)),
        ('The Magic Hourglass', ComicBookInfo(f'{FC} #291, September 1950', 'March 16th, 1950', RTOM)),
        ('Big-top Bedlam', ComicBookInfo(f'{FC} #300, November 1950', 'April 20th, 1950', RTOM)),
])

UNCLE_SCROOGE_LONG_STORIES = collections.OrderedDict([
        ('Only a Poor Old Man', ComicBookInfo(f'{FC} #386, March 1952', 'September 27th, 1951', RTOM)),
])

COMICS_AND_STORIES = collections.OrderedDict([
        ('Managing the Echo System', ComicBookInfo(f'{CS} #105, June 1949', 'January 13th, 1949', RTOM)),
        ('Plenty of Pets', ComicBookInfo(f'{CS} #106, July 1949', 'January 27th, 1949', RTOM)),
])
