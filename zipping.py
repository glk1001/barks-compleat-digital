import logging
import os
import shutil
from pathlib import Path
from typing import Union

from barks_fantagraphics.comic_book import ComicBook
from barks_fantagraphics.comics_utils import get_relpath
from consts import DRY_RUN_STR


def zip_comic_book(dry_run: bool, comic: ComicBook, max_dest_timestamp: float):
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Zipping directory "{get_relpath(comic.get_dest_dir())}"'
            f' to "{get_relpath(comic.get_dest_comic_zip())}".'
        )
    else:
        logging.info(
            f'Zipping directory "{get_relpath(comic.get_dest_dir())}" to'
            f' "{get_relpath(comic.get_dest_comic_zip())}".'
        )

        os.makedirs(comic.get_dest_zip_root_dir(), exist_ok=True)
        temp_zip_file = comic.get_dest_dir() + ".zip"

        shutil.make_archive(comic.get_dest_dir(), "zip", comic.get_dest_dir())
        if not os.path.isfile(temp_zip_file):
            raise Exception(f'Could not create temporary zip file "{temp_zip_file}".')

        os.replace(temp_zip_file, comic.get_dest_comic_zip())
        if not os.path.isfile(comic.get_dest_comic_zip()):
            raise Exception(f'Could not create final comic zip "{comic.get_dest_comic_zip()}".')


def create_symlinks_to_comic_zip(dry_run: bool, comic: ComicBook):
    if not os.path.exists(comic.get_dest_comic_zip()):
        raise Exception(f'Could not find comic zip file "{comic.get_dest_comic_zip()}".')

    create_symlink_zip(
        dry_run,
        comic.get_dest_comic_zip(),
        comic.get_dest_series_zip_symlink_dir(),
        comic.get_dest_series_comic_zip_symlink(),
    )

    create_symlink_zip(
        dry_run,
        comic.get_dest_comic_zip(),
        comic.get_dest_year_zip_symlink_dir(),
        comic.get_dest_year_comic_zip_symlink(),
    )


def create_symlink_zip(dry_run: bool, zip_file: str, symlink_dir: str, symlink: str) -> None:
    if dry_run:
        logging.info(
            f'{DRY_RUN_STR}: Symlinking (relative) comic zip file "{get_relpath(zip_file)}" to'
            f' "{get_relpath(symlink)}".'
        )
    else:
        logging.info(
            f'Symlinking (relative) the comic zip file "{get_relpath(zip_file)}" to'
            f' "{get_relpath(symlink)}".'
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

    logging.debug(f'"{relative_source}" -> "{destination.name}" in "{get_relpath(target_dir)}"')
    target_dir_fd = os.open(str(target_dir.absolute()), os.O_RDONLY)
    try:
        os.symlink(relative_source, destination.name, dir_fd=target_dir_fd)
    finally:
        os.close(target_dir_fd)
