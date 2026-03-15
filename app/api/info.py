"""Lightweight API information endpoints."""
"""Info endpoints micro-docstring for clarity."""
"""Expose lightweight application information for quick introspection."""
from fastapi import APIRouter

router = APIRouter(tags=["Info"])

VERSION = "1.0.0"
APP_NAME = "RAG AI System"
DESCRIPTION = "Production-ready Retrieval-Augmented Generation system"


@router.get("/info")
async def get_app_info():
    """Get application information."""
    return {
        "name": APP_NAME,
        "version": VERSION,
        "description": DESCRIPTION,
        "api_version": "v1"
    }


@router.get("/info/version")
async def get_version():
    """Get version information."""
    return {
        "version": VERSION,
        "major": 1,
        "minor": 0,
        "patch": 0
    }
"""Info endpoints micro-docstring update for clarity."""
