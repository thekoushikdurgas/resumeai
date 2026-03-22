"""Pydantic domain models (aligned with ai-resume-editor TypeScript types)."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class PersonalDetails(BaseModel):
    name: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""
    photo: str = ""


class Experience(BaseModel):
    id: str
    company: str = ""
    role: str = ""
    employmentType: str = ""
    location: str = ""
    locationType: str = ""
    isCurrent: bool = False
    startDate: str = ""
    endDate: str = ""
    description: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    media: List[str] = Field(default_factory=list)


class Education(BaseModel):
    id: str
    institution: str = ""
    degree: str = ""
    duration: str = ""
    score: str = ""
    description: List[str] = Field(default_factory=list)


class Skill(BaseModel):
    id: str
    name: str = ""
    level: int = 0


class Certificate(BaseModel):
    id: str
    name: str = ""


class Hobby(BaseModel):
    id: str
    name: str = ""


class SuggestedSkill(BaseModel):
    name: str
    category: Literal["Frontend", "Backend", "Programming", "Cloud"]


class ATSScoreResult(BaseModel):
    score: int
    summary: str
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)


class Resume(BaseModel):
    personalDetails: PersonalDetails
    objective: str = ""
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    backendSkills: List[Skill] = Field(default_factory=list)
    frontendSkills: List[Skill] = Field(default_factory=list)
    programmingSkills: List[Skill] = Field(default_factory=list)
    cloudSkills: List[Skill] = Field(default_factory=list)
    certificates: List[Certificate] = Field(default_factory=list)
    hobbies: List[Hobby] = Field(default_factory=list)
