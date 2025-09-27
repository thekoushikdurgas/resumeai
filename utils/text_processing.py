"""
Text Processing Utilities for Resume/CV AI Application
Provides advanced text processing and NLP utilities.

This module provides:
- Text preprocessing and cleaning
- NLP processing utilities
- Text analysis functions
- Keyword extraction and analysis
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import string
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import Counter

from .logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("text_processing")

class TextProcessor:
    """
    Text processing utilities class with comprehensive logging.
    
    This class provides advanced text processing including preprocessing,
    NLP processing, text analysis, and keyword extraction for the Resume/CV
    AI application.
    
    Key Features:
    - Text preprocessing and cleaning
    - NLP processing utilities
    - Text analysis functions
    - Keyword extraction and analysis
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _stop_words (set): Set of common stop words
        _punctuation (set): Set of punctuation characters
    """
    
    def __init__(self):
        """Initialize text processor with comprehensive logging."""
        logger.info("Initializing Text Processor")
        self._initialization_time = datetime.now()
        
        # Initialize stop words
        self._stop_words = self._load_stop_words()
        
        # Initialize punctuation
        self._punctuation = set(string.punctuation)
        
        try:
            logger.info("Text Processor initialized successfully")
            logger.info(f"Loaded {len(self._stop_words)} stop words")
        except Exception as e:
            logger.error(f"Text Processor initialization failed: {e}")
            raise
    
    def _load_stop_words(self) -> set:
        """Load common stop words."""
        try:
            # Common English stop words
            stop_words = {
                'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                'to', 'was', 'will', 'with', 'would', 'you', 'your', 'i', 'me',
                'my', 'we', 'our', 'us', 'they', 'them', 'their', 'this', 'these',
                'those', 'have', 'had', 'having', 'do', 'does', 'did', 'doing',
                'can', 'could', 'should', 'would', 'may', 'might', 'must', 'shall'
            }
            return stop_words
        except Exception as e:
            logger.error(f"Failed to load stop words: {e}")
            return set()
    
    def preprocess_text(self, text: str, remove_stop_words: bool = True, 
                       remove_punctuation: bool = True, lowercase: bool = True) -> str:
        """
        Preprocess text for analysis.
        
        Args:
            text (str): Text to preprocess
            remove_stop_words (bool): Whether to remove stop words
            remove_punctuation (bool): Whether to remove punctuation
            lowercase (bool): Whether to convert to lowercase
            
        Returns:
            str: Preprocessed text
        """
        try:
            if not text:
                return ""
            
            # Convert to lowercase
            if lowercase:
                text = text.lower()
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove punctuation
            if remove_punctuation:
                text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Remove stop words
            if remove_stop_words:
                words = text.split()
                words = [word for word in words if word not in self._stop_words]
                text = ' '.join(words)
            
            return text
        except Exception as e:
            logger.error(f"Failed to preprocess text: {e}")
            return text
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text.
        
        Args:
            text (str): Text to extract sentences from
            
        Returns:
            List[str]: List of sentences
        """
        try:
            if not text:
                return []
            
            # Split by sentence endings
            sentences = re.split(r'[.!?]+', text)
            
            # Clean and filter sentences
            sentences = [s.strip() for s in sentences if s.strip()]
            
            return sentences
        except Exception as e:
            logger.error(f"Failed to extract sentences: {e}")
            return []
    
    def extract_words(self, text: str, min_length: int = 2) -> List[str]:
        """
        Extract words from text.
        
        Args:
            text (str): Text to extract words from
            min_length (int): Minimum word length
            
        Returns:
            List[str]: List of words
        """
        try:
            if not text:
                return []
            
            # Preprocess text
            text = self.preprocess_text(text, remove_stop_words=False, 
                                      remove_punctuation=True, lowercase=True)
            
            # Split into words and filter
            words = text.split()
            words = [word for word in words if len(word) >= min_length]
            
            return words
        except Exception as e:
            logger.error(f"Failed to extract words: {e}")
            return []
    
    def extract_keywords(self, text: str, top_n: int = 10, min_length: int = 3) -> List[Tuple[str, int]]:
        """
        Extract keywords from text with frequency counts.
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to return
            min_length (int): Minimum keyword length
            
        Returns:
            List[Tuple[str, int]]: List of (keyword, frequency) tuples
        """
        try:
            if not text:
                return []
            
            # Extract words
            words = self.extract_words(text, min_length)
            
            # Count word frequencies
            word_counts = Counter(words)
            
            # Get top keywords
            top_keywords = word_counts.most_common(top_n)
            
            return top_keywords
        except Exception as e:
            logger.error(f"Failed to extract keywords: {e}")
            return []
    
    def calculate_text_metrics(self, text: str) -> Dict[str, Any]:
        """
        Calculate various text metrics.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Dictionary of text metrics
        """
        try:
            if not text:
                return {}
            
            # Basic metrics
            char_count = len(text)
            word_count = len(text.split())
            sentence_count = len(self.extract_sentences(text))
            
            # Word length metrics
            words = self.extract_words(text)
            if words:
                avg_word_length = sum(len(word) for word in words) / len(words)
                max_word_length = max(len(word) for word in words)
            else:
                avg_word_length = 0
                max_word_length = 0
            
            # Sentence length metrics
            sentences = self.extract_sentences(text)
            if sentences:
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
                max_sentence_length = max(len(s.split()) for s in sentences)
            else:
                avg_sentence_length = 0
                max_sentence_length = 0
            
            # Readability metrics (simplified)
            readability_score = self._calculate_readability(text)
            
            return {
                'char_count': char_count,
                'word_count': word_count,
                'sentence_count': sentence_count,
                'avg_word_length': round(avg_word_length, 2),
                'max_word_length': max_word_length,
                'avg_sentence_length': round(avg_sentence_length, 2),
                'max_sentence_length': max_sentence_length,
                'readability_score': readability_score
            }
        except Exception as e:
            logger.error(f"Failed to calculate text metrics: {e}")
            return {}
    
    def _calculate_readability(self, text: str) -> float:
        """
        Calculate simplified readability score.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Readability score (0-100)
        """
        try:
            if not text:
                return 0.0
            
            sentences = self.extract_sentences(text)
            words = self.extract_words(text)
            
            if not sentences or not words:
                return 0.0
            
            # Simple readability formula
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables = sum(self._count_syllables(word) for word in words) / len(words)
            
            # Simplified Flesch Reading Ease
            score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
            
            return max(0, min(100, score))
        except Exception as e:
            logger.error(f"Failed to calculate readability: {e}")
            return 0.0
    
    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word.
        
        Args:
            word (str): Word to count syllables in
            
        Returns:
            int: Number of syllables
        """
        try:
            if not word:
                return 0
            
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllable_count += 1
                prev_was_vowel = is_vowel
            
            # Handle silent 'e'
            if word.endswith('e') and syllable_count > 1:
                syllable_count -= 1
            
            return max(1, syllable_count)
        except Exception as e:
            logger.error(f"Failed to count syllables for '{word}': {e}")
            return 1
    
    def extract_skills(self, text: str, skill_keywords: List[str] = None) -> List[str]:
        """
        Extract skills from text.
        
        Args:
            text (str): Text to extract skills from
            skill_keywords (List[str]): List of skill keywords to look for
            
        Returns:
            List[str]: List of found skills
        """
        try:
            if not text:
                return []
            
            # Default skill keywords
            if skill_keywords is None:
                skill_keywords = [
                    'python', 'java', 'javascript', 'sql', 'html', 'css',
                    'machine learning', 'data analysis', 'project management',
                    'leadership', 'communication', 'problem solving',
                    'aws', 'azure', 'docker', 'kubernetes', 'git'
                ]
            
            # Convert to lowercase for comparison
            text_lower = text.lower()
            found_skills = []
            
            for skill in skill_keywords:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            
            return found_skills
        except Exception as e:
            logger.error(f"Failed to extract skills: {e}")
            return []
    
    def extract_experience_years(self, text: str) -> int:
        """
        Extract years of experience from text.
        
        Args:
            text (str): Text to extract experience from
            
        Returns:
            int: Years of experience
        """
        try:
            if not text:
                return 0
            
            # Look for experience patterns
            experience_patterns = [
                r'(\d+)\s*years?\s*of\s*experience',
                r'(\d+)\s*years?\s*experience',
                r'experience\s*of\s*(\d+)\s*years?',
                r'(\d+)\+?\s*years?'
            ]
            
            for pattern in experience_patterns:
                matches = re.findall(pattern, text.lower())
                if matches:
                    return int(matches[0])
            
            return 0
        except Exception as e:
            logger.error(f"Failed to extract experience years: {e}")
            return 0
    
    def extract_education_level(self, text: str) -> str:
        """
        Extract education level from text.
        
        Args:
            text (str): Text to extract education from
            
        Returns:
            str: Education level
        """
        try:
            if not text:
                return ""
            
            text_lower = text.lower()
            
            # Education level keywords
            education_levels = {
                'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
                'masters': ['masters', 'master', 'ms', 'm.s', 'ma', 'm.a', 'mba', 'm.b.a'],
                'bachelors': ['bachelors', 'bachelor', 'bs', 'b.s', 'ba', 'b.a', 'bachelor\'s'],
                'associates': ['associates', 'associate', 'aa', 'a.a', 'as', 'a.s'],
                'high school': ['high school', 'hs', 'h.s', 'diploma']
            }
            
            for level, keywords in education_levels.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        return level.title()
            
            return ""
        except Exception as e:
            logger.error(f"Failed to extract education level: {e}")
            return ""
    
    def calculate_readability(self, text: str) -> Dict[str, float]:
        """
        Calculate readability metrics for text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, float]: Readability metrics
        """
        try:
            logger.debug(f"Calculating readability for text (length: {len(text)})")
            
            if not text or not isinstance(text, str):
                logger.warning("Invalid text provided for readability calculation")
                return {}
            
            # Extract sentences and words
            sentences = self.extract_sentences(text)
            words = self.extract_words(text)
            
            if not sentences or not words:
                return {}
            
            # Basic metrics
            sentence_count = len(sentences)
            word_count = len(words)
            character_count = len(text)
            
            # Average words per sentence
            avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
            
            # Average characters per word
            avg_chars_per_word = character_count / word_count if word_count > 0 else 0
            
            # Flesch Reading Ease (simplified)
            # Score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
            # ASL = Average Sentence Length, ASW = Average Syllables per Word
            flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * (avg_chars_per_word / 2.5))
            flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
            
            # Simple readability level
            if flesch_score >= 90:
                level = "Very Easy"
            elif flesch_score >= 80:
                level = "Easy"
            elif flesch_score >= 70:
                level = "Fairly Easy"
            elif flesch_score >= 60:
                level = "Standard"
            elif flesch_score >= 50:
                level = "Fairly Difficult"
            elif flesch_score >= 30:
                level = "Difficult"
            else:
                level = "Very Difficult"
            
            metrics = {
                "flesch_score": round(flesch_score, 2),
                "reading_level": level,
                "avg_words_per_sentence": round(avg_words_per_sentence, 2),
                "avg_chars_per_word": round(avg_chars_per_word, 2),
                "sentence_count": sentence_count,
                "word_count": word_count,
                "character_count": character_count
            }
            
            logger.debug(f"Calculated readability metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate readability: {e}")
            return {}
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text.
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            Dict[str, List[str]]: Extracted entities by type
        """
        try:
            logger.debug(f"Extracting entities from text (length: {len(text)})")
            
            if not text or not isinstance(text, str):
                logger.warning("Invalid text provided for entity extraction")
                return {}
            
            entities = {
                "emails": [],
                "phones": [],
                "urls": [],
                "dates": [],
                "numbers": [],
                "locations": [],
                "organizations": []
            }
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            entities["emails"] = re.findall(email_pattern, text)
            
            # Extract phone numbers
            phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
            phone_matches = re.findall(phone_pattern, text)
            entities["phones"] = [''.join(match) for match in phone_matches]
            
            # Extract URLs
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            entities["urls"] = re.findall(url_pattern, text)
            
            # Extract dates (simple patterns)
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD/MM/YYYY
                r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
                r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b'     # DD Month YYYY
            ]
            
            for pattern in date_patterns:
                entities["dates"].extend(re.findall(pattern, text, re.IGNORECASE))
            
            # Extract numbers
            number_pattern = r'\b\d+(?:\.\d+)?\b'
            entities["numbers"] = re.findall(number_pattern, text)
            
            # Simple location extraction (capitalized words that might be places)
            location_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
            potential_locations = re.findall(location_pattern, text)
            
            # Filter out common non-location words
            non_locations = {
                'The', 'This', 'That', 'These', 'Those', 'There', 'Here', 'Where',
                'When', 'What', 'Who', 'Why', 'How', 'Yes', 'No', 'Not', 'But',
                'And', 'Or', 'So', 'Because', 'Since', 'Until', 'While', 'During',
                'Before', 'After', 'Above', 'Below', 'Between', 'Among', 'Through',
                'Under', 'Over', 'Around', 'Inside', 'Outside', 'Within', 'Without'
            }
            
            entities["locations"] = [loc for loc in potential_locations if loc not in non_locations]
            
            # Simple organization extraction (words with common company suffixes)
            org_pattern = r'\b[A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Corporation|Company|Co|Ltd|Limited|Group|Associates|Partners|Solutions|Systems|Technologies|Services|Enterprises|Industries)\b'
            entities["organizations"] = re.findall(org_pattern, text)
            
            # Remove duplicates and empty lists
            for key in entities:
                entities[key] = list(set(entities[key]))
                entities[key] = [item for item in entities[key] if item.strip()]
            
            logger.debug(f"Extracted entities: {sum(len(v) for v in entities.values())} total")
            return entities
            
        except Exception as e:
            logger.error(f"Failed to extract entities: {e}")
            return {}
    
    def get_text_processor_info(self) -> Dict[str, Any]:
        """
        Get text processor information and statistics.
        
        Returns:
            Dict[str, Any]: Text processor information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "stop_words_count": len(self._stop_words),
                "punctuation_count": len(self._punctuation),
                "text_processor_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get text processor info: {e}")
            return {
                "error": str(e),
                "text_processor_timestamp": datetime.now().isoformat()
            }

# Create global text processor instance
text_processor = TextProcessor()

# Export commonly used functions
preprocess_text = text_processor.preprocess_text
extract_sentences = text_processor.extract_sentences
extract_words = text_processor.extract_words
extract_keywords = text_processor.extract_keywords
calculate_text_metrics = text_processor.calculate_text_metrics
extract_skills = text_processor.extract_skills
extract_experience_years = text_processor.extract_experience_years
extract_education_level = text_processor.extract_education_level
calculate_readability = text_processor.calculate_readability
extract_entities = text_processor.extract_entities