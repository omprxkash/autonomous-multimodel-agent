"""
Redis cache abstraction with domain-intel, DNS, and threat-lookup TTL helpers.
Falls back to an in-process dict when Redis is unavailable.
"""
import json
import time
from typing import Any, Optional

try:
    import redis as _redis_lib
    _REDIS_OK = True
except ImportError:
    _REDIS_OK = False

from app.core.config import settings

# TTL constants (seconds)
TTL_DNS = 3600          # 1 hour — DNS records change rarely
TTL_WHOIS = 86400       # 24 hours — WHOIS data is stable
TTL_THREAT_FEED = 1800  # 30 minutes — phishing feeds update frequently
TTL_IP_REP = 3600       # 1 hour — IP reputation scores


def _make_key(namespace: str, *parts: Any) -> str:
    return f"mp:{namespace}:" + ":".join(str(p) for p in parts)


class _DictCache:
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        value, exp = entry
        if time.time() > exp:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)


class _RedisCache:
    def __init__(self, url: str):
        self._r = _redis_lib.from_url(url, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        try:
            raw = self._r.get(key)
            return json.loads(raw) if raw is not None else None
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        try:
            self._r.set(key, json.dumps(value), ex=ttl)
        except Exception:
            pass

    def delete(self, key: str) -> None:
        try:
            self._r.delete(key)
        except Exception:
            pass


class CacheService:
    """Unified cache with domain-specific helper methods."""

    def __init__(self):
        self._backend = self._build()

    def _build(self):
        if _REDIS_OK:
            try:
                c = _RedisCache(settings.REDIS_URL)
                c._r.ping()
                return c
            except Exception:
                pass
        return _DictCache()

    # --- Generic ---

    def get(self, key: str) -> Optional[Any]:
        return self._backend.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._backend.set(key, value, ttl)

    def delete(self, key: str) -> None:
        self._backend.delete(key)

    # --- Domain helpers ---

    def get_dns(self, domain: str) -> Optional[dict]:
        return self.get(_make_key("dns", domain))

    def set_dns(self, domain: str, result: dict) -> None:
        self.set(_make_key("dns", domain), result, TTL_DNS)

    def get_whois(self, domain: str) -> Optional[dict]:
        return self.get(_make_key("whois", domain))

    def set_whois(self, domain: str, result: dict) -> None:
        self.set(_make_key("whois", domain), result, TTL_WHOIS)

    # --- Threat intel helpers ---

    def get_threat(self, url_or_domain: str) -> Optional[dict]:
        return self.get(_make_key("threat", url_or_domain))

    def set_threat(self, url_or_domain: str, result: dict) -> None:
        self.set(_make_key("threat", url_or_domain), result, TTL_THREAT_FEED)

    def get_openphish_feed(self) -> Optional[list]:
        return self.get(_make_key("feed", "openphish"))

    def set_openphish_feed(self, urls: list) -> None:
        self.set(_make_key("feed", "openphish"), urls, TTL_THREAT_FEED)

    def get_ip_reputation(self, ip: str) -> Optional[dict]:
        return self.get(_make_key("ip", ip))

    def set_ip_reputation(self, ip: str, result: dict) -> None:
        self.set(_make_key("ip", ip), result, TTL_IP_REP)


cache = CacheService()
