import unittest

from cronee import CroneeEmptyValuesError
from cronee.parser import parse_generic_element, parse_field, parse_dow_element


class TestParseField(unittest.TestCase):
    def test_valid_asterisk(self):
        modifier, _, values = parse_field('*', set(range(0, 10)), {}, {}, parse_generic_element)
        self.assertEqual(0, modifier)
        self.assertEqual({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, values)

    def test_valid_positive_modifier(self):
        modifier, _, values = parse_field('5+1', set(range(0, 10)), {}, {}, parse_generic_element)
        self.assertEqual(-1, modifier)
        self.assertEqual({5}, values)

    def test_valid_negative_modifier(self):
        modifier, _, values = parse_field('5-1', set(range(0, 10)), {}, {}, parse_generic_element)
        self.assertEqual(1, modifier)
        self.assertEqual({5}, values)

    def test_valid_inversion(self):
        _, _, values = parse_field('!2..5', set(range(0, 10)), {}, {}, parse_generic_element)
        self.assertEqual({0, 1, 6, 7, 8, 9}, values)

    def test_valid_list(self):
        _, _, values = parse_field('0,1,2,3', set(range(0, 10)), {}, {}, parse_generic_element)
        self.assertEqual({0, 1, 2, 3}, values)

    def test_valid_complex_expression(self):
        modifier, _, values = parse_field('!2..10/2,DEC-3', set(range(1, 13)), {'DEC': {12}}, {}, parse_generic_element)
        self.assertEqual(3, modifier)
        self.assertEqual({1, 3, 5, 7, 9, 11}, values)

    def test_valid_complex_expression_2(self):
        modifier, _, values = parse_field('!*/5,TRIM4,3..5',
                                          set(range(1, 13)),
                                          {'TRIM4': {10, 11, 12}},
                                          {},
                                          parse_generic_element)
        self.assertEqual(0, modifier)
        self.assertEqual({2, 7, 8, 9}, values)

    def test_valid_index_in_list(self):
        modifier, validators, values = parse_field('3,FRI#3,4',
                                                   set(range(1, 8)),
                                                   {'FRI': {5}},
                                                   {},
                                                   parse_dow_element)
        self.assertEqual(0, modifier)
        self.assertEqual({3, 4}, values)
        self.assertEqual(1, len(validators))

    def test_empty_value_error(self):
        with self.assertRaises(CroneeEmptyValuesError):
            parse_field('!*', set(range(0, 10)), {}, {}, parse_generic_element)
