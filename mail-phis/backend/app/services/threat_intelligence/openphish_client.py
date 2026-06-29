"""
OpenPhish feed client with Redis-backed feed caching.
The community feed is a plain-text list of phishing URLs, refreshed every 12 hours.
"""
import httpx
from dataclasses import dataclass, field
from typing import Optional
from app.core.cache import cache

OPENPHISH_FEED_URL = "https://openphish.com/feed.txt"
_TIMEOUT = 5.0


@dataclass
class OpenPhishResult:
    status: str = "unknown"   # "hit" | "miss" | "error"
    matched_url: Optional[str] = None
    error: Optional[str] = None


async def _fetch_feed() -> list[str]:
    cached = cache.get_openphish_feed()
    if cached is not None:
        return cached
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.get(OPENPHISH_FEED_URL)
            r.raise_for_status()
            urls = [line.strip() for line in r.text.splitlines() if line.strip()]
            cache.set_openphish_feed(urls)
            return urls
    except Exception:
        return []


async def check_openphish(url: str) -> OpenPhishResult:
    try:
        feed = await _fetch_feed()
        for entry in feed:
            if url.startswith(entry) or entry.startswith(url.split("?")[0]):
                return OpenPhishResult(status="hit", matched_url=entry)
        return OpenPhishResult(status="miss")
    except Exception as exc:
        return OpenPhishResult(status="error", error=str(exc))
