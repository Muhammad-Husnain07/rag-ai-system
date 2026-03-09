from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.models.user import User
from app.services.document_service import process_document
from app.utils.file_parser import validate_file
import os


class BatchProcessingService:
    """Service for batch processing multiple documents."""
    
    def __init__(self):
        self.processing_queue: List[dict] = []
        self.max_queue_size = 100
    
    async def add_to_queue(
        self,
        db: AsyncSession,
        user: User,
        files: List[tuple],
        titles: Optional[List[str]] = None
    ) -> dict:
        """Add multiple files to processing queue."""
        if len(files) > self.max_queue_size:
            raise ValueError(f"Maximum {self.max_queue_size} files allowed")
        
        results = []
        
        for i, (file, file_content) in enumerate(files):
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            is_valid, error_msg = validate_file(
                file.filename,
                len(file_content),
                10
            )
            
            if not is_valid:
                results.append({
                    "filename": file.filename,
                    "status": "failed",
                    "error": error_msg
                })
                continue
            
            title = titles[i] if titles and i < len(titles) else file.filename
            
            try:
                document = await process_document(db, user, file, title)
                results.append({
                    "filename": file.filename,
                    "status": "completed",
                    "document_id": document.id,
                    "chunk_count": document.chunk_count
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "total": len(files),
            "completed": len([r for r in results if r["status"] == "completed"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results
        }
    
    async def get_queue_status(self, user_id: int) -> dict:
        """Get processing queue status for user."""
        user_queue = [item for item in self.processing_queue if item.get("user_id") == user_id]
        
        return {
            "total_queued": len(user_queue),
            "processing": len([item for item in user_queue if item.get("status") == "processing"]),
            "completed": len([item for item in user_queue if item.get("status") == "completed"]),
            "failed": len([item for item in user_queue if item.get("status") == "failed"])
        }


batch_service = BatchProcessingService()
