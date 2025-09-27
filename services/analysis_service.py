"""
Analysis Service for Resume/CV AI Application
Handles resume and job analysis operations.

This module provides:
- Resume analysis and scoring
- Job matching analysis
- Skills extraction and analysis
- ATS compatibility checking
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from utils.logger import setup_logger
from utils.text_processing import text_processor

# Initialize logger with module-specific name
logger = setup_logger("analysis_service")

class AnalysisService:
    """
    Analysis service class with comprehensive logging.
    
    This class provides resume and job analysis including scoring,
    matching, skills extraction, and ATS compatibility checking for
    the Resume/CV AI application.
    
    Key Features:
    - Resume analysis and scoring
    - Job matching analysis
    - Skills extraction and analysis
    - ATS compatibility checking
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _analysis_cache (Dict[str, Dict]): Analysis results cache
        _skills_database (Dict[str, List]): Skills database for matching
    """
    
    def __init__(self):
        """Initialize analysis service with comprehensive logging."""
        logger.info("Initializing Analysis Service")
        self._initialization_time = datetime.now()
        
        # Initialize analysis components
        self._analysis_cache = {}
        self._skills_database = {}
        
        try:
            # Load skills database
            self._load_skills_database()
            
            logger.info("Analysis Service initialized successfully")
            logger.info(f"Loaded {len(self._skills_database)} skill categories")
            
        except Exception as e:
            logger.error(f"Analysis Service initialization failed: {e}")
            raise
    
    def _load_skills_database(self):
        """Load skills database for analysis."""
        try:
            # Initialize skills database with common skills
            self._skills_database = {
                'programming_languages': [
                    'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go',
                    'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql'
                ],
                'web_technologies': [
                    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                    'django', 'flask', 'spring', 'laravel', 'asp.net', 'jquery'
                ],
                'databases': [
                    'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                    'cassandra', 'oracle', 'sqlite', 'dynamodb'
                ],
                'cloud_platforms': [
                    'aws', 'azure', 'google cloud', 'heroku', 'digitalocean',
                    'linode', 'vultr', 'cloudflare'
                ],
                'tools_and_frameworks': [
                    'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
                    'jira', 'confluence', 'slack', 'trello', 'asana'
                ],
                'soft_skills': [
                    'leadership', 'communication', 'teamwork', 'problem solving',
                    'time management', 'project management', 'critical thinking',
                    'adaptability', 'creativity', 'analytical thinking'
                ]
            }
            
            logger.debug(f"Loaded {len(self._skills_database)} skill categories")
            
        except Exception as e:
            logger.error(f"Failed to load skills database: {e}")
            self._skills_database = {}
    
    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze resume and provide comprehensive insights.
        
        Args:
            resume_data (Dict[str, Any]): Resume data to analyze
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            logger.info("Starting resume analysis")
            start_time = time.time()
            
            # Extract text content
            text_content = self._extract_resume_text(resume_data)
            
            # Perform various analyses
            skills_analysis = self._analyze_skills(text_content)
            experience_analysis = self._analyze_experience(resume_data)
            education_analysis = self._analyze_education(resume_data)
            structure_analysis = self._analyze_resume_structure(resume_data)
            ats_analysis = self._analyze_ats_compatibility(resume_data)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(
                skills_analysis, experience_analysis, education_analysis,
                structure_analysis, ats_analysis
            )
            
            analysis_time = time.time() - start_time
            
            result = {
                'success': True,
                'overall_score': overall_score,
                'skills_analysis': skills_analysis,
                'experience_analysis': experience_analysis,
                'education_analysis': education_analysis,
                'structure_analysis': structure_analysis,
                'ats_analysis': ats_analysis,
                'recommendations': self._generate_recommendations(
                    skills_analysis, experience_analysis, education_analysis,
                    structure_analysis, ats_analysis
                ),
                'analysis_time': round(analysis_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache analysis result
            self._analysis_cache[f"resume_{hash(text_content)}"] = result
            
            logger.info(f"Resume analysis completed in {analysis_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze resume: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_resume_text(self, resume_data: Dict[str, Any]) -> str:
        """Extract text content from resume data."""
        try:
            text_parts = []
            
            # Extract from different sections
            if 'summary' in resume_data:
                text_parts.append(resume_data['summary'])
            
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    text_parts.append(exp.get('title', ''))
                    text_parts.append(exp.get('description', ''))
            
            if 'education' in resume_data:
                for edu in resume_data['education']:
                    text_parts.append(edu.get('degree', ''))
                    text_parts.append(edu.get('school', ''))
            
            if 'skills' in resume_data:
                text_parts.extend(resume_data['skills'])
            
            return ' '.join(text_parts)
            
        except Exception as e:
            logger.error(f"Failed to extract resume text: {e}")
            return ""
    
    def _analyze_skills(self, text_content: str) -> Dict[str, Any]:
        """Analyze skills in resume text."""
        try:
            # Extract skills using text processor
            found_skills = text_processor.extract_skills(text_content)
            
            # Categorize skills
            categorized_skills = {}
            for category, skills in self._skills_database.items():
                category_skills = []
                for skill in found_skills:
                    if skill.lower() in [s.lower() for s in skills]:
                        category_skills.append(skill)
                categorized_skills[category] = category_skills
            
            # Calculate skills score
            total_skills = len(found_skills)
            unique_categories = len([cat for cat, skills in categorized_skills.items() if skills])
            skills_score = min(100, (total_skills * 10) + (unique_categories * 5))
            
            return {
                'found_skills': found_skills,
                'categorized_skills': categorized_skills,
                'total_skills': total_skills,
                'unique_categories': unique_categories,
                'skills_score': skills_score
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze skills: {e}")
            return {'error': str(e)}
    
    def _analyze_experience(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze work experience."""
        try:
            experience = resume_data.get('experience', [])
            
            if not experience:
                return {
                    'experience_count': 0,
                    'total_years': 0,
                    'experience_score': 0,
                    'experience_level': 'No Experience'
                }
            
            # Calculate total years of experience
            total_years = 0
            for exp in experience:
                years = text_processor.extract_experience_years(exp.get('description', ''))
                if years > 0:
                    total_years += years
                else:
                    # Estimate based on date range if available
                    if 'start_date' in exp and 'end_date' in exp:
                        try:
                            from datetime import datetime
                            start = datetime.strptime(exp['start_date'], '%Y-%m-%d')
                            end = datetime.strptime(exp['end_date'], '%Y-%m-%d')
                            years = (end - start).days / 365.25
                            total_years += years
                        except:
                            total_years += 1  # Default to 1 year if dates are invalid
            
            # Determine experience level
            if total_years < 1:
                experience_level = 'Entry Level'
            elif total_years < 3:
                experience_level = 'Junior'
            elif total_years < 7:
                experience_level = 'Mid Level'
            elif total_years < 15:
                experience_level = 'Senior'
            else:
                experience_level = 'Executive'
            
            # Calculate experience score
            experience_score = min(100, total_years * 10)
            
            return {
                'experience_count': len(experience),
                'total_years': round(total_years, 1),
                'experience_score': experience_score,
                'experience_level': experience_level
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze experience: {e}")
            return {'error': str(e)}
    
    def _analyze_education(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze education background."""
        try:
            education = resume_data.get('education', [])
            
            if not education:
                return {
                    'education_count': 0,
                    'highest_degree': 'No Education',
                    'education_score': 0
                }
            
            # Find highest degree
            degree_levels = {
                'phd': 5, 'doctorate': 5, 'doctoral': 5,
                'masters': 4, 'master': 4, 'ms': 4, 'ma': 4, 'mba': 4,
                'bachelors': 3, 'bachelor': 3, 'bs': 3, 'ba': 3,
                'associates': 2, 'associate': 2, 'aa': 2, 'as': 2,
                'high school': 1, 'hs': 1, 'diploma': 1
            }
            
            highest_level = 0
            highest_degree = 'No Degree'
            
            for edu in education:
                degree = edu.get('degree', '').lower()
                for degree_type, level in degree_levels.items():
                    if degree_type in degree and level > highest_level:
                        highest_level = level
                        highest_degree = edu.get('degree', '')
            
            # Calculate education score
            education_score = highest_level * 20
            
            return {
                'education_count': len(education),
                'highest_degree': highest_degree,
                'education_score': education_score
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze education: {e}")
            return {'error': str(e)}
    
    def _analyze_resume_structure(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume structure and formatting."""
        try:
            # Check for required sections
            required_sections = ['contact', 'summary', 'experience', 'education', 'skills']
            present_sections = [section for section in required_sections if section in resume_data]
            
            # Check section completeness
            section_scores = {}
            for section in required_sections:
                if section in resume_data:
                    if section == 'contact':
                        contact = resume_data[section]
                        score = 0
                        if contact.get('name'): score += 25
                        if contact.get('email'): score += 25
                        if contact.get('phone'): score += 25
                        if contact.get('location'): score += 25
                        section_scores[section] = score
                    elif section == 'summary':
                        summary = resume_data[section]
                        score = min(100, len(summary) * 2) if summary else 0
                        section_scores[section] = score
                    elif section == 'experience':
                        experience = resume_data[section]
                        score = min(100, len(experience) * 20) if experience else 0
                        section_scores[section] = score
                    elif section == 'education':
                        education = resume_data[section]
                        score = min(100, len(education) * 25) if education else 0
                        section_scores[section] = score
                    elif section == 'skills':
                        skills = resume_data[section]
                        score = min(100, len(skills) * 5) if skills else 0
                        section_scores[section] = score
                else:
                    section_scores[section] = 0
            
            # Calculate overall structure score
            structure_score = sum(section_scores.values()) / len(required_sections)
            
            return {
                'present_sections': present_sections,
                'missing_sections': [s for s in required_sections if s not in present_sections],
                'section_scores': section_scores,
                'structure_score': round(structure_score, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze resume structure: {e}")
            return {'error': str(e)}
    
    def _analyze_ats_compatibility(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ATS compatibility."""
        try:
            # Check for ATS-friendly elements
            ats_checks = {
                'standard_format': True,  # Assuming standard format
                'no_graphics': True,  # Assuming no graphics
                'standard_sections': True,  # Assuming standard sections
                'contact_info_complete': False,
                'keywords_present': False,
                'consistent_formatting': True  # Assuming consistent formatting
            }
            
            # Check contact info completeness
            if 'contact' in resume_data:
                contact = resume_data['contact']
                if all(contact.get(field) for field in ['name', 'email', 'phone']):
                    ats_checks['contact_info_complete'] = True
            
            # Check for keywords
            text_content = self._extract_resume_text(resume_data)
            if text_content and len(text_content) > 100:
                ats_checks['keywords_present'] = True
            
            # Calculate ATS score
            ats_score = sum(ats_checks.values()) / len(ats_checks) * 100
            
            return {
                'ats_checks': ats_checks,
                'ats_score': round(ats_score, 1),
                'recommendations': self._get_ats_recommendations(ats_checks)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze ATS compatibility: {e}")
            return {'error': str(e)}
    
    def _get_ats_recommendations(self, ats_checks: Dict[str, bool]) -> List[str]:
        """Get ATS recommendations based on checks."""
        recommendations = []
        
        if not ats_checks['contact_info_complete']:
            recommendations.append("Ensure contact information is complete (name, email, phone)")
        
        if not ats_checks['keywords_present']:
            recommendations.append("Add more relevant keywords to improve ATS compatibility")
        
        return recommendations
    
    def _calculate_overall_score(self, skills_analysis: Dict, experience_analysis: Dict,
                               education_analysis: Dict, structure_analysis: Dict,
                               ats_analysis: Dict) -> float:
        """Calculate overall resume score."""
        try:
            scores = []
            
            if 'skills_score' in skills_analysis:
                scores.append(skills_analysis['skills_score'])
            
            if 'experience_score' in experience_analysis:
                scores.append(experience_analysis['experience_score'])
            
            if 'education_score' in education_analysis:
                scores.append(education_analysis['education_score'])
            
            if 'structure_score' in structure_analysis:
                scores.append(structure_analysis['structure_score'])
            
            if 'ats_score' in ats_analysis:
                scores.append(ats_analysis['ats_score'])
            
            if scores:
                return round(sum(scores) / len(scores), 1)
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Failed to calculate overall score: {e}")
            return 0.0
    
    def _generate_recommendations(self, skills_analysis: Dict, experience_analysis: Dict,
                                education_analysis: Dict, structure_analysis: Dict,
                                ats_analysis: Dict) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Skills recommendations
        if skills_analysis.get('total_skills', 0) < 5:
            recommendations.append("Add more technical skills to strengthen your profile")
        
        # Experience recommendations
        if experience_analysis.get('total_years', 0) < 2:
            recommendations.append("Consider highlighting relevant projects or internships")
        
        # Structure recommendations
        if structure_analysis.get('missing_sections'):
            recommendations.append(f"Add missing sections: {', '.join(structure_analysis['missing_sections'])}")
        
        # ATS recommendations
        if ats_analysis.get('recommendations'):
            recommendations.extend(ats_analysis['recommendations'])
        
        return recommendations
    
    def analyze_job_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze job-resume match.
        
        Args:
            resume_data (Dict[str, Any]): Resume data
            job_data (Dict[str, Any]): Job description data
            
        Returns:
            Dict[str, Any]: Job match analysis result
        """
        try:
            logger.info("Starting job match analysis")
            start_time = time.time()
            
            # Extract text from both resume and job
            resume_text = self._extract_resume_text(resume_data)
            job_text = job_data.get('description', '')
            
            # Analyze skills match
            skills_match = self._analyze_skills_match(resume_text, job_text)
            
            # Analyze experience match
            experience_match = self._analyze_experience_match(resume_data, job_data)
            
            # Analyze keyword match
            keyword_match = self._analyze_keyword_match(resume_text, job_text)
            
            # Calculate overall match score
            overall_match = self._calculate_job_match_score(skills_match, experience_match, keyword_match)
            
            analysis_time = time.time() - start_time
            
            result = {
                'success': True,
                'overall_match': overall_match,
                'skills_match': skills_match,
                'experience_match': experience_match,
                'keyword_match': keyword_match,
                'recommendations': self._generate_job_match_recommendations(
                    skills_match, experience_match, keyword_match
                ),
                'analysis_time': round(analysis_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Job match analysis completed in {analysis_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze job match: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_skills_match(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Analyze skills match between resume and job."""
        try:
            # Extract skills from both texts
            resume_skills = text_processor.extract_skills(resume_text)
            job_skills = text_processor.extract_skills(job_text)
            
            # Find matching skills
            matching_skills = [skill for skill in resume_skills if skill.lower() in [s.lower() for s in job_skills]]
            missing_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in resume_skills]]
            
            # Calculate match percentage
            if job_skills:
                match_percentage = (len(matching_skills) / len(job_skills)) * 100
            else:
                match_percentage = 0
            
            return {
                'resume_skills': resume_skills,
                'job_skills': job_skills,
                'matching_skills': matching_skills,
                'missing_skills': missing_skills,
                'match_percentage': round(match_percentage, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze skills match: {e}")
            return {'error': str(e)}
    
    def _analyze_experience_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze experience match between resume and job."""
        try:
            # Get experience from resume
            resume_experience = resume_data.get('experience', [])
            resume_years = sum(
                text_processor.extract_experience_years(exp.get('description', ''))
                for exp in resume_experience
            )
            
            # Get required experience from job
            job_text = job_data.get('description', '')
            required_years = text_processor.extract_experience_years(job_text)
            
            # Calculate match
            if required_years > 0:
                if resume_years >= required_years:
                    experience_match = 100
                else:
                    experience_match = (resume_years / required_years) * 100
            else:
                experience_match = 100  # No specific requirement
            
            return {
                'resume_years': resume_years,
                'required_years': required_years,
                'experience_match': round(experience_match, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze experience match: {e}")
            return {'error': str(e)}
    
    def _analyze_keyword_match(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Analyze keyword match between resume and job."""
        try:
            # Extract keywords from both texts
            resume_keywords = text_processor.extract_keywords(resume_text, top_n=20)
            job_keywords = text_processor.extract_keywords(job_text, top_n=20)
            
            # Find matching keywords
            resume_keyword_set = {kw[0].lower() for kw in resume_keywords}
            job_keyword_set = {kw[0].lower() for kw in job_keywords}
            
            matching_keywords = resume_keyword_set.intersection(job_keyword_set)
            missing_keywords = job_keyword_set - resume_keyword_set
            
            # Calculate match percentage
            if job_keyword_set:
                keyword_match = (len(matching_keywords) / len(job_keyword_set)) * 100
            else:
                keyword_match = 0
            
            return {
                'matching_keywords': list(matching_keywords),
                'missing_keywords': list(missing_keywords),
                'keyword_match': round(keyword_match, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze keyword match: {e}")
            return {'error': str(e)}
    
    def _calculate_job_match_score(self, skills_match: Dict, experience_match: Dict, keyword_match: Dict) -> float:
        """Calculate overall job match score."""
        try:
            scores = []
            
            if 'match_percentage' in skills_match:
                scores.append(skills_match['match_percentage'])
            
            if 'experience_match' in experience_match:
                scores.append(experience_match['experience_match'])
            
            if 'keyword_match' in keyword_match:
                scores.append(keyword_match['keyword_match'])
            
            if scores:
                return round(sum(scores) / len(scores), 1)
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Failed to calculate job match score: {e}")
            return 0.0
    
    def _generate_job_match_recommendations(self, skills_match: Dict, experience_match: Dict, keyword_match: Dict) -> List[str]:
        """Generate job match recommendations."""
        recommendations = []
        
        # Skills recommendations
        if skills_match.get('missing_skills'):
            recommendations.append(f"Consider adding these skills: {', '.join(skills_match['missing_skills'][:5])}")
        
        # Experience recommendations
        if experience_match.get('experience_match', 0) < 80:
            recommendations.append("Highlight relevant experience and projects")
        
        # Keyword recommendations
        if keyword_match.get('missing_keywords'):
            recommendations.append(f"Include these keywords: {', '.join(keyword_match['missing_keywords'][:5])}")
        
        return recommendations
    
    def get_analysis_service_info(self) -> Dict[str, Any]:
        """
        Get analysis service information and statistics.
        
        Returns:
            Dict[str, Any]: Analysis service information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "skills_categories": len(self._skills_database),
                "cached_analyses": len(self._analysis_cache),
                "analysis_service_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get analysis service info: {e}")
            return {
                "error": str(e),
                "analysis_service_timestamp": datetime.now().isoformat()
            }
