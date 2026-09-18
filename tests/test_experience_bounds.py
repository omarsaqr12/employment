"""Regression tests for open-ended experience labels in saved job pages."""
import unittest

from job_parser import parse_experience


class ExperienceBoundsTests(unittest.TestCase):
    def test_plus_means_at_least(self):
        self.assertEqual(parse_experience("3+ years"), (3, None, "at_least"))

    def test_or_more_means_at_least(self):
        self.assertEqual(parse_experience("5 or more years"), (5, None, "at_least"))


if __name__ == "__main__":
    unittest.main()
