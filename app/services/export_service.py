import json
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation, Message


class ExportService:
    """Service for exporting user data."""
    
    async def export_documents(
        self,
        db: AsyncSession,
        user: User,
        format: str = "json"
    ) -> dict:
        """Export all user documents."""
        result = await db.execute(
            select(Document).where(Document.user_id == user.id)
        )
        documents = result.scalars().all()
        
        if format == "json":
            return {
                "exported_at": datetime.utcnow().isoformat(),
                "total": len(documents),
                "documents": [
                    {
                        "id": doc.id,
                        "title": doc.title,
                        "file_name": doc.file_name,
                        "file_type": doc.file_type,
                        "content": doc.content_text,
                        "chunk_count": doc.chunk_count,
                        "status": doc.status,
                        "created_at": doc.created_at.isoformat() if doc.created_at else None
                    }
                    for doc in documents
                ]
            }
        
        return {"error": "Unsupported format"}
    
    async def export_conversations(
        self,
        db: AsyncSession,
        user: User,
        format: str = "json"
    ) -> dict:
        """Export all user conversations and messages."""
        result = await db.execute(
            select(Conversation).where(Conversation.user_id == user.id)
        )
        conversations = result.scalars().all()
        
        export_data = []
        
        for conv in conversations:
            result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at)
            )
            messages = result.scalars().all()
            
            export_data.append({
                "id": conv.id,
                "title": conv.title,
                "document_id": conv.document_id,
                "created_at": conv.created_at.isoformat() if conv.created_at else None,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat() if msg.created_at else None
                    }
                    for msg in messages
                ]
            })
        
        return {
            "exported_at": datetime.utcnow().isoformat(),
            "total": len(export_data),
            "conversations": export_data
        }
    
    async def export_all(
        self,
        db: AsyncSession,
        user: User
    ) -> dict:
        """Export all user data."""
        documents = await self.export_documents(db, user)
        conversations = await self.export_conversations(db, user)
        
        return {
            "exported_at": datetime.utcnow().isoformat(),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            },
            "documents": documents,
            "conversations": conversations
        }


class ImportService:
    """Service for importing user data."""
    
    async def import_documents(
        self,
        db: AsyncSession,
        user: User,
        data: dict
    ) -> dict:
        """Import documents from JSON data."""
        if "documents" not in data:
            return {"error": "Invalid data format"}
        
        imported = 0
        failed = 0
        errors = []
        
        for doc_data in data["documents"]:
            try:
                document = Document(
                    user_id=user.id,
                    title=doc_data.get("title", "Imported Document"),
                    file_name=doc_data.get("file_name", "imported.txt"),
                    file_type=doc_data.get("file_type", ".txt"),
                    file_size=len(doc_data.get("content", "")),
                    content_text=doc_data.get("content", "")[:10000],
                    chunk_count=doc_data.get("chunk_count", 0),
                    status="imported"
                )
                db.add(document)
                imported += 1
            except Exception as e:
                failed += 1
                errors.append({"document": doc_data.get("title"), "error": str(e)})
        
        await db.commit()
        
        return {
            "imported": imported,
            "failed": failed,
            "errors": errors
        }


export_service = ExportService()
import_service = ImportService()
