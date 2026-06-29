"""
Risk Scoring Engine
Dual-bucket scoring: suspicion_score − trust_score, clamped 0–100.
Content-only NLP signals alone cannot produce a PHISHING verdict.
"""
from typing import Dict, List, Tuple, Optional


SUSPICION_WEIGHTS: Dict[str, float] = {
    # Authentication failures
    "spf_fail": 20.0,
    "dkim_fail": 25.0,
    "dmarc_fail": 30.0,
    # Header mismatches
    "reply_to_mismatch": 15.0,
    "return_path_mismatch": 5.0,
    "sender_domain_mismatch": 10.0,
    # URL structural
    "url_length": 0.04,
    "num_subdomains": 3.0,
    "contains_ip_address": 30.0,
    "url_shortened": 8.0,
    "url_entropy_score": 3.0,
    "username_in_url": 15.0,
    # URL obfuscation
    "percent_encoding_count": 2.0,
    "double_slash_redirect": 10.0,
    "mixed_case_domain": 5.0,
    # Domain age (tiered)
    "domain_very_recent": 40.0,
    "domain_recent_registration": 25.0,
    # Threat intelligence
    "openphish_match": 50.0,
    "phishtank_match": 50.0,
    "urlhaus_match": 50.0,
    "domain_blacklisted": 50.0,
    "ip_blacklisted": 40.0,
    "country_risk_score": 10.0,
    # Brand impersonation
    "brand_sender_domain_mismatch": 30.0,
    "brand_homograph_detected": 30.0,
    # Redirect behaviour
    "redirect_count": 3.0,
    "final_domain_mismatch": 15.0,
    "redirect_to_ip": 12.0,
    "meta_refresh_detected": 8.0,
    # NLP / content (content-only — see CONTENT_ONLY_FEATURES)
    "urgency_keyword_count": 5.0,
    "credential_request_keywords": 10.0,
    "financial_request_keywords": 5.0,
    "security_alert_keywords": 5.0,
    "threat_language_score": 10.0,
    "imperative_language_score": 5.0,
    "webmail_phishing_phrase_count": 15.0,
    "helpdesk_impersonation_detected": 25.0,
    "generic_anchor_link_detected": 20.0,
    # Attachment risk
    "has_executable_attachment": 40.0,
    "has_script_attachment": 35.0,
    "has_macro_document": 35.0,
    "double_extension_detected": 40.0,
    "mime_mismatch_detected": 15.0,
    "archive_with_executable": 30.0,
    # Email structure
    "javascript_in_email": 15.0,
    "hidden_links_detected": 12.0,
    "num_forms": 8.0,
    # Display name spoofing
    "display_name_brand_spoofing": 35.0,
}

TRUST_WEIGHTS: Dict[str, float] = {
    "spf_pass": 10.0,
    "dkim_pass": 15.0,
    "dmarc_pass": 20.0,
    "authentication_all_pass": 15.0,
    "bulk_mail_indicator": 15.0,
    "esp_detected": 10.0,
    "brand_sender_domain_match": 10.0,
    "url_domain_matches_sender": 10.0,
    "url_domain_subdomain_of_sender": 10.0,
    "url_domain_cdn": 5.0,
    "has_unsubscribe_link": 5.0,
    "has_tracking_pixel": 5.0,
    "marketing_template_signals": 5.0,
    "domain_age_days": 0.01,  # capped at 30
}

# NLP signals that cannot alone push verdict to PHISHING
CONTENT_ONLY_FEATURES = {
    "urgency_keyword_count",
    "credential_request_keywords",
    "financial_request_keywords",
    "security_alert_keywords",
    "threat_language_score",
    "imperative_language_score",
    "webmail_phishing_phrase_count",
    "helpdesk_impersonation_detected",
    "generic_anchor_link_detected",
}

