import pytest
from app.services.nlp_detector import analyze_nlp


def _make_email(subject: str = "", body: str = "") -> dict:
    return {
        "subject": subject,
        "body_parts": [{"content_type": "text/plain", "content": body}],
    }


def test_clean_email_scores_low():
    result = analyze_nlp(_make_email("Meeting tomorrow", "Hi, just checking in."))
    assert result["nlp_score"] < 10
    assert result["urgency_hits"] == []


def test_urgency_phrase_detected():
    result = analyze_nlp(_make_email("Urgent", "Act now or your account will be suspended!"))
    assert len(result["urgency_hits"]) > 0
    assert result["nlp_score"] > 0


def test_credential_phrase_detected():
    result = analyze_nlp(_make_email("Verify", "Please enter your password to confirm your credentials."))
    assert len(result["credential_hits"]) > 0


def test_financial_phrase_detected():
    result = analyze_nlp(_make_email("You have won", "Lottery prize money wire transfer unclaimed funds"))
    assert len(result["financial_hits"]) > 0


def test_impersonation_detected():
    result = analyze_nlp(_make_email("IT Support", "Your administrator requires you to update your system."))
    assert len(result["impersonation_hits"]) > 0


def test_html_body_stripped():
    result = analyze_nlp({
        "subject": "",
        "body_parts": [{"content_type": "text/html",
                        "content": "<b>Act now</b> or your account will be suspended!"}],
    })
    assert len(result["urgency_hits"]) > 0


def test_nlp_score_capped():
    body = " ".join(["act now enter your password wire transfer it department you have won"] * 10)
    result = analyze_nlp(_make_email("urgent", body))
    assert result["nlp_score"] <= 60
