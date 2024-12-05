import logging
import os
from typing import List

from barks_fantagraphics.comics_utils import (
    get_timestamp_str,
    get_timestamp_as_str,
    dest_file_is_older_than_srce,
    file_is_older_than_timestamp,
)


def get_shorter_ini_filename(ini_file: str) -> str:
    return os.path.basename(ini_file)


def get_list_of_numbers(list_str: str) -> List[int]:
    if not list_str:
        return list()
    if "-" not in list_str:
        return [int(list_str)]

    p_start, p_end = list_str.split("-")
    return [n for n in range(int(p_start), int(p_end) + 1)]


def dest_file_is_out_of_date_wrt_srce(srce_file: str, dest_file: str) -> bool:
    if not os.path.isfile(dest_file):
        logging.debug(f'Dest file "{dest_file}" not found.')
        return False

    if dest_file_is_older_than_srce(srce_file, dest_file, False):
        logging.debug(get_dest_file_out_of_date_wrt_to_src_msg(srce_file, dest_file))
        return True

    return False


def zip_file_is_out_of_date_wrt_dest(zip_file: str, max_dest_timestamp: float) -> bool:
    if not os.path.isfile(zip_file):
        logging.debug(f'Dest zip file "{zip_file}" not found.')
        return False

    if file_is_older_than_timestamp(zip_file, max_dest_timestamp):
        logging.debug(get_zip_file_out_of_date_wrt_max_dest_msg(zip_file, max_dest_timestamp))
        return True

    return False


def symlink_is_out_of_date_wrt_dest(symlink: str, max_dest_timestamp: float) -> bool:
    if file_is_older_than_timestamp(symlink, max_dest_timestamp):
        logging.debug(get_symlink_out_of_date_wrt_max_dest_msg(symlink, max_dest_timestamp))
        return True

    return False


def symlink_is_out_of_date_wrt_zip(symlink: str, zip_file: str) -> bool:
    if not os.path.islink(symlink):
        logging.debug(f'Dest file "{symlink}" not found.')
        return False

    if dest_file_is_older_than_srce(symlink, zip_file, False):
        logging.debug(get_symlink_out_of_date_wrt_zip_msg(symlink, zip_file))
        return True

    return False


def get_dest_file_out_of_date_wrt_to_src_msg(srce_file: str, dest_file: str) -> str:
    return (
        f'The dest image file "{dest_file}" ({get_timestamp_str(dest_file)})'
        f" is out of date WRT"
        f' srce file "{srce_file}" ({get_timestamp_str(srce_file)}).'
    )


def get_file_out_of_date_wrt_max_dest_msg(file: str, max_dest_timestamp: float) -> str:
    return (
        f"The file \"{file}\" timestamp '{get_timestamp_str(file)}',"
        f" is out of date WRT"
        f" max dest page timestamp '{get_timestamp_as_str(max_dest_timestamp)}'."
    )


def get_zip_file_out_of_date_wrt_max_dest_msg(zip_file: str, max_dest_timestamp: float) -> str:
    return (
        f"Zip file \"{zip_file}\" timestamp '{get_timestamp_str(zip_file)}',"
        f" is out of date WRT"
        f" max dest page timestamp '{get_timestamp_as_str(max_dest_timestamp)}'."
    )


def get_symlink_out_of_date_wrt_zip_msg(symlink: str, zip_file: str) -> str:
    return (
        f"Symlink \"{symlink}\" timestamp '{get_timestamp_str(symlink)}',"
        f" is out of date WRT"
        f' zip file "{zip_file}" ({get_timestamp_str(zip_file)}).'
    )


def get_symlink_out_of_date_wrt_max_dest_msg(symlink: str, max_dest_timestamp: float) -> str:
    return (
        f"Symlink \"{symlink}\" timestamp '{get_timestamp_str(symlink)}',"
        f" is out of date WRT"
        f" max dest image timestamp '{get_timestamp_as_str(max_dest_timestamp)}'."
    )
