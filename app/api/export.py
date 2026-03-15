from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.export_service import export_service, import_service

router = APIRouter(prefix="/export", tags=["Data Management"])


class ImportDataRequest(BaseModel):
    data: dict


@router.get("/documents", response_model=dict)
async def export_user_documents(
    format: str = Query("json", regex="^(json)$"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Export all user documents."""
    return await export_service.export_documents(db, current_user, format)


@router.get("/conversations", response_model=dict)
async def export_user_conversations(
    format: str = Query("json", regex="^(json)$"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Export all user conversations and messages."""
    return await export_service.export_conversations(db, current_user, format)


@router.get("/all", response_model=dict)
async def export_all_data(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Export all user data including documents and conversations."""
    return await export_service.export_all(db, current_user)


@router.post("/import/documents", response_model=dict)
async def import_documents(
    import_data: ImportDataRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Import documents from JSON data."""
    result = await import_service.import_documents(db, current_user, import_data.data)
    return {
        "message": f"Imported {result.get('imported', 0)} documents",
        "details": result
    }
"""Data export/import endpoints for user data backups."""
