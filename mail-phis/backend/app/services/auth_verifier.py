import re
import asyncio
import dns.asyncresolver
import dns.exception
from typing import Any

TIMEOUT = 3.0


async def verify_auth(parsed_email: dict[str, Any], header_results: dict[str, Any]) -> dict[str, Any]:
    sender_domain = header_results.get("sender_domain", "")
    if not sender_domain:
        return _unknown_all("no sender domain")

    spf, dkim, dmarc = await asyncio.gather(
        _check_spf(sender_domain),
        _check_dkim(parsed_email.get("headers", {}), sender_domain),
        _check_dmarc(sender_domain),
        return_exceptions=True,
    )

    if isinstance(spf, Exception):
        spf = {"result": "error", "detail": str(spf)}
    if isinstance(dkim, Exception):
        dkim = {"result": "error", "detail": str(dkim)}
    if isinstance(dmarc, Exception):
        dmarc = {"result": "error", "detail": str(dmarc)}

    display_name = header_results.get("display_name", "")
    spoofed_brand = _detect_brand_spoof(display_name, sender_domain)

    return {
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc,
        "display_name_spoof": spoofed_brand,
        "auth_score": _auth_score(spf, dkim, dmarc, spoofed_brand),
    }


async def _check_spf(domain: str) -> dict:
    try:
        resolver = dns.asyncresolver.Resolver()
        resolver.lifetime = TIMEOUT
        answers = await resolver.resolve(domain, "TXT")
        for rdata in answers:
            txt = b"".join(rdata.strings).decode("utf-8", errors="replace")
            if txt.startswith("v=spf1"):
                result = "pass" if "~all" not in txt and "-all" not in txt else "softfail"
                if "-all" in txt:
                    result = "fail"
                return {"result": result, "record": txt[:200]}
        return {"result": "none", "record": None}
    except dns.exception.NXDOMAIN:
        return {"result": "none", "record": None}
    except Exception as e:
        return {"result": "temperror", "detail": str(e)[:100]}


async def _check_dkim(headers: dict, domain: str) -> dict:
    dkim_header = headers.get("DKIM-Signature") or headers.get("dkim-signature")
    if not dkim_header:
        return {"result": "none", "selector": None}
    m = re.search(r"s=([^;]+)", dkim_header)
    selector = m.group(1).strip() if m else "default"
    try:
        resolver = dns.asyncresolver.Resolver()
        resolver.lifetime = TIMEOUT
        await resolver.resolve(f"{selector}._domainkey.{domain}", "TXT")
        return {"result": "pass", "selector": selector}
    except dns.exception.NXDOMAIN:
        return {"result": "fail", "selector": selector, "detail": "key record not found"}
    except Exception as e:
        return {"result": "temperror", "selector": selector, "detail": str(e)[:100]}


async def _check_dmarc(domain: str) -> dict:
    try:
        resolver = dns.asyncresolver.Resolver()
        resolver.lifetime = TIMEOUT
        answers = await resolver.resolve(f"_dmarc.{domain}", "TXT")
        for rdata in answers:
            txt = b"".join(rdata.strings).decode("utf-8", errors="replace")
            if txt.startswith("v=DMARC1"):
                policy_m = re.search(r"p=(\w+)", txt)
                policy = policy_m.group(1) if policy_m else "none"
                return {"result": "pass", "policy": policy, "record": txt[:200]}
        return {"result": "none"}
    except dns.exception.NXDOMAIN:
        return {"result": "none"}
    except Exception as e:
        return {"result": "temperror", "detail": str(e)[:100]}


KNOWN_BRANDS = [
    "paypal", "apple", "microsoft", "google", "amazon", "netflix",
    "bank", "chase", "wells fargo", "citibank", "fedex", "dhl", "ups",
    "linkedin", "facebook", "instagram", "twitter", "dropbox",
]


def _detect_brand_spoof(display_name: str, sender_domain: str) -> bool:
    dn_lower = display_name.lower()
    for brand in KNOWN_BRANDS:
        if brand in dn_lower and brand not in sender_domain:
            return True
    return False


def _auth_score(spf: dict, dkim: dict, dmarc: dict, spoofed: bool) -> int:
    score = 0
    if spf.get("result") not in ("pass", "softfail"):
        score += 15
    if dkim.get("result") != "pass":
        score += 15
    if dmarc.get("result") != "pass":
        score += 10
    if spoofed:
        score += 20
    return score


def _unknown_all(reason: str) -> dict:
    return {
        "spf": {"result": "unknown", "detail": reason},
        "dkim": {"result": "unknown", "detail": reason},
        "dmarc": {"result": "unknown", "detail": reason},
        "display_name_spoof": False,
        "auth_score": 0,
    }
