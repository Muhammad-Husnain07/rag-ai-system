from typing import Optional
from pydantic import BaseModel


class SystemSettings(BaseModel):
    ai_provider: str = "openai"
    llm_model: str = "gpt-4"
    embedding_model: str = "text-embedding-ada-002"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_chunks: int = 5
    max_file_size_mb: int = 10
    system_prompt: str = """You are a helpful AI assistant that answers questions based on the provided documents.

Instructions:
- Answer the question based only on the provided context
- If the answer cannot be found in the context, say so clearly
- Be concise and accurate
- Cite the sources when possible"""


class SettingsManager:
    """Runtime settings manager for user preferences."""
    
    def __init__(self):
        self._settings: dict[int, SystemSettings] = {}
    
    def get_settings(self, user_id: int) -> SystemSettings:
        if user_id not in self._settings:
            self._settings[user_id] = SystemSettings()
        return self._settings[user_id]
    
    def update_settings(self, user_id: int, settings: SystemSettings):
        self._settings[user_id] = settings
    
    def reset_settings(self, user_id: int):
        if user_id in self._settings:
            del self._settings[user_id]


settings_manager = SettingsManager()
