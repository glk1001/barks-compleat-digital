from __future__ import annotations

from collections import OrderedDict

from barks_fantagraphics.barks_tags import (
    BARKS_TAG_ALIASES,
    BARKS_TAG_GROUPS,
    BARKS_TAG_GROUPS_ALIASES,
    BARKS_TAGGED_TITLES,
    TagGroups,
    Tags,
)
from barks_fantagraphics.barks_titles import BARKS_TITLE_INFO, Titles

PREFIX_LEN = 2


class BarksTitleSearch:
    def __init__(self) -> None:
        self.title_prefix_dict: OrderedDict[str, list[Titles]] = self._get_title_prefix_dict()
        self.tag_prefix_dict: dict[str, list[str]] = self._get_tag_prefix_dict()

    def get_titles_matching_prefix(self, prefix: str) -> list[Titles]:
        prefix = prefix.lower()

        if len(prefix) == 0:
            return []
        if len(prefix) == 1:
            return self._get_titles_with_one_char_search(prefix)

        short_prefix = prefix[:PREFIX_LEN]
        if short_prefix not in self.title_prefix_dict:
            return []

        title_list = []
        for title in self.title_prefix_dict[short_prefix]:
            title_info = BARKS_TITLE_INFO[title]
            if title_info.get_title_str().lower().startswith(prefix):
                title_list.append(title)

        return title_list

    @staticmethod
    def get_titles_as_strings(titles: list[Titles]) -> list[str]:
        title_info_list = []
        for title in titles:
            title_info_list.append(BARKS_TITLE_INFO[title].get_display_title())

        return title_info_list

    def _get_titles_with_one_char_search(self, prefix: str) -> list[Titles]:
        assert len(prefix) == 1

        title_list = []
        for key in self.title_prefix_dict:
            if not key.startswith(prefix):
                continue

            title_list.extend(self.title_prefix_dict[key])

        return title_list

    @staticmethod
    def get_titles_containing(word: str) -> list[Titles]:
        if len(word) <= 1:
            return []

        word = word.lower()

        title_list = []

        for info in BARKS_TITLE_INFO:
            if word in info.get_title_str().lower():
                title_list.append(info.title)

        return title_list

    @staticmethod
    def _get_title_prefix_dict() -> OrderedDict[str, list[Titles]]:
        pref_dict = OrderedDict()

        for info in BARKS_TITLE_INFO:
            prefix = info.get_title_str()[:PREFIX_LEN].lower()
            if prefix not in pref_dict:
                pref_dict[prefix] = []
            pref_dict[prefix].append(info.title)

        return pref_dict

    def get_tags_matching_prefix(self, prefix: str) -> list[Tags | TagGroups]:
        prefix = prefix.lower()

        if len(prefix) == 0:
            return []
        if len(prefix) == 1:
            return self._get_titles_with_one_char_tag_search(prefix)

        short_prefix = prefix[:PREFIX_LEN]
        if short_prefix not in self.tag_prefix_dict:
            return []

        tag_list = []
        for alias_tag_str in self.tag_prefix_dict[short_prefix]:
            if not alias_tag_str.startswith(prefix):
                continue
            if alias_tag_str in BARKS_TAG_ALIASES:
                tag_list.append(BARKS_TAG_ALIASES[alias_tag_str])
            if alias_tag_str in BARKS_TAG_GROUPS_ALIASES:
                tag_list.append(BARKS_TAG_GROUPS_ALIASES[alias_tag_str])

        return list(set(tag_list))

    @staticmethod
    def get_titles_from_alias_tag(alias_tag_str: str) -> tuple[Tags, list[Titles]]:
        tag = None
        title_list = []

        if alias_tag_str in BARKS_TAG_ALIASES:
            tag = BARKS_TAG_ALIASES[alias_tag_str]
            unique_extend(title_list, BARKS_TAGGED_TITLES[tag])

        if alias_tag_str in BARKS_TAG_GROUPS_ALIASES:
            tag_group = BARKS_TAG_GROUPS_ALIASES[alias_tag_str]
            tags = BARKS_TAG_GROUPS[tag_group]
            for tag in tags:
                unique_extend(title_list, BARKS_TAGGED_TITLES[tag])
            tag = tag_group

        return tag, sorted(title_list)

    @staticmethod
    def _get_titles_with_one_char_tag_search(prefix: str) -> list[Tags]:
        assert len(prefix) == 1

        return []

    def _get_tag_prefix_dict(self) -> dict[str, list[str]]:
        alias_tag_dict = self._get_alias_tag_prefix_dict(BARKS_TAG_ALIASES)
        alias_tag_group_dict = self._get_alias_tag_prefix_dict(BARKS_TAG_GROUPS_ALIASES)

        pref_dict = {}

        for alias_tag_prefix in alias_tag_dict:
            pref_dict[alias_tag_prefix] = alias_tag_dict[alias_tag_prefix]

        for alias_tag_prefix in alias_tag_group_dict:
            if alias_tag_prefix in alias_tag_dict:
                pref_dict[alias_tag_prefix].extend(alias_tag_group_dict[alias_tag_prefix])
            else:
                pref_dict[alias_tag_prefix] = alias_tag_group_dict[alias_tag_prefix]

        return pref_dict

    @staticmethod
    def _get_alias_tag_prefix_dict(
        alias_dict: dict[str, Tags] | dict[str, TagGroups],
    ) -> dict[str, list[str]]:
        pref_dict = {}

        for tag_alias_str in alias_dict:
            prefix = tag_alias_str[:PREFIX_LEN].lower()
            if prefix not in pref_dict:
                pref_dict[prefix] = []
            pref_dict[prefix].append(tag_alias_str)

        return pref_dict


# Assumes 'original_list' and 'extra_list' have no duplicates.
def unique_extend(original_list: list[Titles], extras_list: list[Titles]) -> None:
    seen = set(original_list)

    for item in extras_list:
        if item not in seen:
            original_list.append(item)
