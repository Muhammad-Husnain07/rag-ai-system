import os
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile

from app.models.document import Document, DocumentChunk
from app.models.user import User
from app.core.config import settings
from app.utils.file_parser import extract_text_from_file, validate_file
from app.utils.text_chunker import chunk_text
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service


async def process_document(
    db: AsyncSession,
    user: User,
    file: UploadFile,
    title: str
) -> Document:
    """Process uploaded document: extract text, chunk, embed, and store."""
    file_content = await file.read()
    file_size = len(file_content)
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    is_valid, error_msg = validate_file(file.filename, file_size, settings.MAX_FILE_SIZE_MB)
    if not is_valid:
        raise ValueError(error_msg)
    
    text_content = await extract_text_from_file(file_content, file_extension)
    
    if not text_content.strip():
        raise ValueError("No text could be extracted from the document")
    
    document = Document(
        user_id=user.id,
        title=title or file.filename,
        file_name=file.filename,
        file_type=file_extension,
        file_size=file_size,
        content_text=text_content[:10000],
        status="processing"
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    try:
        chunks = chunk_text(
            text_content,
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP
        )
        
        for i, chunk_content in enumerate(chunks):
            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=i,
                content=chunk_content
            )
            db.add(chunk)
        
        document.chunk_count = len(chunks)
        
        embeddings = await embedding_service.generate_embeddings(chunks)
        
        ids = [f"doc_{document.id}_chunk_{i}" for i in range(len(chunks))]
        metadata = [
            {
                "document_id": str(document.id),
                "user_id": str(user.id),
                "chunk_index": i,
                "content": chunks[i][:500],
                "source": document.file_name
            }
            for i in range(len(chunks))
        ]
        
        await vector_service.upsert_vectors(embeddings, ids, metadata)
        
        for i, chunk in enumerate(chunks):
            chunk.embedding_id = ids[i]
        
        document.pinecone_id = f"doc_{document.id}"
        document.status = "completed"
        
        await db.commit()
        await db.refresh(document)
        
    except Exception as e:
        document.status = "failed"
        await db.commit()
        raise ValueError(f"Error processing document: {str(e)}")
    
    return document


async def get_user_documents(db: AsyncSession, user: User) -> List[Document]:
    """Get all documents for a user."""
    result = await db.execute(
        select(Document)
        .where(Document.user_id == user.id)
        .order_by(Document.created_at.desc())
    )
    return result.scalars().all()


async def get_document(db: AsyncSession, document_id: int, user_id: int) -> Optional[Document]:
    """Get a specific document."""
    result = await db.execute(
        select(Document)
        .where(Document.id == document_id, Document.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def delete_document(db: AsyncSession, document: Document):
    """Delete a document and its vectors."""
    try:
        await vector_service.delete_by_filter({
            "document_id": str(document.id)
        })
    except Exception:
        pass
    
    await db.delete(document)
    await db.commit()
