"""
Resume data models and structures for Resume/CV AI Application.

This module provides comprehensive data models for resume components including:
- Contact information structures
- Work experience and education models
- Skills and project representations
- Certification and language models
- Resume metadata and analysis results
- Complete resume aggregation models

All models use Python dataclasses for clean, type-safe data structures
with automatic validation and serialization capabilities.

Author: Resume AI Team
Created: 2024
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class ContactInfo:
    """
    Contact information structure for resume candidates.
    
    This dataclass represents all contact-related information for a resume
    including personal details, professional profiles, and contact methods.
    
    Attributes:
        name (Optional[str]): Full name of the candidate
        email (Optional[str]): Primary email address for contact
        phone (Optional[str]): Primary phone number for contact
        linkedin (Optional[str]): LinkedIn profile URL
        github (Optional[str]): GitHub profile URL
        website (Optional[str]): Personal or professional website URL
        location (Optional[str]): Current location or address
        
    Example:
        >>> contact = ContactInfo(
        ...     name="John Doe",
        ...     email="john.doe@email.com",
        ...     phone="+1-555-123-4567",
        ...     location="San Francisco, CA"
        ... )
    """
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None

@dataclass
class WorkExperience:
    """
    Work experience structure for resume entries.
    
    This dataclass represents a single work experience entry with comprehensive
    details including position, company, duration, achievements, and technologies.
    
    Attributes:
        title (Optional[str]): Job title or position name
        company (Optional[str]): Company or organization name
        start_date (Optional[str]): Start date of employment (YYYY-MM format recommended)
        end_date (Optional[str]): End date of employment (YYYY-MM format, None for current)
        duration_months (Optional[int]): Calculated duration in months
        description (Optional[str]): Detailed job description and responsibilities
        achievements (List[str]): List of key achievements and accomplishments
        technologies (List[str]): List of technologies, tools, and frameworks used
        location (Optional[str]): Work location or office address
        employment_type (Optional[str]): Type of employment (Full-time, Part-time, Contract, etc.)
        
    Example:
        >>> exp = WorkExperience(
        ...     title="Senior Software Engineer",
        ...     company="Tech Corp",
        ...     start_date="2020-01",
        ...     end_date="2023-12",
        ...     description="Led development of microservices architecture",
        ...     achievements=["Reduced API response time by 50%", "Led team of 5 engineers"],
        ...     technologies=["Python", "Django", "PostgreSQL", "Docker"]
        ... )
    """
    title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    achievements: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    location: Optional[str] = None
    employment_type: Optional[str] = None  # Full-time, Part-time, Contract, etc.

@dataclass
class Education:
    """
    Education structure for resume entries.
    
    This dataclass represents educational background including degrees, institutions,
    academic achievements, and relevant coursework information.
    
    Attributes:
        degree (Optional[str]): Degree type and major (e.g., "Bachelor of Science in Computer Science")
        institution (Optional[str]): Name of the educational institution
        graduation_date (Optional[str]): Graduation date (YYYY-MM format recommended)
        gpa (Optional[str]): Grade Point Average (can be string to include scale)
        relevant_coursework (List[str]): List of relevant courses taken
        honors (List[str]): List of academic honors, awards, or distinctions
        location (Optional[str]): Institution location
        field_of_study (Optional[str]): Specific field or major of study
        
    Example:
        >>> edu = Education(
        ...     degree="Bachelor of Science in Computer Science",
        ...     institution="University of California",
        ...     graduation_date="2019-05",
        ...     gpa="3.8/4.0",
        ...     relevant_coursework=["Data Structures", "Algorithms", "Machine Learning"],
        ...     honors=["Dean's List", "Summa Cum Laude"]
        ... )
    """
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    relevant_coursework: List[str] = field(default_factory=list)
    honors: List[str] = field(default_factory=list)
    location: Optional[str] = None
    field_of_study: Optional[str] = None

@dataclass
class Skill:
    """
    Skill structure for resume entries.
    
    This dataclass represents individual skills with proficiency levels,
    experience duration, and related certifications.
    
    Attributes:
        name (str): Name of the skill (required)
        category (str): Skill category (e.g., "Technical", "Soft Skills", "Languages")
        proficiency (str): Proficiency level (Beginner, Intermediate, Advanced, Expert)
        years_experience (Optional[int]): Number of years of experience with this skill
        last_used (Optional[str]): Date when this skill was last used (YYYY-MM format)
        certifications (List[str]): List of related certifications or credentials
        
    Example:
        >>> skill = Skill(
        ...     name="Python",
        ...     category="Programming Languages",
        ...     proficiency="Advanced",
        ...     years_experience=5,
        ...     last_used="2024-01"
        ... )
    """
    name: str
    category: str = "General"
    proficiency: str = "Intermediate"  # Beginner, Intermediate, Advanced, Expert
    years_experience: Optional[int] = None
    last_used: Optional[str] = None
    certifications: List[str] = field(default_factory=list)

@dataclass
class Project:
    """
    Project structure for resume entries.
    
    This dataclass represents individual projects including personal,
    academic, or professional projects with comprehensive details.
    
    Attributes:
        name (Optional[str]): Project name or title
        description (Optional[str]): Detailed project description and objectives
        technologies (List[str]): List of technologies, tools, and frameworks used
        url (Optional[str]): Project URL or repository link
        start_date (Optional[str]): Project start date (YYYY-MM format)
        end_date (Optional[str]): Project end date (YYYY-MM format, None for ongoing)
        role (Optional[str]): Role in the project (e.g., "Lead Developer", "Team Member")
        team_size (Optional[int]): Number of team members involved
        achievements (List[str]): List of key achievements and outcomes
        
    Example:
        >>> project = Project(
        ...     name="E-commerce Platform",
        ...     description="Built a full-stack e-commerce platform with payment integration",
        ...     technologies=["React", "Node.js", "MongoDB", "Stripe"],
        ...     url="https://github.com/user/ecommerce-platform",
        ...     role="Full-stack Developer",
        ...     team_size=3
        ... )
    """
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = field(default_factory=list)
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    role: Optional[str] = None
    team_size: Optional[int] = None
    achievements: List[str] = field(default_factory=list)

@dataclass
class Certification:
    """
    Certification structure for resume entries.
    
    This dataclass represents professional certifications, licenses,
    and credentials with validation details.
    
    Attributes:
        name (str): Certification name (required)
        issuer (Optional[str]): Issuing organization or authority
        issue_date (Optional[str]): Date when certification was issued (YYYY-MM format)
        expiry_date (Optional[str]): Certification expiry date (YYYY-MM format, None for permanent)
        credential_id (Optional[str]): Unique credential or license ID
        url (Optional[str]): URL to verify or view the certification
        
    Example:
        >>> cert = Certification(
        ...     name="AWS Solutions Architect",
        ...     issuer="Amazon Web Services",
        ...     issue_date="2023-06",
        ...     expiry_date="2026-06",
        ...     credential_id="AWS-SA-12345"
        ... )
    """
    name: str
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    url: Optional[str] = None

@dataclass
class Language:
    """
    Language proficiency structure for resume entries.
    
    This dataclass represents language skills with proficiency levels
    and related certifications.
    
    Attributes:
        name (str): Language name (required)
        proficiency (str): Proficiency level (Native, Fluent, Conversational, Basic)
        certifications (List[str]): List of language proficiency certifications
        
    Example:
        >>> lang = Language(
        ...     name="Spanish",
        ...     proficiency="Fluent",
        ...     certifications=["DELE B2"]
        ... )
    """
    name: str
    proficiency: str  # Native, Fluent, Conversational, Basic
    certifications: List[str] = field(default_factory=list)

@dataclass
class ParsedResume:
    """
    Main resume structure aggregating all resume components.
    
    This dataclass represents a complete resume with all sections including
    contact information, work experience, education, skills, projects, and metadata.
    It serves as the primary data structure for resume analysis and processing.
    
    Attributes:
        contact_info (ContactInfo): Contact information (required)
        summary (Optional[str]): Professional summary or objective statement
        work_experience (List[WorkExperience]): List of work experience entries
        education (List[Education]): List of educational background entries
        skills (List[Skill]): List of skills and competencies
        projects (List[Project]): List of projects and portfolio items
        certifications (List[Certification]): List of professional certifications
        languages (List[Language]): List of language proficiencies
        parse_confidence (float): Confidence score of parsing accuracy (0.0-100.0)
        raw_text (Optional[str]): Original raw text content of the resume
        file_path (Optional[str]): Path to the original resume file
        created_at (Optional[datetime]): Timestamp when resume was created/parsed
        updated_at (Optional[datetime]): Timestamp when resume was last updated
        
    Example:
        >>> resume = ParsedResume(
        ...     contact_info=ContactInfo(name="John Doe", email="john@example.com"),
        ...     summary="Experienced software engineer with 5+ years in full-stack development",
        ...     work_experience=[work_exp1, work_exp2],
        ...     education=[edu1],
        ...     skills=[skill1, skill2],
        ...     parse_confidence=95.5
        ... )
    """
    contact_info: ContactInfo
    summary: Optional[str] = None
    work_experience: List[WorkExperience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    languages: List[Language] = field(default_factory=list)
    parse_confidence: float = 0.0
    raw_text: Optional[str] = None
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class ResumeMetadata:
    """
    Resume metadata for database storage and analysis tracking.
    
    This dataclass contains metadata about resume files and analysis history
    for efficient storage, retrieval, and tracking of resume processing.
    
    Attributes:
        file_name (str): Original filename of the resume (required)
        file_type (str): File type/extension (e.g., "pdf", "docx", "txt")
        file_size (int): File size in bytes
        upload_date (datetime): Date when resume was uploaded/processed
        experience_years (int): Total years of work experience extracted
        education_level (str): Highest education level (e.g., "Bachelor's", "Master's")
        industry (Optional[str]): Primary industry or field of work
        last_analyzed (Optional[datetime]): Date of last analysis
        analysis_count (int): Number of times this resume has been analyzed
        tags (List[str]): List of tags for categorization and search
        
    Example:
        >>> metadata = ResumeMetadata(
        ...     file_name="john_doe_resume.pdf",
        ...     file_type="pdf",
        ...     file_size=245760,
        ...     upload_date=datetime.now(),
        ...     experience_years=5,
        ...     education_level="Bachelor's",
        ...     industry="Technology"
        ... )
    """
    file_name: str
    file_type: str
    file_size: int
    upload_date: datetime
    experience_years: int
    education_level: str
    industry: Optional[str] = None
    last_analyzed: Optional[datetime] = None
    analysis_count: int = 0
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None

@dataclass
class ResumeTemplate:
    """Resume template structure."""
    name: str
    description: str
    category: str
    industry: Optional[str] = None
    layout: str = "single_column"  # single_column, two_column, skills_sidebar
    color_scheme: str = "blue"
    sections: List[str] = field(default_factory=list)
    is_ats_friendly: bool = True
    preview_image: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class ResumeSection:
    """Individual resume section structure."""
    section_type: str  # summary, experience, education, skills, projects, etc.
    title: str
    content: str
    order: int
    is_visible: bool = True
    is_required: bool = False
    word_count: int = 0
    last_modified: Optional[datetime] = None

@dataclass
class ResumeAnalysisMetrics:
    """Metrics from resume analysis."""
    ats_score: float = 0.0
    keyword_density: float = 0.0
    readability_score: float = 0.0
    action_verb_score: float = 0.0
    quantification_score: float = 0.0
    skills_coverage: float = 0.0
    experience_relevance: float = 0.0
    education_relevance: float = 0.0
    overall_score: float = 0.0
    word_count: int = 0
    page_count: int = 0
    section_completeness: Dict[str, float] = field(default_factory=dict)

@dataclass
class ResumeComparison:
    """Resume comparison structure."""
    resume_id_1: str
    resume_id_2: str
    similarity_score: float
    differences: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    compared_at: Optional[datetime] = None

@dataclass
class ResumeVersion:
    """Resume version control structure."""
    version_number: int
    resume_id: str
    created_at: datetime
    changes: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    is_current: bool = False
    notes: Optional[str] = None
