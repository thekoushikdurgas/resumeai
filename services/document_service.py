"""
Document Service for Resume/CV AI Application
Handles document processing and management.

This module provides:
- Document upload and processing
- Document format conversion
- Document validation
- Document storage management
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

from utils.logger import setup_logger
from utils.file_handler import file_handler

# Initialize logger with module-specific name
logger = setup_logger("document_service")

class DocumentService:
    """
    Document service class with comprehensive logging.
    
    This class provides document processing including upload, conversion,
    validation, and storage management for the Resume/CV AI application.
    
    Key Features:
    - Document upload and processing
    - Document format conversion
    - Document validation
    - Document storage management
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _supported_formats (set): Supported document formats
        _processing_queue (List[Dict]): Document processing queue
        _processed_documents (Dict[str, Dict]): Processed documents cache
    """
    
    def __init__(self):
        """Initialize document service with comprehensive logging."""
        logger.info("Initializing Document Service")
        self._initialization_time = datetime.now()
        
        # Initialize document processing
        self._supported_formats = {'.pdf', '.docx', '.doc', '.txt', '.rtf'}
        self._processing_queue = []
        self._processed_documents = {}
        
        try:
            logger.info("Document Service initialized successfully")
            logger.info(f"Supported formats: {self._supported_formats}")
            
        except Exception as e:
            logger.error(f"Document Service initialization failed: {e}")
            raise
    
    def upload_document(self, file_data: bytes, filename: str, 
                       user_id: str = None) -> Dict[str, Any]:
        """
        Upload and process a document.
        
        Args:
            file_data (bytes): Document file data
            filename (str): Name of the file
            user_id (str): ID of the user uploading the document
            
        Returns:
            Dict[str, Any]: Upload result
        """
        try:
            logger.info(f"Uploading document: {filename}")
            start_time = time.time()
            
            # Validate file format
            file_ext = Path(filename).suffix.lower()
            if file_ext not in self._supported_formats:
                return {
                    'success': False,
                    'error': f'Unsupported file format: {file_ext}',
                    'supported_formats': list(self._supported_formats)
                }
            
            # Save file using file handler
            from io import BytesIO
            file_stream = BytesIO(file_data)
            save_result = file_handler.save_uploaded_file(file_stream, filename, user_id)
            
            if not save_result['success']:
                return save_result
            
            # Process document
            processing_result = self._process_document(save_result['file_path'], filename)
            
            upload_time = time.time() - start_time
            
            result = {
                'success': True,
                'filename': filename,
                'file_path': save_result['file_path'],
                'file_size': save_result['file_size'],
                'processing_result': processing_result,
                'upload_time': round(upload_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Document uploaded and processed in {upload_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to upload document '{filename}': {e}")
            return {'success': False, 'error': str(e)}
    
    def _process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """
        Process uploaded document.
        
        Args:
            file_path (str): Path to the document file
            filename (str): Name of the file
            
        Returns:
            Dict[str, Any]: Processing result
        """
        try:
            logger.info(f"Processing document: {filename}")
            start_time = time.time()
            
            # Get file info
            file_info = file_handler.get_file_info(file_path)
            
            # Extract text content
            text_content = self._extract_text_content(file_path, filename)
            
            # Analyze document structure
            structure_analysis = self._analyze_document_structure(text_content)
            
            # Extract metadata
            metadata = self._extract_document_metadata(text_content, file_info)
            
            processing_time = time.time() - start_time
            
            result = {
                'success': True,
                'text_content': text_content,
                'structure_analysis': structure_analysis,
                'metadata': metadata,
                'processing_time': round(processing_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache processed document
            self._processed_documents[filename] = result
            
            logger.info(f"Document processed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process document '{filename}': {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_text_content(self, file_path: str, filename: str) -> str:
        """
        Extract text content from document.
        
        Args:
            file_path (str): Path to the document file
            filename (str): Name of the file
            
        Returns:
            str: Extracted text content
        """
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.txt':
                return self._extract_text_from_txt(file_path)
            elif file_ext == '.pdf':
                return self._extract_text_from_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                return self._extract_text_from_docx(file_path)
            elif file_ext == '.rtf':
                return self._extract_text_from_rtf(file_path)
            else:
                return "Unsupported file format for text extraction"
                
        except Exception as e:
            logger.error(f"Failed to extract text content from '{filename}': {e}")
            return ""
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to extract text from TXT file: {e}")
            return ""
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            # Placeholder implementation
            # In a real implementation, you would use libraries like PyPDF2 or pdfplumber
            return "PDF text extraction not implemented. Please use a supported library like PyPDF2 or pdfplumber."
        except Exception as e:
            logger.error(f"Failed to extract text from PDF file: {e}")
            return ""
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            # Placeholder implementation
            # In a real implementation, you would use libraries like python-docx
            return "DOCX text extraction not implemented. Please use a supported library like python-docx."
        except Exception as e:
            logger.error(f"Failed to extract text from DOCX file: {e}")
            return ""
    
    def _extract_text_from_rtf(self, file_path: str) -> str:
        """Extract text from RTF file."""
        try:
            # Placeholder implementation
            # In a real implementation, you would use libraries like striprtf
            return "RTF text extraction not implemented. Please use a supported library like striprtf."
        except Exception as e:
            logger.error(f"Failed to extract text from RTF file: {e}")
            return ""
    
    def _analyze_document_structure(self, text_content: str) -> Dict[str, Any]:
        """
        Analyze document structure.
        
        Args:
            text_content (str): Text content to analyze
            
        Returns:
            Dict[str, Any]: Structure analysis result
        """
        try:
            # Basic structure analysis
            lines = text_content.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            
            # Identify potential sections
            sections = []
            current_section = None
            
            for line in non_empty_lines:
                if self._is_section_header(line):
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        'title': line,
                        'content': []
                    }
                elif current_section:
                    current_section['content'].append(line)
            
            if current_section:
                sections.append(current_section)
            
            return {
                'total_lines': len(lines),
                'non_empty_lines': len(non_empty_lines),
                'sections': sections,
                'section_count': len(sections)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze document structure: {e}")
            return {'error': str(e)}
    
    def _is_section_header(self, line: str) -> bool:
        """
        Check if a line is a section header.
        
        Args:
            line (str): Line to check
            
        Returns:
            bool: True if line appears to be a section header
        """
        try:
            # Simple heuristics for section headers
            line_upper = line.upper()
            
            # Check for common section headers
            common_headers = [
                'EXPERIENCE', 'EDUCATION', 'SKILLS', 'SUMMARY', 'OBJECTIVE',
                'PROFESSIONAL SUMMARY', 'WORK EXPERIENCE', 'ACADEMIC BACKGROUND',
                'TECHNICAL SKILLS', 'CERTIFICATIONS', 'PROJECTS', 'ACHIEVEMENTS'
            ]
            
            for header in common_headers:
                if header in line_upper:
                    return True
            
            # Check if line is short and in caps
            if len(line) < 50 and line.isupper() and len(line.split()) <= 5:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check section header: {e}")
            return False
    
    def _extract_document_metadata(self, text_content: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract document metadata.
        
        Args:
            text_content (str): Text content to analyze
            file_info (Dict[str, Any]): File information
            
        Returns:
            Dict[str, Any]: Document metadata
        """
        try:
            # Basic metadata extraction
            metadata = {
                'filename': file_info.get('filename', ''),
                'file_size': file_info.get('file_size', 0),
                'created_time': file_info.get('created_time', ''),
                'modified_time': file_info.get('modified_time', ''),
                'mime_type': file_info.get('mime_type', ''),
                'text_length': len(text_content),
                'word_count': len(text_content.split()),
                'line_count': len(text_content.split('\n'))
            }
            
            # Extract potential contact information
            contact_info = self._extract_contact_info(text_content)
            metadata['contact_info'] = contact_info
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract document metadata: {e}")
            return {'error': str(e)}
    
    def _extract_contact_info(self, text_content: str) -> Dict[str, Any]:
        """
        Extract contact information from text.
        
        Args:
            text_content (str): Text content to analyze
            
        Returns:
            Dict[str, Any]: Contact information
        """
        try:
            import re
            
            contact_info = {}
            
            # Extract email
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text_content)
            if emails:
                contact_info['email'] = emails[0]
            
            # Extract phone numbers
            phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
            phones = re.findall(phone_pattern, text_content)
            if phones:
                contact_info['phone'] = ''.join(phones[0])
            
            # Extract LinkedIn profile
            linkedin_pattern = r'linkedin\.com/in/[\w-]+'
            linkedin = re.search(linkedin_pattern, text_content, re.IGNORECASE)
            if linkedin:
                contact_info['linkedin'] = linkedin.group()
            
            return contact_info
            
        except Exception as e:
            logger.error(f"Failed to extract contact info: {e}")
            return {}
    
    def get_processed_document(self, filename: str) -> Dict[str, Any]:
        """
        Get processed document by filename.
        
        Args:
            filename (str): Name of the processed document
            
        Returns:
            Dict[str, Any]: Processed document data
        """
        try:
            if filename in self._processed_documents:
                return self._processed_documents[filename]
            else:
                return {'error': f'Document {filename} not found in processed documents'}
                
        except Exception as e:
            logger.error(f"Failed to get processed document '{filename}': {e}")
            return {'error': str(e)}
    
    def list_processed_documents(self) -> List[str]:
        """
        Get list of processed document filenames.
        
        Returns:
            List[str]: List of processed document filenames
        """
        try:
            return list(self._processed_documents.keys())
        except Exception as e:
            logger.error(f"Failed to list processed documents: {e}")
            return []
    
    def delete_processed_document(self, filename: str) -> bool:
        """
        Delete processed document.
        
        Args:
            filename (str): Name of the document to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if filename in self._processed_documents:
                del self._processed_documents[filename]
                logger.info(f"Processed document deleted: {filename}")
                return True
            else:
                logger.warning(f"Processed document not found: {filename}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete processed document '{filename}': {e}")
            return False
    
    def get_document_service_info(self) -> Dict[str, Any]:
        """
        Get document service information and statistics.
        
        Returns:
            Dict[str, Any]: Document service information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "supported_formats": list(self._supported_formats),
                "processed_documents_count": len(self._processed_documents),
                "processed_documents": list(self._processed_documents.keys()),
                "processing_queue_size": len(self._processing_queue),
                "document_service_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get document service info: {e}")
            return {
                "error": str(e),
                "document_service_timestamp": datetime.now().isoformat()
            }
