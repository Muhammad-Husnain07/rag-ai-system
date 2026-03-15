"""Admin endpoints for system management (tiny docstring)."""
"""Admin endpoints for system management (tiny docstring)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation, Message
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])


class SystemStats(BaseModel):
    total_users: int
    total_documents: int
    total_conversations: int
    total_messages: int
    active_users_24h: int


class UserListItem(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system-wide statistics (admin only)."""
    if not settings.ADMIN_EMAILS or current_user.email not in settings.ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    total_users = await db.scalar(select(func.count(User.id))) or 0
    total_documents = await db.scalar(select(func.count(Document.id))) or 0
    total_conversations = await db.scalar(select(func.count(Conversation.id))) or 0
    total_messages = await db.scalar(select(func.count(Message.id))) or 0
    
    return SystemStats(
        total_users=total_users,
        total_documents=total_documents,
        total_conversations=total_conversations,
        total_messages=total_messages,
        active_users_24h=0
    )


@router.get("/users", response_model=list)
async def list_all_users(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List all users (admin only)."""
    if not settings.ADMIN_EMAILS or current_user.email not in settings.ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    
    return [
        UserListItem(
            id=u.id,
            email=u.email,
            username=u.username,
            is_active=u.is_active,
            created_at=u.created_at.isoformat() if u.created_at else ""
        )
        for u in users
    ]


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Deactivate a user (admin only)."""
    if not settings.ADMIN_EMAILS or current_user.email not in settings.ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    await db.commit()
    
    return {"message": f"User {user.username} deactivated"}


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Activate a user (admin only)."""
    if not settings.ADMIN_EMAILS or current_user.email not in settings.ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    await db.commit()
    
    return {"message": f"User {user.username} activated"}
