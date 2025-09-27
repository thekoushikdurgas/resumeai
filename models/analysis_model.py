"""
Analysis result data models and structures for Resume/CV AI Application.

This module provides comprehensive data models for analysis results including:
- Resume analysis and scoring structures
- ATS compatibility analysis results
- Job matching and compatibility scores
- Career insights and recommendations
- Enhancement suggestions and metrics

All models use Python dataclasses and enums for clean, type-safe data structures
with automatic validation and serialization capabilities.

Author: Resume AI Team
Created: 2024
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisType(Enum):
    """
    Types of analysis that can be performed on resumes and job descriptions.
    
    This enum defines the different types of analysis operations supported
    by the resume AI system for comprehensive evaluation and enhancement.
    
    Values:
        RESUME_ANALYSIS: General resume content and structure analysis
        JOB_MATCHING: Resume-job compatibility and matching analysis
        ATS_CHECK: Applicant Tracking System compatibility analysis
        SKILL_ANALYSIS: Skills assessment and gap analysis
        CAREER_INSIGHTS: Career development and progression insights
        ENHANCEMENT: Resume improvement and optimization suggestions
    """
    RESUME_ANALYSIS = "resume_analysis"
    JOB_MATCHING = "job_matching"
    ATS_CHECK = "ats_check"
    SKILL_ANALYSIS = "skill_analysis"
    CAREER_INSIGHTS = "career_insights"
    ENHANCEMENT = "enhancement"

class SeverityLevel(Enum):
    """
    Severity levels for issues, problems, and recommendations.
    
    This enum defines the severity levels used to categorize issues
    and recommendations in analysis results for prioritization.
    
    Values:
        LOW: Minor issues or suggestions with low priority
        MEDIUM: Moderate issues or suggestions requiring attention
        HIGH: Important issues or suggestions that should be addressed
        CRITICAL: Critical issues that must be fixed immediately
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AnalysisResult:
    """
    Base analysis result structure for all types of resume and job analysis.
    
    This dataclass serves as the foundation for all analysis results, providing
    a consistent structure for scores, issues, recommendations, and metadata.
    
    Attributes:
        analysis_id (str): Unique identifier for the analysis (required)
        analysis_type (AnalysisType): Type of analysis performed (required)
        resume_id (Optional[str]): Unique identifier of the analyzed resume
        job_id (Optional[str]): Unique identifier of the analyzed job (for job matching)
        overall_score (float): Overall analysis score (0.0-100.0)
        confidence (float): Confidence level of the analysis (0.0-100.0)
        issues (List[str]): List of identified issues or problems
        recommendations (List[str]): List of improvement recommendations
        strengths (List[str]): List of identified strengths and positive aspects
        weaknesses (List[str]): List of identified weaknesses and areas for improvement
        metrics (Dict[str, float]): Dictionary of detailed metrics and scores
        created_at (Optional[datetime]): Timestamp when analysis was performed
        processing_time (Optional[float]): Time taken to perform the analysis in seconds
        
    Example:
        >>> result = AnalysisResult(
        ...     analysis_id="analysis_12345",
        ...     analysis_type=AnalysisType.RESUME_ANALYSIS,
        ...     resume_id="resume_67890",
        ...     overall_score=85.5,
        ...     confidence=92.0,
        ...     strengths=["Strong technical skills", "Clear work history"],
        ...     recommendations=["Add more quantifiable achievements"]
        ... )
    """
    analysis_id: str
    analysis_type: AnalysisType
    resume_id: Optional[str] = None
    job_id: Optional[str] = None
    overall_score: float = 0.0
    confidence: float = 0.0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    processing_time: Optional[float] = None

@dataclass
class ATSResult:
    """
    ATS (Applicant Tracking System) compatibility analysis result.
    
    This dataclass represents the results of ATS compatibility analysis
    including format validation, keyword optimization, and structure assessment.
    
    Attributes:
        ats_score (float): Overall ATS compatibility score (0.0-100.0)
        format_score (float): Format compatibility score (0.0-100.0)
        keyword_score (float): Keyword optimization score (0.0-100.0)
        structure_score (float): Structure and layout score (0.0-100.0)
        content_score (float): Content quality and relevance score (0.0-100.0)
        compatibility_issues (List[str]): List of ATS compatibility problems
        keyword_matches (List[str]): List of keywords successfully identified
        missing_keywords (List[str]): List of important keywords not found
        format_issues (List[str]): List of format-related problems
        structure_issues (List[str]): List of structure and layout problems
        recommendations (List[str]): List of improvement recommendations
        ats_systems_tested (List[str]): List of ATS systems tested against
        
    Example:
        >>> ats_result = ATSResult(
        ...     ats_score=85.5,
        ...     format_score=90.0,
        ...     keyword_score=80.0,
        ...     missing_keywords=["Python", "Machine Learning"],
        ...     recommendations=["Add more industry-specific keywords"]
        ... )
    """
    ats_score: float
    format_score: float
    keyword_score: float
    structure_score: float
    content_score: float
    compatibility_issues: List[str] = field(default_factory=list)
    keyword_matches: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    format_issues: List[str] = field(default_factory=list)
    structure_issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    ats_systems_tested: List[str] = field(default_factory=list)

