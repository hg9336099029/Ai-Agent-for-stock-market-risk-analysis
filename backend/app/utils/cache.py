"""
Simple in-memory cache for API responses
"""

from datetime import datetime, timedelta
from typing import Any, Optional

# Simple dict-based cache
_cache = {}

def set_cache(key: str, value: Any, ttl_seconds: int = 3600):
    """Set a value in cache with TTL"""
    expiry = datetime.now() + timedelta(seconds=ttl_seconds)
    _cache[key] = {
        "value": value,
        "expiry": expiry
    }

def get_cache(key: str) -> Optional[Any]:
    """Get a value from cache if not expired"""
    if key not in _cache:
        return None
    
    cached_item = _cache[key]
    if datetime.now() > cached_item["expiry"]:
        # Expired, remove it
        del _cache[key]
        return None
    
    return cached_item["value"]

def clear_cache():
    """Clear all cache"""
    global _cache
    _cache = {}

def remove_cache(key: str):
    """Remove specific cache key"""
    if key in _cache:
        del _cache[key]
