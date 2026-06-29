"""
Security configuration — shared constants for all analysis services.
Brand keywords, suspicious TLDs, risky extensions, URL shorteners.
"""
import hashlib

BRAND_KEYWORDS = [
    "paypal", "microsoft", "apple", "google", "amazon", "netflix",
    "facebook", "instagram", "whatsapp", "twitter", "linkedin",
    "dropbox", "adobe", "chase", "wellsfargo", "bankofamerica",
    "citibank", "hsbc", "barclays", "usps", "fedex", "dhl",
    "irs", "hmrc", "gov", "admin", "support", "security",
    "verify", "confirm", "update", "suspend", "locked", "urgent",
]

SUSPICIOUS_TLDS = [
    ".ru", ".cn", ".tk", ".ml", ".ga", ".cf", ".gq",
    ".xyz", ".top", ".buzz", ".club", ".work", ".date",
    ".bid", ".stream", ".click", ".link", ".info", ".pw",
]

EXECUTABLE_EXTENSIONS = [
    ".exe", ".msi", ".bat", ".cmd", ".com", ".scr", ".pif",
    ".vbs", ".vbe", ".js", ".jse", ".wsf", ".wsh", ".ps1",
    ".psm1", ".reg",
]

MACRO_EXTENSIONS = [
    ".docm", ".xlsm", ".pptm", ".dotm", ".xltm",
]

ARCHIVE_EXTENSIONS = [
    ".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".img",
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "is.gd", "buff.ly", "j.mp", "rb.gy", "cutt.ly",
    "shorturl.at", "tiny.cc",
]


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_url_hash(url: str) -> str:
    normalized = url.strip().lower().rstrip("/")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
