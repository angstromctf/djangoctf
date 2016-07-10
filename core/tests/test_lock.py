"""
Test the pre-contest lock and unit-tests for basic functions
"""

from unittest import TestCase
from django.utils.dateparse import parse_datetime
from ..utils import time


class TestTiming(TestCase):
    def test_before_true(self):
        time.contest_start = parse_datetime("2116-02-13 00:00:00-05")
        self.assertTrue(time.before_start())

    def test_before_false(self):
        time.contest_start = parse_datetime("2016-03-13 00:00:00-05")
        self.assertFalse(time.before_start())

    def test_after_true(self):
        time.contest_end = parse_datetime("2016-03-13 00:00:00-05")
        self.assertTrue(time.after_end())

    def test_after_false(self):
        time.contest_end = parse_datetime("2116-02-13 00:00:00-05")
        self.assertFalse(time.after_end())
