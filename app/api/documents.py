from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.document import (
    DocumentResponse,
    DocumentDetailResponse,
    DocumentUploadResponse
)
from app.services.document_service import (
    process_document,
    get_user_documents,
    get_document,
    delete_document
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(""),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a document (PDF, TXT, or MD) for processing."""
    try:
        document = await process_document(db, current_user, file, title)
        return DocumentUploadResponse(
            id=document.id,
            title=document.title,
            file_name=document.file_name,
            status=document.status,
            chunk_count=document.chunk_count,
            message="Document uploaded and processed successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all documents for the current user."""
    documents = await get_user_documents(db, current_user)
    return documents


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document_details(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get details of a specific document."""
    document = await get_document(db, document_id, current_user.id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a document."""
    document = await get_document(db, document_id, current_user.id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    await delete_document(db, document)
