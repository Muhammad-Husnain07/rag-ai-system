from typing import List, Optional
import openai
from app.core.config import settings


class EmbeddingService:
    """Service for generating text embeddings using OpenAI or OpenRouter."""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.model = settings.embedding_model
        
        if self.provider == "openrouter":
            openai.api_key = settings.OPENROUTER_API_KEY
            openai.base_url = "https://openrouter.ai/api/v1"
        else:
            openai.api_key = settings.OPENAI_API_KEY
            openai.base_url = "https://api.openai.com/v1"
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = await openai.Embedding.acreate(
            model=self.model,
            input=text
        )
        return response["data"][0]["embedding"]
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = await openai.Embedding.acreate(
            model=self.model,
            input=texts
        )
        return [item["embedding"] for item in response["data"]]


embedding_service = EmbeddingService()
