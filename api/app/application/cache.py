import os, json, time
from typing import Callable, Optional
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_client = None

def _get_client():
    global _client
    if _client is None:
        _client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return _client

def cache_get(key: str) -> Optional[dict]:
    r = _get_client()
    val = r.get(key)
    return json.loads(val) if val else None

def cache_set(key: str, value: dict, ttl_seconds: int = 60):
    r = _get_client()
    r.setex(key, ttl_seconds, json.dumps(value))

def cache_delete(prefix: str):
    """Borra claves por prefijo (invalidación simple)."""
    r = _get_client()
    for k in r.scan_iter(match=f"{prefix}*"):
        r.delete(k)
