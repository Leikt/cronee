import unittest
from datetime import datetime

from cronee import CroneeOutOfBoundError
from cronee.parser import parse_index
from cronee.cronee import dow_index_validator


class TestParseIndex(unittest.TestCase):
    def test_valid_input(self):
        validator = parse_index(
            'FRI#2',
            set(range(1, 8)),
            {'FRI': {5}},
            set(range(1, 6)),
            {},
            dow_index_validator
        )
        self.assertTrue(validator(datetime(2023, 1, 13, 8, 0)))
        self.assertFalse(validator(datetime(2023, 1, 14, 8, 0)))

    def test_out_of_bound_index(self):
        with self.assertRaises(CroneeOutOfBoundError):
            parse_index(
                'FRI#22',
                set(range(1, 8)),
                {'FRI': {5}},
                set(range(1, 6)),
                {},
                dow_index_validator)
