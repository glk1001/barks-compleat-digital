import string
import unittest
from typing import List

from barks_fantagraphics.barks_titles import (
    ComicBookInfo,
    BARKS_TITLE_INFO,
    Titles,
    check_story_submitted_order,
    # Import the raw data for some tests
    SHORT_ISSUE_NAME,
    Issues,
    NUM_TITLES,
    BARKS_TITLES,
)


class TestComicBookInfo(unittest.TestCase):

    def test_get_issue_title(self):
        """Tests the formatting of the issue title."""
        info = ComicBookInfo(
            title=Titles(0),
            is_barks_title=True,
            issue_name=Issues.FC,
            issue_number=178,
            issue_month=12,
            issue_year=1947,
            submitted_day=22,
            submitted_month=7,
            submitted_year=1947,
        )
        expected_issue_title = f"{SHORT_ISSUE_NAME[Issues.FC]} 178"
        self.assertEqual(info.get_short_issue_title(), expected_issue_title)

        info_us = ComicBookInfo(
            title=Titles(0),
            is_barks_title=False,
            issue_name=Issues.US,
            issue_number=31,
            issue_month=9,
            issue_year=1960,
            submitted_day=12,
            submitted_month=2,
            submitted_year=1960,
        )
        expected_title_us = f"{SHORT_ISSUE_NAME[Issues.US]} 31"
        self.assertEqual(info_us.get_short_issue_title(), expected_title_us)


class TestBarksInfo(unittest.TestCase):

    def test_sorted_by_chronological_number(self):
        """Tests if the titles list is sorted correctly."""
        for i in range(len(BARKS_TITLE_INFO) - 1):
            self.assertEqual(
                BARKS_TITLE_INFO[i].chronological_number + 1,
                BARKS_TITLE_INFO[i + 1].chronological_number,
                f"Chronological order failed between"
                f"  item {i} ('{BARKS_TITLE_INFO[i].get_short_issue_title()}')"
                f" and item {i+1} ('{BARKS_TITLE_INFO[i+1].get_short_issue_title()}')",
            )

    def test_chronological_numbers_covered(self):
        for info in BARKS_TITLE_INFO:
            self.assertEqual(
                info.chronological_number,
                info.title + 1,
                f"Chronological number not equal to title + 1;"
                f" title: {info.title} ('{info.get_short_issue_title()}')",
            )

    def test_correct_title_strings(self):
        for title, title_str in enumerate(BARKS_TITLES):
            expected_enum_var = self.get_title_var(title_str)
            actual_enum_var = Titles(title).name
            self.assertEqual(
                actual_enum_var,
                expected_enum_var,
                f"Barks title does not match Titles enum name;"
                f" title: {title_str}; actual_enum_var: {actual_enum_var};"
                f" expected_enum_var: {expected_enum_var} )",
            )

    def test_titles_match_title_info(self):
        for title in Titles:
            self.assertEqual(
                title,
                BARKS_TITLE_INFO[title].title,
                f"Barks title info title does not match Titles enum"
                f" title enum: {title};"
                f" title info title: {BARKS_TITLE_INFO[title].title} )",
            )

    @staticmethod
    def get_title_var(title: str) -> str:
        enum_var = title.upper()

        enum_var = enum_var.replace(" ", "_")
        enum_var = enum_var.replace("-", "_")

        str_punc = string.punctuation
        str_punc = str_punc.replace("_", "")
        str_punc = str_punc.replace("-", "")
        for punc in str_punc:
            enum_var = enum_var.replace(punc, "")

        if enum_var.startswith("THE_"):
            enum_var = enum_var[4:] + "_THE"
        elif enum_var.startswith("A_"):
            enum_var = enum_var[2:] + "_A"

        return enum_var

    def test_correct_number_of_titles(self):
        assert NUM_TITLES == len(BARKS_TITLES)
        assert NUM_TITLES == len(BARKS_TITLE_INFO)
        self.assertEqual(1, BARKS_TITLE_INFO[0].chronological_number)
        self.assertEqual(NUM_TITLES, BARKS_TITLE_INFO[-1].chronological_number)

    def test_story_submitted_order(self):
        try:
            check_story_submitted_order(BARKS_TITLE_INFO)
        except Exception as e:
            self.fail(f"get_all_comic_book_info raised an unexpected exception: {e}")


class TestCheckStorySubmittedOrder(unittest.TestCase):

    def test_valid_order(self):
        """Tests that correctly ordered data passes."""
        valid_data: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, 1, 1, 1940),
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 2, 1940),
            # Day -1 is ok
            ComicBookInfo(Titles(2), True, Issues.FC, 3, 3, 1940, -1, 2, 1940),
            ComicBookInfo(Titles(3), True, Issues.FC, 4, 4, 1940, 15, 2, 1940),
            ComicBookInfo(Titles(4), True, Issues.FC, 5, 5, 1941, 1, 1, 1941),
        ]
        try:
            check_story_submitted_order(valid_data)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception for valid data: {e}"
            )

    def test_invalid_month(self):
        """Tests detection of invalid submission month."""
        invalid_data: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, 1, 1, 1940),
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 13, 1940),  # Invalid month 13
        ]
        with self.assertRaisesRegex(Exception, "Invalid submission month: 13"):
            check_story_submitted_order(invalid_data)

        invalid_data_zero: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, 1, 0, 1940),  # Invalid month 0
        ]
        with self.assertRaisesRegex(Exception, "Invalid submission month: 0"):
            check_story_submitted_order(invalid_data_zero)

    def test_out_of_order_submission_date(self):
        """Tests detection of out-of-order submission dates."""
        invalid_data: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, 15, 2, 1940),
            # Submitted earlier than A
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 2, 1940),
        ]
        with self.assertRaisesRegex(Exception, "Out of order submitted date"):
            check_story_submitted_order(invalid_data)

    def test_out_of_order_chronological_number(self):
        """Tests detection of out-of-order chronological numbers."""
        invalid_data: List[ComicBookInfo] = [
            ComicBookInfo(Titles(2), True, Issues.FC, 1, 1, 1940, 1, 1, 1940),
            # Chrono 1 (out of order)
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 2, 1940),
        ]
        with self.assertRaisesRegex(Exception, "Out of order chronological number"):
            check_story_submitted_order(invalid_data)

    def test_handles_day_minus_one(self):
        """Tests that submitted_day=-1 is handled correctly."""
        data: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, -1, 1, 1940),
            # Same month, later day
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 1, 1940),
            # Later month, day -1
            ComicBookInfo(Titles(2), True, Issues.FC, 3, 3, 1940, -1, 2, 1940),
        ]
        try:
            check_story_submitted_order(data)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception with day=-1: {e}"
            )

        # Check case where -1 makes dates equal (should pass)
        data_equal: List[ComicBookInfo] = [
            ComicBookInfo(Titles(0), True, Issues.FC, 1, 1, 1940, -1, 1, 1940),
            ComicBookInfo(Titles(1), True, Issues.FC, 2, 2, 1940, 1, 1, 1940),
        ]
        try:
            check_story_submitted_order(data_equal)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception"
                f" with day=-1 making dates equal: {e}"
            )
