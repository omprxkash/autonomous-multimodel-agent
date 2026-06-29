"""
URLhaus (abuse.ch) API client with typed result dataclass.
Free API — no key required.
"""
import httpx
from dataclasses import dataclass
from typing import Optional

URLHAUS_API = "https://urlhaus-api.abuse.ch/v1/url/"
_TIMEOUT = 5.0


@dataclass
class URLhausResult:
    status: str = "unknown"    # "hit" | "miss" | "error"
    url_status: Optional[str] = None   # "online" | "offline" | "unknown"
    threat: Optional[str] = None       # e.g. "malware_download"
    tags: list[str] = None
    date_added: Optional[str] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


async def check_urlhaus(url: str) -> URLhausResult:
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.post(URLHAUS_API, data={"url": url})
            r.raise_for_status()
            data = r.json()

        query_status = data.get("query_status", "")
        if query_status == "is_phishing":
            return URLhausResult(
                status="hit",
                url_status=data.get("url_status"),
                threat=data.get("threat"),
                tags=data.get("tags") or [],
                date_added=data.get("date_added"),
            )
        elif query_status == "no_results":
            return URLhausResult(status="miss")
        else:
            return URLhausResult(status="miss")

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return URLhausResult(status="error", error="rate_limited")
        return URLhausResult(status="error", error=str(exc))
    except Exception as exc:
        return URLhausResult(status="error", error=str(exc))
