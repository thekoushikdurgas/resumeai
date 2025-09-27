"""
Export Engine Module for Resume/CV AI Application
Handles multi-format resume export and generation.

This module provides:
- PDF resume generation and export
- DOCX resume creation and formatting
- HTML resume rendering
- JSON data export
- Multiple template support
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import os
import logging
import time
from typing import Dict, List, Optional, Any, BinaryIO
from datetime import datetime
from pathlib import Path
import json

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# DOCX generation
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# HTML generation
from jinja2 import Template

from models.resume_model import ParsedResume
from models.template_model import ResumeTemplate
from core.template_engine import TemplateEngine
from utils.helpers import clean_text, generate_unique_id
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("export_engine")

class ExportEngine:
    """
    Advanced export engine for multi-format resume generation with comprehensive logging.
    
    This class provides sophisticated export capabilities including PDF, DOCX, HTML,
    and JSON generation with template support and customization options.
    
    Key Features:
    - PDF resume generation and export
    - DOCX resume creation and formatting
    - HTML resume rendering
    - JSON data export
    - Multiple template support
    - Comprehensive logging and error handling
    
    Attributes:
        template_engine (TemplateEngine): Template engine for rendering
        export_templates (Dict): Export-specific templates
        output_directory (str): Directory for exported files
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, template_engine: TemplateEngine, output_directory: str = "data/exports/"):
        """
        Initialize the ExportEngine with comprehensive logging.
        
        Args:
            template_engine (TemplateEngine): Template engine for rendering
            output_directory (str): Directory for exported files
            
        Raises:
            Exception: If ExportEngine initialization fails
        """
        logger.info("Initializing ExportEngine")
        self._initialization_time = time.time()
        
        # Initialize dependencies
        self.template_engine = template_engine
        self.output_directory = output_directory
        
        # Initialize export templates
        self.export_templates = {}
        
        try:
            # Create output directory
            os.makedirs(output_directory, exist_ok=True)
            
            # Load export templates
            logger.debug("Loading export templates")
            self._load_export_templates()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ExportEngine initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Output directory: {output_directory}")
            logger.info(f"Loaded {len(self.export_templates)} export templates")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ExportEngine initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Export functionality may not work correctly")
            raise
    
    def _load_export_templates(self):
        """Load export-specific templates."""
        self.export_templates = {
            "pdf": {
                "styles": {
                    "title": {"fontSize": 18, "fontName": "Helvetica-Bold", "alignment": TA_CENTER},
                    "heading": {"fontSize": 14, "fontName": "Helvetica-Bold", "spaceAfter": 12},
                    "body": {"fontSize": 10, "fontName": "Helvetica", "spaceAfter": 6},
                    "bullet": {"fontSize": 10, "fontName": "Helvetica", "leftIndent": 20}
                }
            },
            "docx": {
                "styles": {
                    "title": {"size": Pt(18), "bold": True},
                    "heading": {"size": Pt(14), "bold": True},
                    "body": {"size": Pt(10)},
                    "bullet": {"size": Pt(10)}
                }
            },
            "html": {
                "template": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{{ resume.contact_info.name }} - Resume</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
                        .section { margin-bottom: 25px; }
                        .section h2 { color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
                        .experience-item, .education-item { margin-bottom: 15px; }
                        .skills-category { margin-bottom: 10px; }
                        .contact-info { margin-bottom: 10px; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>{{ resume.contact_info.name }}</h1>
                        <div class="contact-info">
                            {% if resume.contact_info.email %}{{ resume.contact_info.email }}{% endif %}
                            {% if resume.contact_info.phone %} | {{ resume.contact_info.phone }}{% endif %}
                            {% if resume.contact_info.location %} | {{ resume.contact_info.location }}{% endif %}
                        </div>
                    </div>
                    
                    {% if resume.summary %}
                    <div class="section">
                        <h2>Professional Summary</h2>
                        <p>{{ resume.summary }}</p>
                    </div>
                    {% endif %}
                    
                    {% if resume.work_experience %}
                    <div class="section">
                        <h2>Work Experience</h2>
                        {% for exp in resume.work_experience %}
                        <div class="experience-item">
                            <h3>{{ exp.title }} - {{ exp.company }}</h3>
                            <p><em>{{ exp.start_date }} - {{ exp.end_date or 'Present' }}</em></p>
                            {% if exp.description %}<p>{{ exp.description }}</p>{% endif %}
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                    {% if resume.education %}
                    <div class="section">
                        <h2>Education</h2>
                        {% for edu in resume.education %}
                        <div class="education-item">
                            <h3>{{ edu.degree }} in {{ edu.field }}</h3>
                            <p>{{ edu.institution }} - {{ edu.graduation_date or 'In Progress' }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                    {% if resume.skills %}
                    <div class="section">
                        <h2>Skills</h2>
                        {% set skills_by_category = {} %}
                        {% for skill in resume.skills %}
                            {% set category = skill.subcategory or skill.category.value %}
                            {% if category not in skills_by_category %}
                                {% set _ = skills_by_category.update({category: []}) %}
                            {% endif %}
                            {% set _ = skills_by_category[category].append(skill.name) %}
                        {% endfor %}
                        {% for category, skills in skills_by_category.items() %}
                        <div class="skills-category">
                            <strong>{{ category }}:</strong> {{ skills | join(', ') }}
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                </body>
                </html>
                """
            }
        }
    
    def export_to_pdf(self, resume: ParsedResume, filename: str = None, template_name: str = "Modern Professional") -> str:
        """
        Export resume to PDF format with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume data to export
            filename (str): Output filename (optional)
            template_name (str): Template to use for export
            
        Returns:
            str: Path to exported PDF file
            
        Raises:
            Exception: If PDF export fails
        """
        try:
            logger.debug("Exporting resume to PDF")
            start_time = time.time()
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"resume_{timestamp}.pdf"
            
            # Ensure .pdf extension
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Create full path
            filepath = os.path.join(self.output_directory, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            # Get styles
            styles = getSampleStyleSheet()
            pdf_styles = self.export_templates["pdf"]["styles"]
            
            # Create custom styles
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], **pdf_styles["title"])
            heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], **pdf_styles["heading"])
            body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], **pdf_styles["body"])
            bullet_style = ParagraphStyle('CustomBullet', parent=styles['Normal'], **pdf_styles["bullet"])
            
            # Build content
            content = []
            
            # Header
            if resume.contact_info.name:
                content.append(Paragraph(resume.contact_info.name, title_style))
                content.append(Spacer(1, 12))
            
            # Contact information
            contact_info = []
            if resume.contact_info.email:
                contact_info.append(resume.contact_info.email)
            if resume.contact_info.phone:
                contact_info.append(resume.contact_info.phone)
            if resume.contact_info.location:
                contact_info.append(resume.contact_info.location)
            
            if contact_info:
                content.append(Paragraph(" | ".join(contact_info), body_style))
                content.append(Spacer(1, 20))
            
            # Professional Summary
            if resume.summary:
                content.append(Paragraph("Professional Summary", heading_style))
                content.append(Paragraph(resume.summary, body_style))
                content.append(Spacer(1, 12))
            
            # Work Experience
            if resume.work_experience:
                content.append(Paragraph("Work Experience", heading_style))
                for exp in resume.work_experience:
                    # Job title and company
                    job_info = f"{exp.title}"
                    if exp.company:
                        job_info += f" - {exp.company}"
                    content.append(Paragraph(job_info, body_style))
                    
                    # Duration
                    if exp.start_date and exp.end_date:
                        duration = f"{exp.start_date} - {exp.end_date}"
                    elif exp.start_date:
                        duration = f"{exp.start_date} - Present"
                    else:
                        duration = ""
                    
                    if duration:
                        content.append(Paragraph(duration, body_style))
                    
                    # Description
                    if exp.description:
                        content.append(Paragraph(exp.description, bullet_style))
                    
                    content.append(Spacer(1, 12))
            
            # Education
            if resume.education:
                content.append(Paragraph("Education", heading_style))
                for edu in resume.education:
                    education_info = f"{edu.degree}"
                    if edu.field:
                        education_info += f" in {edu.field}"
                    if edu.institution:
                        education_info += f" - {edu.institution}"
                    if edu.graduation_date:
                        education_info += f" ({edu.graduation_date})"
                    
                    content.append(Paragraph(education_info, body_style))
                    content.append(Spacer(1, 6))
            
            # Skills
            if resume.skills:
                content.append(Paragraph("Skills", heading_style))
                
                # Group skills by category
                skills_by_category = {}
                for skill in resume.skills:
                    category = skill.subcategory or skill.category.value
                    if category not in skills_by_category:
                        skills_by_category[category] = []
                    skills_by_category[category].append(skill.name)
                
                for category, skills in skills_by_category.items():
                    skills_text = f"{category}: {', '.join(skills)}"
                    content.append(Paragraph(skills_text, body_style))
                    content.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(content)
            
            export_time = time.time() - start_time
            logger.info(f"PDF export completed in {export_time:.2f}s")
            logger.info(f"Exported to: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export resume to PDF: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def export_to_docx(self, resume: ParsedResume, filename: str = None, template_name: str = "Modern Professional") -> str:
        """
        Export resume to DOCX format with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume data to export
            filename (str): Output filename (optional)
            template_name (str): Template to use for export
            
        Returns:
            str: Path to exported DOCX file
            
        Raises:
            Exception: If DOCX export fails
        """
        try:
            logger.debug("Exporting resume to DOCX")
            start_time = time.time()
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"resume_{timestamp}.docx"
            
            # Ensure .docx extension
            if not filename.endswith('.docx'):
                filename += '.docx'
            
            # Create full path
            filepath = os.path.join(self.output_directory, filename)
            
            # Create DOCX document
            doc = Document()
            
            # Get styles
            docx_styles = self.export_templates["docx"]["styles"]
            
            # Header
            if resume.contact_info.name:
                title = doc.add_heading(resume.contact_info.name, 0)
                title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Contact information
            contact_info = []
            if resume.contact_info.email:
                contact_info.append(resume.contact_info.email)
            if resume.contact_info.phone:
                contact_info.append(resume.contact_info.phone)
            if resume.contact_info.location:
                contact_info.append(resume.contact_info.location)
            
            if contact_info:
                contact_para = doc.add_paragraph(" | ".join(contact_info))
                contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                contact_para.runs[0].font.size = Pt(10)
            
            # Professional Summary
            if resume.summary:
                doc.add_heading("Professional Summary", level=1)
                summary_para = doc.add_paragraph(resume.summary)
                summary_para.runs[0].font.size = Pt(10)
            
            # Work Experience
            if resume.work_experience:
                doc.add_heading("Work Experience", level=1)
                for exp in resume.work_experience:
                    # Job title and company
                    job_info = f"{exp.title}"
                    if exp.company:
                        job_info += f" - {exp.company}"
                    
                    job_para = doc.add_paragraph(job_info)
                    job_para.runs[0].font.bold = True
                    job_para.runs[0].font.size = Pt(11)
                    
                    # Duration
                    if exp.start_date and exp.end_date:
                        duration = f"{exp.start_date} - {exp.end_date}"
                    elif exp.start_date:
                        duration = f"{exp.start_date} - Present"
                    else:
                        duration = ""
                    
                    if duration:
                        duration_para = doc.add_paragraph(duration)
                        duration_para.runs[0].font.italic = True
                        duration_para.runs[0].font.size = Pt(10)
                    
                    # Description
                    if exp.description:
                        desc_para = doc.add_paragraph(exp.description)
                        desc_para.runs[0].font.size = Pt(10)
                    
                    doc.add_paragraph()  # Add space between experiences
            
            # Education
            if resume.education:
                doc.add_heading("Education", level=1)
                for edu in resume.education:
                    education_info = f"{edu.degree}"
                    if edu.field:
                        education_info += f" in {edu.field}"
                    if edu.institution:
                        education_info += f" - {edu.institution}"
                    if edu.graduation_date:
                        education_info += f" ({edu.graduation_date})"
                    
                    edu_para = doc.add_paragraph(education_info)
                    edu_para.runs[0].font.bold = True
                    edu_para.runs[0].font.size = Pt(11)
                    
                    doc.add_paragraph()  # Add space between education entries
            
            # Skills
            if resume.skills:
                doc.add_heading("Skills", level=1)
                
                # Group skills by category
                skills_by_category = {}
                for skill in resume.skills:
                    category = skill.subcategory or skill.category.value
                    if category not in skills_by_category:
                        skills_by_category[category] = []
                    skills_by_category[category].append(skill.name)
                
                for category, skills in skills_by_category.items():
                    skills_text = f"{category}: {', '.join(skills)}"
                    skills_para = doc.add_paragraph(skills_text)
                    skills_para.runs[0].font.size = Pt(10)
            
            # Save document
            doc.save(filepath)
            
            export_time = time.time() - start_time
            logger.info(f"DOCX export completed in {export_time:.2f}s")
            logger.info(f"Exported to: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export resume to DOCX: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def export_to_html(self, resume: ParsedResume, filename: str = None, template_name: str = "Modern Professional") -> str:
        """
        Export resume to HTML format with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume data to export
            filename (str): Output filename (optional)
            template_name (str): Template to use for export
            
        Returns:
            str: Path to exported HTML file
            
        Raises:
            Exception: If HTML export fails
        """
        try:
            logger.debug("Exporting resume to HTML")
            start_time = time.time()
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"resume_{timestamp}.html"
            
            # Ensure .html extension
            if not filename.endswith('.html'):
                filename += '.html'
            
            # Create full path
            filepath = os.path.join(self.output_directory, filename)
            
            # Get HTML template
            html_template = self.export_templates["html"]["template"]
            template = Template(html_template)
            
            # Render HTML
            html_content = template.render(resume=resume)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            export_time = time.time() - start_time
            logger.info(f"HTML export completed in {export_time:.2f}s")
            logger.info(f"Exported to: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export resume to HTML: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def export_to_json(self, resume: ParsedResume, filename: str = None) -> str:
        """
        Export resume to JSON format with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume data to export
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to exported JSON file
            
        Raises:
            Exception: If JSON export fails
        """
        try:
            logger.debug("Exporting resume to JSON")
            start_time = time.time()
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"resume_{timestamp}.json"
            
            # Ensure .json extension
            if not filename.endswith('.json'):
                filename += '.json'
            
            # Create full path
            filepath = os.path.join(self.output_directory, filename)
            
            # Convert resume to dictionary
            resume_dict = resume.dict() if hasattr(resume, 'dict') else resume.__dict__
            
            # Add export metadata
            export_data = {
                "resume_data": resume_dict,
                "export_metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "export_format": "json",
                    "version": "1.0"
                }
            }
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            export_time = time.time() - start_time
            logger.info(f"JSON export completed in {export_time:.2f}s")
            logger.info(f"Exported to: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to export resume to JSON: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            raise
    
    def export_multiple_formats(self, resume: ParsedResume, formats: List[str] = None, 
                               base_filename: str = None) -> Dict[str, str]:
        """
        Export resume to multiple formats simultaneously.
        
        Args:
            resume (ParsedResume): Resume data to export
            formats (List[str]): List of formats to export (pdf, docx, html, json)
            base_filename (str): Base filename for all exports
            
        Returns:
            Dict[str, str]: Dictionary mapping format to file path
            
        Raises:
            Exception: If multi-format export fails
        """
        try:
            logger.debug(f"Exporting resume to multiple formats: {formats}")
            start_time = time.time()
            
            if formats is None:
                formats = ["pdf", "docx", "html", "json"]
            
            # Generate base filename if not provided
            if not base_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_filename = f"resume_{timestamp}"
            
            exported_files = {}
            
            # Export to each format
            for format_type in formats:
                try:
                    if format_type == "pdf":
                        filepath = self.export_to_pdf(resume, f"{base_filename}.pdf")
                    elif format_type == "docx":
                        filepath = self.export_to_docx(resume, f"{base_filename}.docx")
                    elif format_type == "html":
                        filepath = self.export_to_html(resume, f"{base_filename}.html")
                    elif format_type == "json":
                        filepath = self.export_to_json(resume, f"{base_filename}.json")
                    else:
                        logger.warning(f"Unsupported format: {format_type}")
                        continue
                    
                    exported_files[format_type] = filepath
                    logger.debug(f"Successfully exported to {format_type}: {filepath}")
                    
                except Exception as e:
                    logger.error(f"Failed to export to {format_type}: {e}")
                    continue
            
            export_time = time.time() - start_time
            logger.info(f"Multi-format export completed in {export_time:.2f}s")
            logger.info(f"Exported {len(exported_files)} formats successfully")
            
            return exported_files
            
        except Exception as e:
            logger.error(f"Failed to export resume to multiple formats: {e}")
            return {}
    
    def get_export_summary(self, exported_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Get summary of exported files.
        
        Args:
            exported_files (Dict[str, str]): Dictionary of exported files
            
        Returns:
            Dict[str, Any]: Export summary with statistics
        """
        try:
            logger.debug("Generating export summary")
            
            if not exported_files:
                return {
                    "total_files": 0,
                    "formats": [],
                    "file_sizes": {},
                    "export_timestamp": datetime.now().isoformat()
                }
            
            # Calculate file sizes
            file_sizes = {}
            for format_type, filepath in exported_files.items():
                try:
                    size = os.path.getsize(filepath)
                    file_sizes[format_type] = {
                        "size_bytes": size,
                        "size_mb": round(size / (1024 * 1024), 2)
                    }
                except Exception as e:
                    logger.warning(f"Failed to get size for {filepath}: {e}")
                    file_sizes[format_type] = {"size_bytes": 0, "size_mb": 0}
            
            summary = {
                "total_files": len(exported_files),
                "formats": list(exported_files.keys()),
                "file_sizes": file_sizes,
                "export_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Export summary generated: {len(exported_files)} files")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate export summary: {e}")
            return {
                "total_files": 0,
                "formats": [],
                "file_sizes": {},
                "export_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def cleanup_old_exports(self, max_age_days: int = 30) -> int:
        """
        Clean up old exported files.
        
        Args:
            max_age_days (int): Maximum age of files to keep (in days)
            
        Returns:
            int: Number of files cleaned up
        """
        try:
            logger.debug(f"Cleaning up exports older than {max_age_days} days")
            
            if not os.path.exists(self.output_directory):
                return 0
            
            cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
            cleaned_count = 0
            
            for filename in os.listdir(self.output_directory):
                filepath = os.path.join(self.output_directory, filename)
                
                if os.path.isfile(filepath):
                    file_mtime = os.path.getmtime(filepath)
                    
                    if file_mtime < cutoff_time:
                        try:
                            os.remove(filepath)
                            cleaned_count += 1
                            logger.debug(f"Removed old file: {filename}")
                        except Exception as e:
                            logger.warning(f"Failed to remove {filename}: {e}")
            
            logger.info(f"Cleaned up {cleaned_count} old export files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old exports: {e}")
            return 0
