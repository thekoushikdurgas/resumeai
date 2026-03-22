"""AI operations."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import verify_api_key
from app.core.config import get_settings
from app.core.exceptions import AIServiceError
from app.schemas.requests import (
    ATSImproveRequest,
    ATSScoreRequest,
    EnhanceSectionRequest,
    GenerateLatexRequest,
    LinkedInImportRequest,
    SuggestSkillsRequest,
)
from app.schemas.responses import (
    ATSScoreResponse,
    EnhancedTextResponse,
    LatexResponse,
    PhotoEnhanceResponse,
    SuggestSkillsResponse,
)
from app.models.resume import Resume
from app.services import ai_service

router = APIRouter()
settings = get_settings()


@router.post("/parse", response_model=Resume, status_code=status.HTTP_200_OK)
async def parse_resume(
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key),
):
    data = await file.read()
    if len(data) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="file too large")
    try:
        return await ai_service.parse_resume_file(data, file.content_type or "application/octet-stream")
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/enhance", response_model=EnhancedTextResponse)
async def enhance(
    body: EnhanceSectionRequest,
    _: str = Depends(verify_api_key),
):
    try:
        text = await ai_service.enhance_section(body.content, body.enhancement_type)
        return EnhancedTextResponse(result=text)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/skills", response_model=SuggestSkillsResponse)
async def skills(
    body: SuggestSkillsRequest,
    _: str = Depends(verify_api_key),
):
    try:
        sk = await ai_service.suggest_skills(body.title, body.experience_text)
        return SuggestSkillsResponse(skills=sk)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/ats-score", response_model=ATSScoreResponse)
async def ats_score(
    body: ATSScoreRequest,
    _: str = Depends(verify_api_key),
):
    try:
        r = await ai_service.check_ats_score(body.resume, body.job_description)
        return ATSScoreResponse(
            score=r.score,
            summary=r.summary,
            strengths=r.strengths,
            improvements=r.improvements,
        )
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/ats-improve", response_model=Resume)
async def ats_improve(
    body: ATSImproveRequest,
    _: str = Depends(verify_api_key),
):
    try:
        return await ai_service.improve_resume_for_ats(body.resume, body.job_description)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/latex", response_model=LatexResponse)
async def latex(
    body: GenerateLatexRequest,
    _: str = Depends(verify_api_key),
):
    try:
        tex = await ai_service.generate_latex(body.resume, body.template)
        return LatexResponse(latex=tex)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/photo", response_model=PhotoEnhanceResponse)
async def photo(
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key),
):
    data = await file.read()
    if len(data) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="file too large")
    try:
        url = await ai_service.enhance_photo(data, file.content_type or "image/jpeg")
        return PhotoEnhanceResponse(image_base64=url)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.post("/linkedin", response_model=Resume)
async def linkedin(
    body: LinkedInImportRequest,
    _: str = Depends(verify_api_key),
):
    try:
        return await ai_service.scrape_linkedin(body.url)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