@dataclass
class SkillAnalysis:
    """
    Skill analysis result for comprehensive skills assessment.
    
    This dataclass represents the results of skills analysis including
    categorization, proficiency levels, market demand, and gap analysis.
    
    Attributes:
        technical_skills (List[str]): List of identified technical skills
        soft_skills (List[str]): List of identified soft skills and competencies
        skill_gaps (List[str]): List of skills that are missing or need improvement
        skill_strengths (List[str]): List of strong skills and competencies
        skill_categories (Dict[str, List[str]]): Skills organized by category
        proficiency_levels (Dict[str, str]): Proficiency levels for each skill
        years_experience (Dict[str, int]): Years of experience for each skill
        market_demand (Dict[str, str]): Market demand level for each skill
        recommendations (List[str]): List of skill development recommendations
        
    Example:
        >>> skill_analysis = SkillAnalysis(
        ...     technical_skills=["Python", "Django", "PostgreSQL"],
        ...     soft_skills=["Leadership", "Communication", "Problem Solving"],
        ...     skill_gaps=["Docker", "Kubernetes"],
        ...     proficiency_levels={"Python": "Advanced", "Django": "Intermediate"}
        ... )
    """
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    skill_gaps: List[str] = field(default_factory=list)
    skill_strengths: List[str] = field(default_factory=list)
    skill_categories: Dict[str, List[str]] = field(default_factory=dict)
    proficiency_levels: Dict[str, str] = field(default_factory=dict)
    years_experience: Dict[str, int] = field(default_factory=dict)
    market_demand: Dict[str, str] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class EnhancementSuggestion:
    """Enhancement suggestion structure."""
    suggestion_id: str
    category: str  # content, format, keywords, structure, etc.
    title: str
    description: str
    current_text: Optional[str] = None
    suggested_text: Optional[str] = None
    impact_score: float = 0.0
    effort_level: str = "medium"  # low, medium, high
    priority: SeverityLevel = SeverityLevel.MEDIUM
    reasoning: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    is_applied: bool = False
    applied_at: Optional[datetime] = None

@dataclass
class CareerInsight:
    """Career insight structure."""
    insight_id: str
    category: str  # market_trends, salary_insights, skill_demand, etc.
    title: str
    description: str
    data_points: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    source: Optional[str] = None
    generated_at: Optional[datetime] = None
    relevance_score: float = 0.0

@dataclass
class JobMatchAnalysis:
    """Job matching analysis result."""
    job_id: str
    resume_id: str
    overall_match_score: float
    skill_match_score: float
    experience_match_score: float
    education_match_score: float
    location_match_score: float
    salary_match_score: float
    culture_match_score: float
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    extra_skills: List[str] = field(default_factory=list)
    skill_gaps: List[str] = field(default_factory=list)
    experience_gaps: List[str] = field(default_factory=list)
    education_gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    interview_tips: List[str] = field(default_factory=list)
    salary_negotiation_tips: List[str] = field(default_factory=list)

@dataclass
class ResumeMetrics:
    """Resume metrics and statistics."""
    word_count: int = 0
    page_count: int = 0
    section_count: int = 0
    bullet_points: int = 0
    action_verbs: int = 0
    quantified_achievements: int = 0
    keyword_density: float = 0.0
    readability_score: float = 0.0
    ats_friendliness: float = 0.0
    professional_tone: float = 0.0
    skills_coverage: float = 0.0
    experience_relevance: float = 0.0
    education_relevance: float = 0.0
    contact_completeness: float = 0.0
    section_completeness: Dict[str, float] = field(default_factory=dict)

@dataclass
class ComparisonResult:
    """Resume comparison result."""
    resume_1_id: str
    resume_2_id: str
    similarity_score: float
    differences: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    strengths_resume_1: List[str] = field(default_factory=list)
    strengths_resume_2: List[str] = field(default_factory=list)
    weaknesses_resume_1: List[str] = field(default_factory=list)
    weaknesses_resume_2: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ProgressTracking:
    """Progress tracking structure."""
    user_id: str
    metric_name: str
    current_value: float
    previous_value: Optional[float] = None
    target_value: Optional[float] = None
    improvement_percentage: Optional[float] = None
    trend: Optional[str] = None  # improving, declining, stable
    milestones: List[str] = field(default_factory=list)
    next_goals: List[str] = field(default_factory=list)
    last_updated: Optional[datetime] = None

@dataclass
class ReportData:
    """Report data structure."""
    report_id: str
    report_type: str
    title: str
    data: Dict[str, Any] = field(default_factory=dict)
    charts: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    generated_at: Optional[datetime] = None
    format: str = "html"  # html, pdf, json, csv
    is_public: bool = False

@dataclass
class BenchmarkData:
    """Benchmark data structure."""
    industry: str
    experience_level: str
    metric_name: str
    average_value: float
    median_value: float
    percentile_25: float
    percentile_75: float
    percentile_90: float
    sample_size: int
    location: Optional[str] = None
    last_updated: Optional[datetime] = None
    source: Optional[str] = None
