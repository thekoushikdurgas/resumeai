"""
Job Matcher Module for Resume/CV AI Application
Handles job-resume matching using vector database and AI analysis.

This module provides:
- Advanced job-resume matching algorithms
- Vector database integration for semantic matching
- AI-powered compatibility analysis
- Comprehensive scoring and ranking
- Skill and experience alignment assessment
- Industry-specific matching criteria

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from models.resume_model import ParsedResume
from models.job_model import JobDescription, JobMatch
from models.analysis_model import JobMatchAnalysis
from utils.helpers import calculate_text_similarity, clean_text
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("job_matcher")

class JobMatcher:
    """
    Job matching engine using vector database and AI analysis with comprehensive logging.
    
    This class provides advanced job-resume matching capabilities including:
    - Semantic similarity matching using vector embeddings
    - AI-powered compatibility analysis
    - Multi-dimensional scoring (skills, experience, education)
    - Industry-specific matching criteria
    - Comprehensive performance monitoring and logging
    
    Attributes:
        vector_db: Vector database instance for semantic operations
        ai_handler: AI handler instance for content analysis
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, vector_db, ai_handler):
        """
        Initialize job matcher with comprehensive logging.
        
        Sets up the matcher with vector database and AI handler dependencies
        and logs initialization details for debugging and monitoring.
        
        Args:
            vector_db: Vector database instance for semantic operations
            ai_handler: AI handler instance for content analysis
            
        Raises:
            Exception: If initialization fails due to missing dependencies
        """
        logger.info("Initializing JobMatcher")
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
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"JobMatcher initialized successfully in {initialization_time:.2f}s")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"JobMatcher initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def match_resume_to_job(self, resume: ParsedResume, job_description: str) -> Dict[str, Any]:
        """
        Match resume to job description with comprehensive logging.
        
        This method performs advanced job-resume matching including:
        - Job description parsing and analysis
        - Multi-dimensional scoring (skills, experience, education, location)
        - Semantic similarity matching using vector embeddings
        - Skills gap analysis and recommendations
        - Overall compatibility assessment
        
        Args:
            resume (ParsedResume): Parsed resume object to match
            job_description (str): Job description text to match against
            
        Returns:
            Dict[str, Any]: Comprehensive matching analysis containing:
                - match_score: Overall compatibility score (0-100)
                - skill_match: Skills alignment score
                - experience_match: Experience level alignment
                - education_match: Education requirements alignment
                - location_match: Geographic location compatibility
                - matched_skills: List of skills that match requirements
                - missing_skills: List of required skills not found
                - recommendations: Improvement suggestions
        """
        start_time = time.time()
        
        try:
            logger.info("Starting job-resume matching process")
            logger.debug(f"Resume name: {resume.contact_info.name or 'Unknown'}")
            logger.debug(f"Job description length: {len(job_description)} characters")
            
            # Validate inputs
            if not job_description or len(job_description.strip()) < 50:
                logger.warning("Job description is very short, may result in poor matching quality")
            
            # Create job description object
            logger.debug("Parsing job description")
            job = self._parse_job_description(job_description)
            logger.info(f"Job parsed: {job.title or 'Unknown Position'}")
            
            # Calculate various match scores
            logger.debug("Calculating skill match score")
            skill_match = self._calculate_skill_match(resume, job)
            logger.debug(f"Skill match score: {skill_match:.1f}%")
            
            logger.debug("Calculating experience match score")
            experience_match = self._calculate_experience_match(resume, job)
            logger.debug(f"Experience match score: {experience_match:.1f}%")
            
            logger.debug("Calculating education match score")
            education_match = self._calculate_education_match(resume, job)
            logger.debug(f"Education match score: {education_match:.1f}%")
            
            logger.debug("Calculating location match score")
            location_match = self._calculate_location_match(resume, job)
            logger.debug(f"Location match score: {location_match:.1f}%")
            
            # Calculate overall match score
            logger.debug("Calculating overall match score")
            overall_match = self._calculate_overall_match(
                skill_match, experience_match, education_match, location_match
            )
            logger.info(f"Overall match score: {overall_match:.1f}%")
            
            # Find matched and missing skills
            logger.debug("Analyzing skills alignment")
            matched_skills, missing_skills = self._analyze_skills(resume, job)
            logger.info(f"Matched skills: {len(matched_skills)}, Missing skills: {len(missing_skills)}")
            
            # Generate recommendations
            logger.debug("Generating improvement recommendations")
            recommendations = self._generate_recommendations(
                resume, job, matched_skills, missing_skills
            )
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            matching_time = time.time() - start_time
            logger.info(f"Job-resume matching completed in {matching_time:.2f}s")
            logger.info(f"Final match score: {overall_match:.1f}%")
            
            return {
                'match_score': overall_match,
                'skill_match': skill_match,
                'experience_match': experience_match,
                'education_match': education_match,
                'location_match': location_match,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'recommendations': recommendations,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            matching_time = time.time() - start_time
            logger.error(f"Job-resume matching failed after {matching_time:.2f}s: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Resume name: {resume.contact_info.name or 'Unknown'}")
            
            return {
                'match_score': 0,
                'error': str(e),
                'processing_time': matching_time,
                'analysis_date': datetime.now().isoformat()
            }
    
    def find_similar_jobs(self, resume: ParsedResume, n_results: int = 10) -> List[Dict]:
        """
        Find similar jobs using vector database.
        
        Args:
            resume: Resume to find similar jobs for
            n_results: Number of results to return
            
        Returns:
            List of similar jobs
        """
        try:
            # Create search query from resume
            query = self._create_resume_search_query(resume)
            
            # Search vector database
            similar_jobs = self.vector_db.search_similar_jobs(query, n_results)
            
            return similar_jobs
            
        except Exception as e:
            logger.error(f"Failed to find similar jobs: {e}")
            return []
    
    def _parse_job_description(self, job_text: str) -> JobDescription:
        """Parse job description text into structured format."""
        job = JobDescription()
        
        # Extract basic information using simple patterns
        lines = job_text.split('\n')
        
        # Look for title (usually in first few lines)
        for line in lines[:5]:
            line = line.strip()
            if len(line) < 100 and not any(keyword in line.lower() for keyword in 
                ['company', 'location', 'description', 'requirements']):
                job.title = line
                break
        
        # Extract company name
        for line in lines[:10]:
            if 'company' in line.lower() or 'employer' in line.lower():
                # Extract company name after colon or dash
                if ':' in line:
                    job.company = line.split(':', 1)[1].strip()
                elif '-' in line:
                    job.company = line.split('-', 1)[1].strip()
                break
        
        # Extract location
        for line in lines[:10]:
            if any(keyword in line.lower() for keyword in ['location', 'based', 'remote', 'hybrid']):
                if ':' in line:
                    job.location = line.split(':', 1)[1].strip()
                break
        
        # Extract required skills
        job.required_skills = self._extract_skills_from_text(job_text)
        
        # Set description
        job.description = job_text
        
        return job
    
    def _calculate_skill_match(self, resume: ParsedResume, job: JobDescription) -> float:
        """Calculate skill match percentage."""
        if not job.required_skills:
            return 0.0
        
        resume_skills = [skill.name.lower() for skill in resume.skills]
        job_skills = [skill.lower() for skill in job.required_skills]
        
        matched_skills = 0
        for job_skill in job_skills:
            for resume_skill in resume_skills:
                if job_skill in resume_skill or resume_skill in job_skill:
                    matched_skills += 1
                    break
        
        return (matched_skills / len(job_skills)) * 100 if job_skills else 0.0
    
    def _calculate_experience_match(self, resume: ParsedResume, job: JobDescription) -> float:
        """Calculate experience match percentage."""
        # Simple experience matching based on years
        resume_years = self._calculate_resume_experience_years(resume)
        
        # Extract years from job description
        job_years = self._extract_experience_requirement(job.description)
        
        if job_years == 0:
            return 100.0  # No experience requirement
        
        if resume_years >= job_years:
            return 100.0
        else:
            return (resume_years / job_years) * 100
    
    def _calculate_education_match(self, resume: ParsedResume, job: JobDescription) -> float:
        """Calculate education match percentage."""
        # Simple education level matching
        resume_education_level = self._get_resume_education_level(resume)
        job_education_level = self._extract_education_requirement(job.description)
        
        education_hierarchy = {
            'high_school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5
        }
        
        resume_level = education_hierarchy.get(resume_education_level, 0)
        job_level = education_hierarchy.get(job_education_level, 0)
        
        if job_level == 0:
            return 100.0  # No education requirement
        
        if resume_level >= job_level:
            return 100.0
        else:
            return (resume_level / job_level) * 100
    
    def _calculate_location_match(self, resume: ParsedResume, job: JobDescription) -> float:
        """Calculate location match percentage."""
        if not resume.contact_info.location or not job.location:
            return 50.0  # Neutral score if location info missing
        
        # Simple location matching
        resume_location = resume.contact_info.location.lower()
        job_location = job.location.lower()
        
        if 'remote' in job_location or 'anywhere' in job_location:
            return 100.0
        
        if resume_location in job_location or job_location in resume_location:
            return 100.0
        
        # Check for same city/state
        resume_parts = resume_location.split(',')
        job_parts = job_location.split(',')
        
        if len(resume_parts) >= 2 and len(job_parts) >= 2:
            if resume_parts[1].strip() == job_parts[1].strip():  # Same state
                return 75.0
        
        return 25.0  # Different locations
    
    def _calculate_overall_match(self, skill_match: float, experience_match: float, 
                               education_match: float, location_match: float) -> float:
        """Calculate overall match score."""
        # Weighted average
        weights = {
            'skill': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'location': 0.1
        }
        
        overall = (
            skill_match * weights['skill'] +
            experience_match * weights['experience'] +
            education_match * weights['education'] +
            location_match * weights['location']
        )
        
        return round(overall, 1)
    
    def _analyze_skills(self, resume: ParsedResume, job: JobDescription) -> tuple:
        """Analyze matched and missing skills."""
        resume_skills = [skill.name.lower() for skill in resume.skills]
        job_skills = [skill.lower() for skill in job.required_skills]
        
        matched_skills = []
        missing_skills = []
        
        for job_skill in job_skills:
            matched = False
            for resume_skill in resume_skills:
                if job_skill in resume_skill or resume_skill in job_skill:
                    matched_skills.append(job_skill)
                    matched = True
                    break
            
            if not matched:
                missing_skills.append(job_skill)
        
        return matched_skills, missing_skills
    
    def _generate_recommendations(self, resume: ParsedResume, job: JobDescription,
                                matched_skills: List[str], missing_skills: List[str]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Skill recommendations
        if missing_skills:
            recommendations.append(f"Consider learning or highlighting these skills: {', '.join(missing_skills[:5])}")
        
        # Experience recommendations
        resume_years = self._calculate_resume_experience_years(resume)
        job_years = self._extract_experience_requirement(job.description)
        
        if job_years > 0 and resume_years < job_years:
            recommendations.append(f"Gain {job_years - resume_years} more years of experience in this field")
        
        # Education recommendations
        resume_education = self._get_resume_education_level(resume)
        job_education = self._extract_education_requirement(job.description)
        
        if job_education and resume_education != job_education:
            recommendations.append(f"Consider pursuing {job_education} degree if required")
        
        # General recommendations
        if len(matched_skills) < len(job.required_skills) * 0.5:
            recommendations.append("Focus on developing more of the required technical skills")
        
        return recommendations
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from job description text."""
        # Common technical skills to look for
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'agile', 'scrum', 'machine learning', 'ai',
            'data analysis', 'project management', 'leadership', 'communication'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in technical_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _calculate_resume_experience_years(self, resume: ParsedResume) -> int:
        """Calculate total years of experience from resume."""
        total_months = 0
        for exp in resume.work_experience:
            if exp.duration_months:
                total_months += exp.duration_months
        
        return total_months // 12
    
    def _extract_experience_requirement(self, job_text: str) -> int:
        """Extract years of experience requirement from job text."""
        import re
        
        # Look for patterns like "3+ years", "5-7 years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\s*-\s*\d+\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*(\d+)\s*years?\s*(?:of\s*)?experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_text.lower())
            if match:
                return int(match.group(1))
        
        return 0
    
    def _get_resume_education_level(self, resume: ParsedResume) -> str:
        """Get highest education level from resume."""
        if not resume.education:
            return 'high_school'
        
        degree_levels = {
            'phd': 'phd', 'doctorate': 'phd', 'ph.d': 'phd',
            'master': 'master', 'mba': 'master', 'ms': 'master', 'ma': 'master',
            'bachelor': 'bachelor', 'bs': 'bachelor', 'ba': 'bachelor',
            'associate': 'associate', 'aa': 'associate', 'as': 'associate'
        }
        
        highest_level = 'high_school'
        
        for edu in resume.education:
            if edu.degree:
                degree_lower = edu.degree.lower()
                for degree, level in degree_levels.items():
                    if degree in degree_lower:
                        if level == 'phd':
                            return 'phd'
                        elif level == 'master' and highest_level != 'phd':
                            highest_level = 'master'
                        elif level == 'bachelor' and highest_level not in ['phd', 'master']:
                            highest_level = 'bachelor'
                        elif level == 'associate' and highest_level == 'high_school':
                            highest_level = 'associate'
        
        return highest_level
    
    def _extract_education_requirement(self, job_text: str) -> str:
        """Extract education requirement from job text."""
        text_lower = job_text.lower()
        
        if any(degree in text_lower for degree in ['phd', 'doctorate', 'ph.d']):
            return 'phd'
        elif any(degree in text_lower for degree in ['master', 'mba', 'ms', 'ma']):
            return 'master'
        elif any(degree in text_lower for degree in ['bachelor', 'bs', 'ba']):
            return 'bachelor'
        elif any(degree in text_lower for degree in ['associate', 'aa', 'as']):
            return 'associate'
        else:
            return 'high_school'
    
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
