from dataclasses import dataclass
import collections


@dataclass
class SourceBook:
    title: str
    pub: str
    year: int
    colorist: str


FAN = "Fantagraphics"
RTOM = 'Rich Tommaso'
CB = 'Carl Barks'
DD = 'Donald Duck'
US = 'Uncle Scrooge'

SOURCE_COMICS = {
        'FANTA_05': SourceBook(f"{CB} Vol. 5 - {DD} - Christmas on Bear Mountain (Digital-Empire)", FAN, 2013, RTOM),
        'FANTA_06': SourceBook(f"{CB} Vol. 6 - {DD} - The Old Castle's Secret (Digital-Empire)", FAN, 2013, RTOM),
        'FANTA_07': SourceBook(f"{CB} Vol. 7 - {DD} - Lost in the Andes (Digital-Empire)", FAN, 2011, RTOM),
        'FANTA_08': SourceBook(f"{CB} Vol. 8 - {DD} - Trail of the Unicorn (Digital-Empire)", FAN, 2014, RTOM),
        'FANTA_09': SourceBook(f"{CB} Vol. 9 - {DD} - The Pixilated Parrot (Digital-Empire)", FAN, 2015, RTOM),
        'FANTA_10': SourceBook(f"{CB} Vol. 10 - {DD} - Terror of the Beagle Boys (Digital-Empire)", FAN, 2016, RTOM),
        'FANTA_11': SourceBook(f"{CB} Vol. 11 - {DD} - A Christmas for Shacktown (Digital-Empire)", FAN, 2012, RTOM),
        'FANTA_12': SourceBook(f"{CB} Vol. 12 - {US} - Only a Poor Old Man(Digital - Empire)", FAN, 2012, RTOM),
        'FANTA_13': SourceBook(f"{CB} Vol. 13 - {DD} - Trick or Treat (Digital-Empire)", FAN, 2015, RTOM),
        'FANTA_14': SourceBook(f"{CB} Vol. 14 - {US} - The Seven Cities of Gold (Digital-Empire)", FAN, 2014, RTOM),
        'FANTA_15': SourceBook(f"{CB} Vol. 15 - {DD} - The Ghost Sheriff of Last Gasp (Digital-Empire)", FAN, 2016,
                               RTOM),
        'FANTA_16': SourceBook(f"{CB} Vol. 16 - {US} - The Lost Crown of Genghis Khan (Digital-Empire)", FAN, 2017,
                               RTOM),
        'FANTA_17': SourceBook(f"{CB} Vol. 17 - {DD} - The Secret of Hondorica (Digital-Empire)", FAN, 2017, RTOM),
        'FANTA_18': SourceBook(f"{CB} Vol. 18 - {DD} - The Lost Peg Leg Mine (Digital-Empire)", FAN, 2018, RTOM),
        'FANTA_19': SourceBook(f"{CB} Vol. 19 - {DD} - The Black Pearls of Tabu Yama (Bean-Empire)", FAN, 2018, RTOM),
        'FANTA_20': SourceBook(f"{CB} Vol. 20 - {US} - The Mines of King Solomon (Bean-Empire)", FAN, 2019, RTOM),
}


@dataclass
class ComicBookInfo:
    first_published: str
    first_submitted: str
    grouping: str


FC = 'Four Color'
CP = 'Christmas Parade'
MC = "Boys' and Girls' March of Comics"

DDA = "Donald Duck Adventures"

DONALD_DUCK_ADVENTURES_START_NUM = 14
DONALD_DUCK_ADVENTURES = collections.OrderedDict([
        ('Adventure "Down Under"', ComicBookInfo(f'{FC} #159, August 1947', 'April 4th, 1947', DDA)),
        ('The Ghost of the Grotto', ComicBookInfo(f'{FC} #159, August 1947', 'April 15th, 1947', DDA)),
        ('Christmas on Bear Mountain', ComicBookInfo(f'{FC} #178, December 1947', 'July 22nd, 1947', DDA)),
        ('The Old Castle\'s Secret', ComicBookInfo(f'{FC} #189, June 1948', 'December 3rd, 1947', DDA)),
        ('Sheriff of Bullet Valley', ComicBookInfo(f'{FC} #199, October 1948', 'March 16th, 1948', DDA)),
        ('The Golden Christmas Tree', ComicBookInfo(f'{FC} #203, December 1948', 'June 30th, 1948', DDA)),
        ('Darkest Africa', ComicBookInfo(f'{MC} #20, 1948', 'September 26th, 1948', DDA)),
        ('Lost in the Andes', ComicBookInfo(f'{FC} #223, April 1949', 'October 21st, 1948', DDA)),
        ('Race to the South Seas', ComicBookInfo(f'{MC} #41, 1949', 'December 15th, 1948', DDA)),
        ('Voodoo Hoodoo', ComicBookInfo(f'{FC} #238, August 1949', 'March 3rd, 1949', DDA)),
        ('Letter to Santa', ComicBookInfo(f'{CP} #1, November 1949', 'June 1st, 1949', DDA)),
        ('Luck of the North', ComicBookInfo(f'{FC} #256, December 1949', 'June 29th, 1949', DDA)),
        ('Trail of the Unicorn', ComicBookInfo(f'{FC} #263, February 1950', 'September 8th, 1949', DDA)),
])
