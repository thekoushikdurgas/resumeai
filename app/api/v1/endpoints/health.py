"""Health endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings

settings = get_settings()
router = APIRouter()


@router.get("")
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}


@router.get("/info")
async def health_info():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
    }
