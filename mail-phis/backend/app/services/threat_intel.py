import asyncio
import hashlib
from typing import Any
import httpx
from app.core.config import settings

TIMEOUT = 8.0


async def query_threat_intel(url: str) -> dict[str, Any]:
    tasks = [
        _query_openphish(url),
        _query_phishtank(url),
        _query_urlhaus(url),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    openphish, phishtank, urlhaus = [
        r if not isinstance(r, Exception) else {"status": "error", "detail": str(r)[:100]}
        for r in results
    ]
    hit = any(
        r.get("status") == "hit"
        for r in [openphish, phishtank, urlhaus]
        if isinstance(r, dict)
    )
    return {
        "openphish": openphish,
        "phishtank": phishtank,
        "urlhaus": urlhaus,
        "any_hit": hit,
    }


async def _query_openphish(url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get("https://openphish.com/feed.txt")
            if resp.status_code == 200:
                urls = resp.text.splitlines()
                hit = url in urls or any(url.startswith(u) for u in urls[:5000])
                return {"status": "hit" if hit else "clean", "source": "openphish"}
            return {"status": "unknown", "source": "openphish", "http": resp.status_code}
    except Exception as e:
        return {"status": "unknown", "source": "openphish", "error": str(e)[:80]}


async def _query_phishtank(url: str) -> dict:
    if not settings.PHISHTANK_API_KEY:
        return {"status": "skipped", "source": "phishtank", "reason": "no api key"}
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                "https://checkurl.phishtank.com/checkurl/",
                data={
                    "url": url,
                    "format": "json",
                    "app_key": settings.PHISHTANK_API_KEY,
                },
            )
            if resp.status_code == 429:
                await asyncio.sleep(1)
                resp = await client.post(
                    "https://checkurl.phishtank.com/checkurl/",
                    data={"url": url, "format": "json", "app_key": settings.PHISHTANK_API_KEY},
                )
            data = resp.json()
            in_db = data.get("results", {}).get("in_database", False)
            verified = data.get("results", {}).get("verified", False)
            return {
                "status": "hit" if (in_db and verified) else "clean",
                "source": "phishtank",
                "in_database": in_db,
            }
    except Exception as e:
        return {"status": "unknown", "source": "phishtank", "error": str(e)[:80]}


async def _query_urlhaus(url: str) -> dict:
    try:
        headers = {}
        if settings.URLHAUS_AUTH_KEY:
            headers["Auth-Key"] = settings.URLHAUS_AUTH_KEY
        async with httpx.AsyncClient(timeout=TIMEOUT, headers=headers) as client:
            resp = await client.post(
                "https://urlhaus-api.abuse.ch/v1/url/",
                data={"url": url},
            )
            data = resp.json()
            query_status = data.get("query_status", "")
            return {
                "status": "hit" if query_status == "is_blacklisted" else "clean",
                "source": "urlhaus",
                "query_status": query_status,
            }
    except Exception as e:
        return {"status": "unknown", "source": "urlhaus", "error": str(e)[:80]}
