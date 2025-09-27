"""
Export Service for Resume/CV AI Application
Handles resume and data export operations.

This module provides:
- Resume export to various formats
- Data export and serialization
- Export template management
- Export validation and processing
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from utils.logger import setup_logger
from utils.export_handler import export_handler

# Initialize logger with module-specific name
logger = setup_logger("export_service")

class ExportService:
    """
    Export service class with comprehensive logging.
    
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
        _export_history (List[Dict]): Export history tracking
        _export_templates (Dict[str, Dict]): Export templates
    """
    
    def __init__(self):
        """Initialize export service with comprehensive logging."""
        logger.info("Initializing Export Service")
        self._initialization_time = datetime.now()
        
        # Initialize export components
        self._export_history = []
        self._export_templates = {}
        
        try:
            # Load export templates
            self._load_export_templates()
            
            logger.info("Export Service initialized successfully")
            logger.info(f"Loaded {len(self._export_templates)} export templates")
            
        except Exception as e:
            logger.error(f"Export Service initialization failed: {e}")
            raise
    
    def _load_export_templates(self):
        """Load export templates."""
        try:
            # Get templates from export handler
            self._export_templates = export_handler.get_export_templates()
            
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
            logger.info(f"Exporting resume to {format} format using {template} template")
            start_time = time.time()
            
            # Validate export parameters
            validation_result = self._validate_export_parameters(format, template, resume_data)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['error'],
                    'validation_errors': validation_result['errors']
                }
            
            # Export using export handler
            export_result = export_handler.export_resume(resume_data, format, template, filename)
            
            if export_result['success']:
                # Add to export history
                self._add_to_export_history(export_result, resume_data, format, template)
                
                export_time = time.time() - start_time
                export_result['export_time'] = round(export_time, 2)
                
                logger.info(f"Resume exported successfully in {export_time:.2f}s")
            else:
                logger.error(f"Resume export failed: {export_result.get('error', 'Unknown error')}")
            
            return export_result
            
        except Exception as e:
            logger.error(f"Failed to export resume: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_export_parameters(self, format: str, template: str, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate export parameters."""
        try:
            errors = []
            
            # Validate format
            supported_formats = export_handler.get_supported_formats()
            if format not in [f.lstrip('.') for f in supported_formats]:
                errors.append(f"Unsupported format: {format}")
            
            # Validate template
            if template not in self._export_templates:
                errors.append(f"Unknown template: {template}")
            
            # Validate resume data
            if not resume_data:
                errors.append("Resume data is empty")
            
            # Check required fields
            required_fields = ['contact', 'summary', 'experience', 'education', 'skills']
            missing_fields = [field for field in required_fields if field not in resume_data]
            if missing_fields:
                errors.append(f"Missing required fields: {', '.join(missing_fields)}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Failed to validate export parameters: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def _add_to_export_history(self, export_result: Dict[str, Any], resume_data: Dict[str, Any],
                              format: str, template: str):
        """Add export to history."""
        try:
            history_entry = {
                'export_id': f"export_{len(self._export_history) + 1}",
                'filename': export_result.get('filename', ''),
                'format': format,
                'template': template,
                'file_size': export_result.get('file_size', 0),
                'export_time': export_result.get('export_time', 0),
                'timestamp': datetime.now().isoformat(),
                'resume_summary': {
                    'name': resume_data.get('contact', {}).get('name', 'Unknown'),
                    'experience_years': self._calculate_experience_years(resume_data),
                    'skills_count': len(resume_data.get('skills', []))
                }
            }
            
            self._export_history.append(history_entry)
            
            # Keep only last 100 exports
            if len(self._export_history) > 100:
                self._export_history = self._export_history[-100:]
            
            logger.debug(f"Added export to history: {history_entry['export_id']}")
            
        except Exception as e:
            logger.error(f"Failed to add export to history: {e}")
    
    def _calculate_experience_years(self, resume_data: Dict[str, Any]) -> float:
        """Calculate total years of experience from resume data."""
        try:
            experience = resume_data.get('experience', [])
            total_years = 0
            
            for exp in experience:
                # Try to extract years from description
                description = exp.get('description', '')
                if description:
                    # Simple heuristic: look for year patterns
                    import re
                    year_pattern = r'(\d+)\s*years?'
                    matches = re.findall(year_pattern, description.lower())
                    if matches:
                        total_years += sum(int(match) for match in matches)
                    else:
                        # Default to 1 year per experience entry
                        total_years += 1
            
            return total_years
            
        except Exception as e:
            logger.error(f"Failed to calculate experience years: {e}")
            return 0.0
    
    def get_export_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get export history.
        
        Args:
            limit (int): Maximum number of exports to return
            
        Returns:
            List[Dict[str, Any]]: Export history
        """
        try:
            return self._export_history[-limit:] if limit > 0 else self._export_history
            
        except Exception as e:
            logger.error(f"Failed to get export history: {e}")
            return []
    
    def get_export_templates(self) -> Dict[str, Any]:
        """
        Get available export templates.
        
        Returns:
            Dict[str, Any]: Export templates
        """
        return self._export_templates
    
    def get_supported_formats(self) -> List[str]:
        """
        Get supported export formats.
        
        Returns:
            List[str]: Supported formats
        """
        try:
            return [f.lstrip('.') for f in export_handler.get_supported_formats()]
        except Exception as e:
            logger.error(f"Failed to get supported formats: {e}")
            return []
    
    def export_analysis_data(self, analysis_data: Dict[str, Any], format: str = 'json') -> Dict[str, Any]:
        """
        Export analysis data.
        
        Args:
            analysis_data (Dict[str, Any]): Analysis data to export
            format (str): Export format
            
        Returns:
            Dict[str, Any]: Export result
        """
        try:
            logger.info(f"Exporting analysis data to {format} format")
            start_time = time.time()
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.{format}"
            
            # Export data
            if format == 'json':
                result = self._export_json_data(analysis_data, filename)
            elif format == 'csv':
                result = self._export_csv_data(analysis_data, filename)
            else:
                return {'success': False, 'error': f'Unsupported format: {format}'}
            
            if result['success']:
                export_time = time.time() - start_time
                result['export_time'] = round(export_time, 2)
                
                logger.info(f"Analysis data exported successfully in {export_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to export analysis data: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_json_data(self, data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """Export data to JSON format."""
        try:
            import json
            from pathlib import Path
            
            # Create exports directory if it doesn't exist
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)
            
            # Write JSON file
            file_path = exports_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            return {
                'success': True,
                'filename': filename,
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"Failed to export JSON data: {e}")
            return {'success': False, 'error': str(e)}
    
    def _export_csv_data(self, data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """Export data to CSV format."""
        try:
            import csv
            from pathlib import Path
            
            # Create exports directory if it doesn't exist
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)
            
            # Write CSV file
            file_path = exports_dir / filename
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write headers
                writer.writerow(['Field', 'Value'])
                
                # Write data
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        value = str(value)
                    writer.writerow([key, value])
            
            return {
                'success': True,
                'filename': filename,
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"Failed to export CSV data: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_export_statistics(self) -> Dict[str, Any]:
        """
        Get export statistics.
        
        Returns:
            Dict[str, Any]: Export statistics
        """
        try:
            if not self._export_history:
                return {
                    'total_exports': 0,
                    'formats_used': {},
                    'templates_used': {},
                    'total_file_size': 0,
                    'average_export_time': 0
                }
            
            # Calculate statistics
            total_exports = len(self._export_history)
            formats_used = {}
            templates_used = {}
            total_file_size = 0
            total_export_time = 0
            
            for export in self._export_history:
                # Count formats
                format_name = export.get('format', 'unknown')
                formats_used[format_name] = formats_used.get(format_name, 0) + 1
                
                # Count templates
                template_name = export.get('template', 'unknown')
                templates_used[template_name] = templates_used.get(template_name, 0) + 1
                
                # Sum file sizes and export times
                total_file_size += export.get('file_size', 0)
                total_export_time += export.get('export_time', 0)
            
            return {
                'total_exports': total_exports,
                'formats_used': formats_used,
                'templates_used': templates_used,
                'total_file_size': total_file_size,
                'average_export_time': round(total_export_time / total_exports, 2) if total_exports > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get export statistics: {e}")
            return {'error': str(e)}
    
    def cleanup_old_exports(self, max_age_days: int = 30) -> int:
        """
        Clean up old export files.
        
        Args:
            max_age_days (int): Maximum age of files in days
            
        Returns:
            int: Number of files cleaned up
        """
        try:
            # Use export handler's cleanup function
            max_age_hours = max_age_days * 24
            cleaned_count = export_handler.cleanup_exports(max_age_hours)
            
            logger.info(f"Cleaned up {cleaned_count} old export files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old exports: {e}")
            return 0
    
    def get_export_service_info(self) -> Dict[str, Any]:
        """
        Get export service information and statistics.
        
        Returns:
            Dict[str, Any]: Export service information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "export_templates_count": len(self._export_templates),
                "export_history_count": len(self._export_history),
                "supported_formats": self.get_supported_formats(),
                "export_statistics": self.get_export_statistics(),
                "export_service_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get export service info: {e}")
            return {
                "error": str(e),
                "export_service_timestamp": datetime.now().isoformat()
            }
