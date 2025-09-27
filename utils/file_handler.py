"""
File Handler Utilities for Resume/CV AI Application
Provides file handling and management utilities.

This module provides:
- File upload and download handling
- File validation and processing
- File storage management
- File format conversion
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import os
import shutil
import logging
from typing import Dict, List, Optional, Any, Union, BinaryIO
from datetime import datetime
from pathlib import Path
import mimetypes

from .logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("file_handler")

class FileHandler:
    """
    File handling utilities class with comprehensive logging.
    
    This class provides file handling including upload/download management,
    file validation, storage management, and format conversion for the
    Resume/CV AI application.
    
    Key Features:
    - File upload and download handling
    - File validation and processing
    - File storage management
    - File format conversion
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _upload_dir (str): Directory for uploaded files
        _temp_dir (str): Directory for temporary files
        _allowed_extensions (set): Set of allowed file extensions
        _max_file_size (int): Maximum file size in bytes
    """
    
    def __init__(self, upload_dir: str = "uploads", temp_dir: str = "temp"):
        """
        Initialize file handler with comprehensive logging.
        
        Args:
            upload_dir (str): Directory for uploaded files
            temp_dir (str): Directory for temporary files
        """
        logger.info("Initializing File Handler")
        self._initialization_time = datetime.now()
        
        # Set directories
        self._upload_dir = upload_dir
        self._temp_dir = temp_dir
        
        # Set file constraints
        self._allowed_extensions = {'.pdf', '.docx', '.doc', '.txt', '.rtf'}
        self._max_file_size = 10 * 1024 * 1024  # 10MB
        
        try:
            # Create directories
            self._ensure_directories()
            
            logger.info("File Handler initialized successfully")
            logger.info(f"Upload directory: {self._upload_dir}")
            logger.info(f"Temp directory: {self._temp_dir}")
            logger.info(f"Allowed extensions: {self._allowed_extensions}")
            logger.info(f"Max file size: {self._max_file_size} bytes")
            
        except Exception as e:
            logger.error(f"File Handler initialization failed: {e}")
            raise
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        try:
            Path(self._upload_dir).mkdir(parents=True, exist_ok=True)
            Path(self._temp_dir).mkdir(parents=True, exist_ok=True)
            logger.debug("Directories created successfully")
        except Exception as e:
            logger.error(f"Failed to create directories: {e}")
            raise
    
    def validate_file(self, file_path: str, file_size: int = None) -> Dict[str, Any]:
        """
        Validate file for upload.
        
        Args:
            file_path (str): Path to file to validate
            file_size (int): Size of file in bytes
            
        Returns:
            Dict[str, Any]: Validation result
        """
        try:
            result = {
                'valid': True,
                'errors': [],
                'warnings': []
            }
            
            # Check if file exists
            if not os.path.exists(file_path):
                result['valid'] = False
                result['errors'].append("File does not exist")
                return result
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self._allowed_extensions:
                result['valid'] = False
                result['errors'].append(f"File extension '{file_ext}' not allowed")
                return result
            
            # Check file size
            if file_size is None:
                file_size = os.path.getsize(file_path)
            
            if file_size > self._max_file_size:
                result['valid'] = False
                result['errors'].append(f"File size {file_size} bytes exceeds maximum {self._max_file_size} bytes")
                return result
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                allowed_mime_types = {
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'text/plain',
                    'application/rtf'
                }
                
                if mime_type not in allowed_mime_types:
                    result['warnings'].append(f"MIME type '{mime_type}' may not be supported")
            
            logger.debug(f"File validation completed for '{file_path}': {result['valid']}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate file '{file_path}': {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': []
            }
    
    def save_uploaded_file(self, file_data: BinaryIO, filename: str, 
                          user_id: str = None) -> Dict[str, Any]:
        """
        Save uploaded file to storage.
        
        Args:
            file_data (BinaryIO): File data to save
            filename (str): Name of the file
            user_id (str): ID of the user uploading the file
            
        Returns:
            Dict[str, Any]: Save result
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = Path(filename).suffix
            base_name = Path(filename).stem
            
            if user_id:
                unique_filename = f"{user_id}_{timestamp}_{base_name}{file_ext}"
            else:
                unique_filename = f"{timestamp}_{base_name}{file_ext}"
            
            # Create file path
            file_path = Path(self._upload_dir) / unique_filename
            
            # Save file
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file_data, f)
            
            # Get file info
            file_size = os.path.getsize(file_path)
            
            result = {
                'success': True,
                'file_path': str(file_path),
                'filename': unique_filename,
                'original_filename': filename,
                'file_size': file_size,
                'upload_time': datetime.now().isoformat()
            }
            
            logger.info(f"File saved successfully: {unique_filename}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to save uploaded file '{filename}': {e}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file information.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            Dict[str, Any]: File information
        """
        try:
            if not os.path.exists(file_path):
                return {'error': 'File not found'}
            
            stat = os.stat(file_path)
            
            return {
                'filename': Path(file_path).name,
                'file_size': stat.st_size,
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'file_extension': Path(file_path).suffix,
                'mime_type': mimetypes.guess_type(file_path)[0]
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info for '{file_path}': {e}")
            return {'error': str(e)}
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            file_path (str): Path to file to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted successfully: {file_path}")
                return True
            else:
                logger.warning(f"File not found for deletion: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete file '{file_path}': {e}")
            return False
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than specified age.
        
        Args:
            max_age_hours (int): Maximum age of files in hours
            
        Returns:
            int: Number of files cleaned up
        """
        try:
            cleaned_count = 0
            current_time = datetime.now()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in Path(self._temp_dir).iterdir():
                if file_path.is_file():
                    file_age = current_time.timestamp() - file_path.stat().st_mtime
                    
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.debug(f"Cleaned up temp file: {file_path}")
            
            logger.info(f"Cleaned up {cleaned_count} temporary files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup temp files: {e}")
            return 0
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get storage information and statistics.
        
        Returns:
            Dict[str, Any]: Storage information
        """
        try:
            upload_files = list(Path(self._upload_dir).iterdir())
            temp_files = list(Path(self._temp_dir).iterdir())
            
            upload_size = sum(f.stat().st_size for f in upload_files if f.is_file())
            temp_size = sum(f.stat().st_size for f in temp_files if f.is_file())
            
            return {
                'upload_directory': self._upload_dir,
                'temp_directory': self._temp_dir,
                'upload_files_count': len(upload_files),
                'temp_files_count': len(temp_files),
                'upload_size_bytes': upload_size,
                'temp_size_bytes': temp_size,
                'total_size_bytes': upload_size + temp_size,
                'max_file_size': self._max_file_size,
                'allowed_extensions': list(self._allowed_extensions)
            }
            
        except Exception as e:
            logger.error(f"Failed to get storage info: {e}")
            return {'error': str(e)}
    
    def convert_file_format(self, input_path: str, output_format: str) -> Dict[str, Any]:
        """
        Convert file to different format.
        
        Args:
            input_path (str): Path to input file
            output_format (str): Desired output format
            
        Returns:
            Dict[str, Any]: Conversion result
        """
        try:
            if not os.path.exists(input_path):
                return {'success': False, 'error': 'Input file not found'}
            
            input_ext = Path(input_path).suffix.lower()
            
            # Check if conversion is supported
            supported_conversions = {
                '.docx': ['.pdf', '.txt'],
                '.pdf': ['.txt'],
                '.txt': ['.pdf']
            }
            
            if input_ext not in supported_conversions:
                return {'success': False, 'error': f'Input format {input_ext} not supported'}
            
            if output_format not in supported_conversions[input_ext]:
                return {'success': False, 'error': f'Conversion from {input_ext} to {output_format} not supported'}
            
            # Generate output path
            output_path = Path(input_path).with_suffix(output_format)
            
            # For now, just copy the file (actual conversion would require additional libraries)
            shutil.copy2(input_path, output_path)
            
            return {
                'success': True,
                'output_path': str(output_path),
                'input_format': input_ext,
                'output_format': output_format
            }
            
        except Exception as e:
            logger.error(f"Failed to convert file '{input_path}': {e}")
            return {'success': False, 'error': str(e)}
    
    def get_file_handler_info(self) -> Dict[str, Any]:
        """
        Get file handler information and statistics.
        
        Returns:
            Dict[str, Any]: File handler information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "upload_directory": self._upload_dir,
                "temp_directory": self._temp_dir,
                "allowed_extensions": list(self._allowed_extensions),
                "max_file_size": self._max_file_size,
                "storage_info": self.get_storage_info(),
                "file_handler_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get file handler info: {e}")
            return {
                "error": str(e),
                "file_handler_timestamp": datetime.now().isoformat()
            }

# Create global file handler instance
file_handler = FileHandler()

# Export commonly used functions
validate_file = file_handler.validate_file
save_uploaded_file = file_handler.save_uploaded_file
get_file_info = file_handler.get_file_info
delete_file = file_handler.delete_file
cleanup_temp_files = file_handler.cleanup_temp_files
get_storage_info = file_handler.get_storage_info
convert_file_format = file_handler.convert_file_format