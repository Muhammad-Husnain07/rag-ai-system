import time
from typing import Optional, Any, Dict
from datetime import datetime, timedelta


class CacheService:
    """Simple in-memory cache service."""
    
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache."""
        expiry = time.time() + (ttl or self._ttl)
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str):
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cache."""
        self._cache.clear()
    
    def cleanup(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self._cache.items()
            if current_time >= expiry
        ]
        for key in expired_keys:
            del self._cache[key]
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        self.cleanup()
        return {
            "total_entries": len(self._cache),
            "ttl_seconds": self._ttl
        }


cache_service = CacheService()
