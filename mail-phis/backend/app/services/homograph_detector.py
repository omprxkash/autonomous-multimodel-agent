"""
Homograph Detector
Detects Unicode homograph attacks, IDN domain spoofing, and typosquatting.
"""
from typing import Optional, List, Tuple

from app.core.security import BRAND_KEYWORDS

# Subset of Unicode confusable characters → ASCII equivalents
CONFUSABLE_MAP = {
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y",
    "х": "x", "ѕ": "s", "і": "i", "ј": "j", "ᴀ": "a", "ᴄ": "c",
    "ᴅ": "d", "ᴇ": "e", "ɡ": "g", "ʜ": "h", "ᴋ": "k", "ʟ": "l",
    "ᴍ": "m", "ɴ": "n", "ᴏ": "o", "ᴘ": "p", "ǫ": "q", "ʀ": "r",
    "ꜱ": "s", "ᴛ": "t", "ᴜ": "u", "ᴠ": "v", "ᴡ": "w", "ᴢ": "z",
    "ⅰ": "i", "ℓ": "l", "ⅿ": "m",
    "０": "0", "１": "1", "２": "2", "３": "3", "４": "4",
    "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
}


class HomographResult:
    def __init__(self):
        self.is_homograph: bool = False
        self.is_idn: bool = False
        self.punycode: Optional[str] = None
        self.normalized_domain: Optional[str] = None
        self.confusable_chars: List[Tuple[str, str]] = []
        self.matched_brand: Optional[str] = None
        self.similarity_score: float = 0.0


def detect_homograph(domain: str) -> HomographResult:
    """Detect if a domain uses homograph characters or typosquatting to impersonate a brand."""
    result = HomographResult()

    if any(ord(c) > 127 for c in domain):
        result.is_idn = True
        try:
            result.punycode = domain.encode("idna").decode("ascii")
        except Exception:
            result.punycode = None

    normalized = _normalize_confusables(domain)
    result.normalized_domain = normalized

    for char in domain:
        if char in CONFUSABLE_MAP:
            result.confusable_chars.append((char, CONFUSABLE_MAP[char]))

    if result.confusable_chars:
        result.is_homograph = True

    domain_lower = normalized.lower()
    for brand in BRAND_KEYWORDS:
        if brand in domain_lower:
            result.matched_brand = brand
            result.similarity_score = _similarity(domain_lower, brand)
            break

    # Typosquatting: near-matches with edit distance ≤ 2
    if not result.matched_brand:
        for brand in BRAND_KEYWORDS:
            sim = _similarity(domain.lower().split(".")[0], brand)
            if 0.75 < sim < 1.0:
                result.matched_brand = brand
                result.similarity_score = sim
                result.is_homograph = True
                break

    return result


def _normalize_confusables(text: str) -> str:
    return "".join(CONFUSABLE_MAP.get(c, c) for c in text)


def _similarity(s1: str, s2: str) -> float:
    if not s1 or not s2:
        return 0.0
    len1, len2 = len(s1), len(s2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )
    distance = matrix[len1][len2]
    return 1.0 - (distance / max(len1, len2))
