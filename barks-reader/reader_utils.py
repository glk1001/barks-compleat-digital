from random import randrange
from typing import Tuple


def probability(percent: int) -> bool:
    return randrange(1, 101) < percent


def get_rand_int(min_max: Tuple[int,int]) -> int:
    return randrange(min_max[0], min_max[1])
