"""
Skills Extraction Module for Resume/CV AI Application
Handles identification, categorization, and analysis of skills from resume content.

This module provides:
- Skills identification from text content
- Technical and soft skills categorization
- Skills gap analysis and recommendations
- Industry-specific skills mapping
- Skills scoring and ranking
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime
import json
import os

from models.resume_model import Skill, SkillCategory
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("skills_extractor")

class SkillsExtractor:
    """
    Advanced skills extraction and analysis with comprehensive logging.
    
    This class provides sophisticated skills identification and categorization
    capabilities including technical skills, soft skills, certifications,
    and industry-specific skills mapping.
    
    Key Features:
    - Multi-source skills identification (resume text, job descriptions)
    - Technical and soft skills categorization
    - Skills gap analysis and recommendations
    - Industry-specific skills mapping
    - Skills scoring and ranking algorithms
    - Comprehensive logging and error handling
    
    Attributes:
        technical_skills_db (Dict): Database of technical skills by category
        soft_skills_db (Dict): Database of soft skills by category
        industry_skills_map (Dict): Industry-specific skills mapping
        skill_synonyms (Dict): Skills synonyms and variations
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, skills_data_path: str = "data/skills/"):
        """
        Initialize the SkillsExtractor with comprehensive logging.
        
        Args:
            skills_data_path (str): Path to skills database files
            
        Raises:
            Exception: If skills database initialization fails
        """
        logger.info("Initializing SkillsExtractor")
        self._initialization_time = time.time()
        
        # Initialize skills databases
        self.technical_skills_db = {}
        self.soft_skills_db = {}
        self.industry_skills_map = {}
        self.skill_synonyms = {}
        self.certifications_db = {}
        
        try:
            # Load skills databases
            logger.debug("Loading skills databases")
            self._load_skills_databases(skills_data_path)
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"SkillsExtractor initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.technical_skills_db)} technical skill categories")
            logger.info(f"Loaded {len(self.soft_skills_db)} soft skill categories")
            logger.info(f"Loaded {len(self.industry_skills_map)} industry mappings")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"SkillsExtractor initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Skills extraction may not function correctly")
            raise
    
    def _load_skills_databases(self, skills_data_path: str):
        """
        Load skills databases from JSON files with comprehensive logging.
        
        Args:
            skills_data_path (str): Path to skills database files
            
        Raises:
            Exception: If any skills database file fails to load
        """
        try:
            logger.debug(f"Loading skills databases from: {skills_data_path}")
            
            # Load technical skills
            technical_skills_file = os.path.join(skills_data_path, "technical_skills.json")
            if os.path.exists(technical_skills_file):
                with open(technical_skills_file, 'r', encoding='utf-8') as f:
                    self.technical_skills_db = json.load(f)
                logger.debug(f"Loaded technical skills: {len(self.technical_skills_db)} categories")
            else:
                logger.warning(f"Technical skills file not found: {technical_skills_file}")
                self.technical_skills_db = self._get_default_technical_skills()
            
            # Load soft skills
            soft_skills_file = os.path.join(skills_data_path, "soft_skills.json")
            if os.path.exists(soft_skills_file):
                with open(soft_skills_file, 'r', encoding='utf-8') as f:
                    self.soft_skills_db = json.load(f)
                logger.debug(f"Loaded soft skills: {len(self.soft_skills_db)} categories")
            else:
                logger.warning(f"Soft skills file not found: {soft_skills_file}")
                self.soft_skills_db = self._get_default_soft_skills()
            
            # Load industry skills mapping
            industry_skills_file = os.path.join(skills_data_path, "industry_keywords.json")
            if os.path.exists(industry_skills_file):
                with open(industry_skills_file, 'r', encoding='utf-8') as f:
                    self.industry_skills_map = json.load(f)
                logger.debug(f"Loaded industry skills: {len(self.industry_skills_map)} industries")
            else:
                logger.warning(f"Industry skills file not found: {industry_skills_file}")
                self.industry_skills_map = self._get_default_industry_skills()
            
            # Load skill synonyms
            skill_categories_file = os.path.join(skills_data_path, "skill_categories.json")
            if os.path.exists(skill_categories_file):
                with open(skill_categories_file, 'r', encoding='utf-8') as f:
                    skill_categories_data = json.load(f)
                    self.skill_synonyms = skill_categories_data.get("synonyms", {})
                logger.debug(f"Loaded skill synonyms: {len(self.skill_synonyms)} entries")
            else:
                logger.warning(f"Skill categories file not found: {skill_categories_file}")
                self.skill_synonyms = {}
            
            # Load certifications
            certifications_file = os.path.join(skills_data_path, "certifications.json")
            if os.path.exists(certifications_file):
                with open(certifications_file, 'r', encoding='utf-8') as f:
                    self.certifications_db = json.load(f)
                logger.debug(f"Loaded certifications: {len(self.certifications_db)} entries")
            else:
                logger.warning(f"Certifications file not found: {certifications_file}")
                self.certifications_db = {}
            
            logger.info("Skills databases loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load skills databases: {e}")
            logger.error("Using default skills databases")
            self._load_default_skills()
    
    def _load_default_skills(self):
        """Load default skills databases when files are not available."""
        logger.debug("Loading default skills databases")
        self.technical_skills_db = self._get_default_technical_skills()
        self.soft_skills_db = self._get_default_soft_skills()
        self.industry_skills_map = self._get_default_industry_skills()
        self.skill_synonyms = {}
        self.certifications_db = {}
    
    def _get_default_technical_skills(self) -> Dict:
        """Get default technical skills database."""
        return {
            "Programming Languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
                "Swift", "Kotlin", "PHP", "Ruby", "Scala", "R", "MATLAB", "SQL"
            ],
            "Web Development": [
                "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
                "Django", "Flask", "Spring Boot", "ASP.NET", "Laravel", "Ruby on Rails"
            ],
            "Data Science": [
                "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras",
                "Jupyter", "R", "MATLAB", "Tableau", "Power BI", "Apache Spark"
            ],
            "Cloud Platforms": [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
                "Ansible", "Jenkins", "GitLab CI/CD", "GitHub Actions"
            ],
            "Databases": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "Oracle",
                "SQL Server", "SQLite", "Cassandra", "DynamoDB"
            ],
            "Mobile Development": [
                "React Native", "Flutter", "Xamarin", "Ionic", "Cordova", "Swift",
                "Kotlin", "Java", "Objective-C"
            ],
            "DevOps": [
                "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "GitHub Actions",
                "Terraform", "Ansible", "Chef", "Puppet", "Prometheus", "Grafana"
            ],
            "Machine Learning": [
                "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy",
                "Jupyter", "Apache Spark", "Hadoop", "MLflow", "Kubeflow"
            ]
        }
    
    def _get_default_soft_skills(self) -> Dict:
        """Get default soft skills database."""
        return {
            "Communication": [
                "Verbal Communication", "Written Communication", "Presentation Skills",
                "Public Speaking", "Active Listening", "Negotiation", "Persuasion"
            ],
            "Leadership": [
                "Team Leadership", "Project Management", "Strategic Thinking",
                "Decision Making", "Mentoring", "Coaching", "Change Management"
            ],
            "Problem Solving": [
                "Analytical Thinking", "Critical Thinking", "Creative Problem Solving",
                "Root Cause Analysis", "Process Improvement", "Innovation"
            ],
            "Collaboration": [
                "Teamwork", "Cross-functional Collaboration", "Conflict Resolution",
                "Stakeholder Management", "Relationship Building", "Cultural Awareness"
            ],
            "Adaptability": [
                "Flexibility", "Learning Agility", "Resilience", "Change Management",
                "Continuous Learning", "Growth Mindset", "Versatility"
            ],
            "Time Management": [
                "Project Planning", "Priority Setting", "Deadline Management",
                "Multitasking", "Organization", "Efficiency", "Productivity"
            ]
        }
    
    def _get_default_industry_skills(self) -> Dict:
        """Get default industry skills mapping."""
        return {
            "Technology": [
                "Software Development", "Cloud Computing", "Data Science", "AI/ML",
                "Cybersecurity", "DevOps", "Mobile Development", "Web Development"
            ],
            "Finance": [
                "Financial Analysis", "Risk Management", "Investment Banking",
                "Accounting", "Trading", "Compliance", "Auditing", "Financial Modeling"
            ],
            "Healthcare": [
                "Medical Knowledge", "Patient Care", "Healthcare IT", "Clinical Research",
                "Regulatory Compliance", "Medical Coding", "Healthcare Analytics"
            ],
            "Marketing": [
                "Digital Marketing", "Content Marketing", "SEO/SEM", "Social Media",
                "Brand Management", "Market Research", "Analytics", "Campaign Management"
            ],
            "Sales": [
                "Lead Generation", "Customer Relationship Management", "Negotiation",
                "Sales Strategy", "Account Management", "Business Development", "Prospecting"
            ]
        }
    
    def extract_skills_from_text(self, text: str, skill_types: List[str] = None) -> List[Skill]:
        """
        Extract skills from text content with comprehensive logging.
        
        Args:
            text (str): Text content to analyze
            skill_types (List[str]): Types of skills to extract (technical, soft, certifications)
            
        Returns:
            List[Skill]: List of extracted skills
            
        Raises:
            Exception: If skill extraction fails
        """
        try:
            logger.debug(f"Extracting skills from text (length: {len(text)})")
            start_time = time.time()
            
            if skill_types is None:
                skill_types = ["technical", "soft", "certifications"]
            
            extracted_skills = []
            text_lower = text.lower()
            
            # Extract technical skills
            if "technical" in skill_types:
                logger.debug("Extracting technical skills")
                technical_skills = self._extract_technical_skills(text_lower)
                extracted_skills.extend(technical_skills)
                logger.debug(f"Found {len(technical_skills)} technical skills")
            
            # Extract soft skills
            if "soft" in skill_types:
                logger.debug("Extracting soft skills")
                soft_skills = self._extract_soft_skills(text_lower)
                extracted_skills.extend(soft_skills)
                logger.debug(f"Found {len(soft_skills)} soft skills")
            
            # Extract certifications
            if "certifications" in skill_types:
                logger.debug("Extracting certifications")
                certifications = self._extract_certifications(text_lower)
                extracted_skills.extend(certifications)
                logger.debug(f"Found {len(certifications)} certifications")
            
            # Remove duplicates and sort by confidence
            extracted_skills = self._deduplicate_skills(extracted_skills)
            extracted_skills.sort(key=lambda x: x.confidence, reverse=True)
            
            extraction_time = time.time() - start_time
            logger.info(f"Skill extraction completed in {extraction_time:.2f}s")
            logger.info(f"Total skills extracted: {len(extracted_skills)}")
            
            return extracted_skills
            
        except Exception as e:
            logger.error(f"Failed to extract skills from text: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return []
    
    def _extract_technical_skills(self, text_lower: str) -> List[Skill]:
        """Extract technical skills from text."""
        technical_skills = []
        
        for category, skills in self.technical_skills_db.items():
            for skill in skills:
                skill_lower = skill.lower()
                
                # Check for exact match
                if skill_lower in text_lower:
                    confidence = 0.9
                # Check for partial match
                elif any(word in text_lower for word in skill_lower.split()):
                    confidence = 0.7
                # Check for synonyms
                elif skill_lower in self.skill_synonyms:
                    synonyms = self.skill_synonyms[skill_lower]
                    if any(synonym.lower() in text_lower for synonym in synonyms):
                        confidence = 0.6
                else:
                    continue
                
                technical_skills.append(Skill(
                    name=skill,
                    category=SkillCategory.TECHNICAL,
                    subcategory=category,
                    confidence=confidence,
                    source="text_extraction"
                ))
        
        return technical_skills
    
    def _extract_soft_skills(self, text_lower: str) -> List[Skill]:
        """Extract soft skills from text."""
        soft_skills = []
        
        for category, skills in self.soft_skills_db.items():
            for skill in skills:
                skill_lower = skill.lower()
                
                # Check for exact match
                if skill_lower in text_lower:
                    confidence = 0.8
                # Check for partial match
                elif any(word in text_lower for word in skill_lower.split()):
                    confidence = 0.6
                else:
                    continue
                
                soft_skills.append(Skill(
                    name=skill,
                    category=SkillCategory.SOFT,
                    subcategory=category,
                    confidence=confidence,
                    source="text_extraction"
                ))
        
        return soft_skills
    
    def _extract_certifications(self, text_lower: str) -> List[Skill]:
        """Extract certifications from text."""
        certifications = []
        
        for cert_name, cert_data in self.certifications_db.items():
            cert_lower = cert_name.lower()
            
            # Check for exact match
            if cert_lower in text_lower:
                confidence = 0.9
            # Check for partial match
            elif any(word in text_lower for word in cert_lower.split()):
                confidence = 0.7
            else:
                continue
            
            certifications.append(Skill(
                name=cert_name,
                category=SkillCategory.CERTIFICATION,
                subcategory=cert_data.get("category", "Professional"),
                confidence=confidence,
                source="text_extraction"
            ))
        
        return certifications
    
    def _deduplicate_skills(self, skills: List[Skill]) -> List[Skill]:
        """Remove duplicate skills and merge similar ones."""
        seen_skills = {}
        
        for skill in skills:
            key = skill.name.lower()
            
            if key in seen_skills:
                # Keep the skill with higher confidence
                if skill.confidence > seen_skills[key].confidence:
                    seen_skills[key] = skill
            else:
                seen_skills[key] = skill
        
        return list(seen_skills.values())
    
    def analyze_skills_gap(self, resume_skills: List[Skill], job_skills: List[Skill]) -> Dict[str, Any]:
        """
        Analyze skills gap between resume and job requirements.
        
        Args:
            resume_skills (List[Skill]): Skills from resume
            job_skills (List[Skill]): Skills from job description
            
        Returns:
            Dict[str, Any]: Skills gap analysis results
        """
        try:
            logger.debug("Analyzing skills gap")
            start_time = time.time()
            
            resume_skill_names = {skill.name.lower() for skill in resume_skills}
            job_skill_names = {skill.name.lower() for skill in job_skills}
            
            # Find matching skills
            matching_skills = resume_skill_names.intersection(job_skill_names)
            
            # Find missing skills
            missing_skills = job_skill_names - resume_skill_names
            
            # Find extra skills
            extra_skills = resume_skill_names - job_skill_names
            
            # Calculate match percentage
            match_percentage = (len(matching_skills) / len(job_skill_names)) * 100 if job_skill_names else 0
            
            # Categorize missing skills
            missing_technical = []
            missing_soft = []
            missing_certifications = []
            
            for skill in job_skills:
                if skill.name.lower() in missing_skills:
                    if skill.category == SkillCategory.TECHNICAL:
                        missing_technical.append(skill)
                    elif skill.category == SkillCategory.SOFT:
                        missing_soft.append(skill)
                    elif skill.category == SkillCategory.CERTIFICATION:
                        missing_certifications.append(skill)
            
            analysis_time = time.time() - start_time
            logger.info(f"Skills gap analysis completed in {analysis_time:.2f}s")
            logger.info(f"Match percentage: {match_percentage:.1f}%")
            logger.info(f"Missing skills: {len(missing_skills)}")
            
            return {
                "match_percentage": match_percentage,
                "matching_skills": list(matching_skills),
                "missing_skills": list(missing_skills),
                "extra_skills": list(extra_skills),
                "missing_technical": [skill.name for skill in missing_technical],
                "missing_soft": [skill.name for skill in missing_soft],
                "missing_certifications": [skill.name for skill in missing_certifications],
                "total_resume_skills": len(resume_skills),
                "total_job_skills": len(job_skills),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze skills gap: {e}")
            return {
                "match_percentage": 0,
                "matching_skills": [],
                "missing_skills": [],
                "extra_skills": [],
                "missing_technical": [],
                "missing_soft": [],
                "missing_certifications": [],
                "total_resume_skills": 0,
                "total_job_skills": 0,
                "analysis_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_skill_recommendations(self, skills_gap_analysis: Dict[str, Any], industry: str = None) -> List[Dict[str, Any]]:
        """
        Get skill development recommendations based on gap analysis.
        
        Args:
            skills_gap_analysis (Dict[str, Any]): Skills gap analysis results
            industry (str): Target industry for recommendations
            
        Returns:
            List[Dict[str, Any]]: Skill development recommendations
        """
        try:
            logger.debug("Generating skill recommendations")
            recommendations = []
            
            missing_technical = skills_gap_analysis.get("missing_technical", [])
            missing_soft = skills_gap_analysis.get("missing_soft", [])
            missing_certifications = skills_gap_analysis.get("missing_certifications", [])
            
            # Technical skills recommendations
            for skill in missing_technical[:5]:  # Top 5 missing technical skills
                recommendations.append({
                    "skill": skill,
                    "category": "Technical",
                    "priority": "High",
                    "recommendation": f"Learn {skill} through online courses, tutorials, or hands-on projects",
                    "resources": self._get_skill_learning_resources(skill, "technical"),
                    "timeline": "3-6 months"
                })
            
            # Soft skills recommendations
            for skill in missing_soft[:3]:  # Top 3 missing soft skills
                recommendations.append({
                    "skill": skill,
                    "category": "Soft",
                    "priority": "Medium",
                    "recommendation": f"Develop {skill} through practice, workshops, or mentoring",
                    "resources": self._get_skill_learning_resources(skill, "soft"),
                    "timeline": "1-3 months"
                })
            
            # Certification recommendations
            for cert in missing_certifications[:3]:  # Top 3 missing certifications
                recommendations.append({
                    "skill": cert,
                    "category": "Certification",
                    "priority": "High",
                    "recommendation": f"Obtain {cert} certification to validate your expertise",
                    "resources": self._get_skill_learning_resources(cert, "certification"),
                    "timeline": "2-4 months"
                })
            
            logger.info(f"Generated {len(recommendations)} skill recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate skill recommendations: {e}")
            return []
    
    def _get_skill_learning_resources(self, skill: str, category: str) -> List[str]:
        """Get learning resources for a specific skill."""
        resources = []
        
        if category == "technical":
            resources = [
                f"Online courses: Coursera, Udemy, edX for {skill}",
                f"Documentation: Official {skill} documentation",
                f"Practice: Build projects using {skill}",
                f"Community: Join {skill} developer communities"
            ]
        elif category == "soft":
            resources = [
                f"Workshops: Attend {skill} training workshops",
                f"Books: Read books on {skill} development",
                f"Practice: Apply {skill} in daily work",
                f"Mentoring: Find a mentor for {skill} development"
            ]
        elif category == "certification":
            resources = [
                f"Study materials: Official {skill} study guides",
                f"Practice exams: Take {skill} practice tests",
                f"Training: Enroll in {skill} certification training",
                f"Community: Join {skill} certification study groups"
            ]
        
        return resources
    
    def get_skills_summary(self, skills: List[Skill]) -> Dict[str, Any]:
        """
        Get comprehensive skills summary with statistics.
        
        Args:
            skills (List[Skill]): List of skills to summarize
            
        Returns:
            Dict[str, Any]: Skills summary with statistics
        """
        try:
            logger.debug("Generating skills summary")
            
            # Categorize skills
            technical_skills = [s for s in skills if s.category == SkillCategory.TECHNICAL]
            soft_skills = [s for s in skills if s.category == SkillCategory.SOFT]
            certifications = [s for s in skills if s.category == SkillCategory.CERTIFICATION]
            
            # Get subcategory counts
            technical_subcategories = {}
            for skill in technical_skills:
                subcat = skill.subcategory
                technical_subcategories[subcat] = technical_subcategories.get(subcat, 0) + 1
            
            soft_subcategories = {}
            for skill in soft_skills:
                subcat = skill.subcategory
                soft_subcategories[subcat] = soft_subcategories.get(subcat, 0) + 1
            
            # Calculate average confidence
            avg_confidence = sum(skill.confidence for skill in skills) / len(skills) if skills else 0
            
            summary = {
                "total_skills": len(skills),
                "technical_skills_count": len(technical_skills),
                "soft_skills_count": len(soft_skills),
                "certifications_count": len(certifications),
                "technical_subcategories": technical_subcategories,
                "soft_subcategories": soft_subcategories,
                "average_confidence": round(avg_confidence, 2),
                "top_skills": [skill.name for skill in sorted(skills, key=lambda x: x.confidence, reverse=True)[:10]],
                "summary_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Skills summary generated: {len(skills)} total skills")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate skills summary: {e}")
            return {
                "total_skills": 0,
                "technical_skills_count": 0,
                "soft_skills_count": 0,
                "certifications_count": 0,
                "technical_subcategories": {},
                "soft_subcategories": {},
                "average_confidence": 0,
                "top_skills": [],
                "summary_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
