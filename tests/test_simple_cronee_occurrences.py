import unittest

from cronee import parse_expression
from helpers import easy_datetime


class TestNextOccurrences(unittest.TestCase):
    def test_dummy(self):
        c = parse_expression('* * * * *')
        occurrences = c.next_occurrences(easy_datetime(year=2023, month=1, day=1, hour=0, minute=0))
        self.assertEqual(
            [
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=1),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=2),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=3),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=4),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=5),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=6),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=7),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=8),
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=9)
            ],
            occurrences
        )

    def test_each_day(self):
        c = parse_expression('0 0 * * *')
        occurrences = c.next_occurrences(easy_datetime(year=2023, month=1, day=1, hour=0, minute=0))
        self.assertEqual(
            [
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=2, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=3, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=4, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=5, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=6, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=7, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=8, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=9, hour=0, minute=0),
                easy_datetime(year=2023, month=1, day=10, hour=0, minute=0)
            ],
            occurrences
        )

    def test_each_month(self):
        c = parse_expression('0 0 1 * *')
        occurrences = c.next_occurrences(easy_datetime(year=2023, month=1, day=1, hour=0, minute=0))
        self.assertEqual(
            [
                easy_datetime(year=2023, month=1, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=2, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=3, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=4, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=5, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=6, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=7, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=8, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=9, day=1, hour=0, minute=0),
                easy_datetime(year=2023, month=10, day=1, hour=0, minute=0)
            ],
            occurrences
        )

    def test_index(self):
        c = parse_expression('0 8 * * FRI#3')
        occurrences = c.next_occurrences(easy_datetime(year=2023, month=1, day=1, hour=0, minute=0), 5)
        self.assertEqual(
            [
                easy_datetime(year=2023, month=1, day=20, hour=8, minute=0),
                easy_datetime(year=2023, month=2, day=17, hour=8, minute=0),
                easy_datetime(year=2023, month=3, day=17, hour=8, minute=0),
                easy_datetime(year=2023, month=4, day=21, hour=8, minute=0),
                easy_datetime(year=2023, month=5, day=19, hour=8, minute=0),
            ],
            occurrences
        )
