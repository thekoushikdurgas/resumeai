"""
Data models for the Resume AI application.
"""

from .resume_model import ParsedResume, ContactInfo, WorkExperience, Education, Skill, Project, ResumeMetadata
from .job_model import JobDescription, JobMetadata
from .analysis_model import AnalysisResult, ATSResult, EnhancementSuggestion, CareerInsight

__all__ = [
    "ParsedResume",
    "ContactInfo", 
    "WorkExperience",
    "Education",
    "Skill",
    "Project",
    "ResumeMetadata",
    "JobDescription",
    "JobMetadata",
    "AnalysisResult",
    "ATSResult", 
    "EnhancementSuggestion",
    "CareerInsight"
]
