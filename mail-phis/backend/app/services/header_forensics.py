import re
from typing import Any

RECEIVED_RE = re.compile(r"from\s+(\S+).*?by\s+(\S+)", re.IGNORECASE | re.DOTALL)
IP_RE = re.compile(r"\[(\d{1,3}(?:\.\d{1,3}){3}|[0-9a-fA-F:]+)\]")


def analyze_headers(parsed_email: dict[str, Any]) -> dict[str, Any]:
    headers = parsed_email.get("headers", {})
    received_headers = _get_all(headers, "Received")

    hops = []
    for r in received_headers:
        m = RECEIVED_RE.search(r)
        ip_match = IP_RE.search(r)
        hops.append({
            "from": m.group(1) if m else None,
            "by": m.group(2) if m else None,
            "originating_ip": ip_match.group(1) if ip_match else None,
            "raw": r[:200],
        })

    originating_ip = None
    for hop in reversed(hops):
        if hop.get("originating_ip"):
            originating_ip = hop["originating_ip"]
            break

    sender_domain = _extract_domain(parsed_email.get("from", ""))
    reply_to_domain = _extract_domain(parsed_email.get("reply_to", ""))
    display_name = _extract_display_name(parsed_email.get("from", ""))

    return {
        "hops": hops,
        "hop_count": len(hops),
        "originating_ip": originating_ip,
        "x_mailer": headers.get("X-Mailer", headers.get("x-mailer")),
        "x_originating_ip": headers.get("X-Originating-IP"),
        "sender_domain": sender_domain,
        "reply_to_domain": reply_to_domain,
        "reply_to_mismatch": bool(reply_to_domain and reply_to_domain != sender_domain),
        "display_name": display_name,
        "missing_received": len(hops) == 0,
    }


def _get_all(headers: dict, key: str) -> list[str]:
    results = []
    for k, v in headers.items():
        if k.lower() == key.lower():
            results.append(v)
    return results


def _extract_domain(address: str) -> str:
    m = re.search(r"@([\w.\-]+)", address)
    return m.group(1).lower() if m else ""


def _extract_display_name(address: str) -> str:
    m = re.match(r'"?([^"<]+)"?\s*<', address)
    return m.group(1).strip() if m else ""
