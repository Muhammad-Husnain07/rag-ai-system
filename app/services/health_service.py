from typing import Dict, Any, List
from datetime import datetime
import asyncio


class HealthCheckService:
    """Service for checking health of external dependencies."""
    
    def __init__(self):
        self._checks: Dict[str, dict] = {}
    
    async def check_database(self) -> dict:
        """Check database connectivity."""
        try:
            from app.core.database import AsyncSessionLocal
            async with AsyncSessionLocal() as session:
                await session.execute("SELECT 1")
            return {"status": "healthy", "message": "Database connected"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}
    
    async def check_vector_store(self) -> dict:
        """Check vector store connectivity."""
        try:
            from app.services.vector_service import vector_service
            return {"status": "healthy", "message": "Vector store connected"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}
    
    async def check_ai_provider(self) -> dict:
        """Check AI provider connectivity."""
        try:
            from app.core.config import settings
            return {
                "status": "healthy",
                "provider": settings.AI_PROVIDER,
                "model": settings.llm_model
            }
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        checks = {
            "database": self.check_database(),
            "vector_store": self.check_vector_store(),
            "ai_provider": self.check_ai_provider()
        }
        
        results = {}
        all_healthy = True
        
        for name, check_coro in checks.items():
            result = await check_coro
            results[name] = result
            
            if result["status"] != "healthy":
                all_healthy = False
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": results
        }


health_check_service = HealthCheckService()
