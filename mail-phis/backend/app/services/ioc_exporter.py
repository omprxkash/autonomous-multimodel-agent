"""
IOC Exporter
Extracts Indicators of Compromise from analysis results for export and SIEM ingestion.
"""
import re
from typing import Dict, List, Any


def extract_iocs(
    analysis_id: str,
    pipeline_results: Dict[str, Any],
    verdict: str,
    score: float,
) -> Dict[str, Any]:
    """Extract all IOCs from pipeline results."""

    iocs: Dict[str, List[Any]] = {
        "ips": [],
        "domains": [],
        "urls": [],
        "email_addresses": [],
        "hashes": [],
        "indicators": [],
    }

    headers = pipeline_results.get("header_forensics", {})
    url_results = pipeline_results.get("url_analysis")
    domain_results = pipeline_results.get("domain_intel")
    threat_results = pipeline_results.get("threat_intel")
    attachments = pipeline_results.get("attachments", [])

    # Originating IP
    originating_ip = headers.get("originating_ip") if headers else None
    if originating_ip:
        iocs["ips"].append({
            "value": originating_ip,
            "context": "smtp_originating_ip",
            "severity": "HIGH" if (threat_results or {}).get("any_hit") else "MEDIUM",
        })

    # From / Reply-To addresses
    from_addr = (pipeline_results.get("email_info") or {}).get("from", "")
    if from_addr:
        iocs["email_addresses"].append({"value": from_addr, "context": "from_header"})

    # URLs from URL analysis
    if url_results:
        url_str = url_results.get("original_url") or url_results.get("url", "")
        if url_str:
            iocs["urls"].append({
                "value": url_str,
                "context": "email_body",
                "threat_hit": (threat_results or {}).get("any_hit", False),
            })
        domain = url_results.get("domain", "")
        if domain:
            iocs["domains"].append({
                "value": domain,
                "context": "url_domain",
                "newly_registered": (domain_results or {}).get("newly_registered", False),
                "homograph": (domain_results or {}).get("homograph", False),
            })

    # Attachment hashes
    for att in attachments:
        sha256 = att.get("sha256", "")
        if sha256:
            iocs["hashes"].append({
                "value": sha256,
                "filename": att.get("filename", ""),
                "context": "email_attachment",
            })

    # Threat intel hits
    if threat_results and threat_results.get("any_hit"):
        for source in ["openphish", "phishtank", "urlhaus"]:
            feed = threat_results.get(source, {})
            if isinstance(feed, dict) and feed.get("status") == "hit":
                iocs["indicators"].append({
                    "type": "url_in_threat_feed",
                    "source": source,
                    "severity": "CRITICAL",
                })

    return {
        "analysis_id": analysis_id,
        "verdict": verdict,
        "risk_score": score,
        "ioc_count": sum(len(v) for v in iocs.values()),
        "iocs": iocs,
    }
