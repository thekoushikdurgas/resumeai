# Resume AI Utilities
# Utility functions for the Resume/CV AI application

import re
import json
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from collections import Counter
import streamlit as st

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespaces and line breaks
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.,;:!?()-]', '', text)
    
    # Fix common formatting issues
    text = text.replace('\u2022', '•')  # Replace bullet characters
    text = text.replace('\u2013', '-')  # Replace en-dash
    text = text.replace('\u2014', '-')  # Replace em-dash
    text = text.replace('\u201c', '"')  # Replace left double quote
    text = text.replace('\u201d', '"')  # Replace right double quote
    text = text.replace('\u2018', "'")  # Replace left single quote
    text = text.replace('\u2019', "'")  # Replace right single quote
    
    return text.strip()

def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from text"""
    contact_info = {}
    
    # Email extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact_info['email'] = emails[0] if emails else ""
    
    # Phone extraction (more comprehensive)
    phone_patterns = [
        r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',  # US format
        r'\+?([0-9]{1,4})[-.\s]?\(?([0-9]{1,4})\)?[-.\s]?([0-9]{1,4})[-.\s]?([0-9]{1,4})',  # International
        r'(\d{10})',  # Simple 10 digit
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            if isinstance(phones[0], tuple):
                contact_info['phone'] = '-'.join(phones[0])
            else:
                contact_info['phone'] = phones[0]
            break
    
    if 'phone' not in contact_info:
        contact_info['phone'] = ""
    
    # LinkedIn extraction
    linkedin_patterns = [
        r'linkedin\.com/in/([\w\-]+)',
        r'linkedin\.com/pub/([\w\-]+)',
        r'(linkedin\.com/in/[\w\-]+)',
    ]
    
    for pattern in linkedin_patterns:
        linkedin_matches = re.findall(pattern, text.lower())
        if linkedin_matches:
            contact_info['linkedin'] = linkedin_matches[0]
            break
    
    if 'linkedin' not in contact_info:
        contact_info['linkedin'] = ""
    
    # GitHub extraction
    github_pattern = r'github\.com/([\w\-]+)'
    github_matches = re.findall(github_pattern, text.lower())
    contact_info['github'] = github_matches[0] if github_matches else ""
    
    # Website extraction
    website_patterns = [
        r'https?://([\w\.-]+\.[\w]{2,})',
        r'www\.([\w\.-]+\.[\w]{2,})',
        r'([\w\.-]+\.(com|org|net|io|dev|me))'
    ]
    
    for pattern in website_patterns:
        websites = re.findall(pattern, text.lower())
        if websites:
            if isinstance(websites[0], tuple):
                contact_info['website'] = websites[0][0]
            else:
                contact_info['website'] = websites[0]
            break
    
    if 'website' not in contact_info:
        contact_info['website'] = ""
    
    return contact_info

def extract_name_from_text(text: str) -> str:
    """Extract name from resume text (first few lines)"""
    lines = text.split('\n')[:5]
    
    # Look for name patterns
    name_patterns = [
        r'^([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)',  # First Last (Middle)
        r'^([A-Z][A-Z\s]+)',  # ALL CAPS name
        r'^(.+?)(?:\n|Email|Phone|\+)',  # Everything before contact info
    ]
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 4:
            continue
            
        # Skip lines with obvious non-name content
        if any(keyword in line.lower() for keyword in ['email', 'phone', 'linkedin', '@', '.com', 'resume', 'cv']):
            continue
            
        # Try name patterns
        for pattern in name_patterns:
            match = re.match(pattern, line)
            if match:
                name = match.group(1).strip()
                # Validate name (should have at least 2 words, reasonable length)
                words = name.split()
                if 2 <= len(words) <= 4 and all(word.isalpha() for word in words):
                    return name
    
    return ""

def calculate_keyword_density(text: str, keywords: List[str]) -> Dict[str, float]:
    """Calculate keyword density in text"""
    text_lower = text.lower()
    word_count = len(text_lower.split())
    
    if word_count == 0:
        return {}
    
    keyword_density = {}
    for keyword in keywords:
        count = text_lower.count(keyword.lower())
        density = (count / word_count) * 100
        keyword_density[keyword] = density
    
    return keyword_density

def extract_years_of_experience(text: str) -> Optional[int]:
    """Extract years of experience from text"""
    experience_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*years?\s*in',
        r'experience.*?(\d+)\+?\s*years?',
        r'over\s*(\d+)\+?\s*years?',
    ]
    
    for pattern in experience_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])
    
    return None

def extract_education_level(text: str) -> str:
    """Extract highest education level from text"""
    education_levels = {
        'phd': ['ph.d', 'phd', 'doctorate', 'doctoral'],
        'masters': ['master', 'mba', 'ms', 'ma', 'm.s.', 'm.a.', 'msc'],
        'bachelors': ['bachelor', 'ba', 'bs', 'b.s.', 'b.a.', 'bsc'],
        'associates': ['associate', 'aa', 'as', 'a.a.', 'a.s.'],
        'high_school': ['high school', 'diploma', 'ged']
    }
    
    text_lower = text.lower()
    
    # Check in order of priority (highest to lowest)
    for level, keywords in education_levels.items():
        if any(keyword in text_lower for keyword in keywords):
            return level
    
    return "unknown"

def generate_ats_keywords(job_description: str) -> List[str]:
    """Generate ATS keywords from job description"""
    if not job_description:
        return []
    
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Clean and tokenize
    text = re.sub(r'[^\w\s]', ' ', job_description.lower())
    words = text.split()
    
    # Filter words
    keywords = [
        word for word in words 
        if len(word) > 2 and word not in stop_words and word.isalpha()
    ]
    
    # Count frequency and get top keywords
    word_freq = Counter(keywords)
    top_keywords = [word for word, count in word_freq.most_common(50)]
    
    return top_keywords

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using simple word overlap"""
    if not text1 or not text2:
        return 0.0
    
    # Tokenize and clean
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def format_currency(amount: Union[int, float], currency: str = "USD") -> str:
    """Format currency amounts"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def generate_unique_id() -> str:
    """Generate a unique ID for tracking"""
    timestamp = datetime.now().isoformat()
    random_data = str(hash(timestamp))
    unique_id = hashlib.md5(random_data.encode()).hexdigest()[:8]
    return unique_id

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits = re.sub(r'[^\d]', '', phone)
    
    # Check if it's a reasonable length (7-15 digits)
    return 7 <= len(digits) <= 15

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure it's not empty
    if not filename:
        filename = "resume"
    
    return filename

def create_progress_data(analyses: List[Dict]) -> pd.DataFrame:
    """Create progress tracking data from analysis history"""
    if not analyses:
        return pd.DataFrame()
    
    progress_data = []
    for analysis in analyses:
        progress_data.append({
            'date': pd.to_datetime(analysis.get('timestamp', datetime.now())),
            'ats_score': analysis.get('ats_score', 0),
            'skill_match': analysis.get('skill_match', 0),
            'analysis_type': analysis.get('type', 'general')
        })
    
    return pd.DataFrame(progress_data)

def calculate_improvement_metrics(current_data: Dict, previous_data: Dict) -> Dict[str, float]:
    """Calculate improvement metrics between two analyses"""
    if not previous_data:
        return {}
    
    improvements = {}
    metrics = ['ats_score', 'skill_match', 'overall_score']
    
    for metric in metrics:
        current_val = current_data.get(metric, 0)
        previous_val = previous_data.get(metric, 0)
        
        if previous_val > 0:
            improvement = ((current_val - previous_val) / previous_val) * 100
            improvements[metric] = round(improvement, 2)
    
    return improvements

def export_to_csv(data: Union[Dict, List[Dict]], filename: str) -> str:
    """Export data to CSV format"""
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)
    
    return df.to_csv(index=False)

def export_to_json(data: Union[Dict, List], filename: str) -> str:
    """Export data to JSON format"""
    return json.dumps(data, indent=2, default=str)

def create_download_link(data: str, filename: str, mime_type: str) -> str:
    """Create a download link for data"""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def parse_date_range(date_str: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    """Parse date range from string (e.g., 'Jan 2020 - Present')"""
    if not date_str:
        return None, None
    
    # Common date patterns
    date_patterns = [
        r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4})',  # Jan 2020 - Dec 2021
        r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})',  # 01/2020 - 12/2021
        r'(\d{4})\s*[-–]\s*(\d{4})',  # 2020 - 2021
        r'(\w+\s+\d{4})\s*[-–]\s*(Present|Current)',  # Jan 2020 - Present
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, date_str, re.IGNORECASE)
        if match:
            start_str, end_str = match.groups()
            
            try:
                # Parse start date
                start_date = pd.to_datetime(start_str).to_pydatetime()
                
                # Parse end date
                if end_str.lower() in ['present', 'current']:
                    end_date = datetime.now()
                else:
                    end_date = pd.to_datetime(end_str).to_pydatetime()
                
                return start_date, end_date
            except:
                continue
    
    return None, None

def calculate_duration_months(start_date: datetime, end_date: datetime) -> int:
    """Calculate duration in months between two dates"""
    if not start_date or not end_date:
        return 0
    
    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    
    return years * 12 + months

def extract_salary_info(text: str) -> Dict[str, Union[str, float]]:
    """Extract salary information from text"""
    salary_patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per year|annually|/year|yr)',
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*[Kk]',  # $50K format
        r'(\d{1,3}(?:,\d{3})*)\s*[Kk]\s*(?:per year|annually)',
        r'salary:?\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
    ]
    
    salary_info = {'found': False, 'amount': 0, 'currency': 'USD', 'period': 'annual'}
    
    for pattern in salary_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            amount_str = matches[0]
            try:
                # Remove commas and convert to float
                amount = float(amount_str.replace(',', ''))
                
                # Handle K notation
                if 'k' in pattern.lower():
                    amount *= 1000
                
                salary_info['found'] = True
                salary_info['amount'] = amount
                break
            except:
                continue
    
    return salary_info

def create_skills_matrix(skills_data: List[Dict[str, str]]) -> pd.DataFrame:
    """Create a skills matrix from skills data"""
    if not skills_data:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(skills_data)
    
    # Add proficiency levels if not present
    if 'proficiency' not in df.columns:
        df['proficiency'] = 'Intermediate'
    
    # Add categories if not present
    if 'category' not in df.columns:
        df['category'] = 'General'
    
    return df

def analyze_resume_completeness(resume_data: Dict) -> Dict[str, Union[bool, float]]:
    """Analyze completeness of resume data"""
    completeness = {
        'has_contact_info': False,
        'has_summary': False,
        'has_experience': False,
        'has_education': False,
        'has_skills': False,
        'overall_score': 0.0
    }
    
    # Check contact information
    personal_info = resume_data.get('personal_info', {})
    if personal_info.get('email') or personal_info.get('phone'):
        completeness['has_contact_info'] = True
    
    # Check other sections
    sections = resume_data.get('sections', {})
    completeness['has_summary'] = bool(sections.get('summary'))
    completeness['has_experience'] = bool(sections.get('experience'))
    completeness['has_education'] = bool(sections.get('education'))
    completeness['has_skills'] = bool(sections.get('skills', {}).get('parsed_skills'))
    
    # Calculate overall score
    total_sections = 5
    completed_sections = sum(completeness[key] for key in completeness if key != 'overall_score')
    completeness['overall_score'] = (completed_sections / total_sections) * 100
    
    return completeness

def generate_improvement_suggestions(completeness: Dict, ats_score: int) -> List[str]:
    """Generate improvement suggestions based on analysis"""
    suggestions = []
    
    # Contact information
    if not completeness['has_contact_info']:
        suggestions.append("Add complete contact information including email and phone number")
    
    # Professional summary
    if not completeness['has_summary']:
        suggestions.append("Include a professional summary highlighting your key qualifications")
    
    # Work experience
    if not completeness['has_experience']:
        suggestions.append("Add detailed work experience with quantifiable achievements")
    
    # Education
    if not completeness['has_education']:
        suggestions.append("Include your educational background and relevant qualifications")
    
    # Skills
    if not completeness['has_skills']:
        suggestions.append("List relevant technical and soft skills for your target role")
    
    # ATS score specific suggestions
    if ats_score < 70:
        suggestions.append("Optimize your resume with relevant keywords from job descriptions")
        suggestions.append("Use standard section headers (Experience, Education, Skills)")
        suggestions.append("Avoid complex formatting that may confuse ATS systems")
    
    if ats_score < 50:
        suggestions.append("Consider using a more ATS-friendly template")
        suggestions.append("Ensure your resume is in PDF or DOCX format")
    
    return suggestions

class ResumeMetrics:
    """Class for calculating various resume metrics"""
    
    @staticmethod
    def readability_score(text: str) -> float:
        """Calculate readability score (simplified version)"""
        if not text:
            return 0.0
        
        sentences = len(re.findall(r'[.!?]+', text))
        words = len(text.split())
        
        if sentences == 0:
            return 0.0
        
        avg_words_per_sentence = words / sentences
        
        # Simple readability score (lower is better, like Flesch-Kincaid)
        score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * (1))  # Simplified
        
        return max(0, min(100, score))
    
    @staticmethod
    def keyword_optimization_score(resume_text: str, job_keywords: List[str]) -> float:
        """Calculate keyword optimization score"""
        if not job_keywords:
            return 50.0  # Default score if no keywords provided
        
        resume_lower = resume_text.lower()
        matched_keywords = sum(1 for keyword in job_keywords if keyword.lower() in resume_lower)
        
        return (matched_keywords / len(job_keywords)) * 100
    
    @staticmethod
    def action_verb_score(text: str) -> float:
        """Calculate action verb usage score"""
        action_verbs = [
            'achieved', 'analyzed', 'built', 'created', 'developed', 'designed', 'established',
            'implemented', 'improved', 'increased', 'led', 'managed', 'optimized', 'reduced',
            'streamlined', 'supervised', 'transformed', 'collaborated', 'coordinated', 'executed'
        ]
        
        text_lower = text.lower()
        found_verbs = sum(1 for verb in action_verbs if verb in text_lower)
        
        # Score based on variety of action verbs
        max_expected = min(len(action_verbs), 10)  # Expect up to 10 different action verbs
        return min(100, (found_verbs / max_expected) * 100)
    
    @staticmethod
    def quantification_score(text: str) -> float:
        """Calculate quantification score based on numbers/metrics"""
        # Look for numbers, percentages, dollar amounts
        number_patterns = [
            r'\d+%',           # Percentages
            r'\$\d+',          # Dollar amounts
            r'\d+\+',          # Numbers with plus
            r'\d{1,3}(?:,\d{3})*',  # Large numbers with commas
            r'\d+\s*(?:million|billion|thousand|k)',  # Written numbers
        ]
        
        quantifications = 0
        for pattern in number_patterns:
            quantifications += len(re.findall(pattern, text, re.IGNORECASE))
        
        # Score based on number of quantifications found
        words = len(text.split())
        if words == 0:
            return 0.0
        
        # Expect about 1 quantification per 50 words
        expected_ratio = words / 50
        score = min(100, (quantifications / max(1, expected_ratio)) * 100)
        
        return score

# Caching decorator for expensive operations
def cache_result(ttl_minutes: int = 30):
    """Simple caching decorator for Streamlit"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Check if result is in session state and not expired
            if 'cache' not in st.session_state:
                st.session_state.cache = {}
            
            if cache_key in st.session_state.cache:
                result, timestamp = st.session_state.cache[cache_key]
                if datetime.now() - timestamp < timedelta(minutes=ttl_minutes):
                    return result
            
            # Calculate result and cache it
            result = func(*args, **kwargs)
            st.session_state.cache[cache_key] = (result, datetime.now())
            
            return result
        return wrapper
    return decorator