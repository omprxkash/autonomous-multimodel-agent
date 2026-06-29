"""
AbuseIPDB IP reputation client.
Returns country risk score and blacklist status.
Requires ABUSEIPDB_API_KEY in environment (degrades gracefully if absent).
"""
import httpx
from dataclasses import dataclass
from typing import Optional
from app.core.cache import cache
from app.core.config import settings

ABUSEIPDB_API = "https://api.abuseipdb.com/api/v2/check"
_TIMEOUT = 5.0

# High-risk country codes (ISO 3166-1 alpha-2) — adjust to your threat model
HIGH_RISK_COUNTRIES = {
    "CN", "RU", "KP", "IR", "NG", "RO", "BR", "IN", "VN", "PK",
}


@dataclass
class IPReputationResult:
    ip: str
    is_blacklisted: bool = False
    abuse_confidence_score: int = 0
    country_code: Optional[str] = None
    country_risk: bool = False
    total_reports: int = 0
    error: Optional[str] = None


async def check_ip_reputation(ip: str) -> IPReputationResult:
    if not ip or ip in ("", "0.0.0.0"):
        return IPReputationResult(ip=ip, error="invalid_ip")

    cached = cache.get_ip_reputation(ip)
    if cached:
        return IPReputationResult(**cached)

    api_key = getattr(settings, "ABUSEIPDB_API_KEY", None)
    if not api_key:
        return IPReputationResult(ip=ip, error="no_api_key")

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.get(
                ABUSEIPDB_API,
                headers={"Key": api_key, "Accept": "application/json"},
                params={"ipAddress": ip, "maxAgeInDays": 90},
            )
            r.raise_for_status()
            data = r.json().get("data", {})

        score = data.get("abuseConfidenceScore", 0)
        country = data.get("countryCode")
        total = data.get("totalReports", 0)
        result = IPReputationResult(
            ip=ip,
            is_blacklisted=score >= 50,
            abuse_confidence_score=score,
            country_code=country,
            country_risk=country in HIGH_RISK_COUNTRIES,
            total_reports=total,
        )
        cache.set_ip_reputation(ip, result.__dict__)
        return result

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return IPReputationResult(ip=ip, error="rate_limited")
        return IPReputationResult(ip=ip, error=str(exc))
    except Exception as exc:
        return IPReputationResult(ip=ip, error=str(exc))
