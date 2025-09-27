"""
Export Handler Utilities for Resume/CV AI Application
Provides export functionality for resumes and data.

This module provides:
- Resume export to various formats
- Data export and serialization
- Export template management
- Export validation and processing
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

from .logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("export_handler")

class ExportHandler:
    """
    Export handler utilities class with comprehensive logging.
    
    This class provides export functionality including resume export,
    data serialization, template management, and export validation for
    the Resume/CV AI application.
    
    Key Features:
    - Resume export to various formats
    - Data export and serialization
    - Export template management
    - Export validation and processing
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _export_dir (str): Directory for exported files
        _supported_formats (set): Set of supported export formats
        _export_templates (dict): Dictionary of export templates
    """
    
    def __init__(self, export_dir: str = "exports"):
        """
        Initialize export handler with comprehensive logging.
        
        Args:
            export_dir (str): Directory for exported files
        """
        logger.info("Initializing Export Handler")
        self._initialization_time = datetime.now()
        
        # Set export directory
        self._export_dir = export_dir
        
        # Set supported formats
        self._supported_formats = {'.pdf', '.docx', '.txt', '.json', '.html'}
        
        # Initialize export templates
        self._export_templates = {}
        
        try:
            # Create export directory
            self._ensure_export_directory()
            
            # Load export templates
            self._load_export_templates()
            
            logger.info("Export Handler initialized successfully")
            logger.info(f"Export directory: {self._export_dir}")
            logger.info(f"Supported formats: {self._supported_formats}")
            logger.info(f"Loaded {len(self._export_templates)} export templates")
            
        except Exception as e:
            logger.error(f"Export Handler initialization failed: {e}")
            raise
    
    def _ensure_export_directory(self):
        """Ensure export directory exists."""
        try:
            Path(self._export_dir).mkdir(parents=True, exist_ok=True)
            logger.debug("Export directory created successfully")
        except Exception as e:
            logger.error(f"Failed to create export directory: {e}")
            raise
    
    def _load_export_templates(self):
        """Load export templates."""
        try:
            # Default export templates
            self._export_templates = {
                'professional': {
                    'name': 'Professional',
                    'description': 'Clean and professional resume template',
                    'sections': ['contact', 'summary', 'experience', 'education', 'skills'],
                    'formatting': {
                        'font_family': 'Arial',
                        'font_size': 11,
                        'line_spacing': 1.15,
                        'margins': {'top': 1, 'bottom': 1, 'left': 1, 'right': 1}
                    }
                },
                'modern': {
                    'name': 'Modern',
                    'description': 'Contemporary resume template with visual elements',
                    'sections': ['contact', 'summary', 'experience', 'education', 'skills', 'projects'],
                    'formatting': {
                        'font_family': 'Calibri',
                        'font_size': 11,
                        'line_spacing': 1.2,
                        'margins': {'top': 0.8, 'bottom': 0.8, 'left': 0.8, 'right': 0.8}
                    }
                },
                'creative': {
                    'name': 'Creative',
                    'description': 'Creative resume template for design professionals',
                    'sections': ['contact', 'summary', 'experience', 'education', 'skills', 'portfolio'],
                    'formatting': {
                        'font_family': 'Helvetica',
                        'font_size': 10,
                        'line_spacing': 1.1,
                        'margins': {'top': 0.5, 'bottom': 0.5, 'left': 0.5, 'right': 0.5}
                    }
                }
            }
            
            logger.debug(f"Loaded {len(self._export_templates)} export templates")
            
        except Exception as e:
            logger.error(f"Failed to load export templates: {e}")
            self._export_templates = {}
    
    def export_resume(self, resume_data: Dict[str, Any], format: str, 
                     template: str = 'professional', filename: str = None) -> Dict[str, Any]:
        """
        Export resume to specified format.
        
        Args:
            resume_data (Dict[str, Any]): Resume data to export
            format (str): Export format (pdf, docx, txt, html, json)
            template (str): Export template to use
            filename (str): Custom filename (optional)
            
        Returns:
            Dict[str, Any]: Export result
        """
        try:
            # Validate format
            if format not in [f.lstrip('.') for f in self._supported_formats]:
                return {'success': False, 'error': f'Unsupported format: {format}'}
            
            # Validate template
            if template not in self._export_templates:
                return {'success': False, 'error': f'Unknown template: {template}'}
            
            # Generate filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"resume_{timestamp}.{format}"
            
            # Create export path
            export_path = Path(self._export_dir) / filename
            
            # Export based on format
            if format == 'json':
                result = self._export_to_json(resume_data, export_path)
            elif format == 'txt':
                result = self._export_to_txt(resume_data, export_path, template)
            elif format == 'html':
                result = self._export_to_html(resume_data, export_path, template)
            elif format == 'pdf':
                result = self._export_to_pdf(resume_data, export_path, template)
            elif format == 'docx':
                result = self._export_to_docx(resume_data, export_path, template)
            else:
                return {'success': False, 'error': f'Export format {format} not implemented'}
            
            if result['success']:
                result['filename'] = filename
                result['export_path'] = str(export_path)
                result['file_size'] = os.path.getsize(export_path)
                result['export_time'] = datetime.now().isoformat()
                
                logger.info(f"Resume exported successfully: {filename}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to export resume: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_to_json(self, resume_data: Dict[str, Any], export_path: Path) -> Dict[str, Any]:
        """Export resume to JSON format."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(resume_data, f, indent=2, ensure_ascii=False, default=str)
            
            return {'success': True, 'format': 'json'}
            
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_to_txt(self, resume_data: Dict[str, Any], export_path: Path, 
                      template: str) -> Dict[str, Any]:
        """Export resume to TXT format."""
        try:
            template_config = self._export_templates[template]
            
            # Generate text content
            content = self._generate_text_content(resume_data, template_config)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {'success': True, 'format': 'txt'}
            
        except Exception as e:
            logger.error(f"Failed to export to TXT: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_to_html(self, resume_data: Dict[str, Any], export_path: Path, 
                       template: str) -> Dict[str, Any]:
        """Export resume to HTML format."""
        try:
            template_config = self._export_templates[template]
            
            # Generate HTML content
            content = self._generate_html_content(resume_data, template_config)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {'success': True, 'format': 'html'}
            
        except Exception as e:
            logger.error(f"Failed to export to HTML: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_to_pdf(self, resume_data: Dict[str, Any], export_path: Path, 
                      template: str) -> Dict[str, Any]:
        """Export resume to PDF format."""
        try:
            # For now, return a placeholder implementation
            # In a real implementation, you would use libraries like reportlab or weasyprint
            
            # Generate HTML content first
            template_config = self._export_templates[template]
            html_content = self._generate_html_content(resume_data, template_config)
            
            # Save as HTML for now (PDF conversion would require additional libraries)
            html_path = export_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Copy HTML to PDF path (placeholder)
            export_path.write_text(html_content)
            
            return {'success': True, 'format': 'pdf', 'note': 'PDF export requires additional libraries'}
            
        except Exception as e:
            logger.error(f"Failed to export to PDF: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_to_docx(self, resume_data: Dict[str, Any], export_path: Path, 
                       template: str) -> Dict[str, Any]:
        """Export resume to DOCX format."""
        try:
            # For now, return a placeholder implementation
            # In a real implementation, you would use libraries like python-docx
            
            # Generate text content
            template_config = self._export_templates[template]
            text_content = self._generate_text_content(resume_data, template_config)
            
            # Save as text for now (DOCX conversion would require additional libraries)
            export_path.write_text(text_content)
            
            return {'success': True, 'format': 'docx', 'note': 'DOCX export requires additional libraries'}
            
        except Exception as e:
            logger.error(f"Failed to export to DOCX: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_text_content(self, resume_data: Dict[str, Any], 
                              template_config: Dict[str, Any]) -> str:
        """Generate text content from resume data."""
        try:
            content = []
            
            # Header
            if 'contact' in resume_data:
                contact = resume_data['contact']
                content.append(f"{contact.get('name', '')}")
                content.append(f"{contact.get('email', '')} | {contact.get('phone', '')}")
                content.append(f"{contact.get('location', '')}")
                content.append("")
            
            # Summary
            if 'summary' in resume_data:
                content.append("PROFESSIONAL SUMMARY")
                content.append("-" * 20)
                content.append(resume_data['summary'])
                content.append("")
            
            # Experience
            if 'experience' in resume_data:
                content.append("EXPERIENCE")
                content.append("-" * 20)
                for exp in resume_data['experience']:
                    content.append(f"{exp.get('title', '')} at {exp.get('company', '')}")
                    content.append(f"{exp.get('start_date', '')} - {exp.get('end_date', '')}")
                    content.append(exp.get('description', ''))
                    content.append("")
            
            # Education
            if 'education' in resume_data:
                content.append("EDUCATION")
                content.append("-" * 20)
                for edu in resume_data['education']:
                    content.append(f"{edu.get('degree', '')} from {edu.get('school', '')}")
                    content.append(f"{edu.get('graduation_date', '')}")
                    content.append("")
            
            # Skills
            if 'skills' in resume_data:
                content.append("SKILLS")
                content.append("-" * 20)
                content.append(", ".join(resume_data['skills']))
                content.append("")
            
            return "\n".join(content)
            
        except Exception as e:
            logger.error(f"Failed to generate text content: {e}")
            return "Error generating content"
    
    def _generate_html_content(self, resume_data: Dict[str, Any], 
                              template_config: Dict[str, Any]) -> str:
        """Generate HTML content from resume data."""
        try:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Resume</title>
                <style>
                    body {{ font-family: {template_config['formatting']['font_family']}; 
                           font-size: {template_config['formatting']['font_size']}pt; 
                           line-height: {template_config['formatting']['line_spacing']}; 
                           margin: {template_config['formatting']['margins']['top']}in; }}
                    h1 {{ color: #333; }}
                    h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
                    .section {{ margin-bottom: 20px; }}
                </style>
            </head>
            <body>
            """
            
            # Header
            if 'contact' in resume_data:
                contact = resume_data['contact']
                html += f"""
                <div class="section">
                    <h1>{contact.get('name', '')}</h1>
                    <p>{contact.get('email', '')} | {contact.get('phone', '')}</p>
                    <p>{contact.get('location', '')}</p>
                </div>
                """
            
            # Summary
            if 'summary' in resume_data:
                html += f"""
                <div class="section">
                    <h2>Professional Summary</h2>
                    <p>{resume_data['summary']}</p>
                </div>
                """
            
            # Experience
            if 'experience' in resume_data:
                html += "<div class='section'><h2>Experience</h2>"
                for exp in resume_data['experience']:
                    html += f"""
                    <div>
                        <h3>{exp.get('title', '')} at {exp.get('company', '')}</h3>
                        <p><em>{exp.get('start_date', '')} - {exp.get('end_date', '')}</em></p>
                        <p>{exp.get('description', '')}</p>
                    </div>
                    """
                html += "</div>"
            
            # Education
            if 'education' in resume_data:
                html += "<div class='section'><h2>Education</h2>"
                for edu in resume_data['education']:
                    html += f"""
                    <div>
                        <h3>{edu.get('degree', '')} from {edu.get('school', '')}</h3>
                        <p><em>{edu.get('graduation_date', '')}</em></p>
                    </div>
                    """
                html += "</div>"
            
            # Skills
            if 'skills' in resume_data:
                html += f"""
                <div class="section">
                    <h2>Skills</h2>
                    <p>{", ".join(resume_data['skills'])}</p>
                </div>
                """
            
            html += "</body></html>"
            return html
            
        except Exception as e:
            logger.error(f"Failed to generate HTML content: {e}")
            return "<html><body><p>Error generating content</p></body></html>"
    
    def get_export_templates(self) -> Dict[str, Any]:
        """
        Get available export templates.
        
        Returns:
            Dict[str, Any]: Dictionary of export templates
        """
        return self._export_templates
    
    def get_supported_formats(self) -> List[str]:
        """
        Get supported export formats.
        
        Returns:
            List[str]: List of supported formats
        """
        return list(self._supported_formats)
    
    def cleanup_exports(self, max_age_hours: int = 168) -> int:
        """
        Clean up exported files older than specified age.
        
        Args:
            max_age_hours (int): Maximum age of files in hours (default: 1 week)
            
        Returns:
            int: Number of files cleaned up
        """
        try:
            cleaned_count = 0
            current_time = datetime.now()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in Path(self._export_dir).iterdir():
                if file_path.is_file():
                    file_age = current_time.timestamp() - file_path.stat().st_mtime
                    
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.debug(f"Cleaned up export file: {file_path}")
            
            logger.info(f"Cleaned up {cleaned_count} export files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup exports: {e}")
            return 0
    
    def get_export_handler_info(self) -> Dict[str, Any]:
        """
        Get export handler information and statistics.
        
        Returns:
            Dict[str, Any]: Export handler information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "export_directory": self._export_dir,
                "supported_formats": list(self._supported_formats),
                "export_templates": list(self._export_templates.keys()),
                "export_handler_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get export handler info: {e}")
            return {
                "error": str(e),
                "export_handler_timestamp": datetime.now().isoformat()
            }

# Create global export handler instance
export_handler = ExportHandler()

# Export commonly used functions
export_resume = export_handler.export_resume
get_export_templates = export_handler.get_export_templates
get_supported_formats = export_handler.get_supported_formats
cleanup_exports = export_handler.cleanup_exports