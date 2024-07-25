import logging

from pages import get_timestamp, get_timestamp_str, get_timestamp_as_str


def is_dest_file_out_of_date(srce_file: str, dest_file: str) -> bool:
    srce_timestamp = get_timestamp(srce_file)
    dest_timestamp = get_timestamp(dest_file)

    if srce_timestamp > dest_timestamp:
        logging.debug(get_dest_file_out_of_date_msg(srce_file, dest_file))
        return True

    return False


def is_zip_file_out_of_date_wrt_dest(zip_file: str, max_dest_timestamp: float) -> bool:
    zip_timestamp = get_timestamp(zip_file)
    if zip_timestamp < max_dest_timestamp:
        logging.debug(
            get_zip_file_out_of_date_wrt_max_dest_msg(zip_file, max_dest_timestamp)
        )
        return True

    return False


def is_symlink_out_of_date_wrt_dest(symlink: str, max_dest_timestamp: float) -> bool:
    symlink_timestamp = get_timestamp(symlink)
    if symlink_timestamp < max_dest_timestamp:
        logging.debug(
            get_symlink_out_of_date_wrt_max_dest_msg(symlink, max_dest_timestamp)
        )
        return True

    return False


def is_symlink_out_of_date_wrt_zip(symlink: str, zip_file: str) -> bool:
    symlink_timestamp = get_timestamp(symlink)
    zip_timestamp = get_timestamp(zip_file)
    if symlink_timestamp < zip_timestamp:
        logging.debug(get_symlink_out_of_date_wrt_zip_msg(symlink, zip_timestamp))
        return True

    return False


def get_dest_file_out_of_date_msg(srce_file: str, dest_file: str) -> str:
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


def get_zip_file_out_of_date_wrt_max_dest_msg(
    zip_file: str, max_dest_timestamp: float
) -> str:
    return (
        f"Zip file \"{zip_file}\" timestamp '{get_timestamp_str(zip_file)}',"
        f" is out of date WRT"
        f" max dest page timestamp '{get_timestamp_as_str(max_dest_timestamp)}'."
    )


def get_symlink_out_of_date_wrt_zip_msg(symlink: str, zip_timestamp: float) -> str:
    return (
        f"Symlink \"{symlink}\" timestamp '{get_timestamp_str(symlink)}',"
        f" is out of date WRT"
        f" zip file timestamp '{get_timestamp_as_str(zip_timestamp)}'."
    )


def get_symlink_out_of_date_wrt_max_dest_msg(
    symlink: str, max_dest_timestamp: float
) -> str:
    return (
        f"Symlink \"{symlink}\" timestamp '{get_timestamp_str(symlink)}',"
        f" is out of date WRT"
        f" max dest image timestamp '{get_timestamp_as_str(max_dest_timestamp)}'."
    )
