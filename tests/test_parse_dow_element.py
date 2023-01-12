import unittest
from datetime import datetime

from cronee.parser import parse_dow_element


class TestParseGenericElement(unittest.TestCase):
    def test_valid_numeric(self):
        _, values = parse_dow_element('10', set(range(0, 100)), {})
        self.assertEqual({10}, values)

    def test_valid_asterisk(self):
        _, values = parse_dow_element('*', set(range(0, 10)), {})
        self.assertEqual({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, values)

    def test_valid_range(self):
        _, values = parse_dow_element('5..10', set(range(1, 12)), {})
        self.assertEqual({5, 6, 7, 8, 9, 10}, values)

    def test_valid_asterisk_step(self):
        _, values = parse_dow_element('*/5', set(range(1, 25)), {})
        self.assertEqual({1, 6, 11, 16, 21}, values)

    def test_valid_range_step(self):
        _, values = parse_dow_element('5..20/7', set(range(0, 60)), {})
        self.assertEqual({5, 12, 19}, values)

    def test_valid_alias(self):
        _, values = parse_dow_element('FRI', set(range(1, 8)), {'FRI': {5}})
        self.assertEqual({5}, values)

    def test_valid_index(self):
        validator, values = parse_dow_element('FRI#2', set(range(1, 8)), {'FRI': {5}})
        self.assertEqual(set(), values)
        self.assertTrue(validator(datetime(2023, 1, 13, 8, 0)))
        self.assertFalse(validator(datetime(2023, 1, 14, 8, 0)))
