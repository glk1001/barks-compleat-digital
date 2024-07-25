import logging
import os
from typing import List


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def get_ini_files(cfg_dir: str) -> List[str]:
    possible_ini_files = [f for f in os.listdir(cfg_dir) if f.endswith(".ini")]

    ini_files = []
    for file in possible_ini_files:
        ini_file = os.path.join(cfg_dir, file)
        if os.path.islink(ini_file):
            logging.debug(f'Skipping ini file symlink in "{ini_file}".')
            continue
        ini_files.append(ini_file)

    return sorted(ini_files)


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]
