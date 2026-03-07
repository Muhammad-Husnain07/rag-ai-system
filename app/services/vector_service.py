from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings


class VectorService:
    """Service for vector database operations using Pinecone."""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self._ensure_index()
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index(self):
        """Ensure the Pinecone index exists."""
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=settings.PINECONE_ENVIRONMENT
                )
            )
    
    async def upsert_vectors(
        self,
        vectors: List[List[float]],
        ids: List[str],
        metadata: List[Dict[str, Any]]
    ):
        """Insert or update vectors in Pinecone."""
        vectors_data = [
            {
                "id": ids[i],
                "values": vectors[i],
                "metadata": metadata[i]
            }
            for i in range(len(vectors))
        ]
        
        self.index.upsert(vectors=vectors_data)
    
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter=filter_dict,
            include_metadata=True
        )
        
        return [
            {
                "id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            }
            for match in results["matches"]
        ]
    
    async def delete_vectors(self, ids: List[str]):
        """Delete vectors by IDs."""
        self.index.delete(ids=ids)
    
    async def delete_by_filter(self, filter_dict: Dict[str, Any]):
        """Delete vectors by filter."""
        self.index.delete(filter=filter_dict)


vector_service = VectorService()
