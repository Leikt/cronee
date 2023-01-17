# import unittest
# from helpers import easy_datetime
# from cronee import parse_expression
# from cronee.cronee import SimpleCronee
#
#
# class TestFieldDelta(unittest.TestCase):
#     def test_minute_simple_expression_equal(self):
#         c: SimpleCronee = parse_expression('30 * * * *')  # NOQA
#         dtime = c.minute_delta(easy_datetime(minute=30, hour=10))
#         self.assertEqual(30, dtime.minute)
#         self.assertEqual(10, dtime.hour)
#
#     def test_minute_simple_expression(self):
#         c: SimpleCronee = parse_expression('30 * * * *')  # NOQA
#         dtime = c.minute_delta(easy_datetime(minute=15, hour=10))
#         self.assertEqual(30, dtime.minute)
#         self.assertEqual(10, dtime.hour)
#
#     def test_minute_simple_expression_goes_next_hour(self):
#         c: SimpleCronee = parse_expression('30 * * * *')  # NOQA
#         dtime = c.minute_delta(easy_datetime(minute=55, hour=10))
#         self.assertEqual(30, dtime.minute)
#         self.assertEqual(11, dtime.hour)
#
#     def test_hour_expression_equal(self):
#         c: SimpleCronee = parse_expression('* 10 * * *')  # NOQA
#         dtime = c.hour_delta(easy_datetime(hour=10, day=12))
#         self.assertEqual(10, dtime.hour)
#         self.assertEqual(12, dtime.day)
#
#     def test_hour_simple_expression(self):
#         c: SimpleCronee = parse_expression('* 10 * * *')  # NOQA
#         dtime = c.hour_delta(easy_datetime(hour=5, day=12))
#         self.assertEqual(10, dtime.hour)
#         self.assertEqual(12, dtime.day)
#
#     def test_hour_simple_expression_goes_next_day(self):
#         c: SimpleCronee = parse_expression('* 10 * * *')  # NOQA
#         dtime = c.hour_delta(easy_datetime(hour=15, day=12))
#         self.assertEqual(10, dtime.hour)
#         self.assertEqual(13, dtime.day)
#
#     def test_dom_simple_expression_equal(self):
#         c: SimpleCronee = parse_expression('* * 20 * *')  # NOQA
#         dtime = c.dom_delta(easy_datetime(day=20, month=3))
#         self.assertEqual(20, dtime.day)
#         self.assertEqual(3, dtime.month)
#
#     def test_dom_simple_expression(self):
#         c: SimpleCronee = parse_expression('* * 20 * *')  # NOQA
#         dtime = c.dom_delta(easy_datetime(day=15, month=3))
#         self.assertEqual(20, dtime.day)
#         self.assertEqual(3, dtime.month)
#
#     def test_dom_simple_expression_goes_next_month(self):
#         c: SimpleCronee = parse_expression('* * 20 * *')  # NOQA
#         dtime = c.dom_delta(easy_datetime(day=25, month=3))
#         self.assertEqual(20, dtime.day)
#         self.assertEqual(4, dtime.month)
#
#         dtime = c.dom_delta(easy_datetime(day=25, month=12, year=2022))
#         self.assertEqual(20, dtime.day)
#         self.assertEqual(1, dtime.month)
#         self.assertEqual(2023, dtime.year)
#
#     def test_dows_simple_expression(self):
#         c: SimpleCronee = parse_expression('* * * * FRI')  # NOQA
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=16))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=20), dtime)
#
#     def test_dows_simple_expression_goes_next_year(self):
#         c: SimpleCronee = parse_expression('* * * * MON')  # NOQA
#         dtime = c.dow_delta(easy_datetime(year=2022, month=12, day=27))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=2), dtime)
#
#     def test_dows_index(self):
#         c: SimpleCronee = parse_expression('* * * * MON#3')  # NOQA
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=1))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=16), dtime)
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=16))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=16), dtime)
#
#     def test_dows_index_goes_next_month(self):
#         c: SimpleCronee = parse_expression('* * * * MON#3') # NOQA
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=17))
#         self.assertEqual(easy_datetime(year=2023, month=2, day=20), dtime)
#
#     def test_dows_index_and_value(self):
#         c: SimpleCronee = parse_expression('* * * * 5,MON#3') # NOQA
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=1))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=6), dtime)
#         dtime = c.dow_delta(easy_datetime(year=2023, month=1, day=14))
#         self.assertEqual(easy_datetime(year=2023, month=1, day=16), dtime)
#
