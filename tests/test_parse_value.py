import unittest
from cronee.parser import parse_value
from cronee import CroneeValueError, CroneeAliasError, CroneeOutOfBoundError


class TestParseValue(unittest.TestCase):
    def test_joker(self):
        values = parse_value('*', {1, 2, 3, 4, 5, 6})
        self.assertEqual({1, 2, 3, 4, 5, 6}, values)

    def test_numerical(self):
        values = parse_value('12', set(range(0, 100)))
        self.assertEqual({12}, values)

    def test_aliases(self):
        values = parse_value('KEY', {0}, {'KEY': {0}})
        self.assertEqual({0}, values)

    def test_syntax_error(self):
        with self.assertRaises(CroneeValueError):
            parse_value('*/3', {0})

    def test_alias_error(self):
        with self.assertRaises(CroneeAliasError):
            parse_value('UNK', {0}, {'KEY': {0}})

    def test_out_of_bound_error(self):
        with self.assertRaises(CroneeOutOfBoundError):
            parse_value('12', set(range(0, 10)))
