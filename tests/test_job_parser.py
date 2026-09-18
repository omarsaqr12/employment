"""Offline fixtures cover the historical selectors, not today's live website."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from job_parser import parse_experience, parse_job_html


class ParserTests(unittest.TestCase):
    def test_experience_cases(self):
        cases = [
            ("3 to 5 years", (3, 5, "range")),
            ("3-5 Years", (3, 5, "range")),
            ("More than 3 years", (3, None, "more_than")),
            ("3 years", (3, 3, "exact")),
            ("Not Specified", (None, None, None)),
            ("", (None, None, None)),
        ]
        for label, expected in cases:
            with self.subTest(label=label):
                self.assertEqual(parse_experience(label), expected)

    def test_full_page(self):
        html = '''<h1>Software Developer</h1>
        <span class="css-47jx3m"><span>3 to 5 years</span></span>
        <span class="css-47jx3m"><span>Experienced</span></span>
        <span class="css-47jx3m"><span>Bachelor's Degree</span></span>
        <span class="css-47jx3m"><span>Confidential</span></span>
        <div class="css-1uobp1k">Build software.</div>
        <div class="css-1t5f0fr">Python required.</div>'''
        record = parse_job_html(html)
        self.assertEqual(record.title, "Software Developer")
        self.assertEqual((record.experience_min_years, record.experience_max_years), (3, 5))
        self.assertIsNone(record.salary_text)
        self.assertEqual(record.requirements, "Python required.")
        self.assertEqual(record.missing_fields, ["salary_text"])

    def test_missing_fields_not_invented(self):
        record = parse_job_html("<h1>Intern</h1>")
        self.assertIsNone(record.experience_min_years)
        self.assertIn("experience", record.missing_fields)
        self.assertIn("description", record.missing_fields)

    def test_unrecognized_page_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "No job title"):
            parse_job_html("<html><body>Access denied</body></html>")

    def test_cli_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "listing.html"
            path.write_text('<h1>Engineer</h1>', encoding="utf-8")
            proc = subprocess.run([sys.executable, "scrapcode.py", str(path)],
                                  capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(proc.stdout)["title"], "Engineer")


if __name__ == "__main__":
    unittest.main()
