from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ApiResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class ListResponse(BaseModel):
    """Standard list response model."""
    items: List[Any]
    total: int
    page: int = 1
    page_size: int = 20
