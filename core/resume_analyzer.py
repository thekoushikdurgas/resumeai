"""
Resume Analyzer Module for Resume/CV AI Application
Advanced resume parsing and analysis with vector database integration.

This module provides:
- Advanced resume parsing and text extraction
- AI-powered content analysis and enhancement
- Vector database integration for semantic matching
- Comprehensive metrics and scoring
- Industry-specific skill recognition
- Educational background analysis

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json

from models.resume_model import (
    ParsedResume, ContactInfo, WorkExperience, Education, 
    Skill, Project, Certification, Language, ResumeMetadata
)
from models.analysis_model import AnalysisResult, ResumeMetrics
from utils.helpers import clean_text, extract_contact_info, is_likely_name, extract_years_from_text, generate_unique_id
from utils.logger import setup_logger
from core.vector_db import VectorDatabase
from core.ai_handler import AIHandler

# Initialize logger with module-specific name
logger = setup_logger("resume_analyzer")

class ResumeAnalyzer:
    """
    Advanced resume analyzer with AI-powered parsing and analysis with comprehensive logging.
    
    This class provides high-level resume analysis capabilities including:
    - Advanced text parsing and structure recognition
    - AI-powered content analysis and enhancement
    - Vector database integration for semantic matching
    - Comprehensive metrics calculation and scoring
    - Industry-specific skill and education recognition
    - Performance monitoring and detailed logging
    
    Attributes:
        vector_db (VectorDatabase): Vector database instance for semantic operations
        ai_handler (AIHandler): AI handler instance for content analysis
        technical_skills (Dict): Dictionary of technical skills by category
        soft_skills (List[str]): List of soft skills for recognition
        degree_patterns (Dict): Regex patterns for degree recognition
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, vector_db: VectorDatabase, ai_handler: AIHandler):
        """
        Initialize resume analyzer with comprehensive logging.
        
        Sets up the analyzer with vector database and AI handler dependencies,
        loads skill databases, and logs initialization details.
        
        Args:
            vector_db (VectorDatabase): Vector database instance for semantic operations
            ai_handler (AIHandler): AI handler instance for content analysis
            
        Raises:
            Exception: If initialization fails due to missing dependencies
        """
        logger.info("Initializing ResumeAnalyzer")
        self._initialization_time = time.time()
        
        try:
            # Validate dependencies
            if not vector_db:
                raise ValueError("VectorDatabase instance is required")
            if not ai_handler:
                raise ValueError("AIHandler instance is required")
            
            self.vector_db = vector_db
            self.ai_handler = ai_handler
            logger.info("Dependencies validated successfully")
            
            # Load skill databases
            logger.debug("Loading technical skills database")
            self.technical_skills = self._load_technical_skills()
            logger.debug(f"Loaded {len(self.technical_skills)} technical skill categories")
            
            logger.debug("Loading soft skills database")
            self.soft_skills = self._load_soft_skills()
            logger.debug(f"Loaded {len(self.soft_skills)} soft skills")
            
            logger.debug("Loading degree patterns")
            self.degree_patterns = self._load_degree_patterns()
            logger.debug(f"Loaded {len(self.degree_patterns)} degree patterns")
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ResumeAnalyzer initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Technical skills categories: {len(self.technical_skills)}")
            logger.info(f"Soft skills loaded: {len(self.soft_skills)}")
            logger.info(f"Degree patterns loaded: {len(self.degree_patterns)}")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ResumeAnalyzer initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def parse_resume(self, text: str, file_metadata: Optional[Dict] = None) -> ParsedResume:
        """
        Parse resume text into structured data with comprehensive logging.
        
        This method performs advanced resume parsing including:
        - Text cleaning and preprocessing
        - Section identification and extraction
        - Contact information parsing
        - Work experience and education extraction
        - Skills and project recognition
        - Confidence scoring and validation
        
        Args:
            text (str): Raw resume text content
            file_metadata (Optional[Dict]): Optional file metadata for context
            
        Returns:
            ParsedResume: Structured resume object with all parsed components
            
        Raises:
            Exception: If parsing fails due to invalid input or processing errors
        """
        start_time = time.time()
        
        try:
            logger.info("Starting resume parsing process")
            logger.debug(f"Input text length: {len(text)} characters")
            logger.debug(f"File metadata provided: {file_metadata is not None}")
            
            # Validate input
            if not text or len(text.strip()) < 50:
                logger.warning("Resume text is very short, may result in poor parsing quality")
            
            # Clean and preprocess text
            logger.debug("Cleaning and preprocessing resume text")
            cleaned_text = clean_text(text)
            logger.debug(f"Cleaned text length: {len(cleaned_text)} characters")
            
            # Identify sections
            logger.debug("Identifying resume sections")
            sections = self._identify_sections(cleaned_text)
            logger.info(f"Identified {len(sections)} resume sections: {list(sections.keys())}")
            
            # If no sections found, try to parse the entire text
            if not sections:
                logger.warning("No clear sections identified, attempting to parse entire text")
                sections = {'full_text': cleaned_text}
            
            # Parse each section
            logger.debug("Parsing contact information")
            contact_info = self._parse_contact_info(cleaned_text)
            logger.info(f"Contact info parsed: {contact_info.name or 'Unknown'}")
            
            logger.debug("Parsing summary section")
            summary = self._parse_summary(sections.get('summary', ''))
            logger.debug(f"Summary length: {len(summary) if summary else 0} characters")
            
            logger.debug("Parsing work experience")
            work_experience = self._parse_work_experience(sections.get('experience', sections.get('full_text', '')))
            logger.info(f"Work experience entries: {len(work_experience)}")
            
            logger.debug("Parsing education")
            education = self._parse_education(sections.get('education', sections.get('full_text', '')))
            logger.info(f"Education entries: {len(education)}")
            
            logger.debug("Parsing skills")
            skills = self._parse_skills(sections.get('skills', sections.get('full_text', '')))
            logger.info(f"Skills identified: {len(skills)}")
            
            logger.debug("Parsing projects")
            projects = self._parse_projects(sections.get('projects', sections.get('full_text', '')))
            logger.info(f"Projects identified: {len(projects)}")
            
            logger.debug("Parsing certifications")
            certifications = self._parse_certifications(cleaned_text)
            logger.info(f"Certifications identified: {len(certifications)}")
            
            logger.debug("Parsing languages")
            languages = self._parse_languages(cleaned_text)
            logger.info(f"Languages identified: {len(languages)}")
            
            # Calculate parse confidence
            logger.debug("Calculating parse confidence score")
            confidence = self._calculate_parse_confidence({
                'contact_info': contact_info,
                'work_experience': work_experience,
                'education': education,
                'skills': skills
            })
            logger.info(f"Parse confidence: {confidence:.1f}%")
            
            # Create parsed resume
            logger.debug("Creating ParsedResume object")
            resume = ParsedResume(
                contact_info=contact_info,
                summary=summary,
                work_experience=work_experience,
                education=education,
                skills=skills,
                projects=projects,
                certifications=certifications,
                languages=languages,
                parse_confidence=confidence,
                raw_text=text,
                created_at=datetime.now()
            )
            
            # Add to vector database
            if file_metadata:
                logger.debug("Creating resume metadata for vector database")
                metadata = ResumeMetadata(
                    file_name=file_metadata.get('name', 'unknown'),
                    file_type=file_metadata.get('type', 'unknown'),
                    file_size=file_metadata.get('size', 0),
                    upload_date=datetime.now(),
                    experience_years=self._calculate_experience_years(work_experience),
                    education_level=self._determine_education_level(education),
                    industry=self._infer_industry(work_experience, skills)
                )
                
                logger.debug("Adding resume to vector database")
                resume_id = self.vector_db.add_resume(resume, metadata)
                logger.info(f"Resume added to vector database with ID: {resume_id}")
            else:
                logger.debug("No file metadata provided, skipping vector database storage")
            
            parsing_time = time.time() - start_time
            logger.info(f"Resume parsing completed successfully in {parsing_time:.2f}s")
            logger.info(f"Parsed resume summary:")
            logger.info(f"  - Name: {contact_info.name or 'Unknown'}")
            logger.info(f"  - Experience entries: {len(work_experience)}")
            logger.info(f"  - Education entries: {len(education)}")
            logger.info(f"  - Skills: {len(skills)}")
            logger.info(f"  - Projects: {len(projects)}")
            logger.info(f"  - Parse confidence: {confidence:.1f}%")
            
            return resume
            
        except Exception as e:
            parsing_time = time.time() - start_time
            logger.error(f"Resume parsing failed after {parsing_time:.2f}s: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Input text length: {len(text)} characters")
            
            # Return minimal resume object
            logger.info("Returning minimal resume object due to parsing failure")
            return ParsedResume(
                contact_info=ContactInfo(),
                raw_text=text,
                created_at=datetime.now(),
                parse_confidence=0.0
            )
    
    async def analyze_resume(self, resume: ParsedResume) -> AnalysisResult:
        """
        Perform comprehensive analysis of parsed resume.
        
        Args:
            resume: Parsed resume object
            
        Returns:
            Analysis result
        """
        try:
            # Use AI for advanced analysis
            ai_analysis = await self.ai_handler.analyze_resume_content(resume)
            
            # Calculate additional metrics
            metrics = self._calculate_resume_metrics(resume)
            
            # Combine AI analysis with calculated metrics
            analysis = AnalysisResult(
                analysis_id=ai_analysis.analysis_id,
                analysis_type=ai_analysis.analysis_type,
                overall_score=ai_analysis.overall_score,
                confidence=ai_analysis.confidence,
                issues=ai_analysis.issues,
                recommendations=ai_analysis.recommendations,
                strengths=ai_analysis.strengths,
                weaknesses=ai_analysis.weaknesses,
                metrics=metrics,
                created_at=datetime.now()
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze resume: {e}")
            logger.exception("Full traceback for resume analysis error:")
            return AnalysisResult(
                analysis_id=generate_unique_id(),
                analysis_type="resume_analysis",
                overall_score=0.0,
                confidence=0.0,
                issues=[f"Analysis failed due to technical error: {str(e)}"],
                recommendations=["Please check the resume format and try again"],
                strengths=[],
                weaknesses=["Unable to complete analysis"],
                metrics=ResumeMetrics(),
                created_at=datetime.now()
            )
    
    def find_similar_resumes(self, resume: ParsedResume, n_results: int = 10) -> List[Dict]:
        """
        Find similar resumes using vector database.
        
        Args:
            resume: Resume to find similar ones for
            n_results: Number of results to return
            
        Returns:
            List of similar resumes
        """
        try:
            # Create search query from resume
            query = self._create_resume_search_query(resume)
            
            # Search vector database
            similar_resumes = self.vector_db.search_similar_resumes(query, n_results)
            
            return similar_resumes
            
        except Exception as e:
            logger.error(f"Failed to find similar resumes: {e}")
            return []
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract resume sections."""
        section_patterns = {
            'summary': [
                r'(?i)(?:professional\s+)?summary(?:\s+of\s+qualifications)?',
                r'(?i)profile',
                r'(?i)objective',
                r'(?i)career\s+objective',
                r'(?i)executive\s+summary',
                r'(?i)about\s+me'
            ],
            'experience': [
                r'(?i)(?:professional\s+)?(?:work\s+)?experience',
                r'(?i)employment(?:\s+history)?',
                r'(?i)career(?:\s+history)?',
                r'(?i)professional\s+background',
                r'(?i)work\s+history',
                r'(?i)employment\s+record'
            ],
            'education': [
                r'(?i)education(?:al\s+background)?',
                r'(?i)academic\s+background',
                r'(?i)qualifications',
                r'(?i)degrees?',
                r'(?i)educational\s+background'
            ],
            'skills': [
                r'(?i)(?:technical\s+)?skills',
                r'(?i)competencies',
                r'(?i)core\s+competencies',
                r'(?i)expertise',
                r'(?i)proficiencies',
                r'(?i)technical\s+expertise'
            ],
            'projects': [
                r'(?i)projects?',
                r'(?i)key\s+projects',
                r'(?i)notable\s+projects',
                r'(?i)portfolio',
                r'(?i)selected\s+projects'
            ],
            'certifications': [
                r'(?i)certifications?',
                r'(?i)licenses?',
                r'(?i)credentials',
                r'(?i)professional\s+certifications?',
                r'(?i)certificates?'
            ]
        }
        
        sections = {}
        text_lines = text.split('\n')
        
        for section_name, patterns in section_patterns.items():
            section_content = self._extract_section_content(text_lines, patterns)
            if section_content:
                sections[section_name] = section_content
        
        return sections
    
    def _extract_section_content(self, lines: List[str], patterns: List[str]) -> str:
        """Extract content for a specific section."""
        section_start = -1
        section_end = len(lines)
        
        # Find section start
        for i, line in enumerate(lines):
            for pattern in patterns:
                if re.search(pattern, line.strip(), re.IGNORECASE):
                    section_start = i
                    break
            if section_start != -1:
                break
        
        if section_start == -1:
            return ""
        
        # Find section end (next major section or end of document)
        all_patterns = []
        for pattern_list in [
            ['SUMMARY', 'PROFILE', 'OBJECTIVE'],
            ['EXPERIENCE', 'EMPLOYMENT', 'CAREER'],
            ['EDUCATION', 'ACADEMIC'],
            ['SKILLS', 'COMPETENCIES'],
            ['PROJECTS?', 'PORTFOLIO'],
            ['CERTIFICATIONS?', 'LICENSES?']
        ]:
            all_patterns.extend(pattern_list)
        
        for i in range(section_start + 1, len(lines)):
            line = lines[i].strip()
            for pattern in all_patterns:
                if re.match(f'^{pattern}', line, re.IGNORECASE) and len(line) < 50:
                    section_end = i
                    break
            if section_end != len(lines):
                break
        
        # Extract content
        content_lines = lines[section_start + 1:section_end]
        return '\n'.join(content_lines).strip()
    
    def _parse_contact_info(self, text: str) -> ContactInfo:
        """Parse contact information."""
        contact = ContactInfo()
        
        # Extract using helper function
        extracted = extract_contact_info(text)
        contact.email = extracted.get('email')
        contact.phone = extracted.get('phone')
        contact.linkedin = extracted.get('linkedin')
        contact.github = extracted.get('github')
        
        # Name extraction (usually in first few lines)
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if is_likely_name(line):
                contact.name = line
                break
        
        # Location extraction
        location_pattern = r'(?:^|\n)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z]{2}(?:\s*\d{5})?)'
        locations = re.findall(location_pattern, text)
        if locations:
            contact.location = locations[0]
        
        return contact
    
    def _parse_summary(self, text: str) -> Optional[str]:
        """Parse professional summary."""
        if not text or len(text.strip()) < 20:
            return None
        
        # Clean up the summary
        summary = re.sub(r'\n+', ' ', text.strip())
        summary = re.sub(r'\s+', ' ', summary)
        
        return summary
    
    def _parse_work_experience(self, text: str) -> List[WorkExperience]:
        """Parse work experience section."""
        if not text:
            return []
        
        experiences = []
        
        # Split by job entries
        job_entries = self._split_job_entries(text)
        
        # Parse each job entry
        for entry in job_entries:
            if len(entry.strip()) < 20:
                continue
                
            experience = self._parse_single_experience(entry)
            if experience.title or experience.company:
                experiences.append(experience)
        
        return experiences
    
    def _split_job_entries(self, text: str) -> List[str]:
        """Split text into individual job entries."""
        # Look for patterns that indicate new jobs
        job_separator_patterns = [
            r'\n(?=[A-Z][^a-z]*\|)',  # Title | Company pattern
            r'\n(?=[A-Z][a-z].*(?:at|@)\s+[A-Z])',  # Title at Company pattern
            r'\n(?=[A-Z][A-Za-z\s]+\n[A-Z][A-Za-z\s]+\|)',  # Multi-line title/company
        ]
        
        # Try to split the text into job entries
        job_entries = [text]  # Start with whole text
        
        for pattern in job_separator_patterns:
            new_entries = []
            for entry in job_entries:
                parts = re.split(pattern, entry)
                new_entries.extend([part.strip() for part in parts if part.strip()])
            job_entries = new_entries
            if len(job_entries) > 1:
                break
        
        return job_entries
    
    def _parse_single_experience(self, text: str) -> WorkExperience:
        """Parse a single work experience entry."""
        experience = WorkExperience()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return experience
        
        # Parse first line (usually title and company)
        first_line = lines[0]
        
        # Pattern: Title | Company | Date
        if '|' in first_line:
            parts = [part.strip() for part in first_line.split('|')]
            if len(parts) >= 2:
                experience.title = parts[0]
                experience.company = parts[1]
                if len(parts) >= 3:
                    start_date, end_date = self._parse_date_range(parts[2])
                    experience.start_date = start_date
                    experience.end_date = end_date
        
        # Pattern: Title at/@ Company
        elif ' at ' in first_line or ' @ ' in first_line:
            separator = ' at ' if ' at ' in first_line else ' @ '
            parts = first_line.split(separator, 1)
            if len(parts) == 2:
                experience.title = parts[0].strip()
                experience.company = parts[1].strip()
        
        # If no clear pattern, assume first line is title
        else:
            experience.title = first_line
            # Look for company in second line
            if len(lines) > 1:
                second_line = lines[1]
                if not self._looks_like_date(second_line) and not second_line.startswith('•'):
                    experience.company = second_line
        
        # Look for dates in subsequent lines
        if not experience.start_date:
            for line in lines[1:3]:  # Check next 2 lines
                if self._looks_like_date(line):
                    start_date, end_date = self._parse_date_range(line)
                    experience.start_date = start_date
                    experience.end_date = end_date
                    break
        
        # Parse achievements (bullet points)
        achievements = []
        technologies = []
        
        for line in lines:
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                achievement = line[1:].strip()
                achievements.append(achievement)
                
                # Extract technologies from achievements
                tech_matches = self._extract_technologies_from_text(achievement)
                technologies.extend(tech_matches)
        
        experience.achievements = achievements
        experience.technologies = list(set(technologies))  # Remove duplicates
        
        # Calculate duration
        if experience.start_date and experience.end_date:
            experience.duration_months = self._calculate_duration_months(
                experience.start_date, experience.end_date
            )
        
        return experience
    
    def _parse_education(self, text: str) -> List[Education]:
        """Parse education section."""
        if not text:
            return []
        
        education_entries = []
        
        # Split by education entries
        entries = re.split(r'\n(?=[A-Z][a-zA-Z\s]*(?:of|in)\s)', text)
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
                
            education = Education()
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            
            if not lines:
                continue
            
            # Parse degree and institution from first line
            first_line = lines[0]
            
            # Pattern: Degree | Institution
            if '|' in first_line:
                parts = [part.strip() for part in first_line.split('|')]
                education.degree = parts[0]
                if len(parts) > 1:
                    education.institution = parts[1]
            
            # Pattern: Degree, Institution or Degree - Institution
            elif ',' in first_line or ' - ' in first_line:
                separator = ',' if ',' in first_line else ' - '
                parts = first_line.split(separator, 1)
                education.degree = parts[0].strip()
                if len(parts) > 1:
                    education.institution = parts[1].strip()
            
            # Look for graduation date and GPA in subsequent lines
            for line in lines[1:]:
                if self._looks_like_date(line):
                    education.graduation_date = line
                elif 'gpa' in line.lower():
                    gpa_match = re.search(r'gpa:?\s*([\d.]+)', line.lower())
                    if gpa_match:
                        education.gpa = gpa_match.group(1)
                elif line.startswith('•') or 'relevant' in line.lower():
                    # Coursework or honors
                    if 'coursework' in line.lower():
                        coursework = re.sub(r'^[•\-\*]\s*', '', line)
                        coursework = re.sub(r'.*coursework:?\s*', '', coursework, flags=re.IGNORECASE)
                        education.relevant_coursework = [c.strip() for c in coursework.split(',')]
                    else:
                        honor = re.sub(r'^[•\-\*]\s*', '', line)
                        education.honors.append(honor)
            
            education_entries.append(education)
        
        return education_entries
    
    def _parse_skills(self, text: str) -> List[Skill]:
        """Parse skills section."""
        if not text:
            return []
        
        skills = []
        
        # Look for categorized skills (e.g., "Programming Languages: Python, Java")
        category_pattern = r'([A-Za-z\s&]+):\s*([^\n]+)'
        category_matches = re.findall(category_pattern, text)
        
        for category, skills_text in category_matches:
            category = category.strip()
            skill_names = [s.strip() for s in skills_text.split(',')]
            
            for skill_name in skill_names:
                if skill_name:
                    skill = Skill(name=skill_name, category=category)
                    skills.append(skill)
        
        # Also look for uncategorized skills
        remaining_text = text
        for category, skills_text in category_matches:
            remaining_text = remaining_text.replace(f"{category}: {skills_text}", "")
        
        # Find individual skills in remaining text
        individual_skills = self._find_skills_in_text(remaining_text)
        for skill_name in individual_skills:
            skill = Skill(name=skill_name, category=self._categorize_skill(skill_name))
            skills.append(skill)
        
        return skills
    
    def _parse_projects(self, text: str) -> List[Project]:
        """Parse projects section."""
        if not text:
            return []
        
        projects = []
        
        # Split by project entries
        project_entries = re.split(r'\n(?=[A-Z][^a-z\n]*(?:\||$))', text)
        
        for entry in project_entries:
            if len(entry.strip()) < 10:
                continue
                
            project = Project()
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            
            if not lines:
                continue
            
            # First line usually contains project name and possibly date
            first_line = lines[0]
            
            if '|' in first_line:
                parts = [part.strip() for part in first_line.split('|')]
                project.name = parts[0]
                if len(parts) > 1 and self._looks_like_date(parts[1]):
                    project.start_date = parts[1]
            else:
                project.name = first_line
            
            # Look for description and technologies in subsequent lines
            description_lines = []
            for line in lines[1:]:
                if line.startswith('•') or line.startswith('-'):
                    description_lines.append(line[1:].strip())
                elif 'technologies:' in line.lower() or 'tech stack:' in line.lower():
                    tech_text = re.sub(r'.*(?:technologies|tech stack):?\s*', '', line, flags=re.IGNORECASE)
                    project.technologies = [t.strip() for t in tech_text.split(',')]
                elif line.startswith('http') or 'github.com' in line.lower():
                    project.url = line
                else:
                    description_lines.append(line)
            
            if description_lines:
                project.description = ' '.join(description_lines)
            
            # Extract technologies from description if not found explicitly
            if not project.technologies and project.description:
                project.technologies = self._extract_technologies_from_text(project.description)
            
            projects.append(project)
        
        return projects
    
    def _parse_certifications(self, text: str) -> List[Certification]:
        """Parse certifications from text."""
        certifications = []
        
        # Look for certification patterns
        cert_patterns = [
            r'(?:certified|certification)\s+[^\n]+',
            r'[A-Z]{2,}\s+certified',
            r'(?:AWS|Google|Microsoft|Oracle|Cisco|CompTIA)\s+[^\n]+',
            r'Professional\s+[^\n]+',
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                cert = Certification(name=match.strip())
                certifications.append(cert)
        
        return certifications
    
    def _parse_languages(self, text: str) -> List[Language]:
        """Parse languages from text."""
        languages = []
        
        # Look for language section
        lang_pattern = r'(?:languages?|linguistic):\s*([^\n]+)'
        lang_matches = re.findall(lang_pattern, text, re.IGNORECASE)
        
        for match in lang_matches:
            langs = [l.strip() for l in match.split(',')]
            for lang in langs:
                if lang:
                    language = Language(name=lang, proficiency="Conversational")
                    languages.append(language)
        
        return languages
    
    def _looks_like_date(self, text: str) -> bool:
        """Check if text looks like a date range."""
        date_patterns = [
            r'\d{4}\s*[-–]\s*\d{4}',
            r'\d{1,2}/\d{4}\s*[-–]\s*\d{1,2}/\d{4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
            r'Present|Current|Now'
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in date_patterns)
    
    def _parse_date_range(self, date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse date range from string."""
        patterns = [
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4})',
            r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})',
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\w+\s+\d{4})\s*[-–]\s*(Present|Current|Now)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                start_date, end_date = match.groups()
                if end_date.lower() in ['present', 'current', 'now']:
                    end_date = 'Present'
                return start_date, end_date
        
        return None, None
    
    def _calculate_duration_months(self, start_date: str, end_date: str) -> int:
        """Calculate duration in months between dates."""
        try:
            if end_date.lower() == 'present':
                end_year = datetime.now().year
            else:
                end_year = int(re.search(r'\d{4}', end_date).group())
            
            start_year = int(re.search(r'\d{4}', start_date).group())
            
            return max(0, (end_year - start_year) * 12)
        except:
            return 0
    
    def _find_skills_in_text(self, text: str) -> List[str]:
        """Find individual skills in text."""
        found_skills = []
        text_lower = text.lower()
        
        # Check against known technical skills
        for skill in self.technical_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize a skill by name."""
        skill_lower = skill_name.lower()
        
        # Programming languages
        if skill_lower in ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust']:
            return 'Programming Languages'
        
        # Frameworks
        if skill_lower in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express']:
            return 'Frameworks'
        
        # Databases
        if skill_lower in ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite']:
            return 'Databases'
        
        # Cloud platforms
        if skill_lower in ['aws', 'azure', 'gcp', 'google cloud']:
            return 'Cloud Platforms'
        
        # Tools
        if skill_lower in ['git', 'docker', 'kubernetes', 'jenkins', 'jira']:
            return 'Tools'
        
        return 'General'
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technology names from text."""
        technologies = []
        text_lower = text.lower()
        
        for tech in self.technical_skills:
            if tech.lower() in text_lower:
                technologies.append(tech)
        
        return technologies
    
    def _calculate_parse_confidence(self, parsed_data: Dict) -> float:
        """Calculate confidence score for parsing quality."""
        confidence = 0.0
        total_weight = 0.0
        
        # Contact info weight: 30%
        contact_weight = 0.3
        contact_score = 0.0
        
        contact_info = parsed_data['contact_info']
        if contact_info.name:
            contact_score += 0.3
        if contact_info.email:
            contact_score += 0.4
        if contact_info.phone:
            contact_score += 0.3
        
        confidence += contact_score * contact_weight
        total_weight += contact_weight
        
        # Work experience weight: 40%
        experience_weight = 0.4
        experience_score = 0.0
        
        experiences = parsed_data['work_experience']
        if experiences:
            exp_quality = 0.0
            for exp in experiences:
                if exp.title and exp.company:
                    exp_quality += 0.5
                if exp.achievements:
                    exp_quality += 0.3
                if exp.start_date:
                    exp_quality += 0.2
            
            experience_score = min(1.0, exp_quality / len(experiences))
        
        confidence += experience_score * experience_weight
        total_weight += experience_weight
        
        # Education weight: 15%
        education_weight = 0.15
        education_score = 0.0
        
        education = parsed_data['education']
        if education:
            for edu in education:
                if edu.degree and edu.institution:
                    education_score += 0.8
                    break
        
        confidence += education_score * education_weight
        total_weight += education_weight
        
        # Skills weight: 15%
        skills_weight = 0.15
        skills_score = 0.0
        
        skills = parsed_data['skills']
        if skills:
            skills_score = min(1.0, len(skills) / 10.0)  # Max confidence at 10+ skills
        
        confidence += skills_score * skills_weight
        total_weight += skills_weight
        
        return min(100.0, (confidence / total_weight) * 100) if total_weight > 0 else 0.0
    
    def _calculate_resume_metrics(self, resume: ParsedResume) -> Dict[str, float]:
        """Calculate resume metrics."""
        metrics = {}
        
        # Basic metrics
        metrics['word_count'] = len(resume.raw_text.split()) if resume.raw_text else 0
        metrics['page_count'] = max(1, metrics['word_count'] // 250)  # Rough estimate
        metrics['section_count'] = len([s for s in [
            resume.summary, resume.work_experience, resume.education, 
            resume.skills, resume.projects
        ] if s])
        
        # Skills metrics
        metrics['skills_count'] = len(resume.skills)
        metrics['technical_skills_count'] = len([s for s in resume.skills if s.category == 'Programming Languages'])
        
        # Experience metrics
        metrics['experience_years'] = self._calculate_experience_years(resume.work_experience)
        metrics['job_count'] = len(resume.work_experience)
        
        # Education metrics
        metrics['education_count'] = len(resume.education)
        metrics['highest_degree'] = self._determine_education_level(resume.education)
        
        return metrics
    
    def _calculate_experience_years(self, work_experience: List[WorkExperience]) -> int:
        """Calculate total years of experience."""
        total_months = 0
        for exp in work_experience:
            if exp.duration_months:
                total_months += exp.duration_months
        
        return total_months // 12
    
    def _determine_education_level(self, education: List[Education]) -> str:
        """Determine highest education level."""
        if not education:
            return "No formal education"
        
        degree_levels = {
            'phd': 5, 'doctorate': 5, 'ph.d': 5,
            'master': 4, 'mba': 4, 'ms': 4, 'ma': 4,
            'bachelor': 3, 'bs': 3, 'ba': 3, 'bachelor': 3,
            'associate': 2, 'aa': 2, 'as': 2,
            'diploma': 1, 'certificate': 1
        }
        
        highest_level = 0
        highest_degree = "High School"
        
        for edu in education:
            if edu.degree:
                degree_lower = edu.degree.lower()
                for degree, level in degree_levels.items():
                    if degree in degree_lower and level > highest_level:
                        highest_level = level
                        highest_degree = edu.degree
        
        return highest_degree
    
    def _infer_industry(self, work_experience: List[WorkExperience], skills: List[Skill]) -> str:
        """Infer industry from work experience and skills."""
        # Simple industry inference based on common patterns
        tech_keywords = ['software', 'developer', 'engineer', 'programming', 'coding']
        finance_keywords = ['finance', 'banking', 'investment', 'financial']
        healthcare_keywords = ['healthcare', 'medical', 'hospital', 'clinical']
        
        all_text = ' '.join([
            exp.title or '' for exp in work_experience
        ] + [skill.name for skill in skills])
        
        text_lower = all_text.lower()
        
        if any(keyword in text_lower for keyword in tech_keywords):
            return "Technology"
        elif any(keyword in text_lower for keyword in finance_keywords):
            return "Finance"
        elif any(keyword in text_lower for keyword in healthcare_keywords):
            return "Healthcare"
        else:
            return "General"
    
    def _create_resume_search_query(self, resume: ParsedResume) -> str:
        """Create search query from resume for vector database."""
        query_parts = []
        
        if resume.summary:
            query_parts.append(resume.summary)
        
        if resume.work_experience:
            for exp in resume.work_experience:
                if exp.title and exp.company:
                    query_parts.append(f"{exp.title} at {exp.company}")
        
        if resume.skills:
            skills_text = ', '.join([skill.name for skill in resume.skills])
            query_parts.append(f"Skills: {skills_text}")
        
        return ' '.join(query_parts)
    
    def _load_technical_skills(self) -> List[str]:
        """Load list of technical skills."""
        return [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
            'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS', 'SASS', 'LESS',
            
            # Frameworks & Libraries
            'React', 'Angular', 'Vue', 'Svelte', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
            'Spring', 'Hibernate', 'Laravel', 'Rails', 'ASP.NET', 'jQuery', 'Bootstrap', 'Tailwind',
            
            # Databases
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'SQLite', 'Oracle', 'Cassandra',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions',
            'Terraform', 'Ansible', 'Chef', 'Puppet', 'Nginx', 'Apache',
            
            # Tools & Other
            'Git', 'SVN', 'Jira', 'Confluence', 'Slack', 'Teams', 'Figma', 'Sketch', 'Photoshop'
        ]
    
    def _load_soft_skills(self) -> List[str]:
        """Load list of soft skills."""
        return [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving', 'Analytical Thinking',
            'Creativity', 'Adaptability', 'Time Management', 'Project Management', 'Mentoring',
            'Collaboration', 'Critical Thinking', 'Decision Making', 'Negotiation', 'Presentation'
        ]
    
    def _load_degree_patterns(self) -> List[str]:
        """Load degree patterns for recognition."""
        return [
            r'Ph\.?D\.?', r'Doctor(?:ate)?', r'M\.?S\.?', r'M\.?A\.?', r'MBA', r'Master',
            r'B\.?S\.?', r'B\.?A\.?', r'Bachelor', r'A\.?A\.?', r'A\.?S\.?', r'Associate'
        ]
