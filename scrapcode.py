"""Offline entry point for extracting a saved job page.

The unfinished live Selenium experiment is preserved as legacy/scrapcode.py.
No requests to third-party services occur through this entry point.
"""
import argparse
import json
from pathlib import Path

from job_parser import parse_job_dict


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Extract metadata from a saved Wuzzuf HTML page")
    parser.add_argument("html_file", type=Path, help="Local HTML file saved with permission")
    args = parser.parse_args(argv)
    try:
        record = parse_job_dict(args.html_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Cannot parse saved page: {exc}\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
