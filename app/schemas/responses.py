"""API response models."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.resume import Resume, SuggestedSkill


class ResumeRecordResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(..., alias="userId", serialization_alias="userId")
    resume: Resume
    created_at: str = Field(..., alias="createdAt", serialization_alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt", serialization_alias="updatedAt")


class EnhancedTextResponse(BaseModel):
    result: str


class SuggestSkillsResponse(BaseModel):
    skills: List[SuggestedSkill]


class ATSScoreResponse(BaseModel):
    score: int
    summary: str
    strengths: List[str]
    improvements: List[str]


class LatexResponse(BaseModel):
    latex: str


class PhotoEnhanceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    image_base64: str = Field(..., alias="imageBase64", serialization_alias="imageBase64")
