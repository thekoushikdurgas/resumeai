# Document Processor - Core Document Processing Module
# app/core/document_processor.py

import streamlit as st
from typing import Dict, List, Optional, Tuple, BinaryIO
import io
import base64
from pathlib import Path
import mimetypes
import tempfile
import os

# Document processing imports
try:
    import PyPDF2
    import pdfplumber
    from docx import Document
    import docx2txt
    from PIL import Image
    import pytesseract  # OCR for image-based PDFs
except ImportError as e:
    st.error(f"Missing document processing dependencies: {e}")

from app.utils.logger import get_logger
from app.utils.text_processing import clean_text, normalize_whitespace
from app.utils.file_handler import validate_file_size, get_file_hash
from app.models.resume_model import DocumentInfo, ExtractionResult

logger = get_logger(__name__)

class DocumentProcessor:
    """Advanced document processing for multiple file formats"""
    
    def __init__(self):
        """Initialize document processor"""
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.extraction_methods = {
            'pdf': ['pdfplumber', 'PyPDF2', 'ocr'],
            'docx': ['python-docx', 'docx2txt'],
            'txt': ['direct']
        }
    
    def process_uploaded_file(self, uploaded_file: BinaryIO) -> ExtractionResult:
        """Process uploaded file and extract text content"""
        
        if uploaded_file is None:
            return ExtractionResult(success=False, error="No file uploaded")
        
        try:
            # Validate file
            validation_result = self._validate_file(uploaded_file)
            if not validation_result['valid']:
                return ExtractionResult(
                    success=False, 
                    error=validation_result['error']
                )
            
            # Get file info
            file_info = self._get_file_info(uploaded_file)
            
            # Extract text based on file type
            text_content = self._extract_text_by_type(uploaded_file, file_info.file_type)
            
            # Clean and process text
            cleaned_text = clean_text(text_content)
            
            # Calculate extraction confidence
            confidence = self._calculate_extraction_confidence(text_content, cleaned_text)
            
            return ExtractionResult(
                success=True,
                text_content=cleaned_text,
                raw_content=text_content,
                file_info=file_info,
                extraction_confidence=confidence,
                word_count=len(cleaned_text.split()),
                char_count=len(cleaned_text)
            )
        
        except Exception as e:
            logger.error(f"Document processing error: {str(e)}", exc_info=True)
            return ExtractionResult(
                success=False,
                error=f"Processing failed: {str(e)}"
            )
    
    def _validate_file(self, uploaded_file: BinaryIO) -> Dict:
        """Validate uploaded file"""
        
        # Check file size
        file_size = len(uploaded_file.getvalue())
        if file_size > self.max_file_size:
            return {
                'valid': False, 
                'error': f"File too large. Maximum size: {self.max_file_size / (1024*1024):.1f}MB"
            }
        
        if file_size == 0:
            return {'valid': False, 'error': "Empty file"}
        
        # Check file extension
        file_extension = Path(uploaded_file.name).suffix.lower()
        if file_extension not in self.supported_formats:
            return {
                'valid': False,
                'error': f"Unsupported format. Supported: {', '.join(self.supported_formats)}"
            }
        
        return {'valid': True}
    
    def _get_file_info(self, uploaded_file: BinaryIO) -> DocumentInfo:
        """Extract file information"""
        
        file_path = Path(uploaded_file.name)
        file_size = len(uploaded_file.getvalue())
        file_hash = get_file_hash(uploaded_file.getvalue())
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        return DocumentInfo(
            filename=file_path.name,
            file_size=file_size,
            file_type=file_path.suffix.lower(),
            mime_type=mime_type,
            file_hash=file_hash
        )
    
    def _extract_text_by_type(self, uploaded_file: BinaryIO, file_type: str) -> str:
        """Extract text based on file type"""
        
        uploaded_file.seek(0)  # Reset file pointer
        
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
    
    def _extract_pdf_text(self, pdf_file: BinaryIO) -> str:
        """Extract text from PDF using multiple methods"""
        
        extracted_text = ""
        
        # Method 1: pdfplumber (best for complex layouts)
        try:
            import pdfplumber
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
            
            if extracted_text.strip():
                logger.info("PDF text extracted using pdfplumber")
                return extracted_text
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Method 2: PyPDF2 (fallback)
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
            
            if extracted_text.strip():
                logger.info("PDF text extracted using PyPDF2")
                return extracted_text
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
        
        # Method 3: OCR for image-based PDFs (if available)
        try:
            if self._is_ocr_available():
                ocr_text = self._extract_pdf_with_ocr(pdf_file)
                if ocr_text.strip():
                    logger.info("PDF text extracted using OCR")
                    return ocr_text
        except Exception as e:
            logger.warning(f"OCR extraction failed: {e}")
        
        # If no method worked
        if not extracted_text.strip():
            raise ValueError("Unable to extract text from PDF. File may be corrupted or image-based.")
        
        return extracted_text
    
    def _extract_docx_text(self, docx_file: BinaryIO) -> str:
        """Extract text from DOCX files"""
        
        try:
            # Method 1: python-docx (preserves structure better)
            docx_file.seek(0)
            doc = Document(docx_file)
            
            text_parts = []
            
            # Extract paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            # Extract tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_parts.append(" | ".join(row_text))
            
            extracted_text = "\n".join(text_parts)
            
            if extracted_text.strip():
                logger.info("DOCX text extracted using python-docx")
                return extracted_text
        
        except Exception as e:
            logger.warning(f"python-docx extraction failed: {e}")
        
        # Method 2: docx2txt (fallback)
        try:
            docx_file.seek(0)
            text = docx2txt.process(docx_file)
            
            if text and text.strip():
                logger.info("DOCX text extracted using docx2txt")
                return text
        
        except Exception as e:
            logger.warning(f"docx2txt extraction failed: {e}")
        
        raise ValueError("Unable to extract text from DOCX file")
    
    def _extract_txt_text(self, txt_file: BinaryIO) -> str:
        """Extract text from TXT files"""
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    txt_file.seek(0)
                    content = txt_file.read().decode(encoding)
                    logger.info(f"TXT file decoded using {encoding}")
                    return content
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Unable to decode text file with supported encodings")
        
        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            raise
    
    def _extract_rtf_text(self, rtf_file: BinaryIO) -> str:
        """Extract text from RTF files"""
        
        try:
            # Simple RTF text extraction
            rtf_file.seek(0)
            rtf_content = rtf_file.read().decode('utf-8', errors='ignore')
            
            # Basic RTF parsing (remove control words)
            import re
            
            # Remove RTF control words and groups
            text = re.sub(r'\\[a-z]+\d*', '', rtf_content)
            text = re.sub(r'[{}]', '', text)
            text = re.sub(r'\\', '', text)
            
            # Clean up whitespace
            text = normalize_whitespace(text)
            
            if text.strip():
                logger.info("RTF text extracted")
                return text
            
            raise ValueError("No text found in RTF file")
        
        except Exception as e:
            logger.error(f"RTF extraction error: {e}")
            raise
    
    def _extract_pdf_with_ocr(self, pdf_file: BinaryIO) -> str:
        """Extract text from PDF using OCR"""
        
        if not self._is_ocr_available():
            return ""
        
        try:
            import pdf2image
            
            # Convert PDF pages to images
            pdf_file.seek(0)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded file temporarily
                temp_pdf_path = os.path.join(temp_dir, "temp.pdf")
                with open(temp_pdf_path, 'wb') as f:
                    f.write(pdf_file.getvalue())
                
                # Convert to images
                images = pdf2image.convert_from_path(temp_pdf_path)
                
                # Extract text from each page
                extracted_text = ""
                for i, image in enumerate(images):
                    try:
                        page_text = pytesseract.image_to_string(image)
                        if page_text.strip():
                            extracted_text += f"\n--- Page {i+1} ---\n{page_text}\n"
                    except Exception as e:
                        logger.warning(f"OCR failed for page {i+1}: {e}")
                
                return extracted_text
        
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            return ""
    
    def _is_ocr_available(self) -> bool:
        """Check if OCR dependencies are available"""
        try:
            import pytesseract
            import pdf2image
            
            # Test tesseract installation
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
    
    def _calculate_extraction_confidence(self, raw_text: str, cleaned_text: str) -> float:
        """Calculate confidence score for text extraction"""
        
        if not raw_text or not cleaned_text:
            return 0.0
        
        confidence = 100.0
        
        # Check for extraction issues
        raw_lines = raw_text.count('\n')
        cleaned_lines = cleaned_text.count('\n')
        
        # Penalize if too much content was lost during cleaning
        if raw_lines > 0:
            content_retention = cleaned_lines / raw_lines
            if content_retention < 0.7:
                confidence -= 20.0
        
        # Check for garbled text (too many non-ASCII characters)
        non_ascii_ratio = sum(1 for c in cleaned_text if ord(c) > 127) / max(len(cleaned_text), 1)
        if non_ascii_ratio > 0.1:
            confidence -= 15.0
        
        # Check for reasonable word count
        word_count = len(cleaned_text.split())
        if word_count < 50:
            confidence -= 25.0
        elif word_count < 100:
            confidence -= 10.0
        
        # Check for common resume elements
        resume_indicators = ['experience', 'education', 'skills', 'work', 'career', 'professional']
        found_indicators = sum(1 for indicator in resume_indicators if indicator.lower() in cleaned_text.lower())
        
        if found_indicators >= 3:
            confidence += 10.0
        elif found_indicators < 2:
            confidence -= 15.0
        
        return max(0.0, min(100.0, confidence))
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return self.supported_formats.copy()
    
    def estimate_processing_time(self, file_size: int, file_type: str) -> float:
        """Estimate processing time in seconds"""
        
        # Base time estimates (in seconds)
        base_times = {
            '.txt': 0.1,
            '.docx': 0.5,
            '.pdf': 1.0,
            '.rtf': 0.3
        }
        
        base_time = base_times.get(file_type, 1.0)
        
        # Adjust based on file size (MB)
        size_mb = file_size / (1024 * 1024)
        size_factor = 1 + (size_mb * 0.5)
        
        return base_time * size_factor
    
    def create_download_link(self, content: str, filename: str, mime_type: str = "text/plain") -> str:
        """Create downloadable link for processed content"""
        
        b64_content = base64.b64encode(content.encode()).decode()
        href = f'<a href="data:{mime_type};base64,{b64_content}" download="{filename}">Download {filename}</a>'
        
        return href