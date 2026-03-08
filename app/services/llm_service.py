from typing import List, Dict, Any
import openai
from app.core.config import settings


class LLMService:
    """Service for generating answers using OpenAI GPT or OpenRouter models."""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.model = settings.llm_model
        
        if self.provider == "openrouter":
            openai.api_key = settings.OPENROUTER_API_KEY
            openai.base_url = "https://openrouter.ai/api/v1"
        else:
            openai.api_key = settings.OPENAI_API_KEY
            openai.base_url = "https://api.openai.com/v1"
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]]
    ) -> tuple[str, List[str]]:
        """
        Generate answer based on question and context.
        
        Returns:
            Tuple of (answer, sources)
        """
        if not context_chunks:
            return "I couldn't find any relevant information in the documents to answer your question.", []
        
        context = "\n\n".join([
            f"Document {i+1}:\n{chunk['metadata'].get('content', '')}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        sources = [
            chunk['metadata'].get('source', f'Chunk {i+1}')
            for i, chunk in enumerate(context_chunks)
        ]
        
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided documents.
        
Instructions:
- Answer the question based only on the provided context
- If the answer cannot be found in the context, say so clearly
- Be concise and accurate
- Cite the sources when possible"""
        
        prompt = f"""Context from documents:
{context}

Question: {question}

Answer:"""
        
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        return answer, sources


llm_service = LLMService()
