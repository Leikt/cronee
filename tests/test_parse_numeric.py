import unittest
from cronee.exceptions import CroneeOutOfBoundError
from cronee.parser import parse_numeric


class TestParseNumeric(unittest.TestCase):
    def test_valid_input(self):
        values = parse_numeric('12', set(range(0, 50)), False)
        self.assertEqual({12}, values)

    def test_valid_input_inversion(self):
        values = parse_numeric('5', set(range(0, 10)), True)
        self.assertEqual({0, 1, 2, 3, 4, 6, 7, 8, 9}, values)

    def test_out_of_bound_error(self):
        with self.assertRaises(CroneeOutOfBoundError):
            parse_numeric('5', set(range(0, 4)), False)
        with self.assertRaises(CroneeOutOfBoundError):
            parse_numeric('5', set(range(0, 4)), True)
