from typing import Any, Dict, List, Optional
from pydantic import validator


class ConfigValidator:
    """Validate configuration values."""
    
    @staticmethod
    def validate_database_url(url: str) -> bool:
        return url.startswith("postgresql://")
    
    @staticmethod
    def validate_pinecone_env(env: str) -> bool:
        return len(env) > 0
    
    @staticmethod
    def validate_jwt_secret(secret: str) -> bool:
        return len(secret) >= 32
    
    @staticmethod
    def validate_rate_limit(limit: int) -> bool:
        return 1 <= limit <= 1000
    
    @staticmethod
    def validate_chunk_size(size: int) -> bool:
        return 100 <= size <= 10000


validator = ConfigValidator()