SEVERITY_MAP: Dict[str, str] = {
    "openphish_match": "CRITICAL",
    "phishtank_match": "CRITICAL",
    "urlhaus_match": "CRITICAL",
    "domain_blacklisted": "CRITICAL",
    "ip_blacklisted": "HIGH",
    "domain_very_recent": "HIGH",
    "domain_recent_registration": "HIGH",
    "reply_to_mismatch": "HIGH",
    "brand_homograph_detected": "HIGH",
    "brand_sender_domain_mismatch": "HIGH",
    "has_executable_attachment": "HIGH",
    "double_extension_detected": "HIGH",
    "contains_ip_address": "HIGH",
    "dmarc_fail": "HIGH",
    "display_name_brand_spoofing": "HIGH",
    "webmail_phishing_phrase_count": "HIGH",
    "helpdesk_impersonation_detected": "HIGH",
    "generic_anchor_link_detected": "HIGH",
    "spf_fail": "MEDIUM",
    "dkim_fail": "MEDIUM",
    "url_shortened": "MEDIUM",
    "username_in_url": "MEDIUM",
    "credential_request_keywords": "MEDIUM",
    "financial_request_keywords": "MEDIUM",
    "has_macro_document": "MEDIUM",
    "javascript_in_email": "MEDIUM",
    "final_domain_mismatch": "MEDIUM",
    "hidden_links_detected": "MEDIUM",
    "url_domain_unrelated_to_sender": "MEDIUM",
    "urgency_keyword_count": "LOW",
    "mixed_case_domain": "LOW",
    "percent_encoding_count": "LOW",
    "sender_domain_mismatch": "LOW",
    "country_risk_score": "LOW",
}


class RiskScoringResult:
    def __init__(self):
        self.risk_score: float = 0.0
        self.suspicion_score: float = 0.0
        self.trust_score: float = 0.0
        self.verdict: str = "SAFE"
        self.indicators: List[Dict] = []
        self.top_contributors: List[Dict] = []


def calculate_risk_score(features: Dict[str, float], context: Optional[Dict] = None) -> RiskScoringResult:
    """
    Dual-bucket risk scoring.
    risk_score = suspicion_score − trust_score, clamped 0–100.
    NLP-only signals cap effective score at SUSPICIOUS (< 75).
    """
    result = RiskScoringResult()

    suspicion_contributions: List[Tuple[str, float]] = []
    trust_contributions: List[Tuple[str, float]] = []

    raw_suspicion = 0.0
    for name, weight in SUSPICION_WEIGHTS.items():
        value = features.get(name, 0.0)
        if value == 0.0:
            continue
        contrib = weight * value
        raw_suspicion += contrib
        suspicion_contributions.append((name, contrib))

    raw_trust = 0.0
    for name, weight in TRUST_WEIGHTS.items():
        value = features.get(name, 0.0)
        if value == 0.0:
            continue
        contrib = weight * value
        if name == "domain_age_days":
            contrib = min(contrib, 30.0)
        raw_trust += contrib
        trust_contributions.append((name, -contrib))

    result.suspicion_score = round(raw_suspicion, 2)
    result.trust_score = round(raw_trust, 2)

    # Content-only protection: NLP signals alone cannot yield PHISHING
    non_content_suspicion = sum(
        c for n, c in suspicion_contributions if n not in CONTENT_ONLY_FEATURES
    )
    if non_content_suspicion == 0.0 and raw_suspicion > 0:
        raw_suspicion = min(raw_suspicion, 74.0)

    result.risk_score = max(0.0, min(100.0, raw_suspicion - raw_trust))

    if result.risk_score >= 75:
        result.verdict = "PHISHING"
    elif result.risk_score >= 50:
        result.verdict = "SUSPICIOUS"
    elif result.risk_score >= 20:
        result.verdict = "MARKETING"
    else:
        result.verdict = "SAFE"

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    for name, contrib in suspicion_contributions:
        if contrib > 0:
            severity = SEVERITY_MAP.get(name, "LOW")
            result.indicators.append({
                "indicator_type": name,
                "severity": severity,
                "score_contribution": round(contrib, 2),
                "confidence": min(abs(contrib) / 50.0, 1.0),
            })
    result.indicators.sort(key=lambda x: severity_order.get(x["severity"], 4))

    all_contribs = suspicion_contributions + trust_contributions
    all_contribs.sort(key=lambda x: abs(x[1]), reverse=True)
    result.top_contributors = [
        {
            "feature_name": n,
            "attribution_score": round(s, 2),
            "direction": "phishing" if s > 0 else "safe",
        }
        for n, s in all_contribs[:10]
    ]

    return result


