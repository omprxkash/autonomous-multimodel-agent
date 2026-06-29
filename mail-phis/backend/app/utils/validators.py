import re
from urllib.parse import urlparse
from app.core.config import settings

URL_RE = re.compile(
    r"^(https?://)"
    r"([a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+)$"
)


def validate_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    return url


def validate_eml_size(size_bytes: int):
    limit = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if size_bytes > limit:
        raise ValueError(f"File exceeds {settings.MAX_FILE_SIZE_MB} MB limit")
