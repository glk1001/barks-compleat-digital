from random import randrange
from typing import Tuple, List

from reader_consts_and_types import Color
from reader_utils import probability, get_rand_int


class RandomColorTint:
    R_INDEX = 0
    G_INDEX = 1
    B_INDEX = 2
    A_INDEX = 3

    def __init__(self):
        self.__affected_indexes = [self.R_INDEX, self.G_INDEX, self.B_INDEX]

        self.__red_range = (200, 255)
        self.__green_range = (200, 255)
        self.__blue_range = (200, 255)
        self.__alpha_range = (200, 255)

        self.__non_random_red = 0.1
        self.__non_random_green = 0.1
        self.__non_random_blue = 0.1

        self.__full_color_probability = 50
        self.__monochrome_probability = 100

    def set_affected_indexes(self, indexes: List[int]) -> None:
        self.__affected_indexes = indexes

    def set_red_range(self, r_min: int, r_max: int) -> None:
        self.__red_range = (r_min, r_max)

    def set_green_range(self, r_min: int, r_max: int) -> None:
        self.__green_range = (r_min, r_max)

    def set_blue_range(self, r_min: int, r_max: int) -> None:
        self.__blue_range = (r_min, r_max)

    def set_alpha_range(self, r_min: int, r_max: int) -> None:
        self.__alpha_range = (r_min, r_max)

    def set_full_color_probability(self, value: int) -> None:
        self.__full_color_probability = value

    def __get_non_random_color(self, alpha: float) -> Color:
        return self.__non_random_red, self.__non_random_green, self.__non_random_blue, alpha

    def __get_color_range(self, index: int) -> Tuple[int, int]:
        if index == self.R_INDEX:
            return self.__red_range
        if index == self.G_INDEX:
            return self.__green_range
        if index == self.B_INDEX:
            return self.__blue_range
        assert False

    def get_random_color(self) -> Color:
        if probability(self.__full_color_probability):
            return 1.0, 1.0, 1.0, 1.0

        alpha = get_rand_int(self.__alpha_range) / 255.0

        if probability(self.__monochrome_probability):
            return self.__get_monochrome_color(alpha)

        return self.__get_rgb_color(alpha)

    def __get_rgb_color(self, alpha: float) -> Color:
        rand_color = list(self.__get_non_random_color(alpha))
        for index in self.__affected_indexes:
            rand_color[index] = get_rand_int(self.__get_color_range(index)) / 255.0

        return tuple(rand_color)

    def __get_monochrome_color(self, alpha: float) -> Color:
        rand_color = list(self.__get_non_random_color(alpha))

        rand_index = randrange(self.R_INDEX, self.B_INDEX + 1)
        rand_color[rand_index] = get_rand_int(self.__get_color_range(rand_index)) / 255.0

        return tuple(rand_color)
