from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # API Configuration
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/rag_db"
    
    # Vector Database
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-west1-aws"
    PINECONE_INDEX_NAME: str = "rag-index"
    
    # AI Providers
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    
    # AI Provider: "openai" or "openrouter"
    AI_PROVIDER: str = "openai"
    
    # OpenRouter Models
    OPENROUTER_LLM_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_EMBEDDING_MODEL: str = "google/text-embedding-004"
    
    # OpenAI Models
    OPENAI_LLM_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # JWT Settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Text Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_CHUNKS: int = 5
    
    # File Settings
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".md", ".docx", ".doc"]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "text/plain",
        "text/markdown",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    # Vector Store: "pinecone", "chroma", or "weaviate"
    VECTOR_STORE: str = "pinecone"
    
    # ChromaDB Settings
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    
    # Weaviate Settings
    WEAVIATE_URL: str = "http://localhost:8080"
    WEAVIATE_API_KEY: str = ""
    
    # Cache Settings
    ENABLE_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 3600
    
    # Admin Settings
    ADMIN_EMAILS: List[str] = []
    ENABLE_ADMIN_API: bool = False
    
    # System Prompt Customization
    SYSTEM_PROMPT: str = """You are a helpful AI assistant that answers questions based on the provided documents.

Instructions:
- Answer the question based only on the provided context
- If the answer cannot be found in the context, say so clearly
- Be concise and accurate
- Cite the sources when possible"""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def llm_model(self) -> str:
        if self.AI_PROVIDER == "openrouter":
            return self.OPENROUTER_LLM_MODEL
        return self.OPENAI_LLM_MODEL
    
    @property
    def embedding_model(self) -> str:
        if self.AI_PROVIDER == "openrouter":
            return self.OPENROUTER_EMBEDDING_MODEL
        return self.OPENAI_EMBEDDING_MODEL


settings = Settings()
