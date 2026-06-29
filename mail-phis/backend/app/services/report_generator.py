import re
from typing import Any


def generate_report(
    analysis_id: str,
    analysis_type: str,
    target: str,
    email_parsed: dict | None,
    header_results: dict | None,
    auth_results: dict | None,
    url_results: dict | None,
    domain_results: dict | None,
    threat_results: dict | None,
    nlp_results: dict | None,
    score_results: dict,
) -> dict[str, Any]:

    iocs = _extract_iocs(
        email_parsed, header_results, url_results, domain_results
    )

    pipeline_summary = {
        "email_parsing": _safe(email_parsed, ["subject", "from", "raw_size", "attachments"]),
        "header_forensics": _safe(header_results, ["hop_count", "originating_ip", "reply_to_mismatch"]),
        "auth_verification": _safe(auth_results, ["spf", "dkim", "dmarc", "display_name_spoof"]),
        "url_analysis": _safe(url_results, ["final_url", "redirect_count", "obfuscation_count", "url_score"]),
        "domain_intel": _safe(domain_results, ["age_days", "newly_registered", "homograph", "typosquat_target"]),
        "threat_intel": _safe(threat_results, ["any_hit", "openphish", "phishtank", "urlhaus"]),
        "nlp_detection": _safe(nlp_results, ["urgency_hits", "credential_hits", "financial_hits", "nlp_score"]),
        "risk_scoring": {
            "score": score_results.get("score"),
            "verdict": score_results.get("verdict"),
            "suspicion_raw": score_results.get("suspicion_raw"),
            "trust_deduction": score_results.get("trust_deduction"),
        },
    }

    return {
        "analysis_id": analysis_id,
        "type": analysis_type,
        "target": target,
        "verdict": score_results.get("verdict"),
        "score": score_results.get("score"),
        "pipeline": pipeline_summary,
        "feature_vector": score_results.get("feature_vector", {}),
        "iocs": iocs,
    }


def _extract_iocs(
    email_parsed: dict | None,
    header_results: dict | None,
    url_results: dict | None,
    domain_results: dict | None,
) -> dict[str, list]:
    iocs: dict[str, list] = {"ips": [], "domains": [], "urls": [], "emails": []}

    if header_results:
        ip = header_results.get("originating_ip")
        if ip:
            iocs["ips"].append(ip)

    if url_results:
        for url in [url_results.get("original_url"), url_results.get("final_url")]:
            if url and url not in iocs["urls"]:
                iocs["urls"].append(url)
        domain = url_results.get("domain")
        if domain and domain not in iocs["domains"]:
            iocs["domains"].append(domain)

    if domain_results:
        d = domain_results.get("domain")
        if d and d not in iocs["domains"]:
            iocs["domains"].append(d)

    if email_parsed:
        from_addr = email_parsed.get("from", "")
        m = re.search(r"[\w.+-]+@[\w.-]+\.\w+", from_addr)
        if m:
            iocs["emails"].append(m.group())

    return {k: list(set(v)) for k, v in iocs.items()}


def _safe(d: dict | None, keys: list[str]) -> dict:
    if not d:
        return {}
    return {k: d.get(k) for k in keys}
