"""SQLAlchemy async engine and session factory."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    pass


def _create_engine() -> AsyncEngine:
    url = settings.DATABASE_URL
    # SQLite (local tests): no asyncpg pool/connect_args
    if url.startswith("sqlite"):
        return create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
        )

    return create_async_engine(
        url,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_recycle=settings.DATABASE_POOL_RECYCLE,
        pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
        pool_reset_on_return=settings.DATABASE_POOL_RESET_ON_RETURN,
        connect_args={
            "server_settings": {
                "application_name": "resume_ai_service",
                "jit": "off",
            },
            "timeout": 10.0,
            "command_timeout": float(settings.AI_TIMEOUT_SECONDS),
        },
    )


engine = _create_engine()

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
