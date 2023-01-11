import unittest
from cronee import CroneeAliasError
from cronee.parser import parse_alias


class TestParseAlias(unittest.TestCase):
    def test_valid_input(self):
        values = parse_alias('ALI', set(range(0, 10)), {'ALI': {5}}, False)
        self.assertEqual({5}, values)

    def test_valid_input_inversion(self):
        values = parse_alias('ALI', set(range(0, 5)), {'ALI': {3}}, True)
        self.assertEqual({0, 1, 2, 4}, values)

    def test_alias_error(self):
        with self.assertRaises(CroneeAliasError):
            parse_alias('UNK', {0}, {}, False)
        with self.assertRaises(CroneeAliasError):
            parse_alias('UNK', {0}, {}, True)
