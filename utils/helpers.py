"""
Helper Utilities for Resume/CV AI Application
Provides common helper functions and utilities.

This module provides:
- Common helper functions
- Data validation utilities
- String processing helpers
- File handling utilities
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import os
import re
import json
import logging
import hashlib
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path

from .logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("helpers")

class Helpers:
    """
    Helper utilities class with comprehensive logging.
    
    This class provides common helper functions including data validation,
    string processing, file handling, and other utility functions for the
    Resume/CV AI application.
    
    Key Features:
    - Common helper functions
    - Data validation utilities
    - String processing helpers
    - File handling utilities
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
    """
    
    def __init__(self):
        """Initialize helpers with comprehensive logging."""
        logger.info("Initializing Helpers")
        self._initialization_time = datetime.now()
        
        try:
            logger.info("Helpers initialized successfully")
        except Exception as e:
                logger.error(f"Helpers initialization failed: {e}")
                raise
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
            Validate email address format.
        
        Args:
                email (str): Email address to validate
            
        Returns:
                bool: True if email is valid, False otherwise
        """
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        except Exception as e:
            logger.error(f"Failed to validate email '{email}': {e}")
            return False
        
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone (str): Phone number to validate
        
        Returns:
            bool: True if phone is valid, False otherwise
        """
        try:
            # Remove all non-digit characters
            digits_only = re.sub(r'\D', '', phone)
            # Check if it's a valid length (7-15 digits)
            return 7 <= len(digits_only) <= 15
        except Exception as e:
            logger.error(f"Failed to validate phone '{phone}': {e}")
            return False

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text (str): Text to clean
        
        Returns:
            str: Cleaned text
        """
        try:
            if not text:
                return ""
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
            
            return text
        except Exception as e:
            logger.error(f"Failed to clean text: {e}")
            return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text.
        
        Args:
            text (str): Text to extract keywords from
            min_length (int): Minimum keyword length
        
        Returns:
            List[str]: List of extracted keywords
        """
        try:
            if not text:
                return []
            
            # Clean text
            text = Helpers.clean_text(text)
            
            # Split into words and filter
            words = text.lower().split()
            keywords = []
            
            for word in words:
                # Remove punctuation and check length
                word = re.sub(r'[^\w]', '', word)
                if len(word) >= min_length:
                    keywords.append(word)
            
            # Remove duplicates and return
            return list(set(keywords))
        except Exception as e:
            logger.error(f"Failed to extract keywords: {e}")
            return []
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.
    
    Args:
            text1 (str): First text
            text2 (str): Second text
        
    Returns:
            float: Similarity score (0-1)
    """
        try:
            if not text1 or not text2:
                return 0.0
            
            # Convert to lowercase and split into words
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
    
            # Calculate Jaccard similarity
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            if not union:
                return 0.0
            
            return len(intersection) / len(union)
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    @staticmethod
    def format_date(date: Union[str, datetime], format_str: str = "%Y-%m-%d") -> str:
        """
        Format date to string.
    
    Args:
            date (Union[str, datetime]): Date to format
            format_str (str): Format string
        
    Returns:
            str: Formatted date string
        """
        try:
            if isinstance(date, str):
                # Try to parse the date
                try:
                    date = datetime.fromisoformat(date)
                except ValueError:
                    # Try other common formats
                    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]:
                        try:
                            date = datetime.strptime(date, fmt)
                            break
                        except ValueError:
                            continue
            else:
                        return date
            
            if isinstance(date, datetime):
                return date.strftime(format_str)
            
            return str(date)
        except Exception as e:
            logger.error(f"Failed to format date: {e}")
            return str(date)
    
    @staticmethod
    def generate_hash(data: str) -> str:
        """
        Generate hash for data.
    
    Args:
            data (str): Data to hash
        
    Returns:
            str: Hash string
        """
        try:
            return hashlib.md5(data.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to generate hash: {e}")
            return ""
    
    @staticmethod
    def safe_json_loads(data: str, default: Any = None) -> Any:
        """
        Safely load JSON data.
    
    Args:
            data (str): JSON string to load
            default (Any): Default value if loading fails
        
    Returns:
            Any: Parsed JSON data or default value
        """
        try:
            return json.loads(data)
        except Exception as e:
            logger.warning(f"Failed to load JSON: {e}")
            return default
    
    @staticmethod
    def safe_json_dumps(data: Any, default: str = "{}") -> str:
        """
        Safely dump data to JSON.
    
    Args:
            data (Any): Data to dump
            default (str): Default value if dumping fails
        
    Returns:
            str: JSON string or default value
        """
        try:
            return json.dumps(data, default=str)
        except Exception as e:
            logger.warning(f"Failed to dump JSON: {e}")
            return default
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """
        Ensure directory exists.
    
    Args:
            path (str): Directory path
        
    Returns:
            bool: True if directory exists or was created, False otherwise
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to ensure directory '{path}': {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
    
    Args:
            file_path (str): Path to file
        
    Returns:
            int: File size in bytes, -1 if error
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Failed to get file size for '{file_path}': {e}")
            return -1
    
    @staticmethod
    def is_valid_file_type(file_path: str, allowed_types: List[str]) -> bool:
        """
        Check if file type is allowed.
        
        Args:
            file_path (str): Path to file
            allowed_types (List[str]): List of allowed file extensions
            
        Returns:
            bool: True if file type is allowed, False otherwise
        """
        try:
            file_ext = Path(file_path).suffix.lower()
            return file_ext in [ext.lower() for ext in allowed_types]
        except Exception as e:
            logger.error(f"Failed to check file type for '{file_path}': {e}")
            return False
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        Truncate text to maximum length.
        
        Args:
            text (str): Text to truncate
            max_length (int): Maximum length
            suffix (str): Suffix to add if truncated
            
        Returns:
            str: Truncated text
        """
        try:
            if not text or len(text) <= max_length:
                return text
            
            return text[:max_length - len(suffix)] + suffix
        except Exception as e:
            logger.error(f"Failed to truncate text: {e}")
            return text
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text (str): Text to normalize
        
        Returns:
            str: Normalized text
        """
        try:
            if not text:
                return ""
            
            # Replace multiple whitespace with single space
            text = re.sub(r'\s+', ' ', text)
            
            # Strip leading and trailing whitespace
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to normalize whitespace: {e}")
            return text

    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """
            Extract numbers from text.
        
        Args:
                text (str): Text to extract numbers from
            
        Returns:
                List[float]: List of extracted numbers
        """
        try:
            if not text:
                return []
            
            # Find all numbers in text
            numbers = re.findall(r'-?\d+\.?\d*', text)
            return [float(num) for num in numbers if num]
        except Exception as e:
            logger.error(f"Failed to extract numbers: {e}")
            return []
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, List[str]]:
        """
        Extract contact information from text.
        
        Args:
            text (str): Text to extract contact info from
            
        Returns:
            Dict[str, List[str]]: Dictionary containing extracted contact information
        """
        try:
            if not text:
                return {"emails": [], "phones": [], "urls": [], "addresses": []}
            
            contact_info = {
                "emails": [],
                "phones": [],
                "urls": [],
                "addresses": []
            }
            
            # Extract email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            contact_info["emails"] = list(set(emails))
            
            # Extract phone numbers (various formats)
            phone_patterns = [
                r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
                r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}',  # International
                r'\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # Simple US
            ]
            
            phones = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            # Clean up phone numbers
            cleaned_phones = []
            for phone in phones:
                # Remove all non-digit characters except +
                cleaned = re.sub(r'[^\d+]', '', phone)
                if len(cleaned) >= 7:  # Minimum phone length
                    cleaned_phones.append(cleaned)
            
            contact_info["phones"] = list(set(cleaned_phones))
            
            # Extract URLs
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, text)
            contact_info["urls"] = list(set(urls))
            
            # Extract potential addresses (basic pattern)
            address_pattern = r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Way|Circle|Cir|Court|Ct)'
            addresses = re.findall(address_pattern, text, re.IGNORECASE)
            contact_info["addresses"] = list(set(addresses))
            
            return contact_info
            
        except Exception as e:
            logger.error(f"Failed to extract contact info: {e}")
            return {"emails": [], "phones": [], "urls": [], "addresses": []}
    
    @staticmethod
    def is_likely_name(text: str) -> bool:
        """
        Determine if text is likely a person's name.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            bool: True if text is likely a name, False otherwise
        """
        try:
            if not text or len(text.strip()) == 0:
                return False
            
            text = text.strip()
            
            # Check if it's too long to be a name (more than 50 characters)
            if len(text) > 50:
                return False
            
            # Check if it contains numbers (names typically don't)
            if re.search(r'\d', text):
                return False
            
            # Check if it contains common non-name patterns
            non_name_patterns = [
                r'@',  # Email
                r'http',  # URL
                r'www\.',  # Website
                r'\d{3}-\d{3}-\d{4}',  # Phone
                r'[A-Z]{2,}',  # All caps (likely acronyms)
                r'[^\w\s\'-]',  # Special characters except apostrophes and hyphens
            ]
            
            for pattern in non_name_patterns:
                if re.search(pattern, text):
                    return False
            
            # Check if it has proper name structure (2-4 words, each starting with capital)
            words = text.split()
            if len(words) < 1 or len(words) > 4:
                return False
            
            # Check if each word starts with a capital letter
            for word in words:
                if not word[0].isupper():
                    return False
                # Check if the rest of the word is lowercase (with some exceptions for names like O'Connor)
                if not all(c.islower() or c in "'-" for c in word[1:]):
                    return False
            
            # Check for common name patterns
            name_patterns = [
                r'^[A-Z][a-z]+ [A-Z][a-z]+$',  # First Last
                r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$',  # First M. Last
                r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$',  # First Middle Last
            ]
            
            for pattern in name_patterns:
                if re.match(pattern, text):
                    return True
            
            # Additional check: if it's 2-3 words and looks like a name
            if len(words) in [2, 3] and all(word[0].isupper() and word[1:].islower() for word in words):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check if text is likely name: {e}")
            return False
    
    @staticmethod
    def extract_years_from_text(text: str) -> List[int]:
        """
        Extract years from text content.
        
        Args:
            text (str): Text to extract years from
            
        Returns:
            List[int]: List of extracted years
        """
        try:
            if not text:
                return []
            
            # Pattern to match 4-digit years (1900-2099)
            year_pattern = r'\b(19|20)\d{2}\b'
            years = re.findall(year_pattern, text)
            
            # Convert to integers and filter reasonable years
            year_list = []
            for year_str in years:
                year = int(year_str)
                # Filter for reasonable years (1900-2030)
                if 1900 <= year <= 2030:
                    year_list.append(year)
            
            # Remove duplicates and sort
            return sorted(list(set(year_list)))
            
        except Exception as e:
            logger.error(f"Failed to extract years from text: {e}")
            return []
    
    @staticmethod
    def calculate_word_count(text: str) -> int:
        """
        Calculate word count in text.
        
        Args:
            text (str): Text to count words in
            
        Returns:
            int: Number of words in the text
        """
        try:
            if not text:
                return 0
            
            # Split text into words and filter out empty strings
            words = [word for word in text.split() if word.strip()]
            return len(words)
            
        except Exception as e:
            logger.error(f"Failed to calculate word count: {e}")
            return 0
    
    @staticmethod
    def remove_duplicates(items: List[Any]) -> List[Any]:
        """
        Remove duplicates from list while preserving order.
    
    Args:
            items (List[Any]): List to remove duplicates from
        
    Returns:
            List[Any]: List without duplicates
        """
        try:
            seen = set()
            result = []
            
            for item in items:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            
            return result
        except Exception as e:
            logger.error(f"Failed to remove duplicates: {e}")
            return items
    
    @staticmethod
    def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
        """
        Split list into chunks of specified size.
    
    Args:
            items (List[Any]): List to chunk
            chunk_size (int): Size of each chunk
        
    Returns:
            List[List[Any]]: List of chunks
        """
        try:
            if chunk_size <= 0:
                return [items]
            
            return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
        except Exception as e:
            logger.error(f"Failed to chunk list: {e}")
            return [items]
    
    def generate_unique_id(self, prefix: str = "id", length: int = 8) -> str:
        """
        Generate a unique identifier.
    
    Args:
            prefix (str): Prefix for the ID
            length (int): Length of the random part
        
    Returns:
            str: Unique identifier
        """
        try:
            logger.debug(f"Generating unique ID with prefix: {prefix}, length: {length}")
            
            import uuid
            import time
            
            # Generate timestamp-based component
            timestamp = str(int(time.time() * 1000))[-6:]  # Last 6 digits of timestamp
            
            # Generate random component
            random_part = str(uuid.uuid4().hex[:length])
            
            # Combine components
            unique_id = f"{prefix}_{timestamp}_{random_part}"
            
            logger.debug(f"Generated unique ID: {unique_id}")
            return unique_id
            
        except Exception as e:
            logger.error(f"Failed to generate unique ID: {e}")
            # Fallback to simple timestamp-based ID
            import time
            return f"{prefix}_{int(time.time())}"
    
    def get_helpers_info(self) -> Dict[str, Any]:
        """
        Get helpers information and statistics.
        
    Returns:
            Dict[str, Any]: Helpers information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "helpers_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get helpers info: {e}")
            return {
                "error": str(e),
                "helpers_timestamp": datetime.now().isoformat()
            }

# Create global helpers instance
helpers = Helpers()

# Export commonly used functions
validate_email = helpers.validate_email
validate_phone = helpers.validate_phone
clean_text = helpers.clean_text
extract_keywords = helpers.extract_keywords
calculate_similarity = helpers.calculate_similarity
format_date = helpers.format_date
generate_hash = helpers.generate_hash
generate_unique_id = helpers.generate_unique_id
safe_json_loads = helpers.safe_json_loads
safe_json_dumps = helpers.safe_json_dumps
ensure_directory = helpers.ensure_directory
get_file_size = helpers.get_file_size
is_valid_file_type = helpers.is_valid_file_type
truncate_text = helpers.truncate_text
normalize_whitespace = helpers.normalize_whitespace
extract_numbers = helpers.extract_numbers
remove_duplicates = helpers.remove_duplicates
chunk_list = helpers.chunk_list
extract_contact_info = helpers.extract_contact_info
is_likely_name = helpers.is_likely_name
extract_years_from_text = helpers.extract_years_from_text
calculate_text_similarity = helpers.calculate_similarity  # Alias for calculate_similarity
calculate_word_count = helpers.calculate_word_count