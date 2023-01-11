import unittest
from cronee import CroneeRangeOrderError, CroneeSyntaxError
from cronee.parser import parse_range


class TestParseRange(unittest.TestCase):
    def test_valid_input(self):
        values = parse_range('0..5', set(range(0, 10)), {})
        self.assertEqual({0, 1, 2, 3, 4, 5}, values)

    def test_range_order_error(self):
        with self.assertRaises(CroneeRangeOrderError):
            parse_range('5..0', set(range(0, 10)), {})

    def test_range_with_aliases(self):
        values = parse_range('JAN..JUN', set(range(1, 12)), {'JAN': {1}, 'JUN': {6}})
        self.assertEqual({1, 2, 3, 4, 5, 6}, values)

    def test_syntax_error(self):
        with self.assertRaises(CroneeSyntaxError):
            parse_range('0..5..10', set(), {})
