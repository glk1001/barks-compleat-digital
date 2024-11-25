import os
from typing import List


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]
