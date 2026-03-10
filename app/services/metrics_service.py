from typing import Dict, Any
from datetime import datetime, timedelta
import time


class MetricsService:
    """Service for tracking application metrics."""
    
    def __init__(self):
        self._requests: Dict[str, list] = {}
        self._errors: Dict[str, int] = {}
        self._start_time = time.time()
        self._api_calls = 0
        self._ai_calls = 0
        self._total_tokens = 0
    
    def record_request(self, endpoint: str, method: str, status_code: int, duration_ms: float):
        """Record an API request."""
        key = f"{method} {endpoint}"
        
        if key not in self._requests:
            self._requests[key] = []
        
        self._requests[key].append({
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code,
            "duration_ms": duration_ms
        })
        
        self._api_calls += 1
        
        if status_code >= 400:
            self._errors[key] = self._errors.get(key, 0) + 1
    
    def record_ai_call(self, tokens_used: int = 0):
        """Record an AI API call."""
        self._ai_calls += 1
        self._total_tokens += tokens_used
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        uptime_seconds = time.time() - self._start_time
        
        return {
            "uptime_seconds": round(uptime_seconds, 2),
            "total_api_calls": self._api_calls,
            "total_ai_calls": self._ai_calls,
            "total_tokens": self._total_tokens,
            "total_errors": sum(self._errors.values()),
            "requests_per_second": round(self._api_calls / uptime_seconds, 2) if uptime_seconds > 0 else 0
        }
    
    def get_endpoint_stats(self) -> Dict[str, Any]:
        """Get endpoint-level statistics."""
        stats = {}
        
        for key, requests in self._requests.items():
            if not requests:
                continue
            
            recent = requests[-100:]
            success = sum(1 for r in recent if r["status_code"] < 400)
            avg_duration = sum(r["duration_ms"] for r in recent) / len(recent) if recent else 0
            
            stats[key] = {
                "total_calls": len(requests),
                "success_rate": round(success / len(recent) * 100, 2) if recent else 0,
                "avg_duration_ms": round(avg_duration, 2),
                "errors": self._errors.get(key, 0)
            }
        
        return stats
    
    def reset_metrics(self):
        """Reset all metrics."""
        self._requests = {}
        self._errors = {}
        self._api_calls = 0
        self._ai_calls = 0
        self._total_tokens = 0
        self._start_time = time.time()


metrics_service = MetricsService()
