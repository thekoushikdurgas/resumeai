"""
LinkedIn Job Scraper Module
A comprehensive LinkedIn job scraping solution with vector database integration.
"""

__version__ = "1.0.0"
__author__ = "Resume AI Team"

from .scraper import LinkedInJobScraper
from .vector_db import VectorDatabase
from .helpers import *

__all__ = [
    'LinkedInJobScraper',
    'VectorDatabase',
    'clean_text',
    'format_salary',
    'extract_skills',
    'extract_experience_level',
    'extract_job_type',
    'parse_location',
    'calculate_days_since_posted',
    'normalize_company_name',
    'extract_contact_info',
    'calculate_text_similarity',
    'generate_job_summary',
    'validate_job_data',
    'format_currency',
    'create_job_hash',
    'batch_process_jobs',
    'get_date_range_filter',
    'clean_html_tags',
    'extract_years_of_experience'
]
