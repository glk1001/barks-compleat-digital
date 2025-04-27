from collections import defaultdict
from enum import Enum, auto

from . import barks_titles as bt


class Tags(Enum):
    SQUARE_EGGS = auto()
    PLAIN_AWFUL = auto()
    SOUTH_AMERICA = auto()
    ANDES = auto()
    FIRE = auto()


BARKS_TAGS = defaultdict(list)

BARKS_TAGS[bt.LOST_IN_THE_ANDES].append((Tags.SQUARE_EGGS, []))
BARKS_TAGS[bt.LOST_IN_THE_ANDES].append((Tags.PLAIN_AWFUL, []))
BARKS_TAGS[bt.LOST_IN_THE_ANDES].append((Tags.ANDES, []))

BARKS_TAGS[bt.FIREBUG_THE].append((Tags.FIRE, []))
