"""
Redirect Chain Tracker
Traces HTTP redirect chains up to MAX_REDIRECTS hops.
Handles meta-refresh HTML redirects, loop detection, and IP destination detection.
"""
import re
from typing import List, Optional
from urllib.parse import urlparse

import httpx

MAX_REDIRECTS = 10
TIMEOUT = 3.0


class RedirectChainResult:
    def __init__(self):
        self.redirect_count: int = 0
        self.redirect_chain: List[str] = []
        self.final_destination: Optional[str] = None
        self.final_domain_mismatch: bool = False
        self.redirect_to_different_domain: bool = False
        self.redirect_to_ip: bool = False
        self.meta_refresh_detected: bool = False
        self.error: Optional[str] = None


async def trace_redirect_chain(url: str) -> RedirectChainResult:
    result = RedirectChainResult()
    result.redirect_chain = [url]
    original_domain = urlparse(url).hostname

    try:
        async with httpx.AsyncClient(
            follow_redirects=False,
            timeout=TIMEOUT,
            verify=False,
        ) as client:
            current_url = url

            for _ in range(MAX_REDIRECTS):
                try:
                    response = await client.get(current_url)
                except httpx.TimeoutException:
                    result.error = f"Timeout reaching {current_url}"
                    break
                except Exception as e:
                    result.error = str(e)[:120]
                    break

                if response.status_code == 200:
                    ct = response.headers.get("content-type", "")
                    if "html" in ct:
                        meta_url = _extract_meta_refresh(response.text)
                        if meta_url:
                            result.meta_refresh_detected = True
                            result.redirect_chain.append(meta_url)
                            result.redirect_count += 1
                            current_url = meta_url
                            continue
                    break

                if response.status_code in (301, 302, 303, 307, 308):
                    location = response.headers.get("location")
                    if not location:
                        break
                    if location.startswith("/"):
                        parsed = urlparse(current_url)
                        location = f"{parsed.scheme}://{parsed.netloc}{location}"
                    result.redirect_chain.append(location)
                    result.redirect_count += 1
                    current_url = location
                else:
                    break

    except Exception as e:
        result.error = str(e)[:120]

    result.final_destination = result.redirect_chain[-1] if result.redirect_chain else url

    final_domain = urlparse(result.final_destination).hostname
    result.final_domain_mismatch = (
        original_domain is not None
        and final_domain is not None
        and original_domain != final_domain
    )

    domains = {urlparse(u).hostname for u in result.redirect_chain if urlparse(u).hostname}
    result.redirect_to_different_domain = len(domains) > 1

    if final_domain:
        result.redirect_to_ip = bool(re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", final_domain))

    return result


def _extract_meta_refresh(html: str) -> Optional[str]:
    pattern = re.compile(
        r'<meta[^>]*http-equiv\s*=\s*["\']?refresh["\']?[^>]*content\s*=\s*["\']?\d+\s*;\s*url\s*=\s*(["\']?)([^"\'>\s]+)\1',
        re.IGNORECASE,
    )
    match = pattern.search(html)
    return match.group(2) if match else None
