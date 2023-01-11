import unittest
from cronee.parser import parse_inversion


class TestParseInversion(unittest.TestCase):
    def test_valid_input(self):
        inversion, expression = parse_inversion('!12,15')
        self.assertTrue(inversion)
        self.assertEqual('12,15', expression)

    def test_no_inversion(self):
        inversion, expression = parse_inversion('12,15')
        self.assertFalse(inversion)
        self.assertEqual('12,15', expression)
