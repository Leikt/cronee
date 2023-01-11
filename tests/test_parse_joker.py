import unittest

from cronee.parser import parse_joker


class TestParseJoker(unittest.TestCase):
    def test_valid_input(self):
        values = parse_joker({1, 2, 3})
        self.assertEqual({1, 2, 3}, values)
