import configparser
import difflib
import logging
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from typing import List, Tuple

from .comic_book import (
    ComicBook,
    ComicBookDirs,
    INTRO_TITLE_DEFAULT_FONT_SIZE,
    INTRO_AUTHOR_DEFAULT_FONT_SIZE,
    get_main_publication_info,
    _get_pages_in_order,
)
from .comics_consts import (
    PageType,
    get_font_path,
    IMAGES_SUBDIR,
    BARKS_ROOT_DIR,
    INTRO_TITLE_DEFAULT_FONT_FILE,
    STORY_TITLES_DIR,
    JPG_FILE_EXT,
    PNG_FILE_EXT,
)
from .comics_utils import (
    get_relpath,
    get_formatted_first_published_str,
    get_formatted_submitted_date,
)
from .fanta_comics_info import (
    FantaComicBookInfo,
    FantaBook,
    get_fanta_volume_str,
    FANTA_SOURCE_COMICS,
    FIRST_VOLUME_NUMBER,
    LAST_VOLUME_NUMBER,
    FANTAGRAPHICS_DIRNAME,
    FANTAGRAPHICS_UPSCAYLED_DIRNAME,
    FANTAGRAPHICS_RESTORED_UPSCAYLED_DIRNAME,
    FANTAGRAPHICS_RESTORED_DIRNAME,
    FANTAGRAPHICS_RESTORED_SVG_DIRNAME,
    FANTAGRAPHICS_FIXES_DIRNAME,
    FANTAGRAPHICS_UPSCAYLED_FIXES_DIRNAME,
    FANTAGRAPHICS_FIXES_SCRAPS_DIRNAME,
    FANTAGRAPHICS_PANEL_SEGMENTS_DIRNAME,
    FANTAGRAPHICS_RESTORED_OCR_DIRNAME,
    ALL_FANTA_COMIC_BOOK_INFO,
    FANTA_VOLUME_OVERRIDES_ROOT,
    FANTA_OVERRIDE_DIRECTORIES,
)
from .page_classes import OriginalPage


def get_default_comics_database_dir() -> str:
    return str(Path(__file__).parent.parent.parent.absolute())


