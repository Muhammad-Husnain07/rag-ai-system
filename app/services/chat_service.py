from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

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
    question: str,
    title: Optional[str] = None
) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(
        user_id=user.id,
        document_id=document.id,
        title=title or (question[:100] if len(question) > 100 else question)
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
    question: str,
    conversation_id: Optional[int] = None
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
    
    if conversation_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user.id
            )
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            conversation = await create_conversation(db, user, document, question)
    else:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.document_id == document_id)
            .order_by(Conversation.created_at.desc())
            .limit(1)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            conversation = await create_conversation(db, user, document, question)
    
    await add_message(db, conversation.id, "user", question)
    await add_message(db, conversation.id, "assistant", answer)
    await db.commit()
    
    return answer, conversation.id, sources


async def get_user_conversations(
    db: AsyncSession,
    user: User,
    limit: int = 50,
    offset: int = 0
) -> List[Conversation]:
    """Get all conversations for a user with pagination."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc(), Conversation.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()


async def get_conversation_messages(
    db: AsyncSession,
    conversation_id: int,
    user_id: int,
    limit: int = 100,
    offset: int = 0
) -> Optional[List[Message]]:
    """Get messages for a conversation with pagination."""
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
        .order_by(Message.created_at.asc())
        .limit(limit)
        .offset(offset)
    )
    
    return result.scalars().all()


async def delete_conversation(
    db: AsyncSession,
    conversation_id: int,
    user_id: int
) -> bool:
    """Delete a conversation and its messages."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        return False
    
    await db.execute(
        delete(Message).where(Message.conversation_id == conversation_id)
    )
    
    await db.delete(conversation)
    await db.commit()
    
    return True


async def update_conversation_title(
    db: AsyncSession,
    conversation_id: int,
    user_id: int,
    new_title: str
) -> Optional[Conversation]:
    """Update conversation title."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        return None
    
    conversation.title = new_title
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


async def search_conversations(
    db: AsyncSession,
    user_id: int,
    query: str,
    limit: int = 20
) -> List[Conversation]:
    """Search conversations by title or message content."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
    )
    conversations = result.scalars().all()
    
    if not query:
        return conversations
    
    query_lower = query.lower()
    filtered = []
    
    for conv in conversations:
        if conv.title and query_lower in conv.title.lower():
            filtered.append(conv)
            continue
            
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.created_at.desc())
            .limit(10)
        )
        messages = result.scalars().all()
        
        for msg in messages:
            if query_lower in msg.content.lower():
                filtered.append(conv)
                break
    
    return filtered[:limit]
