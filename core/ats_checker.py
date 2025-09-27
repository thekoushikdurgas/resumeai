"""
ATS Checker Module for Resume/CV AI Application
Handles Applicant Tracking System compatibility checking.

This module provides:
- ATS compatibility scoring and analysis
- Format validation and optimization recommendations
- Keyword optimization and density analysis
- Structure and content quality assessment
- Industry-specific ATS requirements checking
- Comprehensive compatibility reporting

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from models.resume_model import ParsedResume
from models.analysis_model import ATSResult
from utils.helpers import clean_text, calculate_word_count
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("ats_checker")

class ATSChecker:
    """
    ATS compatibility checker for resumes with comprehensive logging.
    
    This class provides advanced ATS compatibility analysis including:
    - Format validation and optimization recommendations
    - Keyword optimization and density analysis
    - Structure and content quality assessment
    - Industry-specific ATS requirements checking
    - Comprehensive compatibility scoring and reporting
    
    Attributes:
        ai_handler: AI handler instance for content analysis
        ats_keywords: Dictionary of ATS-relevant keywords by category
        format_issues: List of common ATS format problems
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, ai_handler):
        """
        Initialize ATS checker with comprehensive logging.
        
        Sets up the checker with AI handler dependency, loads ATS databases,
        and logs initialization details for debugging and monitoring.
        
        Args:
            ai_handler: AI handler instance for content analysis
            
        Raises:
            Exception: If initialization fails due to missing dependencies
        """
        logger.info("Initializing ATSChecker")
        self._initialization_time = time.time()
        
        try:
            # Validate dependencies
            if not ai_handler:
                raise ValueError("AIHandler instance is required")
            
            self.ai_handler = ai_handler
            logger.info("Dependencies validated successfully")
            
            # Load ATS databases
            logger.debug("Loading ATS keywords database")
            self.ats_keywords = self._load_ats_keywords()
            logger.debug(f"Loaded {len(self.ats_keywords)} ATS keyword categories")
            
            logger.debug("Loading format issues database")
            self.format_issues = self._load_format_issues()
            logger.debug(f"Loaded {len(self.format_issues)} format issue patterns")
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ATSChecker initialized successfully in {initialization_time:.2f}s")
            logger.info(f"ATS keyword categories: {len(self.ats_keywords)}")
            logger.info(f"Format issue patterns: {len(self.format_issues)}")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ATSChecker initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def check_ats_compatibility(self, resume: ParsedResume) -> ATSResult:
        """
        Check ATS compatibility of resume with comprehensive logging.
        
        This method performs advanced ATS compatibility analysis including:
        - Format validation and scoring
        - Keyword optimization analysis
        - Structure and content quality assessment
        - Issue identification and categorization
        - Recommendation generation for improvement
        
        Args:
            resume (ParsedResume): Parsed resume object to analyze
            
        Returns:
            ATSResult: Comprehensive ATS compatibility analysis containing:
                - ats_score: Overall ATS compatibility score (0-100)
                - format_score: Format compatibility score
                - keyword_score: Keyword optimization score
                - structure_score: Structure quality score
                - content_score: Content quality score
                - compatibility_issues: List of compatibility problems
                - recommendations: Improvement suggestions
        """
        start_time = time.time()
        
        try:
            logger.info("Starting ATS compatibility check")
            logger.debug(f"Resume name: {resume.contact_info.name or 'Unknown'}")
            logger.debug(f"Resume text length: {len(resume.raw_text) if resume.raw_text else 0} characters")
            
            # Calculate various ATS scores
            logger.debug("Checking format compatibility")
            format_score = self._check_format_compatibility(resume)
            logger.debug(f"Format score: {format_score:.1f}%")
            
            logger.debug("Checking keyword optimization")
            keyword_score = self._check_keyword_optimization(resume)
            logger.debug(f"Keyword score: {keyword_score:.1f}%")
            
            logger.debug("Checking structure compatibility")
            structure_score = self._check_structure_compatibility(resume)
            logger.debug(f"Structure score: {structure_score:.1f}%")
            
            logger.debug("Checking content quality")
            content_score = self._check_content_quality(resume)
            logger.debug(f"Content score: {content_score:.1f}%")
            
            # Calculate overall ATS score
            ats_score = (format_score + keyword_score + structure_score + content_score) / 4
            logger.info(f"Overall ATS score: {ats_score:.1f}%")
            
            # Identify issues
            logger.debug("Identifying compatibility issues")
            compatibility_issues = self._identify_compatibility_issues(resume)
            logger.info(f"Compatibility issues found: {len(compatibility_issues)}")
            
            logger.debug("Identifying format issues")
            format_issues = self._identify_format_issues(resume)
            logger.info(f"Format issues found: {len(format_issues)}")
            
            logger.debug("Identifying structure issues")
            structure_issues = self._identify_structure_issues(resume)
            logger.info(f"Structure issues found: {len(structure_issues)}")
            
            # Find keyword matches and missing keywords
            logger.debug("Analyzing keywords")
            keyword_matches, missing_keywords = self._analyze_keywords(resume)
            logger.info(f"Keyword matches: {len(keyword_matches)}, Missing keywords: {len(missing_keywords)}")
            
            # Generate recommendations
            logger.debug("Generating ATS recommendations")
            recommendations = self._generate_ats_recommendations(
                resume, compatibility_issues, format_issues, structure_issues, missing_keywords
            )
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            checking_time = time.time() - start_time
            logger.info(f"ATS compatibility check completed in {checking_time:.2f}s")
            logger.info(f"Final ATS score: {ats_score:.1f}%")
            
            return ATSResult(
                ats_score=ats_score,
                format_score=format_score,
                keyword_score=keyword_score,
                structure_score=structure_score,
                content_score=content_score,
                compatibility_issues=compatibility_issues,
                keyword_matches=keyword_matches,
                missing_keywords=missing_keywords,
                format_issues=format_issues,
                structure_issues=structure_issues,
                recommendations=recommendations
            )
            
        except Exception as e:
            checking_time = time.time() - start_time
            logger.error(f"ATS compatibility check failed after {checking_time:.2f}s: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Resume name: {resume.contact_info.name or 'Unknown'}")
            
            return ATSResult(
                ats_score=0.0,
                format_score=0.0,
                keyword_score=0.0,
                structure_score=0.0,
                content_score=0.0,
                compatibility_issues=[f"ATS check failed: {str(e)}"],
                recommendations=[],
                processing_time=checking_time
            )
    
    def _check_format_compatibility(self, resume: ParsedResume) -> float:
        """Check format compatibility with ATS systems."""
        score = 100.0
        issues = []
        
        # Check for common format issues
        if resume.raw_text:
            text = resume.raw_text.lower()
            
            # Check for tables (can cause parsing issues)
            if '|' in text and text.count('|') > 10:
                score -= 20
                issues.append("Excessive use of tables may cause parsing issues")
            
            # Check for headers/footers
            if any(header in text for header in ['page', 'header', 'footer']):
                score -= 15
                issues.append("Headers/footers may not be parsed correctly")
            
            # Check for graphics/images
            if any(graphic in text for graphic in ['image', 'graphic', 'logo', 'photo']):
                score -= 25
                issues.append("Images and graphics are not parsed by ATS")
            
            # Check for complex formatting
            if any(format_char in text for format_char in ['•', '◦', '▪', '▫']):
                score -= 10
                issues.append("Complex bullet points may not be parsed correctly")
        
        return max(0, score)
    
    def _check_keyword_optimization(self, resume: ParsedResume) -> float:
        """Check keyword optimization for ATS."""
        if not resume.raw_text:
            return 0.0
        
        text = resume.raw_text.lower()
        score = 0.0
        
        # Count keyword matches
        keyword_matches = 0
        total_keywords = len(self.ats_keywords)
        
        for keyword in self.ats_keywords:
            if keyword.lower() in text:
                keyword_matches += 1
        
        if total_keywords > 0:
            score = (keyword_matches / total_keywords) * 100
        
        return min(100, score)
    
    def _check_structure_compatibility(self, resume: ParsedResume) -> float:
        """Check resume structure compatibility."""
        score = 100.0
        issues = []
        
        # Check for required sections
        required_sections = ['contact', 'experience', 'education', 'skills']
        present_sections = 0
        
        if resume.contact_info.name:
            present_sections += 1
        if resume.work_experience:
            present_sections += 1
        if resume.education:
            present_sections += 1
        if resume.skills:
            present_sections += 1
        
        if present_sections < len(required_sections):
            score -= (len(required_sections) - present_sections) * 15
            issues.append(f"Missing {len(required_sections) - present_sections} required sections")
        
        # Check for proper section headers
        if resume.raw_text:
            text = resume.raw_text.upper()
            section_headers = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'SUMMARY']
            found_headers = sum(1 for header in section_headers if header in text)
            
            if found_headers < 2:
                score -= 20
                issues.append("Missing clear section headers")
        
        return max(0, score)
    
    def _check_content_quality(self, resume: ParsedResume) -> float:
        """Check content quality for ATS."""
        score = 100.0
        issues = []
        
        # Check word count
        if resume.raw_text:
            word_count = calculate_word_count(resume.raw_text)
            
            if word_count < 200:
                score -= 30
                issues.append("Resume too short - may lack detail")
            elif word_count > 1000:
                score -= 20
                issues.append("Resume too long - may not be fully parsed")
        
        # Check for action verbs
        if resume.raw_text:
            action_verbs = [
                'achieved', 'developed', 'implemented', 'managed', 'created',
                'improved', 'increased', 'reduced', 'led', 'designed'
            ]
            
            text_lower = resume.raw_text.lower()
            action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
            
            if action_verb_count < 3:
                score -= 15
                issues.append("Limited use of action verbs")
        
        # Check for quantified achievements
        if resume.raw_text:
            # Look for numbers and percentages
            numbers = re.findall(r'\d+%|\d+\+|\d+[km]?', resume.raw_text)
            
            if len(numbers) < 2:
                score -= 20
                issues.append("Limited quantified achievements")
        
        return max(0, score)
    
    def _identify_compatibility_issues(self, resume: ParsedResume) -> List[str]:
        """Identify general compatibility issues."""
        issues = []
        
        if not resume.raw_text:
            issues.append("No resume text available for analysis")
            return issues
        
        text = resume.raw_text.lower()
        
        # Check for problematic elements
        if any(element in text for element in ['table', 'column', 'row']):
            issues.append("Tables may not be parsed correctly by ATS")
        
        if any(element in text for element in ['image', 'photo', 'logo', 'graphic']):
            issues.append("Images and graphics are not processed by ATS")
        
        if any(element in text for element in ['header', 'footer', 'page']):
            issues.append("Headers and footers may not be parsed")
        
        # Check for missing contact information
        if not resume.contact_info.email:
            issues.append("Missing email address")
        
        if not resume.contact_info.phone:
            issues.append("Missing phone number")
        
        # Check for file format issues
        if any(char in resume.raw_text for char in ['\t', '\r']):
            issues.append("Contains special characters that may cause parsing issues")
        
        return issues
    
    def _identify_format_issues(self, resume: ParsedResume) -> List[str]:
        """Identify format-specific issues."""
        issues = []
        
        if not resume.raw_text:
            return issues
        
        text = resume.raw_text
        
        # Check for excessive formatting
        if text.count('\n') > 100:
            issues.append("Excessive line breaks may cause parsing issues")
        
        if text.count(' ') > text.count('\n') * 10:
            issues.append("Very long lines may not be parsed correctly")
        
        # Check for special characters
        special_chars = ['•', '◦', '▪', '▫', '→', '←', '↑', '↓']
        for char in special_chars:
            if char in text:
                issues.append(f"Special character '{char}' may not be parsed correctly")
        
        return issues
    
    def _identify_structure_issues(self, resume: ParsedResume) -> List[str]:
        """Identify structure-specific issues."""
        issues = []
        
        # Check for missing sections
        if not resume.work_experience:
            issues.append("Missing work experience section")
        
        if not resume.education:
            issues.append("Missing education section")
        
        if not resume.skills:
            issues.append("Missing skills section")
        
        # Check for empty sections
        if resume.work_experience:
            empty_experiences = [exp for exp in resume.work_experience 
                               if not exp.title and not exp.company]
            if empty_experiences:
                issues.append("Some work experience entries are incomplete")
        
        if resume.education:
            empty_education = [edu for edu in resume.education 
                             if not edu.degree and not edu.institution]
            if empty_education:
                issues.append("Some education entries are incomplete")
        
        return issues
    
    def _analyze_keywords(self, resume: ParsedResume) -> tuple:
        """Analyze keyword matches and missing keywords."""
        if not resume.raw_text:
            return [], []
        
        text = resume.raw_text.lower()
        matched_keywords = []
        missing_keywords = []
        
        for keyword in self.ats_keywords:
            if keyword.lower() in text:
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        return matched_keywords, missing_keywords
    
    def _generate_ats_recommendations(self, resume: ParsedResume, compatibility_issues: List[str],
                                    format_issues: List[str], structure_issues: List[str],
                                    missing_keywords: List[str]) -> List[str]:
        """Generate ATS improvement recommendations."""
        recommendations = []
        
        # General recommendations
        if compatibility_issues:
            recommendations.append("Address compatibility issues to improve ATS parsing")
        
        # Format recommendations
        if format_issues:
            recommendations.append("Simplify formatting to ensure ATS compatibility")
            recommendations.append("Use standard bullet points and avoid special characters")
        
        # Structure recommendations
        if structure_issues:
            recommendations.append("Ensure all required sections are present and complete")
            recommendations.append("Use clear section headers (EXPERIENCE, EDUCATION, SKILLS)")
        
        # Keyword recommendations
        if missing_keywords:
            top_missing = missing_keywords[:5]
            recommendations.append(f"Consider including these relevant keywords: {', '.join(top_missing)}")
        
        # Content recommendations
        if resume.raw_text:
            word_count = calculate_word_count(resume.raw_text)
            if word_count < 300:
                recommendations.append("Add more detail to strengthen your resume")
            elif word_count > 800:
                recommendations.append("Consider condensing content to ensure full ATS parsing")
        
        # Contact information recommendations
        if not resume.contact_info.email:
            recommendations.append("Add a professional email address")
        
        if not resume.contact_info.phone:
            recommendations.append("Include a phone number for contact")
        
        return recommendations
    
    def _load_ats_keywords(self) -> List[str]:
        """Load ATS-relevant keywords."""
        return [
            # Technical Skills
            'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue', 'Node.js',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Azure', 'Docker',
            'Kubernetes', 'Git', 'Agile', 'Scrum', 'Machine Learning', 'AI',
            
            # Soft Skills
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Project Management', 'Time Management', 'Adaptability',
            
            # Industry Terms
            'Data Analysis', 'Software Development', 'Web Development',
            'Mobile Development', 'Cloud Computing', 'DevOps', 'Cybersecurity',
            'Database Administration', 'System Administration', 'Network Administration',
            
            # Certifications
            'AWS Certified', 'Microsoft Certified', 'Google Certified',
            'PMP', 'ITIL', 'CISSP', 'CompTIA',
            
            # Education
            'Bachelor', 'Master', 'PhD', 'MBA', 'Computer Science',
            'Information Technology', 'Engineering', 'Mathematics'
        ]
    
    def _load_format_issues(self) -> List[str]:
        """Load common format issues."""
        return [
            'Tables and columns',
            'Headers and footers',
            'Images and graphics',
            'Special characters',
            'Complex formatting',
            'Multiple columns',
            'Text boxes',
            'Watermarks'
        ]