class ComicsDatabase:
    def __init__(self, database_dir: str):
        self._database_dir = _get_comics_database_dir(database_dir)
        self._story_titles_dir = _get_story_titles_dir(self._database_dir)
        self._all_comic_book_info = ALL_FANTA_COMIC_BOOK_INFO
        self._ini_files = [f for f in os.listdir(self._story_titles_dir) if f.endswith(".ini")]
        self._story_titles = set([Path(f).stem for f in self._ini_files])
        self._issue_titles = self._get_all_issue_titles()
        self._inset_dir = ""
        self._inset_ext = ""

    def set_inset_info(self, inset_dir: str, inset_ext: str):
        self._inset_dir = inset_dir
        self._inset_ext = inset_ext
        assert os.path.isdir(self._inset_dir)
        assert self._inset_ext in [JPG_FILE_EXT, PNG_FILE_EXT]

    def _get_all_issue_titles(self):
        all_issues = {}
        for title in self._all_comic_book_info:
            issue_title = self._all_comic_book_info[title].get_short_issue_title()
            if issue_title not in all_issues:
                all_issues[issue_title] = [title]
            else:
                all_issues[issue_title].append(title)

        return all_issues

    def get_comics_database_dir(self) -> str:
        return self._database_dir

    def get_story_titles_dir(self) -> str:
        return self._story_titles_dir

    def get_ini_file(self, story_title: str) -> str:
        return os.path.join(self._story_titles_dir, story_title + ".ini")

    def get_fanta_volume(self, story_title: str) -> str:
        return self._all_comic_book_info[story_title].fantagraphics_volume

    def is_story_title(self, title: str) -> Tuple[bool, str]:
        if title in self._story_titles:
            return True, ""

        close = difflib.get_close_matches(title, self._story_titles, 1, 0.3)
        close_str = close[0] if close else ""
        return False, close_str

    def get_story_title_from_issue(self, issue_title: str) -> Tuple[bool, List[str], str]:
        issue_title = issue_title.upper()
        if issue_title in self._issue_titles:
            return True, self._issue_titles[issue_title], ""

        close = difflib.get_close_matches(issue_title, self._issue_titles, 1, 0.7)
        close_str = close[0] if close else ""
        return False, [], close_str

    def get_all_story_titles(self) -> List[str]:
        return sorted(self._story_titles)

    def get_all_titles_in_fantagraphics_volumes(
        self, volume_nums: List[int]
    ) -> List[Tuple[str, FantaComicBookInfo]]:
        story_titles = []
        for volume_num in volume_nums:
            fanta_key = get_fanta_volume_str(volume_num)
            for title, comic_info in self._all_comic_book_info.items():
                if comic_info.fantagraphics_volume == fanta_key:
                    story_titles.append((title, comic_info))

        return sorted(story_titles)

    def get_configured_titles_in_fantagraphics_volumes(
        self, volume_nums: List[int]
    ) -> List[Tuple[str, FantaComicBookInfo]]:
        story_titles = []

        for volume in volume_nums:
            story_titles.extend(self.get_configured_titles_in_fantagraphics_volume(volume))

        return sorted(story_titles)

    def get_configured_titles_in_fantagraphics_volume(
        self, volume: int
    ) -> List[Tuple[str, FantaComicBookInfo]]:
        config = ConfigParser(interpolation=ExtendedInterpolation())

        story_titles = []
        fanta_key = f"FANTA_{volume:02}"
        for file in self._ini_files:
            ini_file = os.path.join(self._story_titles_dir, file)
            config.read(ini_file)
            if config["info"]["source_comic"] == fanta_key:
                story_title = Path(ini_file).stem
                comic_info = self._all_comic_book_info[story_title]
                story_titles.append((story_title, comic_info))

        return sorted(story_titles)

    # "$HOME/Books/Carl Barks/Fantagraphics/Carl Barks Vol. 2 - Donald Duck - Frozen Gold"
    #     root_dir      = "$HOME/Books/Carl Barks/Fantagraphics"
    #     fanta dirname = "Fantagraphics"
    #     title         = "Carl Barks Vol. 2 - Donald Duck - Frozen Gold"
    @staticmethod
    def get_fantagraphics_volume_title(volume_num: int) -> str:
        fanta_key = f"FANTA_{volume_num:02}"
        fanta_book = FANTA_SOURCE_COMICS[fanta_key]
        return fanta_book.title

    @staticmethod
    def get_num_pages_in_fantagraphics_volume(volume_num: int) -> int:
        fanta_key = f"FANTA_{volume_num:02}"
        fanta_book = FANTA_SOURCE_COMICS[fanta_key]
        return fanta_book.num_pages

    def _get_comic_book_dirs(self, fanta_book: FantaBook) -> ComicBookDirs:
        return ComicBookDirs(
            srce_dir=self.get_fantagraphics_volume_dir(fanta_book.volume),
            srce_upscayled_dir=self.get_fantagraphics_upscayled_volume_dir(fanta_book.volume),
            srce_restored_dir=self.get_fantagraphics_restored_volume_dir(fanta_book.volume),
            srce_restored_upscayled_dir=self.get_fantagraphics_restored_upscayled_volume_dir(
                fanta_book.volume
            ),
            srce_restored_svg_dir=self.get_fantagraphics_restored_svg_volume_dir(fanta_book.volume),
            srce_restored_ocr_dir=self.get_fantagraphics_restored_ocr_volume_dir(fanta_book.volume),
            srce_fixes_dir=self.get_fantagraphics_fixes_volume_dir(fanta_book.volume),
            srce_upscayled_fixes_dir=self.get_fantagraphics_upscayled_fixes_volume_dir(
                fanta_book.volume
            ),
            panel_segments_dir=self.get_fantagraphics_panel_segments_volume_dir(fanta_book.volume),
        )

    @staticmethod
    def get_root_dir(fanta_subdir: str) -> str:
        return str(os.path.join(BARKS_ROOT_DIR, fanta_subdir))

    def get_fantagraphics_original_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_dirname())

    @staticmethod
    def get_fantagraphics_dirname() -> str:
        return FANTAGRAPHICS_DIRNAME

    def get_fantagraphics_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_original_root_dir(), title))

    def get_fantagraphics_volume_image_dir(self, volume_num: int) -> str:
        return str(os.path.join(self.get_fantagraphics_volume_dir(volume_num), IMAGES_SUBDIR))

    def get_fantagraphics_upscayled_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_upscayled_dirname())

    @staticmethod
    def get_fantagraphics_upscayled_dirname() -> str:
        return FANTAGRAPHICS_UPSCAYLED_DIRNAME

    def get_fantagraphics_upscayled_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_upscayled_root_dir(), title))

    def get_fantagraphics_upscayled_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(self.get_fantagraphics_upscayled_volume_dir(volume_num), IMAGES_SUBDIR)
        )

    def get_fantagraphics_restored_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_restored_dirname())

    @staticmethod
    def get_fantagraphics_restored_dirname() -> str:
        return FANTAGRAPHICS_RESTORED_DIRNAME

    def get_fantagraphics_restored_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_restored_root_dir(), title))

    def get_fantagraphics_restored_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(self.get_fantagraphics_restored_volume_dir(volume_num), IMAGES_SUBDIR)
        )

    def get_fantagraphics_restored_upscayled_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_restored_upscayled_dirname())

    @staticmethod
    def get_fantagraphics_restored_upscayled_dirname() -> str:
        return FANTAGRAPHICS_RESTORED_UPSCAYLED_DIRNAME

    def get_fantagraphics_restored_upscayled_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_restored_upscayled_root_dir(), title))

    def get_fantagraphics_restored_upscayled_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(
                self.get_fantagraphics_restored_upscayled_volume_dir(volume_num), IMAGES_SUBDIR
            )
        )

    def get_fantagraphics_restored_svg_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_restored_svg_dirname())

    @staticmethod
    def get_fantagraphics_restored_svg_dirname() -> str:
        return FANTAGRAPHICS_RESTORED_SVG_DIRNAME

    def get_fantagraphics_restored_svg_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_restored_svg_root_dir(), title))

    def get_fantagraphics_restored_svg_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(self.get_fantagraphics_restored_svg_volume_dir(volume_num), IMAGES_SUBDIR)
        )

    def get_fantagraphics_restored_ocr_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_restored_ocr_dirname())

    @staticmethod
    def get_fantagraphics_restored_ocr_dirname() -> str:
        return FANTAGRAPHICS_RESTORED_OCR_DIRNAME

    def get_fantagraphics_restored_ocr_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_restored_ocr_root_dir(), title))

    def get_fantagraphics_panel_segments_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_panel_segments_dirname())

    @staticmethod
    def get_fantagraphics_panel_segments_dirname() -> str:
        return FANTAGRAPHICS_PANEL_SEGMENTS_DIRNAME

    def get_fantagraphics_panel_segments_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_panel_segments_root_dir(), title))

    def get_fantagraphics_fixes_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_fixes_dirname())

    @staticmethod
    def get_fantagraphics_fixes_dirname() -> str:
        return FANTAGRAPHICS_FIXES_DIRNAME

    def get_fantagraphics_fixes_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_fixes_root_dir(), title))

    def get_fantagraphics_fixes_volume_image_dir(self, volume_num: int) -> str:
        return str(os.path.join(self.get_fantagraphics_fixes_volume_dir(volume_num), IMAGES_SUBDIR))

    def get_fantagraphics_upscayled_fixes_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_upscayled_fixes_dirname())

    @staticmethod
    def get_fantagraphics_upscayled_fixes_dirname() -> str:
        return FANTAGRAPHICS_UPSCAYLED_FIXES_DIRNAME

    def get_fantagraphics_upscayled_fixes_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_upscayled_fixes_root_dir(), title))

    def get_fantagraphics_upscayled_fixes_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(
                self.get_fantagraphics_upscayled_fixes_volume_dir(volume_num), IMAGES_SUBDIR
            )
        )

    def get_fantagraphics_fixes_scraps_root_dir(self) -> str:
        return self.get_root_dir(self.get_fantagraphics_fixes_scraps_dirname())

    @staticmethod
    def get_fantagraphics_fixes_scraps_dirname() -> str:
        return FANTAGRAPHICS_FIXES_SCRAPS_DIRNAME

    def get_fantagraphics_fixes_scraps_volume_dir(self, volume_num: int) -> str:
        title = self.get_fantagraphics_volume_title(volume_num)
        return str(os.path.join(self.get_fantagraphics_fixes_scraps_root_dir(), title))

    def get_fantagraphics_fixes_scraps_volume_image_dir(self, volume_num: int) -> str:
        return str(
            os.path.join(self.get_fantagraphics_fixes_scraps_volume_dir(volume_num), IMAGES_SUBDIR)
        )

    def make_all_fantagraphics_directories(self) -> None:
        for volume in range(FIRST_VOLUME_NUMBER, LAST_VOLUME_NUMBER + 1):
            # Create these directories if they're already not there.
            self._make_vol_dirs(self.get_fantagraphics_upscayled_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_restored_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_restored_upscayled_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_restored_svg_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_restored_ocr_volume_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_fixes_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_upscayled_fixes_volume_image_dir(volume))
            self._make_vol_dirs(self.get_fantagraphics_panel_segments_volume_dir(volume))

            scraps_image_dir = self.get_fantagraphics_fixes_scraps_volume_image_dir(volume)
            self._make_vol_dirs(os.path.join(scraps_image_dir, "standard"))
            self._make_vol_dirs(os.path.join(scraps_image_dir, "upscayled"))
            self._make_vol_dirs(os.path.join(scraps_image_dir, "restored"))

            self._make_vol_dirs(
                os.path.join(FANTA_VOLUME_OVERRIDES_ROOT, FANTA_OVERRIDE_DIRECTORIES[volume])
            )

        # Symlinks - just make sure these exist.
        self._check_symlink_exists(self.get_fantagraphics_upscayled_root_dir())
        self._check_symlink_exists(self.get_fantagraphics_restored_upscayled_root_dir())
        self._check_symlink_exists(self.get_fantagraphics_restored_svg_root_dir())

    @staticmethod
    def _make_vol_dirs(vol_dirname: str) -> None:
        if os.path.isdir(vol_dirname):
            logging.debug(f'Dir already exists - nothing to do: "{vol_dirname}".')
        else:
            os.makedirs(vol_dirname)
            logging.info(f'Created dir "{vol_dirname}".')

    @staticmethod
    def _check_symlink_exists(symlink: str) -> None:
        if not os.path.islink(symlink):
            logging.error(f'Symlink not found: "{symlink}".')
        else:
            logging.debug(f'Symlink exists - all good: "{symlink}".')

    def get_fanta_comic_book_info(self, title: str) -> FantaComicBookInfo:
        found, titles, close = self.get_story_title_from_issue(title)
        if found:
            if len(titles) > 1:
                titles_str = ", ".join([f'"{t}"' for t in titles])
                raise Exception(
                    f"You cannot use an issue title that has multiple titles: {titles_str}."
                )
            title = titles[0]
        elif close:
            raise Exception(f'Could not find issue title "{title}". Did you mean "{close}"?')

        return self._all_comic_book_info[title]

    def get_comic_book(self, title: str) -> ComicBook:
        story_title = ""

        found, titles, close = self.get_story_title_from_issue(title)
        if found:
            if len(titles) > 1:
                titles_str = ", ".join([f'"{t}"' for t in titles])
                raise Exception(
                    f"You cannot use an issue title that has multiple titles: {titles_str}."
                )
            story_title = titles[0]
        elif close:
            raise Exception(f'Could not find issue title "{title}". Did you mean "{close}"?')

        if not story_title:
            found, close = self.is_story_title(title)
            if found:
                story_title = title
            else:
                if close:
                    raise Exception(f'Could not find title "{title}". Did you mean "{close}"?')
                raise Exception(f'Could not find title "{title}".')

        ini_file = self.get_ini_file(story_title)
        logging.debug(f'Getting comic book info from config file "{get_relpath(ini_file)}".')

        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(ini_file)

        issue_title = "" if "issue_title" not in config["info"] else config["info"]["issue_title"]
        intro_inset_file = self.__get_inset_file(ini_file)

        fanta_info: FantaComicBookInfo = self.get_fanta_comic_book_info(story_title)
        fanta_book = FANTA_SOURCE_COMICS[config["info"]["source_comic"]]

        title = config["info"]["title"]
        if not title and fanta_info.comic_book_info.is_barks_title:
            raise Exception(f'"{story_title}" is a barks title and should be set in the ini file.')
        if title and not fanta_info.comic_book_info.is_barks_title:
            raise Exception(
                f'"{story_title}" is a not barks title and should not be set in the ini file.'
            )

        srce_dir_num_page_files = fanta_book.num_pages
        comic_book_dirs = self._get_comic_book_dirs(fanta_book)

        publication_date = get_formatted_first_published_str(fanta_info.comic_book_info)
        submitted_date = get_formatted_submitted_date(fanta_info.comic_book_info)

        publication_text = get_main_publication_info(story_title, fanta_info, fanta_book)
        if "extra_pub_info" in config["info"]:
            publication_text += "\n" + config["info"]["extra_pub_info"]

        # noinspection PyTypeChecker
        config_page_images = [
            OriginalPage(key, PageType[config["pages"][key]]) for key in config["pages"]
        ]

        comic = ComicBook(
            ini_file=ini_file,
            title=title,
            title_font_file=get_font_path(
                config["info"].get("title_font_file", INTRO_TITLE_DEFAULT_FONT_FILE)
            ),
            title_font_size=config["info"].getint("title_font_size", INTRO_TITLE_DEFAULT_FONT_SIZE),
            issue_title=issue_title,
            author_font_size=config["info"].getint(
                "author_font_size", INTRO_AUTHOR_DEFAULT_FONT_SIZE
            ),
            srce_dir_num_page_files=srce_dir_num_page_files,
            dirs=comic_book_dirs,
            intro_inset_file=intro_inset_file,
            config_page_images=config_page_images,
            page_images_in_order=_get_pages_in_order(config_page_images),
            publication_date=publication_date,
            submitted_date=submitted_date,
            publication_text=publication_text,
            fanta_book=fanta_book,
            fanta_info=fanta_info,
        )

        if not os.path.isdir(comic.dirs.srce_dir):
            raise NotADirectoryError(f'Could not find srce directory "{comic.dirs.srce_dir}".')
        if not os.path.isdir(comic.get_srce_image_dir()):
            raise NotADirectoryError(
                f'Could not find srce image directory "{comic.get_srce_image_dir()}".'
            )
        if not os.path.isdir(comic.dirs.srce_upscayled_dir):
            raise NotADirectoryError(
                f"Could not find srce upscayled directory " f'"{comic.dirs.srce_upscayled_dir}".'
            )
        if not os.path.isdir(comic.get_srce_upscayled_image_dir()):
            raise NotADirectoryError(
                f"Could not find srce upscayled image directory"
                f' "{comic.get_srce_upscayled_image_dir()}".'
            )
        if not os.path.isdir(comic.dirs.srce_restored_dir):
            raise NotADirectoryError(
                f"Could not find srce restored directory " f'"{comic.dirs.srce_restored_dir}".'
            )
        if not os.path.isdir(comic.get_srce_restored_image_dir()):
            raise NotADirectoryError(
                f"Could not find srce restored image directory"
                f' "{comic.get_srce_restored_image_dir()}".'
            )
        if not os.path.isdir(comic.dirs.srce_fixes_dir):
            raise NotADirectoryError(
                f'Could not find srce fixes directory "{comic.dirs.srce_fixes_dir}".'
            )
        if not os.path.isdir(comic.get_srce_original_fixes_image_dir()):
            raise NotADirectoryError(
                f"Could not find srce fixes image directory "
                f'"{comic.get_srce_original_fixes_image_dir()}".'
            )

        return comic

    def __get_inset_file(self, ini_file: str) -> str:
        assert self._inset_dir
        assert self._inset_ext

        title = Path(ini_file).stem
        inset_filename = title + self._inset_ext

        return os.path.join(self._inset_dir, inset_filename)


def _get_comics_database_dir(db_dir: str) -> str:
    real_db_dir = os.path.realpath(db_dir)

    if not os.path.isdir(real_db_dir):
        raise Exception(f'Could not find comics database directory "{real_db_dir}".')

    return real_db_dir


def _get_story_titles_dir(db_dir: str) -> str:
    story_titles_dir = os.path.join(db_dir, STORY_TITLES_DIR)

    if not os.path.isdir(story_titles_dir):
        raise Exception(f'Could not find story titles directory "{story_titles_dir}".')

    return story_titles_dir
