from __future__ import annotations
import os
import re
from pathlib import Path
from typing import TypedDict

from selectolax.parser import HTMLParser

MOCK_SITES_DIR = Path(__file__).parent.parent / "data" / "mock_sites"


class RawLead(TypedDict):
    company: str
    domain: str
    industry: str
    employee_count: int | None
    location: str
    contact_name: str
    title: str
    email: str
    tech_stack: list[str]
    source_file: str


def _parse_html(html: str, source: str) -> RawLead | None:
    tree = HTMLParser(html)

    def text(selector: str) -> str:
        node = tree.css_first(selector)
        return node.text(strip=True) if node else ""

    company = text(".company-name")
    domain = text(".domain") or text("[class*='domain']")
    industry_raw = text(".industry")
    employees_raw = text(".employees")
    location = text(".location")
    contact_name = text(".contact-name")
    title = text(".contact-title")
    email = text(".contact-email")
    tech_raw = text(".tech-stack p") or text(".tech-stack")

    if not company or not domain:
        return None

    employee_count: int | None = None
    match = re.search(r"(\d[\d,]*)", employees_raw)
    if match:
        employee_count = int(match.group(1).replace(",", ""))

    tech_stack = _extract_tech(tech_raw)
    industry = _clean_industry(industry_raw)

    return RawLead(
        company=company,
        domain=domain.strip(),
        industry=industry,
        employee_count=employee_count,
        location=location,
        contact_name=contact_name,
        title=title,
        email=email,
        tech_stack=tech_stack,
        source_file=source,
    )


_TECH_KEYWORDS = {
    "python", "postgresql", "postgres", "aws", "react", "fastapi",
    "kubernetes", "docker", "go", "rust", "node.js", "nodejs",
    "java", "mysql", "php", "redis", "kafka", "spark", "dbt",
    "terraform", "prometheus", "react", "typescript",
}


def _extract_tech(raw: str) -> list[str]:
    found = []
    lower = raw.lower()
    for kw in _TECH_KEYWORDS:
        if kw in lower:
            found.append(kw if kw != "postgresql" else "postgres")
    return sorted(set(found))


def _clean_industry(raw: str) -> str:
    first_part = raw.split("/")[0].strip()
    return first_part.lower() if first_part else raw.lower()


def scrape_mock() -> list[RawLead]:
    results: list[RawLead] = []
    for html_file in sorted(MOCK_SITES_DIR.glob("*.html")):
        html = html_file.read_text(encoding="utf-8")
        lead = _parse_html(html, html_file.name)
        if lead:
            results.append(lead)
    return results


def scrape_urls(urls: list[str]) -> list[RawLead]:
    import httpx

    results: list[RawLead] = []
    with httpx.Client(timeout=15) as client:
        for url in urls:
            try:
                resp = client.get(url, follow_redirects=True)
                resp.raise_for_status()
                lead = _parse_html(resp.text, url)
                if lead:
                    results.append(lead)
            except Exception:
                continue
    return results


