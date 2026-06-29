import asyncio
import unicodedata
import re
from datetime import datetime, timezone
from typing import Any
import dns.asyncresolver
import dns.exception
import whois

TIMEOUT = 3.0
CONFUSABLE_MAP = str.maketrans("аеорсух", "aeopchx")  # Cyrillic → Latin lookalikes


async def analyze_domain(domain: str) -> dict[str, Any]:
    dns_result, whois_result = await asyncio.gather(
        _dns_lookup(domain),
        asyncio.to_thread(_whois_lookup, domain),
        return_exceptions=True,
    )

    if isinstance(dns_result, Exception):
        dns_result = {"error": str(dns_result)[:100]}
    if isinstance(whois_result, Exception):
        whois_result = {"error": str(whois_result)[:100]}

    age_days = whois_result.get("age_days") if isinstance(whois_result, dict) else None

    return {
        "domain": domain,
        "dns": dns_result,
        "whois": whois_result,
        "age_days": age_days,
        "newly_registered": age_days is not None and age_days < 30,
        "homograph": _is_homograph(domain),
        "typosquat_target": _typosquat_check(domain),
    }


async def _dns_lookup(domain: str) -> dict:
    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = TIMEOUT
    result = {}

    for record_type in ("A", "MX", "NS"):
        try:
            answers = await resolver.resolve(domain, record_type)
            result[record_type] = [str(r) for r in answers]
        except dns.exception.NXDOMAIN:
            result[record_type] = []
            result["nxdomain"] = True
        except Exception:
            result[record_type] = []

    return result


def _whois_lookup(domain: str) -> dict:
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation:
            if creation.tzinfo is None:
                creation = creation.replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - creation).days
        else:
            age = None
        return {
            "registrar": str(w.registrar or "")[:100],
            "creation_date": str(creation) if creation else None,
            "age_days": age,
            "country": str(w.country or "")[:10],
        }
    except Exception as e:
        return {"error": str(e)[:100]}


def _is_homograph(domain: str) -> bool:
    normalized = unicodedata.normalize("NFKC", domain)
    translated = domain.translate(CONFUSABLE_MAP)
    return normalized != domain or translated != domain


KNOWN_BRANDS_DOMAINS = [
    "paypal", "apple", "microsoft", "google", "amazon", "netflix",
    "chase", "wellsfargo", "citibank", "dropbox", "linkedin",
]


def _typosquat_check(domain: str) -> str | None:
    base = domain.split(".")[0].lower()
    for brand in KNOWN_BRANDS_DOMAINS:
        if brand != base and _edit_distance(base, brand) <= 2:
            return brand
    return None


def _edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[j] = prev[j - 1]
            else:
                dp[j] = 1 + min(prev[j], dp[j - 1], prev[j - 1])
    return dp[n]
