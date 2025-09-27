"""
Template Engine Module for Resume/CV AI Application
Handles resume template processing and generation.

This module provides:
- Resume template loading and management
- Dynamic template rendering
- Template customization and styling
- Multiple format support (HTML, DOCX, PDF)
- Template validation and error handling
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import os
import json
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import re

from models.resume_model import ParsedResume
from models.template_model import ResumeTemplate, TemplateSection, TemplateStyle
from utils.helpers import clean_text, generate_unique_id
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("template_engine")

class TemplateEngine:
    """
    Advanced template engine for resume generation with comprehensive logging.
    
    This class provides sophisticated template processing capabilities including
    template loading, dynamic rendering, customization, and multi-format output
    for professional resume generation.
    
    Key Features:
    - Template loading and management
    - Dynamic template rendering with data binding
    - Template customization and styling
    - Multiple format support (HTML, DOCX, PDF)
    - Template validation and error handling
    - Comprehensive logging and error handling
    
    Attributes:
        templates_dir (str): Directory containing template files
        loaded_templates (Dict): Cache of loaded templates
        default_styles (Dict): Default styling options
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, templates_dir: str = "data/templates/"):
        """
        Initialize the TemplateEngine with comprehensive logging.
        
        Args:
            templates_dir (str): Directory containing template files
            
        Raises:
            Exception: If TemplateEngine initialization fails
        """
        logger.info("Initializing TemplateEngine")
        self._initialization_time = time.time()
        
        # Initialize template directory and cache
        self.templates_dir = templates_dir
        self.loaded_templates = {}
        self.default_styles = {}
        
        try:
            # Create templates directory if it doesn't exist
            os.makedirs(templates_dir, exist_ok=True)
            
            # Load default styles
            logger.debug("Loading default styles")
            self._load_default_styles()
            
            # Load available templates
            logger.debug("Loading available templates")
            self._load_available_templates()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"TemplateEngine initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.loaded_templates)} templates")
            logger.info(f"Templates directory: {templates_dir}")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"TemplateEngine initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Template processing may not function correctly")
            raise
    
    def _load_default_styles(self):
        """Load default styling options."""
        self.default_styles = {
            "colors": {
                "primary": "#1f77b4",
                "secondary": "#2ca02c",
                "accent": "#ff7f0e",
                "text": "#333333",
                "background": "#ffffff",
                "border": "#e0e0e0"
            },
            "fonts": {
                "heading": "Arial, sans-serif",
                "body": "Arial, sans-serif",
                "monospace": "Courier New, monospace"
            },
            "sizes": {
                "heading1": "24px",
                "heading2": "20px",
                "heading3": "18px",
                "body": "14px",
                "small": "12px"
            },
            "spacing": {
                "section_margin": "20px",
                "item_margin": "10px",
                "line_height": "1.5"
            }
        }
    
    def _load_available_templates(self):
        """Load available templates from the templates directory."""
        try:
            template_files = [f for f in os.listdir(self.templates_dir) if f.endswith('.json')]
            
            for template_file in template_files:
                template_path = os.path.join(self.templates_dir, template_file)
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    
                    template = ResumeTemplate(**template_data)
                    self.loaded_templates[template.name] = template
                    logger.debug(f"Loaded template: {template.name}")
                    
                except Exception as e:
                    logger.warning(f"Failed to load template {template_file}: {e}")
                    continue
            
            logger.info(f"Successfully loaded {len(self.loaded_templates)} templates")
            
        except Exception as e:
            logger.error(f"Failed to load available templates: {e}")
            # Create default templates if none exist
            self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates if none exist."""
        logger.debug("Creating default templates")
        
        # Modern Professional Template
        modern_professional = ResumeTemplate(
            name="Modern Professional",
            description="Clean, modern design suitable for most industries",
            category="Professional",
            sections=[
                TemplateSection(
                    name="header",
                    type="contact",
                    required=True,
                    order=1,
                    template="<div class='header'><h1>{name}</h1><p>{contact_info}</p></div>"
                ),
                TemplateSection(
                    name="summary",
                    type="text",
                    required=False,
                    order=2,
                    template="<div class='summary'><h2>Professional Summary</h2><p>{summary}</p></div>"
                ),
                TemplateSection(
                    name="experience",
                    type="list",
                    required=True,
                    order=3,
                    template="<div class='experience'><h2>Work Experience</h2>{experience_items}</div>"
                ),
                TemplateSection(
                    name="education",
                    type="list",
                    required=True,
                    order=4,
                    template="<div class='education'><h2>Education</h2>{education_items}</div>"
                ),
                TemplateSection(
                    name="skills",
                    type="list",
                    required=True,
                    order=5,
                    template="<div class='skills'><h2>Skills</h2>{skills_items}</div>"
                )
            ],
            styles=TemplateStyle(
                primary_color="#1f77b4",
                secondary_color="#2ca02c",
                font_family="Arial, sans-serif",
                font_size="14px"
            )
        )
        
        self.loaded_templates["Modern Professional"] = modern_professional
        
        # Save default template
        self._save_template(modern_professional)
    
    def _save_template(self, template: ResumeTemplate):
        """Save template to file."""
        try:
            template_file = os.path.join(self.templates_dir, f"{template.name.lower().replace(' ', '_')}.json")
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template.dict(), f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved template: {template.name}")
        except Exception as e:
            logger.error(f"Failed to save template {template.name}: {e}")
    
    def get_available_templates(self) -> List[ResumeTemplate]:
        """
        Get list of available templates.
        
        Returns:
            List[ResumeTemplate]: List of available templates
        """
        try:
            logger.debug("Getting available templates")
            return list(self.loaded_templates.values())
        except Exception as e:
            logger.error(f"Failed to get available templates: {e}")
            return []
    
    def get_template(self, template_name: str) -> Optional[ResumeTemplate]:
        """
        Get specific template by name.
        
        Args:
            template_name (str): Name of the template
            
        Returns:
            Optional[ResumeTemplate]: Template object or None if not found
        """
        try:
            logger.debug(f"Getting template: {template_name}")
            return self.loaded_templates.get(template_name)
        except Exception as e:
            logger.error(f"Failed to get template {template_name}: {e}")
            return None
    
    def render_resume(self, resume: ParsedResume, template_name: str, custom_styles: Dict[str, Any] = None) -> str:
        """
        Render resume using specified template with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume data to render
            template_name (str): Name of the template to use
            custom_styles (Dict[str, Any]): Custom styling options
            
        Returns:
            str: Rendered HTML content
            
        Raises:
            Exception: If template rendering fails
        """
        try:
            logger.debug(f"Rendering resume with template: {template_name}")
            start_time = time.time()
            
            # Get template
            template = self.get_template(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Prepare data for rendering
            render_data = self._prepare_render_data(resume, template)
            
            # Apply custom styles if provided
            if custom_styles:
                template.styles = self._merge_styles(template.styles, custom_styles)
            
            # Render template sections
            rendered_sections = []
            for section in template.sections:
                if section.required or self._has_section_data(resume, section.name):
                    rendered_section = self._render_section(section, render_data, template.styles)
                    if rendered_section:
                        rendered_sections.append(rendered_section)
            
            # Combine sections
            html_content = self._combine_sections(rendered_sections, template.styles)
            
            rendering_time = time.time() - start_time
            logger.info(f"Resume rendering completed in {rendering_time:.2f}s")
            logger.info(f"Rendered {len(rendered_sections)} sections")
            
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to render resume: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def _prepare_render_data(self, resume: ParsedResume, template: ResumeTemplate) -> Dict[str, Any]:
        """Prepare data for template rendering."""
        try:
            # Basic contact information
            contact_info = []
            if resume.contact_info.name:
                contact_info.append(resume.contact_info.name)
            if resume.contact_info.email:
                contact_info.append(resume.contact_info.email)
            if resume.contact_info.phone:
                contact_info.append(resume.contact_info.phone)
            if resume.contact_info.location:
                contact_info.append(resume.contact_info.location)
            
            # Experience items
            experience_items = []
            for exp in resume.work_experience:
                exp_html = f"""
                <div class="experience-item">
                    <h3>{exp.title} - {exp.company}</h3>
                    <p class="duration">{exp.start_date} - {exp.end_date or 'Present'}</p>
                    <p class="description">{exp.description}</p>
                </div>
                """
                experience_items.append(exp_html)
            
            # Education items
            education_items = []
            for edu in resume.education:
                edu_html = f"""
                <div class="education-item">
                    <h3>{edu.degree} in {edu.field}</h3>
                    <p class="institution">{edu.institution}</p>
                    <p class="year">{edu.graduation_date or 'In Progress'}</p>
                </div>
                """
                education_items.append(edu_html)
            
            # Skills items
            skills_by_category = {}
            for skill in resume.skills:
                category = skill.subcategory or skill.category.value
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.name)
            
            skills_items = []
            for category, skills in skills_by_category.items():
                skills_html = f"""
                <div class="skills-category">
                    <h4>{category}</h4>
                    <p>{', '.join(skills)}</p>
                </div>
                """
                skills_items.append(skills_html)
            
            return {
                "name": resume.contact_info.name or "Your Name",
                "contact_info": " | ".join(contact_info),
                "summary": resume.summary or "",
                "experience_items": "".join(experience_items),
                "education_items": "".join(education_items),
                "skills_items": "".join(skills_items)
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare render data: {e}")
            return {}
    
    def _has_section_data(self, resume: ParsedResume, section_name: str) -> bool:
        """Check if resume has data for the specified section."""
        if section_name == "summary":
            return bool(resume.summary)
        elif section_name == "experience":
            return bool(resume.work_experience)
        elif section_name == "education":
            return bool(resume.education)
        elif section_name == "skills":
            return bool(resume.skills)
        return False
    
    def _render_section(self, section: TemplateSection, data: Dict[str, Any], styles: TemplateStyle) -> str:
        """Render a single template section."""
        try:
            # Get section data
            section_data = data.get(section.name, {})
            
            # Render section template
            rendered = section.template.format(**data)
            
            # Apply section-specific styling
            if section.type == "contact":
                rendered = f'<div class="section contact-section">{rendered}</div>'
            elif section.type == "text":
                rendered = f'<div class="section text-section">{rendered}</div>'
            elif section.type == "list":
                rendered = f'<div class="section list-section">{rendered}</div>'
            
            return rendered
            
        except Exception as e:
            logger.warning(f"Failed to render section {section.name}: {e}")
            return ""
    
    def _combine_sections(self, sections: List[str], styles: TemplateStyle) -> str:
        """Combine rendered sections into complete HTML."""
        try:
            # Create CSS styles
            css = self._generate_css(styles)
            
            # Combine sections
            body_content = "".join(sections)
            
            # Create complete HTML
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resume</title>
                <style>
                    {css}
                </style>
            </head>
            <body>
                <div class="resume-container">
                    {body_content}
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            logger.error(f"Failed to combine sections: {e}")
            return ""
    
    def _generate_css(self, styles: TemplateStyle) -> str:
        """Generate CSS styles for the template."""
        return f"""
        body {{
            font-family: {styles.font_family};
            font-size: {styles.font_size};
            line-height: 1.5;
            color: {styles.text_color or '#333333'};
            background-color: {styles.background_color or '#ffffff'};
            margin: 0;
            padding: 20px;
        }}
        
        .resume-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            border-bottom: 2px solid {styles.primary_color};
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: {styles.primary_color};
            margin: 0;
            font-size: 28px;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: {styles.primary_color};
            border-bottom: 1px solid {styles.border_color or '#e0e0e0'};
            padding-bottom: 5px;
            margin-bottom: 15px;
        }}
        
        .experience-item, .education-item {{
            margin-bottom: 20px;
        }}
        
        .experience-item h3, .education-item h3 {{
            color: {styles.secondary_color or styles.primary_color};
            margin: 0 0 5px 0;
        }}
        
        .duration, .institution, .year {{
            font-style: italic;
            color: #666;
            margin: 0;
        }}
        
        .skills-category {{
            margin-bottom: 15px;
        }}
        
        .skills-category h4 {{
            color: {styles.secondary_color or styles.primary_color};
            margin: 0 0 5px 0;
            font-size: 16px;
        }}
        
        .summary p {{
            text-align: justify;
            line-height: 1.6;
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            .resume-container {{
                box-shadow: none;
                padding: 0;
            }}
        }}
        """
    
    def _merge_styles(self, base_styles: TemplateStyle, custom_styles: Dict[str, Any]) -> TemplateStyle:
        """Merge custom styles with base template styles."""
        try:
            # Convert base styles to dict
            base_dict = base_styles.dict() if hasattr(base_styles, 'dict') else base_styles
            
            # Merge custom styles
            merged_dict = {**base_dict, **custom_styles}
            
            # Create new TemplateStyle object
            return TemplateStyle(**merged_dict)
            
        except Exception as e:
            logger.warning(f"Failed to merge styles: {e}")
            return base_styles
    
    def create_custom_template(self, name: str, description: str, sections: List[TemplateSection], styles: TemplateStyle) -> ResumeTemplate:
        """
        Create a custom template with comprehensive logging.
        
        Args:
            name (str): Template name
            description (str): Template description
            sections (List[TemplateSection]): Template sections
            styles (TemplateStyle): Template styles
            
        Returns:
            ResumeTemplate: Created template object
        """
        try:
            logger.debug(f"Creating custom template: {name}")
            
            # Create template
            template = ResumeTemplate(
                name=name,
                description=description,
                category="Custom",
                sections=sections,
                styles=styles
            )
            
            # Save template
            self.loaded_templates[name] = template
            self._save_template(template)
            
            logger.info(f"Custom template created: {name}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to create custom template: {e}")
            raise
    
    def validate_template(self, template: ResumeTemplate) -> List[str]:
        """
        Validate template structure and content.
        
        Args:
            template (ResumeTemplate): Template to validate
            
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        try:
            logger.debug(f"Validating template: {template.name}")
            errors = []
            
            # Check required fields
            if not template.name:
                errors.append("Template name is required")
            
            if not template.sections:
                errors.append("Template must have at least one section")
            
            # Check sections
            for i, section in enumerate(template.sections):
                if not section.name:
                    errors.append(f"Section {i+1}: Name is required")
                
                if not section.template:
                    errors.append(f"Section {i+1}: Template is required")
                
                if section.order < 1:
                    errors.append(f"Section {i+1}: Order must be positive")
            
            # Check for duplicate section names
            section_names = [s.name for s in template.sections]
            if len(section_names) != len(set(section_names)):
                errors.append("Duplicate section names found")
            
            # Check for duplicate section orders
            section_orders = [s.order for s in template.sections]
            if len(section_orders) != len(set(section_orders)):
                errors.append("Duplicate section orders found")
            
            logger.info(f"Template validation completed: {len(errors)} errors found")
            return errors
            
        except Exception as e:
            logger.error(f"Failed to validate template: {e}")
            return [f"Validation error: {str(e)}"]
    
    def get_template_preview(self, template_name: str, sample_data: Dict[str, Any] = None) -> str:
        """
        Get template preview with sample data.
        
        Args:
            template_name (str): Name of the template
            sample_data (Dict[str, Any]): Sample data for preview
            
        Returns:
            str: HTML preview content
        """
        try:
            logger.debug(f"Generating template preview: {template_name}")
            
            # Get template
            template = self.get_template(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Use sample data if provided, otherwise create default
            if not sample_data:
                sample_data = self._get_sample_data()
            
            # Render preview
            preview_html = self.render_resume(sample_data, template_name)
            
            logger.info(f"Template preview generated: {template_name}")
            return preview_html
            
        except Exception as e:
            logger.error(f"Failed to generate template preview: {e}")
            return f"<p>Error generating preview: {str(e)}</p>"
    
    def _get_sample_data(self) -> Dict[str, Any]:
        """Get sample data for template preview."""
        return {
            "name": "John Doe",
            "contact_info": "john.doe@email.com | (555) 123-4567 | New York, NY",
            "summary": "Experienced software developer with 5+ years of expertise in full-stack development.",
            "experience_items": """
            <div class="experience-item">
                <h3>Senior Software Developer - Tech Company</h3>
                <p class="duration">2020 - Present</p>
                <p class="description">Led development of scalable web applications using modern technologies.</p>
            </div>
            """,
            "education_items": """
            <div class="education-item">
                <h3>Bachelor of Science in Computer Science</h3>
                <p class="institution">University of Technology</p>
                <p class="year">2018</p>
            </div>
            """,
            "skills_items": """
            <div class="skills-category">
                <h4>Programming Languages</h4>
                <p>Python, JavaScript, Java, SQL</p>
            </div>
            """
        }
