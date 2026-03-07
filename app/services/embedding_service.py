from typing import List
import openai
from app.core.config import settings


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.EMBEDDING_MODEL
    
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
