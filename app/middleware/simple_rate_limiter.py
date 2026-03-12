from typing import Optional, Any
import hashlib
import hmac
import time


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        self._requests: dict = {}
    
    def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, Optional[str]]:
        """Check if request is within rate limit."""
        now = time.time()
        window_start = now - window_seconds
        
        if key not in self._requests:
            self._requests[key] = []
        
        self._requests[key] = [
            req_time for req_time in self._requests[key]
            if req_time > window_start
        ]
        
        if len(self._requests[key]) >= max_requests:
            return False, f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds."
        
        self._requests[key].append(now)
        return True, None
    
    def reset(self, key: str):
        """Reset rate limit for a key."""
        if key in self._requests:
            del self._requests[key]


rate_limiter = RateLimiter()
