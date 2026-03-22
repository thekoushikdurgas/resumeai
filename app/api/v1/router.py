"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import ai, health, resume

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
