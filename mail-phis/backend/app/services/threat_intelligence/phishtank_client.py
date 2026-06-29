"""
PhishTank API client with typed result dataclass.
Uses the free API (no key required, but rate-limited to 1 req/s per IP).
"""
import httpx
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote

PHISHTANK_API = "https://checkurl.phishtank.com/checkurl/"
_TIMEOUT = 5.0


@dataclass
class PhishTankResult:
    status: str = "unknown"    # "hit" | "miss" | "error"
    in_database: bool = False
    valid: bool = False
    phish_id: Optional[int] = None
    phish_detail_url: Optional[str] = None
    error: Optional[str] = None


async def check_phishtank(url: str, api_key: Optional[str] = None) -> PhishTankResult:
    payload = {"url": url, "format": "json"}
    if api_key:
        payload["app_key"] = api_key

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(
                PHISHTANK_API,
                data=payload,
                headers={"User-Agent": "phishing-detector/1.0"},
            )
            r.raise_for_status()
            data = r.json().get("results", {})
            in_db = data.get("in_database", False)
            valid = data.get("valid", False)

            if in_db and valid:
                return PhishTankResult(
                    status="hit",
                    in_database=True,
                    valid=True,
                    phish_id=data.get("phish_id"),
                    phish_detail_url=data.get("phish_detail_url"),
                )
            return PhishTankResult(status="miss", in_database=in_db, valid=valid)

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return PhishTankResult(status="error", error="rate_limited")
        return PhishTankResult(status="error", error=str(exc))
    except Exception as exc:
        return PhishTankResult(status="error", error=str(exc))
