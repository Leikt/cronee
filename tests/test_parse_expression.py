import unittest
from datetime import timedelta

from cronee import parse_expression
from cronee.cronee import SimpleCronee


class TestParseExpression(unittest.TestCase):
    def test_dummy_expression(self):
        c: SimpleCronee = parse_expression('* * * * *')  # NOQA
        self.assertEqual(set(range(0, 60)), c.minutes)
        self.assertEqual(set(range(0, 24)), c.hours)
        self.assertEqual(set(range(1, 32)), c.doms)
        self.assertEqual(set(range(1, 13)), c.months)
        self.assertEqual(set(range(1, 8)), c.dows)
        self.assertEqual([[], [], [], [], []], c.other_validators)
        self.assertEqual(timedelta(), c.offset)

    def test_numerical_expression(self):
        c: SimpleCronee = parse_expression('5 6 8 10 2')  # NOQA
        self.assertEqual({5}, c.minutes)
        self.assertEqual({6}, c.hours)
        self.assertEqual({8}, c.doms)
        self.assertEqual({10}, c.months)
        self.assertEqual({2}, c.dows)
        self.assertEqual([[], [], [], [], []], c.other_validators)
        self.assertEqual(timedelta(), c.offset)

    def test_range_expression(self):
        c: SimpleCronee = parse_expression('5..30 6..8 8..10 3..11 2..4')  # NOQA
        self.assertEqual(set(range(5, 31)), c.minutes)
        self.assertEqual(set(range(6, 9)), c.hours)
        self.assertEqual(set(range(8, 11)), c.doms)
        self.assertEqual(set(range(3, 12)), c.months)
        self.assertEqual(set(range(2, 5)), c.dows)
        self.assertEqual([[], [], [], [], []], c.other_validators)
        self.assertEqual(timedelta(), c.offset)

    def test_modifiers(self):
        c: SimpleCronee = parse_expression('5-1 3+5 2+3 1+2 2+3')  # NOQA
        self.assertEqual(timedelta(days=3 + 3, minutes=-1, hours=5), c.offset)

    def test_index(self):
        c: SimpleCronee = parse_expression('* * * * FRI#3')  # NOQA
        self.assertEqual(1, len(c.other_validators[4]))
