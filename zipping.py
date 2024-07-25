import logging
import os
import shutil
from pathlib import Path
from typing import Union

from comic_book import ComicBook
from consts import DRY_RUN_STR
from out_of_date_checking import (
    is_zip_file_out_of_date_wrt_dest,
    is_symlink_out_of_date_wrt_zip,
)


def zip_comic_book(
    dry_run: bool, no_cache: bool, comic: ComicBook, max_dest_timestamp: float
):
    if (
        not no_cache
        and os.path.isfile(comic.get_dest_comic_zip())
        and not is_zip_file_out_of_date_wrt_dest(
            comic.get_dest_comic_zip(), max_dest_timestamp
        )
    ):
        logging.debug(
            f'Caching on - keeping existing zip file "{comic.get_dest_comic_zip()}".'
        )
        return

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Zipping directory "{comic.get_dest_dir()}"'
            f' to "{comic.get_dest_comic_zip()}".'
        )
    else:
        logging.info(
            f'Zipping directory "{comic.get_dest_dir()}" to "{comic.get_dest_comic_zip()}".'
        )

        os.makedirs(comic.get_dest_zip_root_dir(), exist_ok=True)
        temp_zip_file = comic.get_dest_dir() + ".zip"

        shutil.make_archive(comic.get_dest_dir(), "zip", comic.get_dest_dir())
        if not os.path.isfile(temp_zip_file):
            raise Exception(f'Could not create temporary zip file "{temp_zip_file}".')

        os.replace(temp_zip_file, comic.get_dest_comic_zip())
        if not os.path.isfile(comic.get_dest_comic_zip()):
            raise Exception(
                f'Could not create final comic zip "{comic.get_dest_comic_zip()}".'
            )


def create_symlinks_to_comic_zip(dry_run: bool, no_cache: bool, comic: ComicBook):
    if not os.path.exists(comic.get_dest_comic_zip()):
        raise Exception(
            f'Could not find comic zip file "{comic.get_dest_comic_zip()}".'
        )

    create_symlink_zip(
        dry_run,
        no_cache,
        comic.get_dest_comic_zip(),
        comic.get_dest_series_zip_symlink_dir(),
        comic.get_dest_series_comic_zip_symlink(),
    )

    create_symlink_zip(
        dry_run,
        no_cache,
        comic.get_dest_comic_zip(),
        comic.get_dest_year_zip_symlink_dir(),
        comic.get_dest_year_comic_zip_symlink(),
    )


def create_symlink_zip(
    dry_run: bool, no_cache: bool, zip_file: str, symlink_dir: str, symlink: str
) -> None:
    if (
        not no_cache
        and os.path.islink(symlink)
        and not is_symlink_out_of_date_wrt_zip(symlink, zip_file)
    ):
        logging.debug(f'Caching on - keeping existing symlink file "{symlink}".')
        return

    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Symlinking (relative) comic zip file "{zip_file}" to "{symlink}".'
        )
    else:
        logging.info(
            f'Symlinking (relative) the comic zip file "{zip_file}" to "{symlink}".'
        )

        if not os.path.exists(symlink_dir):
            os.makedirs(symlink_dir)
        if os.path.islink(symlink):
            os.remove(symlink)

        relative_symlink(zip_file, symlink)
        if not os.path.islink(symlink):
            raise Exception(f'Could not create symlink "{symlink}".')


def relative_symlink(target: Union[Path, str], destination: Union[Path, str]):
    """Create a symlink pointing to ``target`` from ``location``.
    Args:
        target: The target of the symlink (the file/directory that is pointed to)
        destination: The location of the symlink itself.
    """
    target = Path(target)
    destination = Path(destination)

    target_dir = destination.parent
    target_dir.mkdir(exist_ok=True, parents=True)

    relative_source = os.path.relpath(target, target_dir)

    logging.debug(f"{relative_source} -> {destination.name} in {target_dir}")
    target_dir_fd = os.open(str(target_dir.absolute()), os.O_RDONLY)
    try:
        os.symlink(relative_source, destination.name, dir_fd=target_dir_fd)
    finally:
        os.close(target_dir_fd)
