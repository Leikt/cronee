import unittest

from cronee import parse_expression
from helpers import easy_datetime


class TestSimpleCroneeNextOccurrence(unittest.TestCase):
    def test_dummy_expression(self):
        c = parse_expression('* * * * *')
        dtime = easy_datetime()
        self.assertEqual(dtime, c.next_occurrence(dtime))

    def test_simple_expression(self):
        c = parse_expression('35 10 * * *')
        dtime = c.next_occurrence(easy_datetime(hour=1, minute=5))
        self.assertEqual(easy_datetime(hour=10, minute=35), dtime)

    def test_simple_expression_large_computation(self):
        c = parse_expression('* * 31 12 *')
        dtime = c.next_occurrence(easy_datetime(month=1, day=1))
        self.assertEqual(easy_datetime(hour=0, minute=0, day=31, month=12), dtime)
