"""
Document Processing Module for Resume/CV AI Application
Handles extraction and processing of various document formats.

This module provides:
- Multi-format document processing (PDF, DOCX, TXT, RTF)
- Text extraction with OCR fallback capabilities
- File validation and security checks
- Content cleaning and preprocessing
- Comprehensive error handling and logging

Author: Resume AI Team
Created: 2024
"""

import os
import logging
import time
from typing import Dict, List, Optional, Any, BinaryIO
from datetime import datetime
import io

import PyPDF2
import pdfplumber
import docx
from docx import Document
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    import mimetypes

from models.resume_model import ParsedResume, ContactInfo, WorkExperience, Education, Skill, Project
from utils.helpers import clean_text, extract_contact_info, is_likely_name, extract_years_from_text
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("document_processor")

class DocumentProcessor:
    """
    Advanced document processing for multiple file formats with comprehensive logging.
    
    This class provides high-level document processing capabilities including:
    - Multi-format support (PDF, DOCX, TXT, RTF)
    - Text extraction with fallback mechanisms
    - File validation and security checks
    - Content preprocessing and cleaning
    - Comprehensive error handling and logging
    
    Attributes:
        supported_formats (List[str]): List of supported file extensions
        max_file_size (int): Maximum allowed file size in bytes (10MB)
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize document processor with comprehensive logging.
        
        Sets up supported file formats, size limits, and logs initialization
        details for debugging and monitoring purposes.
        """
        logger.info("Initializing DocumentProcessor")
        self._initialization_time = time.time()
        
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
        initialization_time = time.time() - self._initialization_time
        logger.info(f"DocumentProcessor initialized successfully in {initialization_time:.2f}s")
        logger.info(f"Supported formats: {self.supported_formats}")
        logger.info(f"Max file size: {self.max_file_size / (1024*1024):.1f}MB")
    
    def process_uploaded_file(self, uploaded_file: BinaryIO) -> Dict[str, Any]:
        """
        Process uploaded file and extract text content with comprehensive logging.
        
        This method handles the complete document processing pipeline including
        validation, text extraction, and content cleaning with detailed logging
        for debugging and monitoring.
        
        Args:
            uploaded_file (BinaryIO): Uploaded file object from Streamlit
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - success (bool): Whether processing was successful
                - text (str): Extracted and cleaned text content
                - metadata (dict): File metadata and processing information
                - error (str): Error message if processing failed
        """
        start_time = time.time()
        
        try:
            logger.info("Starting document processing")
            logger.debug(f"Processing uploaded file of type: {type(uploaded_file)}")
            
            # Validate file
            logger.debug("Validating uploaded file")
            validation_result = self._validate_file(uploaded_file)
            if not validation_result['valid']:
                logger.warning(f"File validation failed: {validation_result['error']}")
                return {
                    'success': False,
                    'error': validation_result['error'],
                    'text': '',
                    'metadata': {}
                }
            
            logger.info("File validation passed")
            
            # Get file info
            logger.debug("Extracting file information")
            file_info = self._get_file_info(uploaded_file)
            logger.info(f"File type detected: {file_info['type']}")
            logger.info(f"File size: {file_info['size']} bytes")
            
            # Extract text based on file type
            logger.debug(f"Extracting text using {file_info['type']} processor")
            text = self._extract_text_by_type(uploaded_file, file_info['type'])
            
            if not text:
                processing_time = time.time() - start_time
                logger.error(f"Text extraction failed after {processing_time:.2f}s")
                return {
                    'success': False,
                    'error': 'No text could be extracted from the file',
                    'text': '',
                    'metadata': file_info
                }
            
            logger.info(f"Text extracted successfully, length: {len(text)} characters")
            
            # Clean and process text
            logger.debug("Cleaning and preprocessing extracted text")
            cleaned_text = clean_text(text)
            logger.info(f"Text cleaned, final length: {len(cleaned_text)} characters")
            
            processing_time = time.time() - start_time
            logger.info(f"Document processing completed successfully in {processing_time:.2f}s")
            
            return {
                'success': True,
                'text': cleaned_text,
                'raw_text': text,
                'metadata': file_info,
                'word_count': len(cleaned_text.split()),
                'character_count': len(cleaned_text)
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Document processing failed after {processing_time:.2f}s: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Uploaded file type: {type(uploaded_file)}")
            
            return {
                'success': False,
                'error': f'File processing failed: {str(e)}',
                'text': '',
                'metadata': {},
                'processing_time': processing_time
            }
    
    def _validate_file(self, uploaded_file: BinaryIO) -> Dict[str, Any]:
        """
        Validate uploaded file with comprehensive logging.
        
        Performs security and format validation including:
        - File size checks against maximum limits
        - File format validation against supported types
        - Basic security checks for malicious content
        
        Args:
            uploaded_file (BinaryIO): Uploaded file object to validate
            
        Returns:
            Dict[str, Any]: Validation result containing:
                - valid (bool): Whether file passed validation
                - error (str): Error message if validation failed
        """
        try:
            logger.debug("Starting file validation")
            logger.debug(f"File name: {getattr(uploaded_file, 'name', 'Unknown')}")
            
            # Check file size
            logger.debug("Checking file size")
            uploaded_file.seek(0, 2)  # Seek to end
            file_size = uploaded_file.tell()
            uploaded_file.seek(0)  # Reset to beginning
            
            logger.debug(f"File size: {file_size} bytes ({file_size / (1024*1024):.2f}MB)")
            
            if file_size > self.max_file_size:
                error_msg = f'File size exceeds maximum limit of {self.max_file_size // (1024*1024)}MB'
                logger.warning(f"File size validation failed: {error_msg}")
                return {
                    'valid': False,
                    'error': error_msg
                }
            
            logger.debug("File size validation passed")
            
            # Check file type
            logger.debug("Checking file format")
            file_name = getattr(uploaded_file, 'name', '')
            file_extension = os.path.splitext(file_name)[1].lower()
            
            logger.debug(f"File extension: {file_extension}")
            
            if file_extension not in self.supported_formats:
                error_msg = f'Unsupported file format. Supported formats: {", ".join(self.supported_formats)}'
                logger.warning(f"File format validation failed: {error_msg}")
                return {
                    'valid': False,
                    'error': error_msg
                }
            
            logger.info("File validation passed successfully")
            return {'valid': True, 'error': None}
            
        except Exception as e:
            logger.error(f"File validation failed with exception: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return {
                'valid': False,
                'error': f'File validation failed: {str(e)}'
            }
    
    def _get_file_info(self, uploaded_file: BinaryIO) -> Dict[str, Any]:
        """
        Get file information.
        
        Args:
            uploaded_file: Uploaded file object
            
        Returns:
            File information dictionary
        """
        try:
            # Get file size
            uploaded_file.seek(0, 2)
            file_size = uploaded_file.tell()
            uploaded_file.seek(0)
            
            # Get file extension
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            # Detect MIME type
            try:
                if MAGIC_AVAILABLE:
                    mime_type = magic.from_buffer(uploaded_file.read(1024), mime=True)
                    uploaded_file.seek(0)
                else:
                    # Fallback to mimetypes module
                    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                    if mime_type is None:
                        mime_type = 'application/octet-stream'
            except:
                mime_type = 'application/octet-stream'
            
            return {
                'name': uploaded_file.name,
                'type': file_extension,
                'size': file_size,
                'mime_type': mime_type,
                'uploaded_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return {
                'name': uploaded_file.name,
                'type': 'unknown',
                'size': 0,
                'mime_type': 'application/octet-stream',
                'uploaded_at': datetime.now().isoformat()
            }
    
    def _extract_text_by_type(self, uploaded_file: BinaryIO, file_type: str) -> str:
        """
        Extract text based on file type.
        
        Args:
            uploaded_file: Uploaded file object
            file_type: File extension
            
        Returns:
            Extracted text
        """
        try:
            if file_type == '.pdf':
                return self._extract_pdf_text(uploaded_file)
            elif file_type in ['.docx', '.doc']:
                return self._extract_docx_text(uploaded_file)
            elif file_type == '.txt':
                return self._extract_txt_text(uploaded_file)
            elif file_type == '.rtf':
                return self._extract_rtf_text(uploaded_file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Failed to extract text from {file_type}: {e}")
            return ""
    
    def _extract_pdf_text(self, pdf_file: BinaryIO) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_file: PDF file object
            
        Returns:
            Extracted text
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            pdf_file.seek(0)
            with pdfplumber.open(pdf_file) as pdf:
                text_parts = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                if text_parts:
                    return '\n'.join(text_parts)
            
            # Fallback to PyPDF2
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_parts = []
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            # Try OCR as last resort
            return self._extract_pdf_with_ocr(pdf_file)
    
    def _extract_docx_text(self, docx_file: BinaryIO) -> str:
        """
        Extract text from DOCX file.
        
        Args:
            docx_file: DOCX file object
            
        Returns:
            Extracted text
        """
        try:
            docx_file.seek(0)
            doc = Document(docx_file)
            
            text_parts = []
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_parts.append(' | '.join(row_text))
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            logger.error(f"DOCX text extraction failed: {e}")
            return ""
    
    def _extract_txt_text(self, txt_file: BinaryIO) -> str:
        """
        Extract text from TXT file.
        
        Args:
            txt_file: TXT file object
            
        Returns:
            Extracted text
        """
        try:
            txt_file.seek(0)
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    txt_file.seek(0)
                    text = txt_file.read().decode(encoding)
                    return text
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            txt_file.seek(0)
            text = txt_file.read().decode('utf-8', errors='replace')
            return text
            
        except Exception as e:
            logger.error(f"TXT text extraction failed: {e}")
            return ""
    
    def _extract_rtf_text(self, rtf_file: BinaryIO) -> str:
        """
        Extract text from RTF file.
        
        Args:
            rtf_file: RTF file object
            
        Returns:
            Extracted text
        """
        try:
            rtf_file.seek(0)
            rtf_content = rtf_file.read().decode('utf-8', errors='replace')
            
            # Simple RTF text extraction (remove RTF formatting codes)
            import re
            
            # Remove RTF control words and groups
            text = re.sub(r'\\[a-z]+\d*\s?', '', rtf_content)
            text = re.sub(r'[{}]', '', text)
            text = re.sub(r'\\[\\{}]', '', text)
            
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            return text
            
        except Exception as e:
            logger.error(f"RTF text extraction failed: {e}")
            return ""
    
    def _extract_pdf_with_ocr(self, pdf_file: BinaryIO) -> str:
        """
        Extract text from PDF using OCR (fallback method).
        
        Args:
            pdf_file: PDF file object
            
        Returns:
            Extracted text
        """
        try:
            # Check if OCR dependencies are available
            if not self._is_ocr_available():
                logger.warning("OCR dependencies not available")
                return ""
            
            import pdf2image
            import pytesseract
            
            # Convert PDF to images
            pdf_file.seek(0)
            images = pdf2image.convert_from_bytes(pdf_file.read())
            
            # Extract text from each image
            text_parts = []
            for image in images:
                text = pytesseract.image_to_string(image)
                if text.strip():
                    text_parts.append(text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            logger.error(f"PDF OCR extraction failed: {e}")
            return ""
    
    def _is_ocr_available(self) -> bool:
        """
        Check if OCR dependencies are available.
        
        Returns:
            True if OCR is available, False otherwise
        """
        try:
            import pdf2image
            import pytesseract
            return True
        except ImportError:
            return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return self.supported_formats.copy()
    
    def estimate_processing_time(self, file_size: int, file_type: str) -> float:
        """
        Estimate processing time for a file.
        
        Args:
            file_size: File size in bytes
            file_type: File extension
            
        Returns:
            Estimated processing time in seconds
        """
        # Base processing time by file type (seconds per MB)
        base_times = {
            '.txt': 0.1,
            '.rtf': 0.2,
            '.docx': 0.5,
            '.pdf': 1.0
        }
        
        base_time = base_times.get(file_type, 1.0)
        file_size_mb = file_size / (1024 * 1024)
        
        return base_time * file_size_mb
    
    def create_download_link(self, content: str, filename: str, mime_type: str = "text/plain") -> str:
        """
        Create download link for content.
        
        Args:
            content: Content to download
            filename: Filename for download
            mime_type: MIME type
            
        Returns:
            Download link
        """
        try:
            import base64
            
            # Encode content
            encoded_content = base64.b64encode(content.encode()).decode()
            
            # Create data URL
            data_url = f"data:{mime_type};base64,{encoded_content}"
            
            return data_url
            
        except Exception as e:
            logger.error(f"Failed to create download link: {e}")
            return ""
