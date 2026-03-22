"""Application configuration."""

import os
from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    PROJECT_NAME: str = "Resume AI Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered resume parsing and enhancement for Contact360"
    ENVIRONMENT: str = Field("development", alias="APP_ENV")
    DEBUG: bool = Field(False, alias="DEBUG")
    PORT: int = Field(8080, alias="PORT")
    LOG_LEVEL: str = Field("INFO", alias="LOG_LEVEL")

    API_KEY: str = Field(..., alias="API_KEY", description="Service-to-service API key")

    GEMINI_API_KEY: str = Field("", alias="GEMINI_API_KEY")
    HF_API_KEY: Optional[str] = Field(None, alias="HF_API_KEY")
    AI_PROVIDER: str = Field("gemini", alias="AI_PROVIDER")  # gemini | huggingface

    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///./resume.db",
        alias="DATABASE_URL",
    )
    DATABASE_ECHO: bool = Field(False, alias="DATABASE_ECHO")
    DATABASE_POOL_SIZE: int = Field(25, alias="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(50, alias="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(30, alias="DATABASE_POOL_TIMEOUT")
    DATABASE_POOL_RECYCLE: int = Field(1800, alias="DATABASE_POOL_RECYCLE")
    DATABASE_POOL_PRE_PING: bool = Field(True, alias="DATABASE_POOL_PRE_PING")
    DATABASE_POOL_RESET_ON_RETURN: str = Field("commit", alias="DATABASE_POOL_RESET_ON_RETURN")

    S3_BUCKET_NAME: str = Field("resume-assets", alias="S3_BUCKET_NAME")

    LAMBDA_S3STORAGE_API_URL: str = Field("", alias="LAMBDA_S3STORAGE_API_URL")
    LAMBDA_S3STORAGE_API_KEY: str = Field("", alias="LAMBDA_S3STORAGE_API_KEY")
    LAMBDA_S3STORAGE_API_TIMEOUT: float = Field(30.0, alias="LAMBDA_S3STORAGE_API_TIMEOUT")

    MAX_UPLOAD_SIZE_MB: int = Field(10, alias="MAX_UPLOAD_SIZE_MB")
    AI_TIMEOUT_SECONDS: int = Field(120, alias="AI_TIMEOUT_SECONDS")

    GEMINI_PARSE_MODEL: str = Field("gemini-2.5-flash", alias="GEMINI_PARSE_MODEL")
    GEMINI_PRO_MODEL: str = Field("gemini-2.5-pro", alias="GEMINI_PRO_MODEL")
    GEMINI_IMAGE_MODEL: str = Field("gemini-2.5-flash-image", alias="GEMINI_IMAGE_MODEL")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
