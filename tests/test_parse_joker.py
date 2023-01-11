import unittest
from cronee.parser import parse_joker
from cronee import CroneeSyntaxError


class TestParseJoker(unittest.TestCase):
    def test_valid_input(self):
        values = parse_joker({1, 2, 3}, False)
        self.assertEqual({1, 2, 3}, values)

    def test_inversion_error(self):
        with self.assertRaises(CroneeSyntaxError):
            parse_joker({0}, True)
