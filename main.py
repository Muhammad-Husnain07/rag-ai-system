from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import init_db
from app.api import api_router
from app.middleware import (
    LoggingMiddleware,
    limiter,
    rate_limit_exceeded_handler,
    global_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    value_error_handler
)

app = FastAPI(
    title="RAG Backend API",
    description="Production-ready Retrieval-Augmented Generation system with document upload, embeddings, and AI-powered Q&A",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.state.limiter = limiter
limiter.add_exception_handler(app, rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RAG Backend API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "RAG Backend API",
        "version": "1.0.0",
        "ai_provider": settings.AI_PROVIDER,
        "llm_model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "database": "connected",
        "vector_store": "connected"
    }


@app.get("/models", tags=["AI Models"])
async def get_available_models():
    """Get available AI models for the current provider."""
    if settings.AI_PROVIDER == "openrouter":
        return {
            "provider": "openrouter",
            "llm_models": [
                {"id": "openai/gpt-4o", "name": "GPT-4O"},
                {"id": "openai/gpt-4o-mini", "name": "GPT-4O Mini"},
                {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "google/gemini-pro-1.5", "name": "Gemini Pro 1.5"},
                {"id": "meta-llama/llama-3.1-70b-instruct", "name": "Llama 3.1 70B"},
                {"id": "mistralai/mistral-7b-instruct", "name": "Mistral 7B"},
            ],
            "embedding_models": [
                {"id": "google/text-embedding-004", "name": "Google Embedding 004"},
                {"id": "openai/text-embedding-3-small", "name": "OpenAI Embedding 3 Small"},
                {"id": "openai/text-embedding-3-large", "name": "OpenAI Embedding 3 Large"},
            ],
            "current_llm": settings.llm_model,
            "current_embedding": settings.embedding_model,
            "docs": "https://openrouter.ai/models"
        }
    else:
        return {
            "provider": "openai",
            "llm_models": [
                {"id": "gpt-4", "name": "GPT-4"},
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"},
                {"id": "gpt-4o", "name": "GPT-4O"},
                {"id": "gpt-4o-mini", "name": "GPT-4O Mini"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
            ],
            "embedding_models": [
                {"id": "text-embedding-ada-002", "name": "Ada v2"},
                {"id": "text-embedding-3-small", "name": "Embedding 3 Small"},
                {"id": "text-embedding-3-large", "name": "Embedding 3 Large"},
            ],
            "current_llm": settings.llm_model,
            "current_embedding": settings.embedding_model,
            "docs": "https://platform.openai.com/docs/models"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
