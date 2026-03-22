"""Request timing middleware."""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.cache_metrics import get_cache_metrics


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Record per-endpoint response times."""

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000
        endpoint = f"{request.method} {request.url.path}"
        metrics = get_cache_metrics()
        metrics.record_response_time(endpoint, duration_ms, cached=False)
        return response
