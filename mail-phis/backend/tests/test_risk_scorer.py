import pytest
from app.services.risk_scorer import calculate_risk_score, RiskScoringResult

def test_clean_email_is_safe():
    features = {
        "spf_pass": 1.0, "dkim_pass": 1.0, "dmarc_pass": 1.0,
        "authentication_all_pass": 1.0, "domain_age_days": 1000.0,
        "has_unsubscribe_link": 1.0,
    }
    result = calculate_risk_score(features)
    assert result.verdict == "SAFE"
    assert result.risk_score < 20

def test_threat_feed_hit_is_phishing():
    features = {"openphish_match": 1.0}
    result = calculate_risk_score(features)
    assert result.verdict == "PHISHING"
    assert result.risk_score >= 75

def test_content_only_nlp_capped_at_suspicious():
    features = {
        "urgency_keyword_count": 5.0,
        "credential_request_keywords": 3.0,
        "financial_request_keywords": 2.0,
        "threat_language_score": 1.0,
    }
    result = calculate_risk_score(features)
    assert result.verdict in ("MARKETING", "SUSPICIOUS")
    assert result.risk_score < 75, "Content-only signals must not reach PHISHING"

def test_auth_failure_raises_score():
    features = {"dmarc_fail": 1.0, "dkim_fail": 1.0, "spf_fail": 1.0}
    result = calculate_risk_score(features)
    assert result.risk_score > 20

def test_newly_registered_domain_is_high_risk():
    features = {"domain_very_recent": 1.0, "dmarc_fail": 1.0}
    result = calculate_risk_score(features)
    assert result.risk_score >= 50

def test_executable_attachment_raises_risk():
    features = {"has_executable_attachment": 1.0, "dkim_fail": 1.0}
    result = calculate_risk_score(features)
    assert result.risk_score >= 50

def test_trust_signals_reduce_score():
    features = {
        "urgency_keyword_count": 3.0,
        "spf_pass": 1.0, "dkim_pass": 1.0, "dmarc_pass": 1.0,
        "authentication_all_pass": 1.0,
        "has_unsubscribe_link": 1.0,
        "bulk_mail_indicator": 1.0,
        "domain_age_days": 500.0,
    }
    result = calculate_risk_score(features)
    assert result.verdict in ("SAFE", "MARKETING")

def test_top_contributors_present():
    features = {"openphish_match": 1.0, "dmarc_fail": 1.0}
    result = calculate_risk_score(features)
    assert len(result.top_contributors) > 0
    assert all("feature_name" in c for c in result.top_contributors)

def test_indicators_sorted_by_severity():
    features = {"openphish_match": 1.0, "url_shortened": 1.0}
    result = calculate_risk_score(features)
    severities = [i["severity"] for i in result.indicators]
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    assert severities == sorted(severities, key=lambda s: order.get(s, 4))
