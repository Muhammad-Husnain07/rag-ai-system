from pydantic import BaseModel
from typing import Optional


class StatusResponse(BaseModel):
    success: bool
    message: str
    code: Optional[str] = None


class StatusCheck(BaseModel):
    status: str
    timestamp: str
