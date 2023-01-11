import unittest
from cronee import CroneeAliasError
from cronee.parser import parse_alias


class TestParseAlias(unittest.TestCase):
    def test_valid_input(self):
        values = parse_alias('ALI', {'ALI': {5}})
        self.assertEqual({5}, values)

    def test_alias_error(self):
        with self.assertRaises(CroneeAliasError):
            parse_alias('UNK', {})
        with self.assertRaises(CroneeAliasError):
            parse_alias('UNK', {})
