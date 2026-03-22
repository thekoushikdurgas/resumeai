"""Business logic for resume CRUD."""

import uuid
from datetime import timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.s3storage_client import get_s3storage_client
from app.core.exceptions import ResumeNotFoundError, ResumeStorageError
from app.models.resume import Resume
from app.models.resume_document import ResumeDocumentRow
from app.models.resume_repository import ResumeRepository
from app.schemas.responses import ResumeRecordResponse


class ResumeService:
    def __init__(self, session: AsyncSession):
        self._repo = ResumeRepository(session)
        self._storage = get_s3storage_client()

    async def create(
        self,
        user_id: str,
        resume: Resume,
        storage_bucket_id: str | None = None,
    ) -> ResumeRecordResponse:
        bucket = (storage_bucket_id or user_id).strip()
        resume_id = str(uuid.uuid4())
        raw = resume.model_dump_json().encode("utf-8")
        filename = f"{resume_id}.json"

        try:
            file_key = await self._storage.upload_resume_json(bucket, filename, raw)
        except ResumeStorageError:
            raise
        except Exception as exc:
            raise ResumeStorageError(str(exc)) from exc

        try:
            row = await self._repo.create(user_id, bucket, resume_id, file_key)
        except Exception:
            try:
                await self._storage.delete_file(bucket, file_key)
            except ResumeStorageError:
                pass
            raise

        return await self._to_response(row)

    async def get(self, resume_id: str) -> ResumeRecordResponse:
        row = await self._repo.get_by_id(resume_id)
        if not row:
            raise ResumeNotFoundError(f"Resume {resume_id} not found")
        return await self._to_response(row)

    async def list_user(self, user_id: str) -> list[ResumeRecordResponse]:
        rows = await self._repo.list_for_user(user_id)
        out: list[ResumeRecordResponse] = []
        for r in rows:
            out.append(await self._to_response(r))
        return out

    async def update(self, resume_id: str, resume: Resume) -> ResumeRecordResponse:
        row = await self._repo.get_by_id(resume_id)
        if not row:
            raise ResumeNotFoundError(f"Resume {resume_id} not found")

        raw = resume.model_dump_json().encode("utf-8")
        filename = f"{resume_id}.json"
        bucket = row.storage_bucket_id

        try:
            new_key = await self._storage.upload_resume_json(bucket, filename, raw)
        except ResumeStorageError:
            raise
        except Exception as exc:
            raise ResumeStorageError(str(exc)) from exc

        if new_key != row.resume_data_key:
            try:
                await self._storage.delete_file(bucket, row.resume_data_key)
            except ResumeStorageError:
                pass
            row.resume_data_key = new_key

        row = await self._repo.update_resume_row(row)
        return await self._to_response(row)

    async def delete(self, resume_id: str) -> None:
        row = await self._repo.delete(resume_id)
        try:
            await self._storage.delete_file(row.storage_bucket_id, row.resume_data_key)
        except ResumeStorageError:
            pass

    async def _to_response(self, row: ResumeDocumentRow) -> ResumeRecordResponse:
        created = row.created_at
        updated = row.updated_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)

        try:
            data = await self._storage.fetch_json_object(
                row.storage_bucket_id,
                row.resume_data_key,
            )
        except ResumeStorageError:
            raise
        except Exception as exc:
            raise ResumeStorageError(str(exc)) from exc

        return ResumeRecordResponse(
            id=row.id,
            user_id=row.user_id,
            resume=Resume.model_validate(data),
            created_at=created.isoformat(),
            updated_at=updated.isoformat(),
        )
