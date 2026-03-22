"""Async CRUD for resume documents."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseError, InvalidResumeIDError, ResumeNotFoundError
from app.models.db import Base, engine
from app.models.resume_document import ResumeDocumentRow
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class ResumeRepository:
    """Persistence for resume metadata; JSON lives in s3storage."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        user_id: str,
        storage_bucket_id: str,
        resume_id: str,
        resume_data_key: str,
    ) -> ResumeDocumentRow:
        try:
            row = ResumeDocumentRow(
                id=resume_id,
                user_id=user_id,
                storage_bucket_id=storage_bucket_id,
                resume_data_key=resume_data_key,
            )
            self._session.add(row)
            await self._session.commit()
            await self._session.refresh(row)
            return row
        except Exception as e:
            await self._session.rollback()
            logger.exception("create resume failed")
            raise DatabaseError(str(e)) from e

    async def get_by_id(self, resume_id: str) -> Optional[ResumeDocumentRow]:
        if not resume_id or len(resume_id) < 8:
            raise InvalidResumeIDError("Invalid resume id")
        result = await self._session.execute(
            select(ResumeDocumentRow).where(ResumeDocumentRow.id == resume_id)
        )
        return result.scalar_one_or_none()

    async def list_for_user(self, user_id: str) -> List[ResumeDocumentRow]:
        result = await self._session.execute(
            select(ResumeDocumentRow)
            .where(ResumeDocumentRow.user_id == user_id)
            .order_by(ResumeDocumentRow.updated_at.desc())
        )
        return list(result.scalars().all())

    async def update_resume_row(self, row: ResumeDocumentRow) -> ResumeDocumentRow:
        """Persist resume_data_key / updated_at changes for an attached row."""
        try:
            row.updated_at = datetime.now(timezone.utc)
            await self._session.commit()
            await self._session.refresh(row)
            return row
        except Exception as e:
            await self._session.rollback()
            raise DatabaseError(str(e)) from e

    async def delete(self, resume_id: str) -> ResumeDocumentRow:
        row = await self.get_by_id(resume_id)
        if not row:
            raise ResumeNotFoundError(f"Resume {resume_id} not found")
        try:
            await self._session.delete(row)
            await self._session.commit()
            return row
        except Exception as e:
            await self._session.rollback()
            raise DatabaseError(str(e)) from e
