from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/rag_db"
    
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str = "us-west1-aws"
    PINECONE_INDEX_NAME: str = "rag-index"
    
    OPENAI_API_KEY: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    RATE_LIMIT_PER_MINUTE: int = 100
    LOG_LEVEL: str = "INFO"
    
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_CHUNKS: int = 5
    LLM_MODEL: str = "gpt-4"
    
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = [".pdf", ".txt", ".md"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
