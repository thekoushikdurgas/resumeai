"""FastAPI application entry."""

import utils.transport
import utils.session
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    AIServiceError,
    AuthenticationError,
    DatabaseError,
    InvalidResumeIDError,
    ResumeAIException,
    ResumeNotFoundError,
    ResumeStorageError,
    ValidationError,
)
from app.middleware.compression import CompressionMiddleware
from app.middleware.monitoring import MonitoringMiddleware
from app.models.resume_repository import init_db
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CompressionMiddleware, minimum_size=1024)
app.add_middleware(MonitoringMiddleware)

app.include_router(api_router, prefix="/v1")


@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "endpoints": {
            "health": "/v1/health",
            "health_info": "/v1/health/info",
            "resume": "/v1/resume",
            "ai": "/v1/ai",
            "docs": "/docs",
        },
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(ResumeAIException)
async def resume_api_exception_handler(request, exc: ResumeAIException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, (ResumeNotFoundError, InvalidResumeIDError)):
        code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ValidationError):
        code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, AuthenticationError):
        code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, DatabaseError):
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(exc, AIServiceError):
        code = status.HTTP_502_BAD_GATEWAY
    elif isinstance(exc, ResumeStorageError):
        code = status.HTTP_502_BAD_GATEWAY
    return JSONResponse(
        status_code=code,
        content={"error": exc.__class__.__name__, "message": str(exc), "success": False},
    )


def handler(event, context):
    """AWS Lambda entry (Mangum)."""
    from mangum import Mangum

    return Mangum(app, lifespan="auto")(event, context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
    )
