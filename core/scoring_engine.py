"""
Scoring Engine Module for Resume/CV AI Application
Handles comprehensive scoring and evaluation algorithms.

This module provides:
- Resume scoring algorithms and metrics
- ATS compatibility scoring
- Job matching score calculations
- Skills gap analysis scoring
- Overall resume quality assessment
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import math
from collections import Counter

from models.resume_model import ParsedResume, Skill, SkillCategory
from models.job_model import JobDescription
from models.analysis_model import AnalysisResult, ATSResult, ScoringMetrics
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("scoring_engine")

class ScoringEngine:
    """
    Advanced scoring engine for resume evaluation with comprehensive logging.
    
    This class provides sophisticated scoring algorithms for resume analysis,
    ATS compatibility, job matching, and overall quality assessment.
    
    Key Features:
    - Resume scoring algorithms and metrics
    - ATS compatibility scoring
    - Job matching score calculations
    - Skills gap analysis scoring
    - Overall resume quality assessment
    - Comprehensive logging and error handling
    
    Attributes:
        scoring_weights (Dict): Weights for different scoring categories
        ats_keywords (List): ATS-friendly keywords for scoring
        industry_standards (Dict): Industry-specific scoring standards
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize the ScoringEngine with comprehensive logging.
        
        Raises:
            Exception: If ScoringEngine initialization fails
        """
        logger.info("Initializing ScoringEngine")
        self._initialization_time = time.time()
        
        # Initialize scoring weights and standards
        self.scoring_weights = {}
        self.ats_keywords = []
        self.industry_standards = {}
        
        try:
            # Load scoring configuration
            logger.debug("Loading scoring configuration")
            self._load_scoring_configuration()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ScoringEngine initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.scoring_weights)} scoring categories")
            logger.info(f"Loaded {len(self.ats_keywords)} ATS keywords")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ScoringEngine initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Scoring may not function correctly")
            raise
    
    def _load_scoring_configuration(self):
        """Load scoring configuration and standards."""
        # Default scoring weights
        self.scoring_weights = {
            "content_quality": 0.25,
            "ats_compatibility": 0.20,
            "skills_relevance": 0.20,
            "experience_quality": 0.15,
            "education_relevance": 0.10,
            "format_structure": 0.10
        }
        
        # ATS keywords for scoring
        self.ats_keywords = [
            "achieved", "developed", "implemented", "managed", "led", "created",
            "improved", "increased", "reduced", "optimized", "delivered", "executed",
            "coordinated", "supervised", "analyzed", "designed", "built", "launched",
            "established", "generated", "enhanced", "streamlined", "automated"
        ]
        
        # Industry-specific scoring standards
        self.industry_standards = {
            "technology": {
                "min_skills": 8,
                "preferred_certifications": ["AWS", "Azure", "Google Cloud", "PMP", "Scrum Master"],
                "key_technologies": ["Python", "Java", "JavaScript", "SQL", "Docker", "Kubernetes"],
                "experience_weight": 0.3
            },
            "finance": {
                "min_skills": 6,
                "preferred_certifications": ["CFA", "CPA", "FRM", "CISA"],
                "key_technologies": ["Excel", "SQL", "Python", "R", "Tableau", "Power BI"],
                "experience_weight": 0.4
            },
            "healthcare": {
                "min_skills": 5,
                "preferred_certifications": ["RN", "MD", "PharmD", "CNA"],
                "key_technologies": ["EMR", "Epic", "Cerner", "HIPAA"],
                "experience_weight": 0.35
            },
            "marketing": {
                "min_skills": 7,
                "preferred_certifications": ["Google Analytics", "HubSpot", "Facebook Blueprint"],
                "key_technologies": ["Google Analytics", "Facebook Ads", "SEO", "SEM", "Email Marketing"],
                "experience_weight": 0.25
            }
        }
    
    def score_resume(self, resume: ParsedResume, job_description: JobDescription = None, industry: str = None) -> AnalysisResult:
        """
        Calculate comprehensive resume score with detailed analysis.
        
        Args:
            resume (ParsedResume): Resume to score
            job_description (JobDescription): Job description for matching (optional)
            industry (str): Target industry for scoring (optional)
            
        Returns:
            AnalysisResult: Comprehensive scoring results
            
        Raises:
            Exception: If resume scoring fails
        """
        try:
            logger.debug("Calculating comprehensive resume score")
            start_time = time.time()
            
            # Calculate individual scores
            content_score = self._score_content_quality(resume)
            ats_score = self._score_ats_compatibility(resume)
            skills_score = self._score_skills_relevance(resume, job_description, industry)
            experience_score = self._score_experience_quality(resume)
            education_score = self._score_education_relevance(resume, industry)
            format_score = self._score_format_structure(resume)
            
            # Calculate weighted overall score
            overall_score = (
                content_score * self.scoring_weights["content_quality"] +
                ats_score * self.scoring_weights["ats_compatibility"] +
                skills_score * self.scoring_weights["skills_relevance"] +
                experience_score * self.scoring_weights["experience_quality"] +
                education_score * self.scoring_weights["education_relevance"] +
                format_score * self.scoring_weights["format_structure"]
            )
            
            # Generate analysis insights
            strengths = self._identify_strengths(resume, content_score, ats_score, skills_score, experience_score)
            weaknesses = self._identify_weaknesses(resume, content_score, ats_score, skills_score, experience_score)
            recommendations = self._generate_recommendations(resume, overall_score, weaknesses)
            
            # Create scoring metrics
            scoring_metrics = ScoringMetrics(
                content_quality=content_score,
                ats_compatibility=ats_score,
                skills_relevance=skills_score,
                experience_quality=experience_score,
                education_relevance=education_score,
                format_structure=format_score,
                overall_score=overall_score
            )
            
            # Create analysis result
            analysis_result = AnalysisResult(
                overall_score=overall_score,
                confidence=min(0.95, overall_score / 100),
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations,
                scoring_metrics=scoring_metrics,
                analysis_timestamp=datetime.now().isoformat()
            )
            
            scoring_time = time.time() - start_time
            logger.info(f"Resume scoring completed in {scoring_time:.2f}s")
            logger.info(f"Overall score: {overall_score:.1f}/100")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Failed to score resume: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return AnalysisResult(
                overall_score=0,
                confidence=0,
                strengths=[],
                weaknesses=["Scoring failed due to technical error"],
                recommendations=["Please try again or contact support"],
                scoring_metrics=ScoringMetrics(),
                analysis_timestamp=datetime.now().isoformat()
            )
    
    def _score_content_quality(self, resume: ParsedResume) -> float:
        """Score content quality and writing effectiveness."""
        try:
            score = 0
            max_score = 100
            
            # Check for professional summary
            if resume.summary and len(resume.summary.strip()) > 50:
                score += 15
                # Check for quantifiable results in summary
                if re.search(r'\d+%|\$\d+|\d+x|\d+ years', resume.summary):
                    score += 10
            
            # Check work experience quality
            if resume.work_experience:
                score += 20
                
                # Check for action verbs in experience
                action_verbs_count = 0
                for exp in resume.work_experience:
                    if exp.description:
                        action_verbs_count += sum(1 for verb in self.ats_keywords if verb in exp.description.lower())
                
                if action_verbs_count > 0:
                    score += min(15, action_verbs_count * 2)
                
                # Check for quantifiable achievements
                quantifiable_count = 0
                for exp in resume.work_experience:
                    if exp.description:
                        quantifiable_count += len(re.findall(r'\d+%|\$\d+|\d+x|\d+ years|\d+ people', exp.description))
                
                if quantifiable_count > 0:
                    score += min(20, quantifiable_count * 3)
            
            # Check skills section
            if resume.skills and len(resume.skills) >= 5:
                score += 15
                if len(resume.skills) >= 10:
                    score += 10
            
            # Check education
            if resume.education:
                score += 10
            
            # Check for contact information completeness
            contact_score = 0
            if resume.contact_info.name:
                contact_score += 5
            if resume.contact_info.email:
                contact_score += 5
            if resume.contact_info.phone:
                contact_score += 5
            if resume.contact_info.location:
                contact_score += 5
            
            score += contact_score
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score content quality: {e}")
            return 50.0
    
    def _score_ats_compatibility(self, resume: ParsedResume) -> float:
        """Score ATS compatibility."""
        try:
            score = 0
            max_score = 100
            
            # Check for ATS-friendly formatting
            resume_text = self._get_resume_text(resume)
            
            # Check for action verbs
            action_verbs_found = sum(1 for verb in self.ats_keywords if verb in resume_text.lower())
            score += min(30, action_verbs_found * 3)
            
            # Check for quantifiable results
            quantifiable_results = len(re.findall(r'\d+%|\$\d+|\d+x|\d+ years|\d+ people|\d+ projects', resume_text))
            score += min(25, quantifiable_results * 4)
            
            # Check for professional keywords
            professional_keywords = ["experience", "skills", "education", "achievement", "leadership", "management"]
            professional_found = sum(1 for keyword in professional_keywords if keyword in resume_text.lower())
            score += min(20, professional_found * 3)
            
            # Check for proper section structure
            sections = ["experience", "education", "skills", "summary"]
            sections_found = sum(1 for section in sections if section in resume_text.lower())
            score += min(15, sections_found * 3)
            
            # Check for consistent formatting (bullet points, dates, etc.)
            bullet_points = resume_text.count('•') + resume_text.count('-') + resume_text.count('*')
            if bullet_points >= 5:
                score += 10
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score ATS compatibility: {e}")
            return 50.0
    
    def _score_skills_relevance(self, resume: ParsedResume, job_description: JobDescription = None, industry: str = None) -> float:
        """Score skills relevance and completeness."""
        try:
            score = 0
            max_score = 100
            
            if not resume.skills:
                return 0
            
            # Base score for having skills
            score += 20
            
            # Score based on number of skills
            skills_count = len(resume.skills)
            if skills_count >= 5:
                score += 20
            if skills_count >= 10:
                score += 10
            if skills_count >= 15:
                score += 10
            
            # Score technical vs soft skills balance
            technical_skills = [s for s in resume.skills if s.category == SkillCategory.TECHNICAL]
            soft_skills = [s for s in resume.skills if s.category == SkillCategory.SOFT]
            
            if technical_skills and soft_skills:
                score += 15  # Good balance
            elif technical_skills:
                score += 10  # Technical focus
            elif soft_skills:
                score += 5   # Soft skills only
            
            # Industry-specific scoring
            if industry and industry.lower() in self.industry_standards:
                industry_standards = self.industry_standards[industry.lower()]
                
                # Check for industry-specific technologies
                industry_techs = industry_standards.get("key_technologies", [])
                industry_techs_found = sum(1 for tech in industry_techs 
                                         for skill in resume.skills 
                                         if tech.lower() in skill.name.lower())
                
                if industry_techs_found > 0:
                    score += min(20, industry_techs_found * 4)
                
                # Check minimum skills requirement
                if skills_count >= industry_standards.get("min_skills", 5):
                    score += 10
            
            # Job-specific scoring
            if job_description and job_description.required_skills:
                job_skills = [skill.lower() for skill in job_description.required_skills]
                resume_skill_names = [skill.name.lower() for skill in resume.skills]
                
                matching_skills = sum(1 for job_skill in job_skills 
                                    for resume_skill in resume_skill_names 
                                    if job_skill in resume_skill or resume_skill in job_skill)
                
                if matching_skills > 0:
                    match_percentage = (matching_skills / len(job_skills)) * 100
                    score += min(25, match_percentage * 0.25)
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score skills relevance: {e}")
            return 50.0
    
    def _score_experience_quality(self, resume: ParsedResume) -> float:
        """Score work experience quality and relevance."""
        try:
            score = 0
            max_score = 100
            
            if not resume.work_experience:
                return 0
            
            # Base score for having experience
            score += 20
            
            # Score based on number of experiences
            exp_count = len(resume.work_experience)
            if exp_count >= 2:
                score += 15
            if exp_count >= 3:
                score += 10
            
            # Score experience descriptions
            for exp in resume.work_experience:
                if exp.description:
                    # Check for action verbs
                    action_verbs = sum(1 for verb in self.ats_keywords if verb in exp.description.lower())
                    score += min(10, action_verbs * 2)
                    
                    # Check for quantifiable results
                    quantifiable = len(re.findall(r'\d+%|\$\d+|\d+x|\d+ years|\d+ people', exp.description))
                    score += min(15, quantifiable * 3)
                    
                    # Check description length (not too short, not too long)
                    word_count = len(exp.description.split())
                    if 20 <= word_count <= 100:
                        score += 5
                    elif 10 <= word_count < 20:
                        score += 3
            
            # Score for career progression (if multiple experiences)
            if exp_count >= 2:
                # Simple check for title progression (this could be more sophisticated)
                titles = [exp.title.lower() for exp in resume.work_experience if exp.title]
                if len(set(titles)) > 1:  # Different titles suggest progression
                    score += 10
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score experience quality: {e}")
            return 50.0
    
    def _score_education_relevance(self, resume: ParsedResume, industry: str = None) -> float:
        """Score education relevance and completeness."""
        try:
            score = 0
            max_score = 100
            
            if not resume.education:
                return 0
            
            # Base score for having education
            score += 30
            
            # Score based on degree level
            degree_levels = {
                "phd": 25, "doctorate": 25, "master": 20, "mba": 20, "bachelor": 15,
                "associate": 10, "certificate": 5, "diploma": 5
            }
            
            for edu in resume.education:
                if edu.degree:
                    degree_lower = edu.degree.lower()
                    for level, points in degree_levels.items():
                        if level in degree_lower:
                            score += points
                            break
            
            # Score for relevant fields
            if industry and industry.lower() in self.industry_standards:
                industry_standards = self.industry_standards[industry.lower()]
                # This could be expanded to check for relevant fields of study
                score += 10
            
            # Score for multiple degrees/certifications
            if len(resume.education) > 1:
                score += 10
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score education relevance: {e}")
            return 50.0
    
    def _score_format_structure(self, resume: ParsedResume) -> float:
        """Score resume format and structure."""
        try:
            score = 0
            max_score = 100
            
            resume_text = self._get_resume_text(resume)
            
            # Check for proper section headers
            sections = ["experience", "education", "skills", "summary", "contact"]
            sections_found = sum(1 for section in sections if section in resume_text.lower())
            score += min(30, sections_found * 6)
            
            # Check for consistent formatting
            bullet_points = resume_text.count('•') + resume_text.count('-') + resume_text.count('*')
            if bullet_points >= 5:
                score += 20
            
            # Check for dates in experience
            date_patterns = [r'\d{4}', r'\d{1,2}/\d{4}', r'\d{4}-\d{4}']
            dates_found = sum(1 for pattern in date_patterns if re.search(pattern, resume_text))
            if dates_found > 0:
                score += 15
            
            # Check for contact information formatting
            if resume.contact_info.email and '@' in resume.contact_info.email:
                score += 10
            if resume.contact_info.phone and re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', resume.contact_info.phone):
                score += 10
            
            # Check for professional email domain
            if resume.contact_info.email and not any(domain in resume.contact_info.email.lower() 
                                                   for domain in ['gmail.com', 'yahoo.com', 'hotmail.com']):
                score += 15
            
            return min(max_score, score)
            
        except Exception as e:
            logger.warning(f"Failed to score format structure: {e}")
            return 50.0
    
    def _get_resume_text(self, resume: ParsedResume) -> str:
        """Get combined text from resume for analysis."""
        text_parts = []
        
        if resume.summary:
            text_parts.append(resume.summary)
        
        for exp in resume.work_experience:
            if exp.description:
                text_parts.append(exp.description)
        
        for edu in resume.education:
            if edu.degree:
                text_parts.append(edu.degree)
            if edu.field:
                text_parts.append(edu.field)
        
        for skill in resume.skills:
            text_parts.append(skill.name)
        
        return " ".join(text_parts)
    
    def _identify_strengths(self, resume: ParsedResume, content_score: float, ats_score: float, 
                           skills_score: float, experience_score: float) -> List[str]:
        """Identify resume strengths based on scores."""
        strengths = []
        
        if content_score >= 80:
            strengths.append("Strong content quality with clear, professional writing")
        
        if ats_score >= 80:
            strengths.append("Excellent ATS compatibility with proper formatting and keywords")
        
        if skills_score >= 80:
            strengths.append("Comprehensive and relevant skills section")
        
        if experience_score >= 80:
            strengths.append("Strong work experience with quantifiable achievements")
        
        if resume.skills and len(resume.skills) >= 10:
            strengths.append("Extensive skills portfolio")
        
        if resume.work_experience and len(resume.work_experience) >= 3:
            strengths.append("Diverse work experience")
        
        # Check for specific strengths
        resume_text = self._get_resume_text(resume)
        if re.search(r'\d+%|\$\d+|\d+x', resume_text):
            strengths.append("Includes quantifiable achievements and metrics")
        
        action_verbs_found = sum(1 for verb in self.ats_keywords if verb in resume_text.lower())
        if action_verbs_found >= 5:
            strengths.append("Uses strong action verbs effectively")
        
        return strengths
    
    def _identify_weaknesses(self, resume: ParsedResume, content_score: float, ats_score: float, 
                            skills_score: float, experience_score: float) -> List[str]:
        """Identify resume weaknesses based on scores."""
        weaknesses = []
        
        if content_score < 60:
            weaknesses.append("Content quality needs improvement - add more specific details and achievements")
        
        if ats_score < 60:
            weaknesses.append("ATS compatibility issues - improve formatting and keyword usage")
        
        if skills_score < 60:
            weaknesses.append("Skills section needs enhancement - add more relevant skills")
        
        if experience_score < 60:
            weaknesses.append("Work experience descriptions need more detail and quantifiable results")
        
        if not resume.summary or len(resume.summary.strip()) < 50:
            weaknesses.append("Add a compelling professional summary")
        
        if not resume.skills or len(resume.skills) < 5:
            weaknesses.append("Expand skills section with relevant technical and soft skills")
        
        if not resume.work_experience:
            weaknesses.append("Add work experience or relevant projects")
        
        # Check for specific weaknesses
        resume_text = self._get_resume_text(resume)
        if not re.search(r'\d+%|\$\d+|\d+x', resume_text):
            weaknesses.append("Add quantifiable achievements and metrics")
        
        action_verbs_found = sum(1 for verb in self.ats_keywords if verb in resume_text.lower())
        if action_verbs_found < 3:
            weaknesses.append("Use more action verbs to strengthen descriptions")
        
        return weaknesses
    
    def _generate_recommendations(self, resume: ParsedResume, overall_score: float, weaknesses: List[str]) -> List[str]:
        """Generate improvement recommendations based on analysis."""
        recommendations = []
        
        # General recommendations based on overall score
        if overall_score < 60:
            recommendations.append("Focus on improving overall resume quality and content")
        elif overall_score < 80:
            recommendations.append("Make targeted improvements to reach excellent quality")
        
        # Specific recommendations based on weaknesses
        for weakness in weaknesses:
            if "content quality" in weakness.lower():
                recommendations.append("Enhance content with specific achievements and quantifiable results")
            elif "ats compatibility" in weakness.lower():
                recommendations.append("Improve ATS compatibility with better formatting and keywords")
            elif "skills section" in weakness.lower():
                recommendations.append("Expand skills section with industry-relevant technical and soft skills")
            elif "work experience" in weakness.lower():
                recommendations.append("Add detailed descriptions with action verbs and measurable outcomes")
            elif "professional summary" in weakness.lower():
                recommendations.append("Write a compelling 2-3 sentence professional summary")
            elif "quantifiable achievements" in weakness.lower():
                recommendations.append("Add numbers, percentages, and metrics to demonstrate impact")
            elif "action verbs" in weakness.lower():
                recommendations.append("Start bullet points with strong action verbs like 'achieved', 'developed', 'implemented'")
        
        # Additional recommendations
        if not recommendations:
            recommendations.append("Continue maintaining high-quality content and formatting")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def calculate_job_match_score(self, resume: ParsedResume, job_description: JobDescription) -> Dict[str, Any]:
        """
        Calculate job matching score between resume and job description.
        
        Args:
            resume (ParsedResume): Resume to match
            job_description (JobDescription): Job description to match against
            
        Returns:
            Dict[str, Any]: Job matching analysis results
        """
        try:
            logger.debug("Calculating job match score")
            start_time = time.time()
            
            # Extract skills from both
            resume_skills = [skill.name.lower() for skill in resume.skills] if resume.skills else []
            job_skills = job_description.required_skills or []
            job_skills_lower = [skill.lower() for skill in job_skills]
            
            # Calculate skill match
            matching_skills = [skill for skill in resume_skills if any(js in skill or skill in js for js in job_skills_lower)]
            skill_match_percentage = (len(matching_skills) / len(job_skills_lower)) * 100 if job_skills_lower else 0
            
            # Calculate experience match
            experience_match = 0
            if resume.work_experience and job_description.required_experience:
                # Simple experience matching (could be more sophisticated)
                resume_years = len(resume.work_experience) * 2  # Approximate years
                required_years = job_description.required_experience
                if resume_years >= required_years:
                    experience_match = 100
                else:
                    experience_match = (resume_years / required_years) * 100
            
            # Calculate education match
            education_match = 0
            if resume.education and job_description.required_education:
                # Simple education matching
                resume_degrees = [edu.degree.lower() for edu in resume.education if edu.degree]
                required_education = job_description.required_education.lower()
                
                if any(degree in required_education or required_education in degree for degree in resume_degrees):
                    education_match = 100
                else:
                    education_match = 50  # Partial match
            
            # Calculate overall match score
            overall_match = (
                skill_match_percentage * 0.5 +
                experience_match * 0.3 +
                education_match * 0.2
            )
            
            # Generate recommendations
            recommendations = []
            if skill_match_percentage < 70:
                missing_skills = [skill for skill in job_skills_lower if not any(rs in skill or skill in rs for rs in resume_skills)]
                recommendations.append(f"Add missing skills: {', '.join(missing_skills[:5])}")
            
            if experience_match < 80:
                recommendations.append("Gain more relevant work experience")
            
            if education_match < 80:
                recommendations.append("Consider additional education or certifications")
            
            analysis_time = time.time() - start_time
            logger.info(f"Job match score calculated in {analysis_time:.2f}s")
            logger.info(f"Overall match: {overall_match:.1f}%")
            
            return {
                "overall_match": round(overall_match, 1),
                "skill_match": round(skill_match_percentage, 1),
                "experience_match": round(experience_match, 1),
                "education_match": round(education_match, 1),
                "matching_skills": matching_skills,
                "missing_skills": [skill for skill in job_skills_lower if not any(rs in skill or skill in rs for rs in resume_skills)],
                "recommendations": recommendations,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate job match score: {e}")
            return {
                "overall_match": 0,
                "skill_match": 0,
                "experience_match": 0,
                "education_match": 0,
                "matching_skills": [],
                "missing_skills": [],
                "recommendations": ["Unable to calculate match score"],
                "analysis_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
