"""Request bodies for JSON endpoints."""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from app.models.resume import ATSScoreResult, Resume


class EnhanceSectionRequest(BaseModel):
    content: Union[str, List[str]]
    enhancement_type: Literal["objective", "description", "hobbies", "education_description"]


class SuggestSkillsRequest(BaseModel):
    title: str
    experience_text: str = Field(..., alias="experienceText")

    model_config = {"populate_by_name": True}


class ATSScoreRequest(BaseModel):
    resume: Resume
    job_description: Optional[str] = Field(None, alias="jobDescription")

    model_config = {"populate_by_name": True}


class ATSImproveRequest(BaseModel):
    resume: Resume
    ats_result: Optional[ATSScoreResult] = Field(None, alias="atsResult")
    job_description: Optional[str] = Field(None, alias="jobDescription")

    model_config = {"populate_by_name": True}


class GenerateLatexRequest(BaseModel):
    resume: Resume
    template: Literal["professional", "academic", "minimalist", "minimal"] = "professional"


class LinkedInImportRequest(BaseModel):
    url: str


class SaveResumeRequest(BaseModel):
    resume: Resume
    user_id: str = Field(..., alias="userId")
    bucket_id: str | None = Field(
        None,
        alias="bucketId",
        description="Logical s3storage bucket id (users.bucket); defaults to userId when omitted.",
    )

    model_config = {"populate_by_name": True}


class UpdateResumeRequest(BaseModel):
    resume: Resume
