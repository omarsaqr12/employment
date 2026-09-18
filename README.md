# Employment data-model and job-page parsing prototype

An **unfinished prototype repository** exploring an employment-platform relational schema and extraction of fields from Wuzzuf job listings. It is not a deployed job board, a running database-backed application, or a validated current Wuzzuf scraper.

## What is here

- [`1/schema (1).sql`](1/schema%20(1).sql): original employment-platform SQL design (companies, jobs, applicants, education, skills and applications). **Historical design; see integrity limitations below.**
- [`1/erd.png`](1/erd.png) and [`1/to help me draw schema.pdf`](1/to%20help%20me%20draw%20schema.pdf): original design materials, retained without alteration.
- [`job_parser.py`](job_parser.py): testable extraction of job title, experience, career/education levels, salary text, description and requirements from **saved HTML** using historical selectors. Missing fields are explicit in the output.
- [`scrapcode.py`](scrapcode.py): offline command-line entry point. The original unfinished live Selenium experiment is preserved unchanged at [`legacy/scrapcode.py`](legacy/scrapcode.py); do not import or execute it unintentionally, because it starts a browser and accesses a third-party website at import time.
- [`tests/test_job_parser.py`](tests/test_job_parser.py): synthetic, offline regression tests for expected and missing-field cases.

## Quickstart: inspect a page you already have permission to save

```bash
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scrapcode.py path/to/saved_job_page.html
```

The last command prints a JSON record. It makes **no network requests** and neither stores records in a database nor verifies today's page markup. Only extract information you are authorized to access, and respect the site's terms and privacy requirements. The original script's Selenium, Chrome and driver-manager dependencies are intentionally not included in the offline quickstart.

## Engineering status and important limitations

1. The **original SQL schema is not migration-ready**. `company` has a three-column primary key, but `c_location.c_name` references only the non-unique name. Similar standalone references to `job.job_requirements` do not match the job's composite primary key. On a database enforcing foreign keys, affected writes can raise `foreign key mismatch`; see [SQLite's foreign-key requirements](https://www.sqlite.org/foreignkeys.html). The SQL is preserved as a design artifact, not claimed to be a validated database deployment.
2. The legacy scraper relies on older CSS class names and a single hard-coded job URL; its selectors have **not** been checked against current Wuzzuf pages. The offline parser tests exercise synthetic examples of the historical structure, not live-site compatibility.
3. No API, user authentication, job ingestion pipeline, persistent scraped dataset, or completed web application is provided. The scraper and schema have **not** been integrated.
4. No original project brief or verified contribution breakdown was available. Ownership and production results are not inferred.

## Next engineering milestones

Design and review a versioned schema with stable surrogate company/job identifiers and complete foreign keys; test it using a disposable SQLite database with foreign keys enabled. Only then consider integrating an authorized collection pipeline with stored fixtures, error handling, rate limits, and privacy review. No live scraping or database migration was performed in this change.
