import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.scraper import scrape_mock
from pipeline.enricher import enrich_all
from pipeline.icp_scorer import score_all
from pipeline.email_generator import generate


def test_scrape_mock_returns_leads():
    leads = scrape_mock()
    assert len(leads) >= 5


def test_scraped_leads_have_required_fields():
    leads = scrape_mock()
    for lead in leads:
        assert lead["company"], f"Missing company in {lead['source_file']}"
        assert lead["domain"], f"Missing domain in {lead['source_file']}"


def test_enrich_all_produces_enriched_leads():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    assert len(enriched) == len(raws)


def test_enriched_has_seniority():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    for e in enriched:
        assert e.seniority in (
            "founder", "vp", "head", "director", "manager", "lead", "ic", "chief", "unknown"
        )


def test_score_all_returns_valid_scores():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    scored = score_all(enriched)
    assert len(scored) == len(enriched)
    for _, result in scored:
        assert 0 <= result["score"] <= 100


def test_score_breakdown_has_all_factors():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    scored = score_all(enriched)
    for _, result in scored:
        for factor in ("industry_match", "size_fit", "seniority", "tech_match", "geo_fit"):
            assert factor in result["breakdown"]


def test_email_generated_for_all_leads():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    scored = score_all(enriched)
    for e, result in scored:
        draft = generate(e, result["score"])
        assert draft and len(draft) > 10


def test_saas_company_scores_above_cold():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    scored = score_all(enriched)
    saas_scores = [
        r["score"] for e, r in scored if e.industry_category == "saas"
    ]
    if saas_scores:
        assert max(saas_scores) > 30


def test_enterprise_company_lower_size_score():
    raws = scrape_mock()
    enriched = enrich_all(raws)
    big = [e for e in enriched if e.employee_count and e.employee_count > 1000]
    if big:
        scored = score_all(big)
        for _, result in scored:
            assert result["breakdown"]["size_fit"]["points"] < 25


def test_no_duplicate_domains():
    raws = scrape_mock()
    domains = [r["domain"] for r in raws]
    assert len(domains) == len(set(domains)), "Duplicate domains found in mock sites"