# ---------------------------------------------------------------------------
# Human-readable indicator detail builder
# ---------------------------------------------------------------------------

_DETAIL_TEMPLATES: Dict[str, str] = {
    "spf_fail": "SPF record check failed — sender's IP is not authorised by the domain's SPF policy.",
    "dkim_fail": "DKIM signature verification failed — message content may have been tampered with in transit.",
    "dmarc_fail": "DMARC policy check failed — neither SPF nor DKIM alignment passes for this domain.",
    "reply_to_mismatch": "Reply-To address differs from the From address — replies will go to a different domain.",
    "contains_ip_address": "URL contains a raw IP address instead of a domain name, a common evasion technique.",
    "url_shortened": "URL uses a shortening service that hides the true destination.",
    "domain_very_recent": "Sending domain was registered less than 7 days ago — very high-risk registration pattern.",
    "domain_recent_registration": "Sending domain was registered within the last 30 days.",
    "openphish_match": "URL matched an entry in the OpenPhish live phishing feed.",
    "phishtank_match": "URL is listed as a verified phishing site in the PhishTank database.",
    "urlhaus_match": "URL appears in the URLhaus malware distribution feed.",
    "domain_blacklisted": "Domain is listed in one or more threat intelligence feeds.",
    "ip_blacklisted": "Originating IP address has a high AbuseIPDB confidence score (≥ 50).",
    "brand_sender_domain_mismatch": "Sender domain appears to impersonate a known brand via typosquatting.",
    "brand_homograph_detected": "Domain contains Unicode characters that visually resemble ASCII letters (homograph attack).",
    "has_executable_attachment": "Email contains an attachment with an executable extension (.exe, .msi, .bat, etc.).",
    "has_macro_document": "Attachment is a macro-enabled Office document (.docm, .xlsm, .pptm).",
    "double_extension_detected": "Attachment filename uses a double extension (e.g. invoice.pdf.exe) to disguise its type.",
    "display_name_brand_spoofing": "Display name in the From header impersonates a known brand while using a different domain.",
    "urgency_keyword_count": "Message body contains urgency-inducing language (e.g. 'act now', 'immediately', 'urgent').",
    "credential_request_keywords": "Message explicitly requests credentials, passwords, or account verification.",
    "financial_request_keywords": "Message contains financial lure language (wire transfer, payment, invoice).",
    "javascript_in_email": "HTML body contains JavaScript, which is not rendered by email clients but can exfiltrate data.",
    "hidden_links_detected": "HTML body contains links styled with display:none or visibility:hidden.",
    "redirect_count": "URL goes through one or more HTTP redirects before reaching the final destination.",
    "final_domain_mismatch": "The final URL domain after redirects differs from the initial domain.",
    "meta_refresh_detected": "HTML body uses a meta-refresh tag to redirect the browser automatically.",
}


def _build_detail(indicator_type: str) -> str:
    """Return a human-readable explanation for an indicator type."""
    return _DETAIL_TEMPLATES.get(
        indicator_type,
        f"Suspicious signal detected: {indicator_type.replace('_', ' ')}.",
    )


def enrich_indicators(indicators: List[Dict]) -> List[Dict]:
    """Add human-readable 'detail' field to each indicator dict."""
    for ind in indicators:
        ind.setdefault("detail", _build_detail(ind.get("indicator_type", "")))
    return indicators


