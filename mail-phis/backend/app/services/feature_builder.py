"""
Feature Builder
Aggregates all analysis pipeline outputs into a unified feature vector for risk scoring.
"""
import re
from typing import Any, Dict, List, Optional


CDN_DOMAINS = {
    "cloudfront.net", "akamai.net", "akamaized.net", "fastly.net",
    "cdn.shopify.com", "cdn.jsdelivr.net", "cloudflare.com",
    "azureedge.net", "amazonaws.com", "googleusercontent.com",
}


def build_feature_vector(
    header_results: Optional[Dict] = None,
    url_results: Optional[Dict] = None,
    domain_results: Optional[Dict] = None,
    threat_results: Optional[Dict] = None,
    nlp_results: Optional[Dict] = None,
    attachment_results: Optional[List[Dict]] = None,
    auth_results: Optional[Dict] = None,
    redirect_result: Optional[Dict] = None,
    email_body_html: Optional[str] = None,
    email_body_text: Optional[str] = None,
    email_urls: Optional[List[str]] = None,
) -> Dict[str, float]:
    """Build the complete feature vector from all analysis results."""
    features: Dict[str, float] = {}

    # =========================================================================
    # 1. Authentication features
    # =========================================================================
    if auth_results:
        spf = (auth_results.get("spf") or {}).get("result", "none")
        dkim = (auth_results.get("dkim") or {}).get("result", "none")
        dmarc = (auth_results.get("dmarc") or {}).get("result", "none")
        features["spf_pass"] = float(spf == "pass")
        features["dkim_pass"] = float(dkim == "pass")
        features["dmarc_pass"] = float(dmarc == "pass")
        features["spf_fail"] = float(spf == "fail")
        features["dkim_fail"] = float(dkim == "fail")
        features["dmarc_fail"] = float(dmarc == "fail")
        features["authentication_all_pass"] = float(
            spf == "pass" and dkim == "pass" and dmarc == "pass"
        )
        features["bulk_mail_indicator"] = float(auth_results.get("bulk_mail_indicator", False))
        features["esp_detected"] = float(auth_results.get("esp_detected", False))
        features["display_name_brand_spoofing"] = float(auth_results.get("display_name_spoof", False))

    if header_results:
        features["reply_to_mismatch"] = float(header_results.get("reply_to_mismatch", False))
        features["return_path_mismatch"] = float(header_results.get("return_path_mismatch", False))
        features["sender_domain_mismatch"] = float(header_results.get("sender_domain_mismatch", False))
        features["num_received_headers"] = float(header_results.get("num_received_headers", 0))

    # =========================================================================
    # 2. URL structural features
    # =========================================================================
    if url_results:
        features["url_length"] = float(url_results.get("url_length", 0))
        features["num_subdomains"] = float(url_results.get("subdomain_depth", 0))
        features["contains_ip_address"] = float(url_results.get("has_ip_host", False))
        features["url_entropy_score"] = float(url_results.get("path_entropy", 0))
        features["url_shortened"] = float(url_results.get("is_shortened", False))
        features["username_in_url"] = float("@" in url_results.get("original_url", ""))

    # =========================================================================
    # 3. URL obfuscation
    # =========================================================================
    if url_results:
        features["percent_encoding_count"] = float(url_results.get("obfuscation_count", 0))
        features["double_slash_redirect"] = float(
            "//" in (url_results.get("original_url", "")).split("://", 1)[-1]
        )

    # =========================================================================
    # 4. Redirect behavior
    # =========================================================================
    if redirect_result:
        features["redirect_count"] = float(redirect_result.get("redirect_count", 0))
        features["final_domain_mismatch"] = float(redirect_result.get("final_domain_mismatch", False))
        features["redirect_to_ip"] = float(redirect_result.get("redirect_to_ip", False))
        features["meta_refresh_detected"] = float(redirect_result.get("meta_refresh_detected", False))
        features["redirect_to_different_domain"] = float(
            redirect_result.get("redirect_to_different_domain", False)
        )
    elif url_results:
        features["redirect_count"] = float(url_results.get("redirect_count", 0))

    # =========================================================================
    # 5. Domain intelligence
    # =========================================================================
    if domain_results:
        age = domain_results.get("age_days")
        if age is not None:
            features["domain_age_days"] = float(age)
            features["domain_very_recent"] = float(age < 7)
            features["domain_recent_registration"] = float(7 <= age < 30)
        features["brand_homograph_detected"] = float(domain_results.get("homograph", False))
        typosquat = domain_results.get("typosquat_target")
        features["brand_sender_domain_mismatch"] = float(typosquat is not None)
        dns = domain_results.get("dns") or {}
        features["has_mx_record"] = float(len(dns.get("MX", [])) > 0)
        features["has_spf_record"] = float(
            any("v=spf1" in t.lower() for t in dns.get("TXT", []))
        )

    # =========================================================================
    # 6. Threat intelligence
    # =========================================================================
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

    # =========================================================================
    # 7. NLP / social engineering
    # =========================================================================
    if nlp_results:
        features["urgency_keyword_count"] = float(nlp_results.get("urgency_keyword_count", 0))
        features["credential_request_keywords"] = float(nlp_results.get("credential_keyword_count", 0))
        features["financial_request_keywords"] = float(nlp_results.get("financial_keyword_count", 0))
        features["security_alert_keywords"] = float(nlp_results.get("security_keyword_count", 0))
        features["threat_language_score"] = float(nlp_results.get("nlp_score", 0) / 100.0)
        features["imperative_language_score"] = float(
            min(nlp_results.get("exclamation_density", 0) * 5, 1.0)
        )

    # =========================================================================
    # 8. Attachment risk
    # =========================================================================
    for att in (attachment_results or []):
        if att.get("has_executable"):
            features["has_executable_attachment"] = 1.0
        if att.get("has_macro"):
            features["has_macro_document"] = 1.0
        if att.get("double_extension"):
            features["double_extension_detected"] = 1.0

    # =========================================================================
    # 9. Email body structure
    # =========================================================================
    features["num_urls_in_email"] = float(len(email_urls or []))

    if email_body_html:
        features["num_forms"] = float(len(re.findall(r"<form\s", email_body_html, re.IGNORECASE)))
        features["javascript_in_email"] = float(
            1 if re.search(r"<script|javascript:", email_body_html, re.IGNORECASE) else 0
        )
        features["hidden_links_detected"] = float(
            1 if re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", email_body_html, re.IGNORECASE) else 0
        )
        has_unsubscribe = bool(re.search(r"unsubscribe", email_body_html, re.IGNORECASE))
        features["has_unsubscribe_link"] = float(has_unsubscribe)
        features["marketing_template_signals"] = float(has_unsubscribe)

    return features
