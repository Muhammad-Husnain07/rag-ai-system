from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.settings import settings_manager, SystemSettings
from app.models.user import User

router = APIRouter(prefix="/settings", tags=["Settings"])


class UpdateSettingsRequest(BaseModel):
    ai_provider: str = "openai"
    llm_model: str = "gpt-4"
    embedding_model: str = "text-embedding-ada-002"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_chunks: int = 5
    system_prompt: str = ""


@router.get("", response_model=dict)
async def get_settings(
    current_user: User = Depends(get_current_active_user)
):
    """Get user settings."""
    settings = settings_manager.get_settings(current_user.id)
    return {
        "ai_provider": settings.ai_provider,
        "llm_model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap,
        "top_k_chunks": settings.top_k_chunks,
        "system_prompt": settings.system_prompt
    }


@router.put("", response_model=dict)
async def update_settings(
    settings_data: UpdateSettingsRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Update user settings."""
    settings = SystemSettings(
        ai_provider=settings_data.ai_provider,
        llm_model=settings_data.llm_model,
        embedding_model=settings_data.embedding_model,
        chunk_size=settings_data.chunk_size,
        chunk_overlap=settings_data.chunk_overlap,
        top_k_chunks=settings_data.top_k_chunks,
        system_prompt=settings_data.system_prompt or """You are a helpful AI assistant that answers questions based on the provided documents.

Instructions:
- Answer the question based only on the provided context
- If the answer cannot be found in the context, say so clearly
- Be concise and accurate
- Cite the sources when possible"""
    )
    
    settings_manager.update_settings(current_user.id, settings)
    
    return {
        "message": "Settings updated successfully",
        "settings": {
            "ai_provider": settings.ai_provider,
            "llm_model": settings.llm_model,
            "embedding_model": settings.embedding_model,
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "top_k_chunks": settings.top_k_chunks
        }
    }


@router.post("/reset", response_model=dict)
async def reset_settings(
    current_user: User = Depends(get_current_active_user)
):
    """Reset settings to defaults."""
    settings_manager.reset_settings(current_user.id)
    return {"message": "Settings reset to defaults"}
