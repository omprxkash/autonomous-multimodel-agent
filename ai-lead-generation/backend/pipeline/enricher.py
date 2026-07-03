from __future__ import annotations
import re
from dataclasses import dataclass
from pipeline.scraper import RawLead


@dataclass
class EnrichedLead:
    company: str
    domain: str
    industry: str
    industry_category: str
    employee_count: int | None
    size_bucket: str
    location: str
    region: str
    contact_name: str
    first_name: str
    title: str
    seniority: str
    email: str
    email_valid: bool
    tech_stack: list[str]


_INDUSTRY_MAP = {
    "saas": "saas",
    "fintech": "fintech",
    "payments": "fintech",
    "data": "data",
    "analytics": "data",
    "developer tools": "devtools",
    "devops": "devtools",
    "devtools": "devtools",
    "cloud": "cloud",
    "infrastructure": "cloud",
    "cybersecurity": "saas",
    "hr tech": "saas",
    "e-commerce": "ecommerce",
    "retail": "ecommerce",
}

_SENIORITY_KEYWORDS = {
    "founder": "founder",
    "co-founder": "founder",
    "ceo": "founder",
    "cto": "founder",
    "chief": "founder",
    "vp": "vp",
    "vice president": "vp",
    "head": "head",
    "director": "director",
    "manager": "manager",
    "lead": "lead",
    "engineer": "ic",
    "coordinator": "ic",
}

_REGION_MAP = {
    "us": "US", "united states": "US", "san francisco": "US", "new york": "US",
    "austin": "US", "chicago": "US",
    "uk": "UK", "united kingdom": "UK", "london": "UK",
    "eu": "EU", "europe": "EU", "berlin": "EU", "amsterdam": "EU",
    "ca": "CA", "canada": "CA", "toronto": "CA",
}


def _size_bucket(count: int | None) -> str:
    if count is None:
        return "unknown"
    if count < 10:
        return "micro"
    if count < 50:
        return "small"
    if count < 200:
        return "mid"
    if count < 1000:
        return "growth"
    return "enterprise"


def _region(location: str) -> str:
    lower = location.lower()
    for key, region in _REGION_MAP.items():
        if key in lower:
            return region
    return "OTHER"


def _seniority(title: str) -> str:
    lower = title.lower()
    for kw, level in _SENIORITY_KEYWORDS.items():
        if kw in lower:
            return level
    return "unknown"


def _industry_category(industry: str) -> str:
    lower = industry.lower()
    for key, cat in _INDUSTRY_MAP.items():
        if key in lower:
            return cat
    return "other"


def _email_valid(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def _first_name(full_name: str) -> str:
    parts = full_name.strip().split()
    return parts[0] if parts else full_name


def enrich(raw: RawLead) -> EnrichedLead:
    return EnrichedLead(
        company=raw["company"],
        domain=raw["domain"],
        industry=raw["industry"],
        industry_category=_industry_category(raw["industry"]),
        employee_count=raw["employee_count"],
        size_bucket=_size_bucket(raw["employee_count"]),
        location=raw["location"],
        region=_region(raw["location"]),
        contact_name=raw["contact_name"],
        first_name=_first_name(raw["contact_name"]),
        title=raw["title"],
        seniority=_seniority(raw["title"]),
        email=raw["email"],
        email_valid=_email_valid(raw["email"]),
        tech_stack=raw["tech_stack"],
    )


def enrich_all(raws: list[RawLead]) -> list[EnrichedLead]:
    return [enrich(r) for r in raws]


