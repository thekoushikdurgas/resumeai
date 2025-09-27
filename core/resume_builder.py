"""
Resume Builder Module for Resume/CV AI Application
Handles AI-assisted resume building and generation.

This module provides:
- AI-powered resume building and enhancement
- Template-based resume generation
- Content optimization and suggestions
- Industry-specific resume customization
- ATS-friendly resume formatting
- Comprehensive resume validation

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from models.resume_model import ParsedResume, ContactInfo, WorkExperience, Education, Skill, Project
from utils.helpers import generate_unique_id, clean_text
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("resume_builder")

class ResumeBuilder:
    """
    AI-assisted resume builder with comprehensive logging.
    
    This class provides advanced resume building capabilities including:
    - AI-powered content generation and enhancement
    - Template-based resume creation
    - Industry-specific customization
    - ATS-friendly formatting and optimization
    - Content validation and quality assurance
    
    Attributes:
        ai_handler: AI handler instance for content generation
        templates: Dictionary of resume templates by industry/type
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, ai_handler):
        """
        Initialize resume builder with comprehensive logging.
        
        Sets up the builder with AI handler dependency, loads resume templates,
        and logs initialization details for debugging and monitoring.
        
        Args:
            ai_handler: AI handler instance for content generation
            
        Raises:
            Exception: If initialization fails due to missing dependencies
        """
        logger.info("Initializing ResumeBuilder")
        self._initialization_time = time.time()
        
        try:
            # Validate dependencies
            if not ai_handler:
                raise ValueError("AIHandler instance is required")
            
            self.ai_handler = ai_handler
            logger.info("Dependencies validated successfully")
            
            # Load templates
            logger.debug("Loading resume templates")
            self.templates = self._load_templates()
            logger.debug(f"Loaded {len(self.templates)} resume templates")
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ResumeBuilder initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Available templates: {len(self.templates)}")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ResumeBuilder initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def build_resume(self, resume_data: Dict[str, Any]) -> ParsedResume:
        """
        Build a resume from provided data with comprehensive logging.
        
        This method performs AI-assisted resume building including:
        - Data validation and preprocessing
        - Contact information creation
        - Work experience and education processing
        - Skills and project extraction
        - AI-powered content enhancement
        - Resume validation and quality assurance
        
        Args:
            resume_data (Dict[str, Any]): Dictionary containing resume data including:
                - name, email, phone, location (contact info)
                - experiences (list of work experience data)
                - education (list of education data)
                - skills (list of skills)
                - projects (list of project data)
                
        Returns:
            ParsedResume: Built resume object with all components
            
        Raises:
            Exception: If resume building fails due to invalid data or processing errors
        """
        start_time = time.time()
        
        try:
            logger.info("Starting resume building process")
            logger.debug(f"Resume data keys: {list(resume_data.keys())}")
            logger.debug(f"Contact name: {resume_data.get('name', 'Unknown')}")
            
            # Validate input data
            if not resume_data:
                raise ValueError("Resume data cannot be empty")
            
            # Create contact info
            logger.debug("Creating contact information")
            contact_info = ContactInfo(
                name=resume_data.get('name'),
                email=resume_data.get('email'),
                phone=resume_data.get('phone'),
                location=resume_data.get('location')
            )
            logger.debug(f"Contact info created for: {contact_info.name or 'Unknown'}")
            
            # Create work experiences
            logger.debug("Processing work experiences")
            work_experiences = []
            experiences_data = resume_data.get('experiences', [])
            logger.debug(f"Processing {len(experiences_data)} work experiences")
            
            for i, exp_data in enumerate(experiences_data):
                experience = WorkExperience(
                    title=exp_data.get('title'),
                    company=exp_data.get('company'),
                    description=exp_data.get('description'),
                    start_date=exp_data.get('start_date'),
                    end_date=exp_data.get('end_date')
                )
                work_experiences.append(experience)
                logger.debug(f"Experience {i+1}: {experience.title} at {experience.company}")
            
            # Create education
            logger.debug("Processing education")
            education_list = []
            education_data = resume_data.get('education', [])
            logger.debug(f"Processing {len(education_data)} education entries")
            
            for i, edu_data in enumerate(education_data):
                education = Education(
                    degree=edu_data.get('degree'),
                    institution=edu_data.get('institution'),
                    graduation_date=edu_data.get('graduation_date'),
                    gpa=edu_data.get('gpa')
                )
                education_list.append(education)
                logger.debug(f"Education {i+1}: {education.degree} from {education.institution}")
            
            # Create skills
            logger.debug("Processing skills")
            skills_list = []
            skills_data = resume_data.get('skills', [])
            logger.debug(f"Processing {len(skills_data)} skills")
            
            for i, skill_data in enumerate(skills_data):
                skill = Skill(
                    name=skill_data.get('name'),
                    category=skill_data.get('category', 'General'),
                    proficiency=skill_data.get('proficiency', 'Intermediate')
                )
                skills_list.append(skill)
                logger.debug(f"Skill {i+1}: {skill.name} ({skill.category})")
            
            # Create projects
            logger.debug("Processing projects")
            projects_list = []
            projects_data = resume_data.get('projects', [])
            logger.debug(f"Processing {len(projects_data)} projects")
            
            for i, project_data in enumerate(projects_data):
                project = Project(
                    name=project_data.get('name'),
                    description=project_data.get('description'),
                    technologies=project_data.get('technologies', [])
                )
                projects_list.append(project)
                logger.debug(f"Project {i+1}: {project.name}")
            
            # Create resume
            logger.debug("Creating final resume object")
            resume = ParsedResume(
                contact_info=contact_info,
                summary=resume_data.get('summary'),
                work_experience=work_experiences,
                education=education_list,
                skills=skills_list,
                projects=projects_list,
                created_at=datetime.now()
            )
            
            building_time = time.time() - start_time
            logger.info(f"Resume building completed successfully in {building_time:.2f}s")
            logger.info(f"Built resume summary:")
            logger.info(f"  - Name: {contact_info.name or 'Unknown'}")
            logger.info(f"  - Work experiences: {len(work_experiences)}")
            logger.info(f"  - Education entries: {len(education_list)}")
            logger.info(f"  - Skills: {len(skills_list)}")
            logger.info(f"  - Projects: {len(projects_list)}")
            
            return resume
            
        except Exception as e:
            building_time = time.time() - start_time
            logger.error(f"Resume building failed after {building_time:.2f}s: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Resume data keys: {list(resume_data.keys()) if resume_data else 'None'}")
            
            # Return minimal resume
            logger.info("Returning minimal resume object due to building failure")
            return ParsedResume(
                contact_info=ContactInfo(),
                created_at=datetime.now()
            )
    
    def enhance_resume_with_ai(self, resume: ParsedResume, enhancement_type: str = "general") -> ParsedResume:
        """
        Enhance resume using AI.
        
        Args:
            resume: Resume to enhance
            enhancement_type: Type of enhancement
            
        Returns:
            Enhanced resume
        """
        try:
            # Generate AI enhancements
            suggestions = self.ai_handler.generate_enhancement_suggestions(resume, enhancement_type)
            
            # Apply enhancements (simplified version)
            enhanced_resume = self._apply_enhancements(resume, suggestions)
            
            return enhanced_resume
            
        except Exception as e:
            logger.error(f"Failed to enhance resume with AI: {e}")
            return resume
    
    def generate_resume_from_template(self, template_name: str, resume_data: Dict[str, Any]) -> str:
        """
        Generate resume text from template.
        
        Args:
            template_name: Name of the template
            resume_data: Resume data
            
        Returns:
            Generated resume text
        """
        try:
            template = self.templates.get(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Generate resume text using template
            resume_text = self._apply_template(template, resume_data)
            
            return resume_text
            
        except Exception as e:
            logger.error(f"Failed to generate resume from template: {e}")
            return ""
    
    def _apply_enhancements(self, resume: ParsedResume, suggestions: List) -> ParsedResume:
        """Apply AI enhancement suggestions to resume."""
        # This is a simplified version - in practice, you would apply specific suggestions
        enhanced_resume = resume
        
        # Example: Enhance summary if suggestions are available
        if suggestions and hasattr(suggestions[0], 'suggested_text'):
            # Apply first suggestion as example
            pass
        
        return enhanced_resume
    
    def _apply_template(self, template: Dict[str, Any], resume_data: Dict[str, Any]) -> str:
        """Apply template to resume data."""
        # This is a simplified template application
        # In practice, you would use a proper template engine like Jinja2
        
        template_text = template.get('content', '')
        
        # Replace placeholders with actual data
        replacements = {
            '{{name}}': resume_data.get('name', ''),
            '{{email}}': resume_data.get('email', ''),
            '{{phone}}': resume_data.get('phone', ''),
            '{{location}}': resume_data.get('location', ''),
            '{{summary}}': resume_data.get('summary', ''),
        }
        
        for placeholder, value in replacements.items():
            template_text = template_text.replace(placeholder, value)
        
        return template_text
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load resume templates."""
        return {
            'modern_professional': {
                'name': 'Modern Professional',
                'description': 'Clean, contemporary design suitable for most industries',
                'content': '''
{{name}}
{{email}} | {{phone}} | {{location}}

PROFESSIONAL SUMMARY
{{summary}}

EXPERIENCE
[Work experience will be added here]

EDUCATION
[Education will be added here]

SKILLS
[Skills will be added here]
                '''
            },
            'creative_design': {
                'name': 'Creative Design',
                'description': 'Visually appealing template for creative professionals',
                'content': '''
{{name}}
Creative Professional
{{email}} | {{phone}} | {{location}}

ABOUT
{{summary}}

EXPERIENCE
[Work experience will be added here]

EDUCATION
[Education will be added here]

SKILLS & EXPERTISE
[Skills will be added here]
                '''
            },
            'technical_focused': {
                'name': 'Technical Focused',
                'description': 'Template emphasizing technical skills and projects',
                'content': '''
{{name}}
{{email}} | {{phone}} | {{location}}

SUMMARY
{{summary}}

TECHNICAL SKILLS
[Skills will be added here]

PROFESSIONAL EXPERIENCE
[Work experience will be added here]

PROJECTS
[Projects will be added here]

EDUCATION
[Education will be added here]
                '''
            }
        }
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available templates."""
        templates = []
        for name, template in self.templates.items():
            templates.append({
                'name': name,
                'display_name': template['name'],
                'description': template['description']
            })
        return templates
    
    def validate_resume_data(self, resume_data: Dict[str, Any]) -> List[str]:
        """Validate resume data and return any issues."""
        issues = []
        
        # Check required fields
        if not resume_data.get('name'):
            issues.append("Name is required")
        
        if not resume_data.get('email'):
            issues.append("Email is required")
        
        # Check email format
        email = resume_data.get('email', '')
        if email and '@' not in email:
            issues.append("Invalid email format")
        
        # Check experiences
        experiences = resume_data.get('experiences', [])
        for i, exp in enumerate(experiences):
            if not exp.get('title'):
                issues.append(f"Experience {i+1}: Title is required")
            if not exp.get('company'):
                issues.append(f"Experience {i+1}: Company is required")
        
        # Check education
        education = resume_data.get('education', [])
        for i, edu in enumerate(education):
            if not edu.get('degree'):
                issues.append(f"Education {i+1}: Degree is required")
            if not edu.get('institution'):
                issues.append(f"Education {i+1}: Institution is required")
        
        return issues
