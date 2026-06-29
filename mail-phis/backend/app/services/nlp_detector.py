import re
import unicodedata
from html.parser import HTMLParser
from typing import Any

URGENCY_PHRASES = [
    "act now", "immediate action", "account suspended", "verify immediately",
    "your account will be", "limited time", "expires today", "respond within",
    "urgent", "attention required", "last chance", "final notice",
]

CREDENTIAL_PHRASES = [
    "enter your password", "confirm your credentials", "verify your identity",
    "update your payment", "enter credit card", "social security",
    "login to confirm", "sign in to verify", "validate your account",
]

FINANCIAL_PHRASES = [
    "you have won", "prize money", "lottery", "wire transfer", "inheritance",
    "unclaimed funds", "transfer fee", "advance fee", "million dollars",
]

IMPERSONATION_PHRASES = [
    "it department", "help desk", "support team", "it support",
    "your administrator", "system administrator", "tech support",
    "your bank", "security department",
]


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return " ".join(self._parts)


def _strip_html(html: str) -> str:
    p = _HTMLStripper()
    p.feed(html)
    return p.get_text()


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.lower()


def _count_hits(text: str, phrases: list[str]) -> list[str]:
    return [p for p in phrases if p in text]


def analyze_nlp(parsed_email: dict[str, Any]) -> dict[str, Any]:
    body_text = ""
    for part in parsed_email.get("body_parts", []):
        content = part.get("content", "")
        if part.get("content_type") == "text/html":
            content = _strip_html(content)
        body_text += " " + content

    subject = parsed_email.get("subject", "")
    full_text = _normalize(subject + " " + body_text)

    urgency_hits = _count_hits(full_text, URGENCY_PHRASES)
    credential_hits = _count_hits(full_text, CREDENTIAL_PHRASES)
    financial_hits = _count_hits(full_text, FINANCIAL_PHRASES)
    impersonation_hits = _count_hits(full_text, IMPERSONATION_PHRASES)

    word_count = len(full_text.split())
    exclamation_density = full_text.count("!") / max(word_count, 1)
    caps_ratio = sum(1 for c in body_text if c.isupper()) / max(len(body_text), 1)

    nlp_score = (
        len(urgency_hits) * 8
        + len(credential_hits) * 12
        + len(financial_hits) * 10
        + len(impersonation_hits) * 10
        + min(exclamation_density * 100, 10)
        + min(caps_ratio * 50, 10)
    )

    return {
        "urgency_hits": urgency_hits,
        "credential_hits": credential_hits,
        "financial_hits": financial_hits,
        "impersonation_hits": impersonation_hits,
        "exclamation_density": round(exclamation_density, 4),
        "caps_ratio": round(caps_ratio, 4),
        "word_count": word_count,
        "nlp_score": round(min(nlp_score, 60), 2),
    }
