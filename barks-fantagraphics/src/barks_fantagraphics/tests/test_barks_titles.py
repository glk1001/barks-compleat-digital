import unittest
from collections import OrderedDict

from barks_fantagraphics.barks_titles import (
    ComicBookInfo,
    ComicBookInfoDict,
    get_all_comic_book_info,
    check_story_submitted_order,
    # Import the raw data for some tests
    SHORT_ISSUE_NAME,  # Needed for get_issue_title test
    FC,  # Example issue name constant
    US,  # Example issue name constant
)


class TestComicBookInfo(unittest.TestCase):

    def test_get_issue_title(self):
        """Tests the formatting of the issue title."""
        info = ComicBookInfo(
            title="Story A",
            is_barks_title=True,
            issue_name=FC,
            issue_number=178,
            issue_month=12,
            issue_year=1947,
            submitted_day=22,
            submitted_month=7,
            submitted_year=1947,
            chronological_number=77,
        )
        expected_issue_title = f"{SHORT_ISSUE_NAME[FC]} 178"
        self.assertEqual(info.get_short_issue_title(), expected_issue_title)

        info_us = ComicBookInfo(
            title="Story A",
            is_barks_title=False,
            issue_name=US,
            issue_number=31,
            issue_month=9,
            issue_year=1960,
            submitted_day=12,
            submitted_month=2,
            submitted_year=1960,
            chronological_number=455,
        )
        expected_title_us = f"{SHORT_ISSUE_NAME[US]} 31"
        self.assertEqual(info_us.get_short_issue_title(), expected_title_us)


class TestGetAllComicBookInfo(unittest.TestCase):

    def test_returns_ordered_dict(self):
        """Tests if the function returns an OrderedDict."""
        result = get_all_comic_book_info()
        self.assertIsInstance(result, OrderedDict)

    def test_sorted_by_chronological_number(self):
        """Tests if the returned dictionary is sorted correctly."""
        result = get_all_comic_book_info()
        items = list(result.values())
        for i in range(len(items) - 1):
            self.assertEqual(
                items[i].chronological_number + 1,
                items[i + 1].chronological_number,
                f"Chronological order failed between"
                f"  item {i} ('{items[i].get_short_issue_title()}')"
                f" and item {i+1} ('{items[i+1].get_short_issue_title()}')",
            )

    def test_correct_number_of_titles(self):
        result = get_all_comic_book_info()
        items = list(result.values())
        num_titles = len(items)
        self.assertEqual(1, items[0].chronological_number)
        self.assertEqual(num_titles, items[-1].chronological_number)

    def test_story_submitted_order(self):
        try:
            result = get_all_comic_book_info()
            check_story_submitted_order(result)
        except Exception as e:
            self.fail(f"get_all_comic_book_info raised an unexpected exception: {e}")


class TestCheckStorySubmittedOrder(unittest.TestCase):

    def test_valid_order(self):
        """Tests that correctly ordered data passes."""
        valid_data: ComicBookInfoDict = OrderedDict(
            [
                ("Story A", ComicBookInfo("Story A", True, FC, 1, 1, 1940, 1, 1, 1940, 1)),
                ("Story B", ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 2, 1940, 2)),
                (
                    "Story C",
                    ComicBookInfo("Story C", True, FC, 3, 3, 1940, -1, 2, 1940, 3),
                ),  # Day -1 is ok
                ("Story D", ComicBookInfo("Story D", True, FC, 4, 4, 1940, 15, 2, 1940, 4)),
                ("Story E", ComicBookInfo("Story E", True, FC, 5, 5, 1941, 1, 1, 1941, 5)),
            ]
        )
        try:
            check_story_submitted_order(valid_data)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception for valid data: {e}"
            )

    def test_invalid_month(self):
        """Tests detection of invalid submission month."""
        invalid_data: ComicBookInfoDict = OrderedDict(
            [
                ("Story A", ComicBookInfo("Story A", True, FC, 1, 1, 1940, 1, 1, 1940, 1)),
                (
                    "Story B",
                    ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 13, 1940, 2),
                ),  # Invalid month 13
            ]
        )
        with self.assertRaisesRegex(Exception, "Invalid submission month: 13"):
            check_story_submitted_order(invalid_data)

        invalid_data_zero: ComicBookInfoDict = OrderedDict(
            [
                (
                    "Story A",
                    ComicBookInfo("Story A", True, FC, 1, 1, 1940, 1, 0, 1940, 1),
                ),  # Invalid month 0
            ]
        )
        with self.assertRaisesRegex(Exception, "Invalid submission month: 0"):
            check_story_submitted_order(invalid_data_zero)

    def test_out_of_order_submission_date(self):
        """Tests detection of out-of-order submission dates."""
        invalid_data: ComicBookInfoDict = OrderedDict(
            [
                ("Story A", ComicBookInfo("Story A", True, FC, 1, 1, 1940, 15, 2, 1940, 1)),
                (
                    "Story B",
                    ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 2, 1940, 2),
                ),  # Submitted earlier than A
            ]
        )
        with self.assertRaisesRegex(Exception, "Out of order submitted date"):
            check_story_submitted_order(invalid_data)

    def test_out_of_order_chronological_number(self):
        """Tests detection of out-of-order chronological numbers."""
        invalid_data: ComicBookInfoDict = OrderedDict(
            [
                (
                    "Story A",
                    ComicBookInfo("Story A", True, FC, 1, 1, 1940, 1, 1, 1940, 5),
                ),  # Chrono 5
                (
                    "Story B",
                    ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 2, 1940, 2),
                ),  # Chrono 2 (out of order)
            ]
        )
        with self.assertRaisesRegex(Exception, "Out of order chronological number"):
            check_story_submitted_order(invalid_data)

    def test_handles_day_minus_one(self):
        """Tests that submitted_day=-1 is handled correctly."""
        data: ComicBookInfoDict = OrderedDict(
            [
                ("Story A", ComicBookInfo("Story A", True, FC, 1, 1, 1940, -1, 1, 1940, 1)),
                (
                    "Story B",
                    ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 1, 1940, 2),
                ),  # Same month, later day
                (
                    "Story C",
                    ComicBookInfo("Story C", True, FC, 3, 3, 1940, -1, 2, 1940, 3),
                ),  # Later month, day -1
            ]
        )
        try:
            check_story_submitted_order(data)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception with day=-1: {e}"
            )

        # Check case where -1 makes dates equal (should pass)
        data_equal: ComicBookInfoDict = OrderedDict(
            [
                ("Story A", ComicBookInfo("Story A", True, FC, 1, 1, 1940, -1, 1, 1940, 1)),
                ("Story B", ComicBookInfo("Story B", True, FC, 2, 2, 1940, 1, 1, 1940, 2)),
            ]
        )
        try:
            check_story_submitted_order(data_equal)
        except Exception as e:
            self.fail(
                f"check_story_submitted_order raised an unexpected exception"
                f" with day=-1 making dates equal: {e}"
            )
