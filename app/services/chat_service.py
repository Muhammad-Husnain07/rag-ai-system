from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation, Message
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from app.services.llm_service import llm_service
from app.core.config import settings


async def create_conversation(
    db: AsyncSession,
    user: User,
    document: Document,
    question: str
) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(
        user_id=user.id,
        document_id=document.id,
        title=question[:100] if len(question) > 100 else question
    )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


async def add_message(
    db: AsyncSession,
    conversation_id: int,
    role: str,
    content: str
) -> Message:
    """Add a message to a conversation."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    
    db.add(message)
    await db.commit()
    await db.refresh(message)
    
    return message


async def ask_question(
    db: AsyncSession,
    user: User,
    document_id: int,
    question: str
) -> tuple[str, int, List[str]]:
    """Ask a question about a document."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == user.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise ValueError("Document not found")
    
    if document.status != "completed":
        raise ValueError("Document is still processing or failed")
    
    query_embedding = await embedding_service.generate_embedding(question)
    
    search_results = await vector_service.search(
        query_vector=query_embedding,
        top_k=settings.TOP_K_CHUNKS,
        filter_dict={"document_id": str(document_id)}
    )
    
    if not search_results:
        raise ValueError("No relevant context found in document")
    
    answer, sources = await llm_service.generate_answer(question, search_results)
    
    result = await db.execute(
        select(Conversation)
        .where(Conversation.document_id == document_id)
        .order_by(Conversation.created_at.desc())
        .limit(1)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        conversation = await create_conversation(db, user, document, question)
    else:
        conversation.updated_at = None
    
    await add_message(db, conversation.id, "user", question)
    await add_message(db, conversation.id, "assistant", answer)
    await db.commit()
    
    return answer, conversation.id, sources


async def get_user_conversations(
    db: AsyncSession,
    user: User
) -> List[Conversation]:
    """Get all conversations for a user."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc(), Conversation.created_at.desc())
    )
    return result.scalars().all()


async def get_conversation_messages(
    db: AsyncSession,
    conversation_id: int,
    user_id: int
) -> Optional[List[Message]]:
    """Get messages for a conversation."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        return None
    
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    
    return result.scalars().all()
