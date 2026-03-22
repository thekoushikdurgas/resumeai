"""HTTP client for the s3storage Lambda API (logical buckets, resume/ prefix)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.exceptions import ResumeStorageError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class S3StorageClient:
    """Minimal async client for resume JSON upload, download, and delete."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        settings = get_settings()
        self.base_url = (base_url or settings.LAMBDA_S3STORAGE_API_URL or "").rstrip("/")
        self.api_key = api_key if api_key is not None else settings.LAMBDA_S3STORAGE_API_KEY
        self.timeout = float(timeout if timeout is not None else settings.LAMBDA_S3STORAGE_API_TIMEOUT)

    def _headers_json(self) -> dict[str, str]:
        h: dict[str, str] = {}
        if self.api_key:
            h["X-API-Key"] = self.api_key
        return h

    async def upload_resume_json(
        self,
        bucket_id: str,
        filename: str,
        data: bytes,
    ) -> str:
        """POST /api/v1/uploads/resume — returns logical file_key (e.g. resume/{id}.json)."""
        if not self.base_url:
            raise ResumeStorageError("LAMBDA_S3STORAGE_API_URL is not configured")
        if not bucket_id or not filename:
            raise ResumeStorageError("bucket_id and filename are required")

        url = f"{self.base_url}/api/v1/uploads/resume"
        headers = self._headers_json()
        # Multipart: let httpx set Content-Type with boundary
        files = {"file": (filename, data, "application/json")}
        params = {"bucket_id": bucket_id}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, params=params, files=files)
        except httpx.HTTPError as exc:
            logger.exception("s3storage upload failed", extra={"bucket_id": bucket_id})
            raise ResumeStorageError(f"Storage upload failed: {exc}") from exc

        if resp.status_code >= 400:
            raise ResumeStorageError(
                f"Storage upload HTTP {resp.status_code}: {resp.text[:500]}",
            )

        try:
            payload = resp.json()
        except json.JSONDecodeError as exc:
            raise ResumeStorageError("Invalid JSON from storage upload") from exc

        key = payload.get("fileKey")
        if not isinstance(key, str) or not key:
            raise ResumeStorageError("Storage upload response missing fileKey")
        return key

    async def get_download_url(self, bucket_id: str, file_key: str) -> tuple[str, int]:
        """GET presigned URL for an object."""
        if not self.base_url:
            raise ResumeStorageError("LAMBDA_S3STORAGE_API_URL is not configured")

        url = f"{self.base_url}/api/v1/buckets/{bucket_id}/objects/download-url"
        params: dict[str, Any] = {"file_key": file_key}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(
                    url,
                    headers={**self._headers_json(), "Content-Type": "application/json"},
                    params=params,
                )
        except httpx.HTTPError as exc:
            raise ResumeStorageError(f"Storage download-url failed: {exc}") from exc

        if resp.status_code >= 400:
            raise ResumeStorageError(
                f"Storage download-url HTTP {resp.status_code}: {resp.text[:500]}",
            )

        try:
            payload = resp.json()
        except json.JSONDecodeError as exc:
            raise ResumeStorageError("Invalid JSON from storage download-url") from exc

        durl = payload.get("downloadUrl")
        ttl = payload.get("expiresIn")
        if not isinstance(durl, str) or not isinstance(ttl, int):
            raise ResumeStorageError("Invalid download URL payload from storage")
        return durl, ttl

    async def fetch_json_object(self, bucket_id: str, file_key: str) -> dict[str, Any]:
        """Presigned GET and parse JSON body."""
        url, _ttl = await self.get_download_url(bucket_id, file_key)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, follow_redirects=True)
        except httpx.HTTPError as exc:
            raise ResumeStorageError(f"Storage fetch failed: {exc}") from exc

        if resp.status_code >= 400:
            raise ResumeStorageError(
                f"Storage object HTTP {resp.status_code}",
            )

        try:
            out = resp.json()
        except json.JSONDecodeError as exc:
            raise ResumeStorageError("Resume JSON in storage is invalid") from exc

        if not isinstance(out, dict):
            raise ResumeStorageError("Resume JSON must be an object")
        return out

    async def delete_file(self, bucket_id: str, file_key: str) -> None:
        """DELETE object from logical bucket."""
        if not self.base_url:
            raise ResumeStorageError("LAMBDA_S3STORAGE_API_URL is not configured")

        url = f"{self.base_url}/api/v1/buckets/{bucket_id}/objects"
        params = {"file_key": file_key}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.delete(
                    url,
                    headers={**self._headers_json(), "Content-Type": "application/json"},
                    params=params,
                )
        except httpx.HTTPError as exc:
            raise ResumeStorageError(f"Storage delete failed: {exc}") from exc

        if resp.status_code >= 400:
            # 404: object already gone — treat as success for delete idempotency
            if resp.status_code == 404:
                return
            raise ResumeStorageError(
                f"Storage delete HTTP {resp.status_code}: {resp.text[:500]}",
            )


@lru_cache(maxsize=1)
def get_s3storage_client() -> S3StorageClient:
    return S3StorageClient()
