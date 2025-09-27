"""
File Uploader Component for Resume/CV AI Application
Handles file upload functionality with validation and processing.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FileUploader:
    """File uploader component with validation and processing."""
    
    def __init__(self, 
                 accepted_types: List[str] = ['.pdf', '.docx', '.doc', '.txt', '.rtf'],
                 max_file_size: int = 10 * 1024 * 1024):  # 10MB
        """
        Initialize file uploader.
        
        Args:
            accepted_types: List of accepted file extensions
            max_file_size: Maximum file size in bytes
        """
        self.accepted_types = accepted_types
        self.max_file_size = max_file_size
    
    def render(self, 
               label: str = "Upload Resume/CV",
               help_text: str = "Upload your resume in PDF, DOCX, DOC, TXT, or RTF format",
               key: str = "file_uploader") -> Optional[Any]:
        """
        Render file uploader widget.
        
        Args:
            label: Label for the uploader
            help_text: Help text to display
            key: Unique key for the widget
            
        Returns:
            Uploaded file object or None
        """
        try:
            uploaded_file = st.file_uploader(
                label=label,
                type=self.accepted_types,
                help=help_text,
                key=key
            )
            
            if uploaded_file is not None:
                # Validate file size
                if uploaded_file.size > self.max_file_size:
                    st.error(f"File size ({uploaded_file.size / 1024 / 1024:.1f}MB) exceeds maximum allowed size ({self.max_file_size / 1024 / 1024:.1f}MB)")
                    return None
                
                # Validate file type
                file_extension = f".{uploaded_file.name.split('.')[-1].lower()}"
                if file_extension not in self.accepted_types:
                    st.error(f"File type {file_extension} is not supported. Accepted types: {', '.join(self.accepted_types)}")
                    return None
                
                logger.info(f"File uploaded successfully: {uploaded_file.name} ({uploaded_file.size} bytes)")
                return uploaded_file
            
            return None
            
        except Exception as e:
            logger.error(f"Error in file uploader: {e}")
            st.error(f"Error uploading file: {e}")
            return None
