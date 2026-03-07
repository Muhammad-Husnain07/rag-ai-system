from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.document import ChatQueryRequest, ChatQueryResponse, ConversationResponse, MessageResponse
from app.services.chat_service import (
    ask_question,
    get_user_conversations,
    get_conversation_messages
)
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/query", response_model=ChatQueryResponse)
async def query_document(
    request: ChatQueryRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Ask a question about a document and get an AI-generated answer."""
    try:
        answer, conversation_id, sources = await ask_question(
            db,
            current_user,
            request.document_id,
            request.question
        )
        
        return ChatQueryResponse(
            answer=answer,
            conversation_id=conversation_id,
            sources=sources,
            model=settings.LLM_MODEL
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all conversations for the current user."""
    conversations = await get_user_conversations(db, current_user)
    return conversations


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get messages for a specific conversation."""
    messages = await get_conversation_messages(db, conversation_id, current_user.id)
    
    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return messages
