from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    title: str


class DocumentCreate(DocumentBase):
    pass


class DocumentChunkResponse(BaseModel):
    id: int
    chunk_index: int
    content: str
    
    class Config:
        from_attributes = True


class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    file_name: str
    file_type: str
    file_size: int
    chunk_count: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    chunks: List[DocumentChunkResponse] = []


class DocumentUploadResponse(BaseModel):
    id: int
    title: str
    file_name: str
    status: str
    chunk_count: int
    message: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    document_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ChatQueryRequest(BaseModel):
    document_id: int
    question: str = Field(..., min_length=1, max_length=2000)


class ChatQueryResponse(BaseModel):
    answer: str
    conversation_id: int
    sources: List[str]
    model: str
