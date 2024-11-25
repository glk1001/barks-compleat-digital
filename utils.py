import logging
import os
from pathlib import Path
from typing import List


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def get_all_story_titles(story_titles_dir: str) -> List[str]:
    possible_ini_files = [f for f in os.listdir(story_titles_dir) if f.endswith(".ini")]

    story_titles = []
    for file in possible_ini_files:
        ini_file = os.path.join(story_titles_dir, file)
        if os.path.islink(ini_file):
            logging.debug(f'Skipping ini file symlink in "{ini_file}".')
            continue
        story_title = Path(ini_file).stem
        story_titles.append(story_title)

    return sorted(story_titles)


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]
