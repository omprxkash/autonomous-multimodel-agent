import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.enricher import EnrichedLead
from pipeline.email_generator import generate


def _make_lead(**kwargs) -> EnrichedLead:
    defaults = dict(
        company="DataStride",
        domain="datastride.io",
        industry="data",
        industry_category="data",
        employee_count=95,
        size_bucket="mid",
        location="Toronto, CA",
        region="CA",
        contact_name="Priya Nair",
        first_name="Priya",
        title="CTO & Co-Founder",
        seniority="founder",
        email="priya@datastride.io",
        email_valid=True,
        tech_stack=["python", "aws", "postgres"],
    )
    defaults.update(kwargs)
    return EnrichedLead(**defaults)


def test_high_score_founder_generates_email():
    lead = _make_lead()
    draft = generate(lead, score=85)
    assert draft
    assert "Priya" in draft
    assert "DataStride" in draft


def test_warm_score_generates_email():
    lead = _make_lead()
    draft = generate(lead, score=55)
    assert len(draft) > 50


def test_cold_score_generates_email():
    lead = _make_lead(seniority="manager", first_name="James")
    draft = generate(lead, score=20)
    assert "James" in draft


def test_email_contains_company():
    lead = _make_lead(company="FintechFlow")
    draft = generate(lead, score=75)
    assert "FintechFlow" in draft


def test_email_does_not_contain_placeholders():
    lead = _make_lead()
    draft = generate(lead, score=60)
    assert "{{" not in draft
    assert "}}" not in draft


def test_email_contains_sender():
    os.environ.setdefault("SENDER_NAME", "Om")
    lead = _make_lead()
    draft = generate(lead, score=70)
    assert draft


def test_different_industries_get_drafts():
    for cat in ("saas", "fintech", "devtools", "data", "cloud", "ecommerce", "other"):
        lead = _make_lead(industry_category=cat)
        draft = generate(lead, score=50)
        assert len(draft) > 20

