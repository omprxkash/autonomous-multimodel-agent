"""
Redis-backed cache with in-process dict fallback.
Falls back to an in-memory LRU-style dict when Redis is unavailable.
"""
import json
import time
from typing import Any, Optional

try:
    import redis as redis_lib
    _redis_available = True
except ImportError:
    _redis_available = False

from app.core.config import settings


def get_cache_key(prefix: str, *parts: Any) -> str:
    return f"dp:{prefix}:" + ":".join(str(p) for p in parts)


class _InMemoryCache:
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}  # key → (value, expires_at)

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at and time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear_pattern(self, pattern: str) -> None:
        prefix = pattern.rstrip("*")
        for k in list(self._store.keys()):
            if k.startswith(prefix):
                del self._store[k]


class _RedisCache:
    def __init__(self, url: str):
        self._client = redis_lib.from_url(url, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        try:
            raw = self._client.get(key)
            return json.loads(raw) if raw is not None else None
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        try:
            self._client.set(key, json.dumps(value), ex=ttl)
        except Exception:
            pass

    def delete(self, key: str) -> None:
        try:
            self._client.delete(key)
        except Exception:
            pass

    def clear_pattern(self, pattern: str) -> None:
        try:
            keys = self._client.keys(pattern)
            if keys:
                self._client.delete(*keys)
        except Exception:
            pass


def _build_cache():
    if _redis_available:
        try:
            c = _RedisCache(settings.REDIS_URL)
            c._client.ping()
            return c
        except Exception:
            pass
    return _InMemoryCache()


cache = _build_cache()
