"""
Job description data models and structures for Resume/CV AI Application.

This module provides comprehensive data models for job descriptions including:
- Job posting details and requirements
- Company and position information
- Skills and qualification structures
- Job matching and analysis models
- Metadata for job storage and tracking

All models use Python dataclasses for clean, type-safe data structures
with automatic validation and serialization capabilities.

Author: Resume AI Team
Created: 2024
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class JobDescription:
    """
    Job description structure for comprehensive job posting representation.
    
    This dataclass represents a complete job posting with all relevant details
    including position requirements, company information, and work conditions.
    
    Attributes:
        title (Optional[str]): Job title or position name
        company (Optional[str]): Company or organization name
        location (Optional[str]): Job location (city, state, country)
        description (Optional[str]): Detailed job description and overview
        requirements (Optional[str]): Required qualifications and experience
        responsibilities (Optional[str]): Key responsibilities and duties
        required_skills (List[str]): List of mandatory skills and competencies
        preferred_skills (List[str]): List of preferred but not required skills
        qualifications (List[str]): List of educational and professional qualifications
        benefits (List[str]): List of compensation and benefit details
        salary_range (Optional[str]): Salary range or compensation information
        employment_type (Optional[str]): Type of employment (Full-time, Part-time, Contract, etc.)
        experience_level (Optional[str]): Required experience level (Entry, Mid, Senior, Executive)
        remote_work (Optional[bool]): Whether remote work is available
        travel_required (Optional[bool]): Whether travel is required for the position
        visa_sponsorship (Optional[bool]): Whether visa sponsorship is available
        application_deadline (Optional[str]): Application deadline date
        start_date (Optional[str]): Expected start date
        department (Optional[str]): Department or division
        reporting_to (Optional[str]): Position or person this role reports to
        team_size (Optional[int]): Size of the team or department
        growth_opportunities (List[str]): Career advancement and growth opportunities
        company_culture (List[str]): Company culture and values
        work_environment (List[str]): Work environment and office details
        
    Example:
        >>> job = JobDescription(
        ...     title="Senior Software Engineer",
        ...     company="Tech Corp",
        ...     location="San Francisco, CA",
        ...     description="Lead development of scalable web applications",
        ...     required_skills=["Python", "Django", "PostgreSQL"],
        ...     employment_type="Full-time",
        ...     experience_level="Senior"
        ... )
    """
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    qualifications: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None  # Full-time, Part-time, Contract, etc.
    experience_level: Optional[str] = None  # Entry, Mid, Senior, Executive
    remote_work: Optional[bool] = None
    travel_required: Optional[bool] = None
    visa_sponsorship: Optional[bool] = None
    application_deadline: Optional[str] = None
    start_date: Optional[str] = None
    department: Optional[str] = None
    reporting_to: Optional[str] = None
    team_size: Optional[int] = None
    growth_opportunities: List[str] = field(default_factory=list)
    company_culture: List[str] = field(default_factory=list)
    work_environment: List[str] = field(default_factory=list)

@dataclass
class JobMetadata:
    """
    Job metadata for database storage and job tracking.
    
    This dataclass contains metadata about job postings for efficient storage,
    retrieval, and tracking of job-related information and statistics.
    
    Attributes:
        job_id (str): Unique identifier for the job posting (required)
        source (str): Source platform (LinkedIn, Indeed, Company Website, etc.)
        url (Optional[str]): URL to the original job posting
        posted_date (Optional[datetime]): Date when the job was posted
        industry (Optional[str]): Industry or sector of the company
        company_size (Optional[str]): Company size category (Startup, SME, Enterprise, etc.)
        company_type (Optional[str]): Company type (Public, Private, Non-profit, etc.)
        experience_required (Optional[str]): Required experience level
        education_required (Optional[str]): Required education level
        employment_type (Optional[str]): Type of employment (Full-time, Part-time, etc.)
        salary_range (Optional[str]): Salary range or compensation information
        location_type (Optional[str]): Work location type (On-site, Remote, Hybrid)
        is_active (bool): Whether the job posting is still active
        application_count (int): Number of applications received
        view_count (int): Number of times the job has been viewed
        tags (List[str]): List of tags for categorization and search
        notes (Optional[str]): Additional notes or comments
        
    Example:
        >>> metadata = JobMetadata(
        ...     job_id="job_12345",
        ...     source="LinkedIn",
        ...     url="https://linkedin.com/jobs/view/12345",
        ...     posted_date=datetime.now(),
        ...     industry="Technology",
        ...     company_size="Enterprise"
        ... )
    """
    job_id: str
    source: str  # LinkedIn, Indeed, Company Website, etc.
    url: Optional[str] = None
    posted_date: Optional[datetime] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    company_type: Optional[str] = None  # Public, Private, Non-profit, etc.
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    employment_type: Optional[str] = None
    salary_range: Optional[str] = None
    location_type: Optional[str] = None  # On-site, Remote, Hybrid
    is_active: bool = True
    application_count: int = 0
    view_count: int = 0
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None

@dataclass
class JobMatch:
    """
    Job matching result structure for resume-job compatibility analysis.
    
    This dataclass represents the results of matching a resume against a job posting
    with detailed scoring across multiple dimensions and improvement recommendations.
    
    Attributes:
        job_id (str): Unique identifier of the matched job (required)
        resume_id (str): Unique identifier of the matched resume (required)
        match_score (float): Overall compatibility score (0.0-100.0)
        skill_match (float): Skills alignment score (0.0-100.0)
        experience_match (float): Experience level alignment score (0.0-100.0)
        education_match (float): Education requirements alignment score (0.0-100.0)
        location_match (float): Geographic location compatibility score (0.0-100.0)
        salary_match (float): Salary expectation alignment score (0.0-100.0)
        culture_match (float): Company culture fit score (0.0-100.0)
        overall_fit (float): Overall job-resume fit score (0.0-100.0)
        missing_skills (List[str]): List of required skills not found in resume
        extra_skills (List[str]): List of additional skills in resume beyond requirements
        recommendations (List[str]): List of improvement recommendations
        matched_at (Optional[datetime]): Timestamp when matching was performed
        
    Example:
        >>> match = JobMatch(
        ...     job_id="job_12345",
        ...     resume_id="resume_67890",
        ...     match_score=85.5,
        ...     skill_match=90.0,
        ...     experience_match=80.0,
        ...     missing_skills=["Docker", "Kubernetes"],
        ...     recommendations=["Gain experience with containerization technologies"]
        ... )
    """
    job_id: str
    resume_id: str
    match_score: float
    skill_match: float
    experience_match: float
    education_match: float
    location_match: float
    salary_match: float
    culture_match: float
    overall_fit: float
    missing_skills: List[str] = field(default_factory=list)
    extra_skills: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    matched_at: Optional[datetime] = None

@dataclass
class JobApplication:
    """
    Job application tracking structure for application management.
    
    This dataclass represents a job application with tracking information
    including status, dates, and related documents.
    
    Attributes:
        application_id (str): Unique identifier for the application (required)
        job_id (str): Unique identifier of the applied job (required)
        resume_id (str): Unique identifier of the resume used (required)
        applied_date (datetime): Date when the application was submitted (required)
        status (str): Current application status (Applied, Under Review, Interview, Rejected, Offered)
        cover_letter (Optional[str]): Cover letter text or file path
        notes (Optional[str]): Additional notes or comments about the application
        follow_up_date (Optional[datetime]): Scheduled follow-up date
        interview_dates (List[datetime]): List of scheduled or completed interview dates
        
    Example:
        >>> application = JobApplication(
        ...     application_id="app_12345",
        ...     job_id="job_67890",
        ...     resume_id="resume_11111",
        ...     applied_date=datetime.now(),
        ...     status="Under Review",
        ...     cover_letter="Dear Hiring Manager...",
        ...     follow_up_date=datetime.now() + timedelta(days=7)
        ... )
    """
    application_id: str
    job_id: str
    resume_id: str
    applied_date: datetime
    status: str  # Applied, Under Review, Interview, Rejected, Offered
    cover_letter: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    interview_dates: List[datetime] = field(default_factory=list)
    rejection_reason: Optional[str] = None
    offer_details: Optional[Dict[str, Any]] = None

@dataclass
class JobSearchCriteria:
    """Job search criteria structure."""
    keywords: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    industries: List[str] = field(default_factory=list)
    experience_levels: List[str] = field(default_factory=list)
    employment_types: List[str] = field(default_factory=list)
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote_work: Optional[bool] = None
    company_sizes: List[str] = field(default_factory=list)
    skills_required: List[str] = field(default_factory=list)
    skills_preferred: List[str] = field(default_factory=list)
    exclude_keywords: List[str] = field(default_factory=list)
    date_posted: Optional[str] = None  # last_24h, last_week, last_month, etc.

@dataclass
class JobAlert:
    """Job alert structure."""
    alert_id: str
    user_id: str
    name: str
    criteria: JobSearchCriteria
    frequency: str  # daily, weekly, monthly
    created_at: datetime
    is_active: bool = True
    last_sent: Optional[datetime] = None
    total_matches: int = 0
    email_notifications: bool = True

@dataclass
class CompanyProfile:
    """Company profile structure."""
    company_id: str
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    revenue: Optional[str] = None
    culture_values: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    work_environment: List[str] = field(default_factory=list)
    growth_stage: Optional[str] = None  # Startup, Growth, Mature, etc.
    tech_stack: List[str] = field(default_factory=list)
    recent_news: List[str] = field(default_factory=list)
    social_media: Dict[str, str] = field(default_factory=dict)

@dataclass
class JobMarketInsights:
    """Job market insights structure."""
    industry: str
    location: str
    time_period: str
    total_jobs: int
    average_salary: Optional[float] = None
    salary_range: Optional[Dict[str, float]] = None
    top_skills: List[str] = field(default_factory=list)
    top_companies: List[str] = field(default_factory=list)
    growth_trend: Optional[str] = None  # Growing, Stable, Declining
    competition_level: Optional[str] = None  # Low, Medium, High
    remote_work_percentage: Optional[float] = None
    contract_vs_permanent: Optional[Dict[str, float]] = None
    experience_distribution: Optional[Dict[str, int]] = None
    education_requirements: Optional[Dict[str, int]] = None
    generated_at: Optional[datetime] = None
