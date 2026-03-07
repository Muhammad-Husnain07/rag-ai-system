from typing import List, Dict, Any
import openai
from app.core.config import settings


class LLMService:
    """Service for generating answers using OpenAI GPT."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL
    
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
        
        prompt = f"""You are a helpful AI assistant that answers questions based on the provided documents.
            
Context from documents:
{context}

Question: {question}

Instructions:
- Answer the question based only on the provided context
- If the answer cannot be found in the context, say so clearly
- Be concise and accurate
- Cite the sources when possible

Answer:"""

        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        return answer, sources


llm_service = LLMService()
