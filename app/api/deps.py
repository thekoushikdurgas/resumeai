"""FastAPI dependencies."""

from collections.abc import AsyncGenerator

from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.db import async_session_factory

settings = get_settings()


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
        )
    return x_api_key


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
