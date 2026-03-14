from pydantic import BaseModel
from typing import Optional


class HealthCheckResponse(BaseModel):
    status: str
    message: Optional[str] = None


class ServiceHealthResponse(BaseModel):
    database: str
    vector_store: str
    ai_provider: str


class DetailedHealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    total_requests: int
    total_errors: int
    services: ServiceHealthResponse