# Legacy dict interface used by existing tasks.py
def compute_score(
    header_results: dict,
    auth_results: dict,
    url_results: dict | None,
    domain_results: dict | None,
    threat_results: dict | None,
    nlp_results: dict,
    attachment_results: list,
) -> dict:
    """Map legacy service outputs to features and run dual-bucket scoring."""
    features: Dict[str, float] = {}

    # Auth
    spf = auth_results.get("spf", {}).get("result", "none")
    dkim = auth_results.get("dkim", {}).get("result", "none")
    dmarc = auth_results.get("dmarc", {}).get("result", "none")
    features["spf_pass"] = float(spf == "pass")
    features["dkim_pass"] = float(dkim == "pass")
    features["dmarc_pass"] = float(dmarc == "pass")
    features["spf_fail"] = float(spf == "fail")
    features["dkim_fail"] = float(dkim == "fail")
    features["dmarc_fail"] = float(dmarc == "fail")
    features["authentication_all_pass"] = float(spf == "pass" and dkim == "pass" and dmarc == "pass")
    features["reply_to_mismatch"] = float(header_results.get("reply_to_mismatch", False))
    features["display_name_brand_spoofing"] = float(auth_results.get("display_name_spoof", False))

    # URL
    if url_results:
        features["url_length"] = float(url_results.get("url_length", 0))
        features["num_subdomains"] = float(url_results.get("subdomain_depth", 0))
        features["contains_ip_address"] = float(url_results.get("has_ip_host", False))
        features["url_entropy_score"] = float(url_results.get("path_entropy", 0))
        features["percent_encoding_count"] = float(url_results.get("obfuscation_count", 0))
        features["redirect_count"] = float(url_results.get("redirect_count", 0))
        features["final_domain_mismatch"] = float(
            url_results.get("final_url", "") != url_results.get("original_url", "")
            and url_results.get("redirect_count", 0) > 0
        )
        features["javascript_in_email"] = 0.0

    # Domain
    if domain_results:
        age = domain_results.get("age_days")
        if age is not None:
            features["domain_age_days"] = float(age)
            features["domain_very_recent"] = float(age < 7)
            features["domain_recent_registration"] = float(7 <= age < 30)
        features["brand_homograph_detected"] = float(domain_results.get("homograph", False))
        typosquat = domain_results.get("typosquat_target")
        features["brand_sender_domain_mismatch"] = float(typosquat is not None)

    # Threat intel
    if threat_results:
        features["openphish_match"] = float(
            (threat_results.get("openphish") or {}).get("status") == "hit"
        )
        features["phishtank_match"] = float(
            (threat_results.get("phishtank") or {}).get("status") == "hit"
        )
        features["urlhaus_match"] = float(
            (threat_results.get("urlhaus") or {}).get("status") == "hit"
        )
        features["domain_blacklisted"] = float(threat_results.get("any_hit", False))

    # NLP
    features["urgency_keyword_count"] = float(nlp_results.get("urgency_keyword_count", 0))
    features["credential_request_keywords"] = float(nlp_results.get("credential_keyword_count", 0))
    features["financial_request_keywords"] = float(nlp_results.get("financial_keyword_count", 0))
    features["threat_language_score"] = float(nlp_results.get("nlp_score", 0) / 100.0)
    features["imperative_language_score"] = float(
        min(nlp_results.get("exclamation_density", 0) * 5, 1.0)
    )

    # Attachments
    for att in attachment_results:
        if att.get("has_executable"):
            features["has_executable_attachment"] = 1.0
        if att.get("has_macro"):
            features["has_macro_document"] = 1.0
        if att.get("double_extension"):
            features["double_extension_detected"] = 1.0

    result = calculate_risk_score(features)
    return {
        "score": round(result.risk_score),
        "verdict": result.verdict,
        "suspicion_raw": result.suspicion_score,
        "trust_deduction": result.trust_score,
        "feature_vector": features,
        "indicators": result.indicators,
        "top_contributors": result.top_contributors,
    }
