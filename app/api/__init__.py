from fastapi import APIRouter
from app.api import auth, documents, chat, settings, analytics, export, admin

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(chat.router)
api_router.include_router(settings.router)
api_router.include_router(analytics.router)
api_router.include_router(export.router)
api_router.include_router(admin.router)
