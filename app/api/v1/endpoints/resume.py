"""Resume CRUD."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, verify_api_key
from app.core.exceptions import ResumeNotFoundError, ResumeStorageError
from app.schemas.requests import SaveResumeRequest, UpdateResumeRequest
from app.schemas.responses import ResumeRecordResponse
from app.services.resume_service import ResumeService

router = APIRouter()


def _svc(session: AsyncSession) -> ResumeService:
    return ResumeService(session)


@router.post("", response_model=ResumeRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    body: SaveResumeRequest,
    _: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        return await _svc(session).create(body.user_id, body.resume, body.bucket_id)
    except ResumeStorageError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/user/{user_id}", response_model=list[ResumeRecordResponse])
async def list_resumes_for_user(
    user_id: str,
    _: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        return await _svc(session).list_user(user_id)
    except ResumeStorageError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/{resume_id}", response_model=ResumeRecordResponse)
async def get_resume(
    resume_id: str,
    _: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        return await _svc(session).get(resume_id)
    except ResumeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ResumeStorageError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.put("/{resume_id}", response_model=ResumeRecordResponse)
async def update_resume(
    resume_id: str,
    body: UpdateResumeRequest,
    _: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        return await _svc(session).update(resume_id, body.resume)
    except ResumeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ResumeStorageError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    _: str = Depends(verify_api_key),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        await _svc(session).delete(resume_id)
    except ResumeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
