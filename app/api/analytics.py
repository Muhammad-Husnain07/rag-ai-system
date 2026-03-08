from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation, Message

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/usage", response_model=dict)
async def get_usage_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user usage statistics."""
    doc_count = await db.scalar(
        select(func.count(Document.id)).where(Document.user_id == current_user.id)
    )
    
    conv_count = await db.scalar(
        select(func.count(Conversation.id)).where(Conversation.user_id == current_user.id)
    )
    
    msg_count = await db.scalar(
        select(func.count(Message.id))
        .join(Conversation)
        .where(Conversation.user_id == current_user.id)
    )
    
    total_chunks = await db.scalar(
        select(func.sum(Document.chunk_count))
        .where(Document.user_id == current_user.id)
    ) or 0
    
    total_file_size = await db.scalar(
        select(func.sum(Document.file_size))
        .where(Document.user_id == current_user.id)
    ) or 0
    
    result = await db.execute(
        select(Document.status, func.count(Document.id))
        .where(Document.user_id == current_user.id)
        .group_by(Document.status)
    )
    status_counts = {row[0]: row[1] for row in result.all()}
    
    return {
        "total_documents": doc_count or 0,
        "total_conversations": conv_count or 0,
        "total_messages": msg_count or 0,
        "total_chunks": total_chunks,
        "total_file_size_bytes": total_file_size,
        "documents_by_status": status_counts
    }


@router.get("/recent-activity", response_model=dict)
async def get_recent_activity(
    days: int = 7,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recent activity summary."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    docs_created = await db.scalar(
        select(func.count(Document.id))
        .where(
            Document.user_id == current_user.id,
            Document.created_at >= cutoff_date
        )
    )
    
    messages_sent = await db.scalar(
        select(func.count(Message.id))
        .join(Conversation)
        .where(
            Conversation.user_id == current_user.id,
            Message.created_at >= cutoff_date
        )
    )
    
    return {
        "period_days": days,
        "documents_created": docs_created or 0,
        "messages_sent": messages_sent or 0
    }


@router.get("/document-stats/{document_id}", response_model=dict)
async def get_document_stats(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get statistics for a specific document."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        return {"error": "Document not found"}
    
    conv_count = await db.scalar(
        select(func.count(Conversation.id))
        .where(Conversation.document_id == document_id)
    )
    
    msg_count = await db.scalar(
        select(func.count(Message.id))
        .join(Conversation)
        .where(Conversation.document_id == document_id)
    )
    
    return {
        "document_id": document_id,
        "title": document.title,
        "file_name": document.file_name,
        "file_size": document.file_size,
        "chunk_count": document.chunk_count,
        "status": document.status,
        "conversations": conv_count or 0,
        "messages": msg_count or 0,
        "created_at": document.created_at.isoformat() if document.created_at else None
    }
