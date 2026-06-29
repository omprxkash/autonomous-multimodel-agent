"""
URL extractor with hidden-URL detection.
Parses both plain-text and HTML email bodies. Detects URLs hidden behind
CSS display:none/visibility:hidden, zero-font-size spans, and white-on-white text.
"""
import re
from dataclasses import dataclass, field
from typing import Optional

try:
    from bs4 import BeautifulSoup
    _BS4 = True
except ImportError:
    _BS4 = False

_URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+", re.IGNORECASE)
_MAX_URLS = 50

# CSS patterns that render content invisible to the human reader
_HIDDEN_PATTERNS = [
    re.compile(r"display\s*:\s*none", re.IGNORECASE),
    re.compile(r"visibility\s*:\s*hidden", re.IGNORECASE),
    re.compile(r"font-size\s*:\s*0", re.IGNORECASE),
    re.compile(r"color\s*:\s*(?:white|#fff(?:fff)?|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))", re.IGNORECASE),
    re.compile(r"opacity\s*:\s*0", re.IGNORECASE),
]


@dataclass
class ExtractedURL:
    url: str
    source: str = "text"        # "text" | "html_anchor" | "html_hidden"
    anchor_text: Optional[str] = None
    is_hidden: bool = False


def _is_hidden_style(style: str) -> bool:
    return any(p.search(style) for p in _HIDDEN_PATTERNS)


def extract_urls(
    text_parts: list[str],
    html_parts: list[str],
) -> list[ExtractedURL]:
    """Extract up to MAX_URLS URLs from text and HTML email body parts."""
    seen: set[str] = set()
    results: list[ExtractedURL] = []

    def _add(url: str, source: str, anchor: Optional[str] = None, hidden: bool = False):
        if url in seen or len(results) >= _MAX_URLS:
            return
        seen.add(url)
        results.append(ExtractedURL(url=url, source=source, anchor_text=anchor, is_hidden=hidden))

    # Plain-text parts
    for text in text_parts:
        for m in _URL_RE.finditer(text):
            _add(m.group(), "text")

    # HTML parts
    for html in html_parts:
        if _BS4:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all("a", href=True):
                href = tag["href"].strip()
                if not href.startswith("http"):
                    continue
                style = tag.get("style", "") + " " + tag.parent.get("style", "")
                hidden = _is_hidden_style(style)
                anchor = tag.get_text(strip=True)[:100] or None
                _add(href, "html_hidden" if hidden else "html_anchor", anchor, hidden)

            # Also catch raw URLs in text nodes not inside anchors
            for m in _URL_RE.finditer(soup.get_text()):
                _add(m.group(), "text")
        else:
            # Fallback: regex only
            for m in _URL_RE.finditer(html):
                _add(m.group(), "html_anchor")

    return results


def find_hidden_urls(html_parts: list[str]) -> list[str]:
    """Return only the URLs that are visually hidden in HTML."""
    extracted = extract_urls([], html_parts)
    return [e.url for e in extracted if e.is_hidden]
