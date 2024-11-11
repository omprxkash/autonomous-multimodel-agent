import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.enricher import EnrichedLead
from pipeline.icp_scorer import score

MOCK_CONFIG = {
    "weights": {
        "industry_match": 30,
        "size_fit": 25,
        "seniority": 20,
        "tech_match": 15,
        "geo_fit": 10,
    },
    "ideal": {
        "industries": ["saas", "fintech", "devtools", "data", "cloud"],
        "size_min": 50,
        "size_max": 1000,
        "seniorities": ["founder", "ceo", "cto", "vp", "head", "director", "chief"],
        "tech": ["python", "postgres", "aws", "react", "fastapi", "kubernetes", "docker"],
        "regions": ["US", "EU", "UK", "CA"],
    },
}


def _make_lead(**kwargs) -> EnrichedLead:
    defaults = dict(
        company="Acme",
        domain="acme.io",
        industry="SaaS",
        industry_category="saas",
        employee_count=200,
        size_bucket="growth",
        location="San Francisco, US",
        region="US",
        contact_name="Jane Doe",
        first_name="Jane",
        title="VP of Engineering",
        seniority="vp",
        email="jane@acme.io",
        email_valid=True,
        tech_stack=["python", "postgres", "aws", "react"],
    )
    defaults.update(kwargs)
    return EnrichedLead(**defaults)


def test_perfect_lead_scores_high():
    lead = _make_lead()
    result = score(lead, MOCK_CONFIG)
    assert result["score"] >= 80


def test_industry_match_contributes():
    matched = _make_lead(industry_category="saas")
    unmatched = _make_lead(industry_category="ecommerce")
    assert score(matched, MOCK_CONFIG)["score"] > score(unmatched, MOCK_CONFIG)["score"]


def test_industry_match_breakdown():
    lead = _make_lead(industry_category="saas")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["industry_match"]["points"] == 30
    assert result["breakdown"]["industry_match"]["matched"] is True


def test_no_industry_match_zero_points():
    lead = _make_lead(industry_category="ecommerce")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["industry_match"]["points"] == 0


def test_size_in_range_full_points():
    lead = _make_lead(employee_count=300)
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["size_fit"]["points"] == 25


def test_size_below_range_partial():
    lead = _make_lead(employee_count=10)
    result = score(lead, MOCK_CONFIG)
    pts = result["breakdown"]["size_fit"]["points"]
    assert 0 < pts < 25


def test_size_above_range_low():
    lead = _make_lead(employee_count=5000)
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["size_fit"]["points"] < 10


def test_founder_seniority_full_points():
    lead = _make_lead(seniority="founder")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["seniority"]["points"] == 20


def test_ic_seniority_zero_points():
    lead = _make_lead(seniority="ic")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["seniority"]["points"] == 0


def test_tech_overlap_partial():
    lead = _make_lead(tech_stack=["python"])
    result = score(lead, MOCK_CONFIG)
    pts = result["breakdown"]["tech_match"]["points"]
    assert 0 < pts < 15


def test_tech_no_overlap():
    lead = _make_lead(tech_stack=["java", "mysql"])
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["tech_match"]["points"] == 0


def test_geo_us_full_points():
    lead = _make_lead(region="US")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["geo_fit"]["points"] == 10


def test_geo_other_zero():
    lead = _make_lead(region="OTHER")
    result = score(lead, MOCK_CONFIG)
    assert result["breakdown"]["geo_fit"]["points"] == 0


def test_score_capped_at_100():
    lead = _make_lead()
    result = score(lead, MOCK_CONFIG)
    assert result["score"] <= 100


def test_score_non_negative():
    lead = _make_lead(
        industry_category="ecommerce",
        employee_count=10000,
        seniority="ic",
        tech_stack=[],
        region="OTHER",
    )
    result = score(lead, MOCK_CONFIG)
    assert result["score"] >= 0


def test_breakdown_keys_present():
    lead = _make_lead()
    result = score(lead, MOCK_CONFIG)
    for key in ("industry_match", "size_fit", "seniority", "tech_match", "geo_fit"):
        assert key in result["breakdown"]

