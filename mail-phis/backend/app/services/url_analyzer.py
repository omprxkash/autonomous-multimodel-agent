import re
import math
import asyncio
import urllib.parse
from typing import Any
import httpx

MAX_REDIRECTS = 10
REQUEST_TIMEOUT = 5.0
OBFUSCATION_PATTERNS = [
    re.compile(r"%[0-9a-fA-F]{2}"),   # URL encoding
    re.compile(r"@"),                   # username@ trick
    re.compile(r"\d{8,}"),             # IP as decimal
    re.compile(r"0x[0-9a-fA-F]+"),    # hex IP
]


def entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((f / n) * math.log2(f / n) for f in freq.values())


async def analyze_url(url: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path

    obfuscation_flags = [bool(p.search(url)) for p in OBFUSCATION_PATTERNS]
    obfuscation_count = sum(obfuscation_flags)

    redirect_chain, final_url, redirect_error = await _trace_redirects(url)

    return {
        "original_url": url,
        "final_url": final_url,
        "domain": domain,
        "path_entropy": round(entropy(path), 3),
        "url_length": len(url),
        "subdomain_depth": domain.count("."),
        "uses_https": parsed.scheme == "https",
        "obfuscation_count": obfuscation_count,
        "redirect_count": len(redirect_chain),
        "redirect_chain": redirect_chain,
        "redirect_error": redirect_error,
        "suspicious_tld": _suspicious_tld(domain),
        "has_ip_host": bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)),
        "url_score": _url_score(url, domain, obfuscation_count, redirect_chain),
    }


async def _trace_redirects(url: str) -> tuple[list[str], str, str | None]:
    chain = []
    current = url
    error = None
    seen = set()

    async with httpx.AsyncClient(
        follow_redirects=False,
        timeout=REQUEST_TIMEOUT,
        verify=False,
    ) as client:
        for _ in range(MAX_REDIRECTS):
            if current in seen:
                error = "redirect loop detected"
                break
            seen.add(current)
            try:
                resp = await client.get(current, headers={"User-Agent": "Mozilla/5.0"})
                if resp.is_redirect:
                    location = resp.headers.get("location", "")
                    if not location.startswith("http"):
                        location = urllib.parse.urljoin(current, location)
                    chain.append(current)
                    current = location
                else:
                    break
            except httpx.TimeoutException:
                error = "timeout"
                break
            except Exception as e:
                error = str(e)[:100]
                break

    return chain, current, error


def _suspicious_tld(domain: str) -> bool:
    suspicious = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".click", ".loan", ".work"}
    return any(domain.endswith(t) for t in suspicious)


def _url_score(url: str, domain: str, obfuscation_count: int, redirects: list) -> int:
    score = 0
    score += min(obfuscation_count * 10, 30)
    score += min(len(redirects) * 5, 20)
    if _suspicious_tld(domain):
        score += 15
    if len(url) > 100:
        score += 5
    if entropy(url) > 4.5:
        score += 10
    return score
