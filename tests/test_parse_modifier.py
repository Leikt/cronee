import unittest

from cronee import CroneeSyntaxError, CroneeValueError
from cronee.parser import parse_modifier, parse_modifiers, KEYWORD_NEGATIVE_MODIFIER, KEYWORD_POSITIVE_MODIFIER


class TestParseModifier(unittest.TestCase):
    def test_valid_negative_input(self):
        modifier, expression = parse_modifier('10-5', -1, KEYWORD_NEGATIVE_MODIFIER, {})
        self.assertEqual('10', expression)
        self.assertEqual(-5, modifier)

    def test_valid_positive_input(self):
        modifier, expression = parse_modifier('10+5', 1, KEYWORD_POSITIVE_MODIFIER, {})
        self.assertEqual('10', expression)
        self.assertEqual(5, modifier)

    def test_syntax_error(self):
        with self.assertRaises(CroneeSyntaxError):
            parse_modifier('10++5', 1, KEYWORD_POSITIVE_MODIFIER, {})
        with self.assertRaises(CroneeSyntaxError):
            parse_modifier('10-2-5', 1, KEYWORD_NEGATIVE_MODIFIER, {})

    def test_value_error(self):
        with self.assertRaises(CroneeValueError):
            parse_modifier(f'10+ALI', 1, KEYWORD_POSITIVE_MODIFIER, {'ALI': {0, 1}})

    def test_valid_input(self):
        modifier, expression = parse_modifiers('10+2', {})
        self.assertEqual(2, modifier)
        self.assertEqual('10', expression)

        modifier, expression = parse_modifiers('10-2', {})
        self.assertEqual(-2, modifier)
        self.assertEqual('10', expression)
