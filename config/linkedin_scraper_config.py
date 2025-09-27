"""
LinkedIn Job Scraper Configuration
Configuration settings for the LinkedIn job scraping functionality.
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ScraperConfig:
    """Configuration class for LinkedIn job scraper"""
    
    # Scraping settings
    delay_range: tuple = (2, 5)  # Random delay between requests (seconds)
    max_retries: int = 3
    max_pages_per_search: int = 10
    respect_robots_txt: bool = True
    user_agent_rotation: bool = True
    
    # Database settings
    persist_directory: str = "./data/linkedin_chroma_db"
    collection_name: str = "linkedin_job_postings"
    embedding_model: str = "all-MiniLM-L6-v2"
    max_results: int = 1000
    
    # Dashboard settings
    page_title: str = "LinkedIn Job Analytics"
    theme: str = "light"
    cache_ttl: int = 3600  # Cache timeout in seconds
    max_display_jobs: int = 50
    
    # Search filters
    experience_levels: List[str] = None
    job_types: List[str] = None
    date_posted_options: List[str] = None
    
    def __post_init__(self):
        """Initialize default values after dataclass creation"""
        if self.experience_levels is None:
            self.experience_levels = [
                "All", "Internship", "Entry level", "Associate", 
                "Mid-Senior level", "Director", "Executive"
            ]
        
        if self.job_types is None:
            self.job_types = [
                "All", "Full-time", "Part-time", "Contract", 
                "Temporary", "Internship"
            ]
        
        if self.date_posted_options is None:
            self.date_posted_options = [
                "All", "Past 24 hours", "Past week", "Past month"
            ]

# LinkedIn search filter mappings
LINKEDIN_FILTERS = {
    'experience_level': {
        'Internship': '1',
        'Entry level': '2', 
        'Associate': '3',
        'Mid-Senior level': '4',
        'Director': '5',
        'Executive': '6'
    },
    'job_type': {
        'Full-time': 'F',
        'Part-time': 'P',
        'Contract': 'C',
        'Temporary': 'T',
        'Internship': 'I'
    },
    'date_posted': {
        'Past 24 hours': 'r86400',
        'Past week': 'r604800',
        'Past month': 'r2592000'
    }
}

# Common job search keywords
JOB_KEYWORDS = {
    'data_science': [
        'data scientist', 'machine learning engineer', 'data analyst',
        'data engineer', 'business analyst', 'research scientist'
    ],
    'software_development': [
        'software engineer', 'full stack developer', 'backend developer',
        'frontend developer', 'mobile developer', 'devops engineer'
    ],
    'ai_ml': [
        'artificial intelligence', 'machine learning', 'deep learning',
        'computer vision', 'natural language processing', 'robotics'
    ],
    'cloud_computing': [
        'cloud engineer', 'aws engineer', 'azure engineer', 'gcp engineer',
        'cloud architect', 'cloud developer'
    ]
}

# Location mappings
LOCATION_MAPPINGS = {
    'united_states': [
        'United States', 'USA', 'US', 'America'
    ],
    'canada': [
        'Canada', 'CA'
    ],
    'united_kingdom': [
        'United Kingdom', 'UK', 'England', 'Scotland', 'Wales'
    ],
    'australia': [
        'Australia', 'AU'
    ],
    'germany': [
        'Germany', 'DE'
    ],
    'france': [
        'France', 'FR'
    ],
    'india': [
        'India', 'IN'
    ],
    'singapore': [
        'Singapore', 'SG'
    ]
}

# Skills and technologies
TECHNICAL_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 
        'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
        'perl', 'shell', 'bash', 'powershell'
    ],
    'web_technologies': [
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
        'django', 'flask', 'spring', 'asp.net', 'laravel', 'jquery',
        'bootstrap', 'sass', 'less', 'webpack', 'babel'
    ],
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server',
        'neo4j', 'couchdb', 'firebase'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
        'linode', 'vultr', 'cloudflare', 'vercel', 'netlify'
    ],
    'devops_tools': [
        'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
        'bitbucket', 'ansible', 'terraform', 'vagrant', 'chef', 'puppet',
        'circleci', 'travis ci', 'github actions'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
        'jupyter', 'tableau', 'power bi', 'spark', 'hadoop', 'kafka',
        'airflow', 'dbt', 'snowflake'
    ],
    'mobile_development': [
        'ios', 'android', 'react native', 'flutter', 'xamarin',
        'cordova', 'phonegap', 'ionic'
    ],
    'methodologies': [
        'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
        'microservices', 'rest api', 'graphql', 'soap'
    ]
}

# User agent strings for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
]

# Rate limiting settings
RATE_LIMITS = {
    'requests_per_minute': 30,
    'requests_per_hour': 1000,
    'concurrent_requests': 5,
    'backoff_factor': 2,
    'max_backoff': 60
}

# Error handling settings
ERROR_HANDLING = {
    'max_retries': 3,
    'retry_delay': 1,
    'timeout': 30,
    'connection_pool_size': 10,
    'connection_pool_maxsize': 20
}

# Data validation settings
VALIDATION_RULES = {
    'min_title_length': 3,
    'max_title_length': 100,
    'min_description_length': 50,
    'max_description_length': 10000,
    'required_fields': ['title', 'company'],
    'optional_fields': ['location', 'description', 'salary', 'skills']
}

# Export settings
EXPORT_SETTINGS = {
    'csv_encoding': 'utf-8',
    'json_indent': 2,
    'excel_sheet_name': 'LinkedIn Jobs',
    'max_export_rows': 10000
}

# Analytics settings
ANALYTICS_SETTINGS = {
    'trending_skills_count': 20,
    'top_companies_count': 10,
    'location_analysis_depth': 5,
    'salary_analysis_bins': 10
}

def get_config() -> ScraperConfig:
    """Get the scraper configuration"""
    return ScraperConfig()

def get_environment_config() -> Dict[str, Any]:
    """Get configuration from environment variables"""
    return {
        'delay_range': (
            int(os.getenv('SCRAPER_MIN_DELAY', '2')),
            int(os.getenv('SCRAPER_MAX_DELAY', '5'))
        ),
        'max_retries': int(os.getenv('SCRAPER_MAX_RETRIES', '3')),
        'max_pages_per_search': int(os.getenv('SCRAPER_MAX_PAGES', '10')),
        'persist_directory': os.getenv('CHROMA_PERSIST_DIR', './data/linkedin_chroma_db'),
        'collection_name': os.getenv('CHROMA_COLLECTION_NAME', 'linkedin_job_postings'),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
        'cache_ttl': int(os.getenv('CACHE_TTL', '3600')),
        'max_display_jobs': int(os.getenv('MAX_DISPLAY_JOBS', '50'))
    }

def validate_config(config: ScraperConfig) -> bool:
    """Validate the configuration"""
    try:
        # Check delay range
        if config.delay_range[0] < 1 or config.delay_range[1] > 60:
            return False
        
        # Check max retries
        if config.max_retries < 1 or config.max_retries > 10:
            return False
        
        # Check max pages
        if config.max_pages_per_search < 1 or config.max_pages_per_search > 50:
            return False
        
        # Check cache TTL
        if config.cache_ttl < 60 or config.cache_ttl > 86400:
            return False
        
        return True
    except Exception:
        return False

# Default configuration instance
DEFAULT_CONFIG = get_config()
