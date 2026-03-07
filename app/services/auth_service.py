from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate, Token


async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Register a new user."""
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")
    
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise ValueError("Username already taken")
    
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password)
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


def generate_tokens(user: User) -> Token:
    """Generate access and refresh tokens for user."""
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
    """Refresh access token using refresh token."""
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token payload")
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise ValueError("User not found or inactive")
    
    return generate_tokens(user)
