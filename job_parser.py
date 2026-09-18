"""Parse saved Wuzzuf job-page HTML. No network or browser activity occurs here.

Selectors reflect the historical page in legacy/scrapcode.py; current Wuzzuf
markup is not verified. Absent fields are reported, not silently fabricated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class JobRecord:
    title: str | None
    experience_min_years: int | None
    experience_max_years: int | None
    experience_relation: str | None
    career_level: str | None
    education_level: str | None
    salary_text: str | None
    description: str | None
    requirements: str | None
    missing_fields: list[str]


def parse_experience(text: str | None) -> tuple[int | None, int | None, str | None]:
    """Parse historical Wuzzuf experience labels without assuming a bound."""
    if not text or text.strip().lower() in {"not specified", "not specified."}:
        return None, None, None
    normalized = " ".join(text.lower().split())
    numbers = [int(n) for n in re.findall(r"\d+", normalized)]
    if not numbers:
        return None, None, None
    if normalized.startswith("more than") or normalized.startswith("over "):
        return numbers[0], None, "more_than"
    if normalized.startswith("at least") or normalized.startswith("minimum"):
        return numbers[0], None, "at_least"
    if len(numbers) >= 2 and (" to " in normalized or "-" in normalized):
        return min(numbers[:2]), max(numbers[:2]), "range"
    if len(numbers) == 1:
        return numbers[0], numbers[0], "exact"
    return None, None, None


def parse_job_html(html: str) -> JobRecord:
    """Extract demonstrable fields from a saved page, with explicit missingness."""
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.select_one("h1")
    title = title_tag.get_text(" ", strip=True) if title_tag else None
    spans = [span.get_text(" ", strip=True) for span in soup.select("span.css-47jx3m > span")]
    if not title and not spans:
        raise ValueError("No job title or historical metadata selectors found")

    def field(index: int) -> str | None:
        if index >= len(spans):
            return None
        value = spans[index].strip()
        return value if value and value.casefold() not in {"not specified", "confidential"} else None

    experience = field(0)
    minimum, maximum, relation = parse_experience(experience)
    description_tag = soup.select_one("div.css-1uobp1k")
    requirements_tag = soup.select_one("div.css-1t5f0fr")
    description = description_tag.get_text(" ", strip=True) if description_tag else None
    requirements = requirements_tag.get_text(" ", strip=True) if requirements_tag else None
    values = {"title": title, "experience": experience, "career_level": field(1),
              "education_level": field(2), "salary_text": field(3),
              "description": description, "requirements": requirements}
    return JobRecord(title, minimum, maximum, relation, field(1), field(2),
                     field(3), description, requirements,
                     [name for name, value in values.items() if value is None])


def parse_job_dict(html: str) -> dict:
    """JSON-serializable representation used by the offline CLI."""
    return asdict(parse_job_html(html))
