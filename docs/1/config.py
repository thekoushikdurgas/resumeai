# Resume AI Configuration
# Configuration settings for the Resume/CV AI application

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class AIConfig:
    """AI model configuration settings"""
    gemini_model: str = "gemini-1.5-flash"
    openai_model: str = "gpt-3.5-turbo"
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 30

@dataclass
class AppConfig:
    """Main application configuration"""
    app_title: str = "Resume/CV AI Assistant"
    page_icon: str = "📄"
    layout: str = "wide"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    supported_formats: List[str] = None
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ['pdf', 'docx', 'txt']

@dataclass
class ATSConfig:
    """ATS scoring configuration"""
    base_score: int = 100
    penalties: Dict[str, int] = None
    
    def __post_init__(self):
        if self.penalties is None:
            self.penalties = {
                'missing_email': 15,
                'missing_phone': 10,
                'too_short': 20,
                'low_keyword_match': 25,
                'bad_format': 30
            }

@dataclass
class SkillsConfig:
    """Skills extraction configuration"""
    technical_skills: List[str] = None
    soft_skills: List[str] = None
    certifications: List[str] = None
    
    def __post_init__(self):
        if self.technical_skills is None:
            self.technical_skills = [
                # Programming Languages
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'sass', 'less',
                
                # Frameworks & Libraries
                'react', 'angular', 'vue', 'svelte', 'node.js', 'express', 'django', 'flask', 'fastapi',
                'spring', 'hibernate', 'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'tailwind',
                
                # Databases
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'oracle', 'cassandra',
                'dynamodb', 'firebase', 'neo4j',
                
                # Cloud & DevOps
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
                'terraform', 'ansible', 'chef', 'puppet', 'nginx', 'apache', 'linux', 'ubuntu', 'centos',
                
                # Data Science & ML
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'anaconda', 'spark', 'hadoop',
                'tableau', 'power bi', 'excel', 'powerpoint',
                
                # Mobile Development
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'cordova', 'ionic',
                
                # Tools & Other
                'git', 'svn', 'jira', 'confluence', 'slack', 'teams', 'figma', 'sketch', 'photoshop',
                'illustrator', 'autocad', 'solidworks', 'unity', 'unreal engine'
            ]
        
        if self.soft_skills is None:
            self.soft_skills = [
                'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
                'creativity', 'adaptability', 'time management', 'project management', 'mentoring',
                'collaboration', 'critical thinking', 'decision making', 'negotiation', 'presentation',
                'customer service', 'sales', 'marketing', 'strategy', 'innovation'
            ]
        
        if self.certifications is None:
            self.certifications = [
                'aws certified', 'azure certified', 'google cloud certified', 'cissp', 'cisa', 'cism',
                'pmp', 'agile', 'scrum master', 'six sigma', 'itil', 'comptia', 'cisco', 'microsoft certified',
                'oracle certified', 'salesforce certified', 'tableau certified', 'google analytics'
            ]

class ConfigManager:
    """Configuration manager for the application"""
    
    def __init__(self):
        self.ai_config = AIConfig()
        self.app_config = AppConfig()
        self.ats_config = ATSConfig()
        self.skills_config = SkillsConfig()
    
    def get_ai_config(self) -> AIConfig:
        return self.ai_config
    
    def get_app_config(self) -> AppConfig:
        return self.app_config
    
    def get_ats_config(self) -> ATSConfig:
        return self.ats_config
    
    def get_skills_config(self) -> SkillsConfig:
        return self.skills_config
    
    def update_from_env(self):
        """Update configuration from environment variables"""
        # AI Configuration
        self.ai_config.gemini_model = os.getenv('GEMINI_MODEL', self.ai_config.gemini_model)
        self.ai_config.openai_model = os.getenv('OPENAI_MODEL', self.ai_config.openai_model)
        self.ai_config.max_tokens = int(os.getenv('AI_MAX_TOKENS', self.ai_config.max_tokens))
        self.ai_config.temperature = float(os.getenv('AI_TEMPERATURE', self.ai_config.temperature))
        
        # App Configuration
        self.app_config.max_file_size = int(os.getenv('MAX_FILE_SIZE', self.app_config.max_file_size))

# Global configuration instance
config = ConfigManager()

# Industry-specific configurations
INDUSTRY_CONFIGS = {
    'technology': {
        'keywords': [
            'software development', 'programming', 'coding', 'algorithms', 'data structures',
            'system design', 'software architecture', 'api development', 'microservices',
            'cloud computing', 'devops', 'ci/cd', 'testing', 'debugging', 'version control'
        ],
        'skills_weight': {
            'technical': 0.6,
            'soft': 0.4
        }
    },
    'finance': {
        'keywords': [
            'financial analysis', 'risk management', 'portfolio management', 'investment banking',
            'corporate finance', 'financial modeling', 'valuation', 'derivatives', 'compliance',
            'regulatory', 'accounting', 'auditing', 'financial reporting'
        ],
        'skills_weight': {
            'technical': 0.4,
            'soft': 0.6
        }
    },
    'healthcare': {
        'keywords': [
            'patient care', 'clinical experience', 'medical records', 'healthcare management',
            'medical coding', 'hipaa compliance', 'quality assurance', 'patient safety',
            'healthcare technology', 'electronic health records', 'telemedicine'
        ],
        'skills_weight': {
            'technical': 0.3,
            'soft': 0.7
        }
    },
    'marketing': {
        'keywords': [
            'digital marketing', 'content marketing', 'social media', 'seo', 'sem', 'ppc',
            'email marketing', 'marketing automation', 'brand management', 'market research',
            'analytics', 'campaign management', 'lead generation', 'conversion optimization'
        ],
        'skills_weight': {
            'technical': 0.4,
            'soft': 0.6
        }
    },
    'education': {
        'keywords': [
            'curriculum development', 'lesson planning', 'classroom management', 'student assessment',
            'educational technology', 'learning management systems', 'pedagogical methods',
            'special education', 'student counseling', 'academic administration'
        ],
        'skills_weight': {
            'technical': 0.2,
            'soft': 0.8
        }
    }
}

# Resume templates configuration
RESUME_TEMPLATES = {
    'modern_professional': {
        'name': 'Modern Professional',
        'description': 'Clean, contemporary design suitable for most industries',
        'sections': ['summary', 'experience', 'education', 'skills'],
        'layout': 'single_column',
        'color_scheme': 'blue'
    },
    'creative_design': {
        'name': 'Creative Design',
        'description': 'Visually appealing template for creative professionals',
        'sections': ['portfolio', 'experience', 'skills', 'education'],
        'layout': 'two_column',
        'color_scheme': 'purple'
    },
    'technical_focused': {
        'name': 'Technical Focused',
        'description': 'Emphasizes technical skills and projects',
        'sections': ['skills', 'projects', 'experience', 'education'],
        'layout': 'skills_sidebar',
        'color_scheme': 'teal'
    },
    'executive_summary': {
        'name': 'Executive Summary',
        'description': 'Professional template for senior-level positions',
        'sections': ['executive_summary', 'achievements', 'experience', 'education'],
        'layout': 'timeline',
        'color_scheme': 'gray'
    },
    'academic_research': {
        'name': 'Academic Research',
        'description': 'Template focused on research and publications',
        'sections': ['research', 'publications', 'education', 'experience'],
        'layout': 'academic',
        'color_scheme': 'black'
    }
}

# Color schemes
COLOR_SCHEMES = {
    'blue': {
        'primary': '#1f77b4',
        'secondary': '#aec7e8',
        'accent': '#ff7f0e',
        'text': '#2c3e50',
        'background': '#ffffff'
    },
    'purple': {
        'primary': '#9467bd',
        'secondary': '#c5b0d5',
        'accent': '#d62728',
        'text': '#2c3e50',
        'background': '#ffffff'
    },
    'teal': {
        'primary': '#17becf',
        'secondary': '#9edae5',
        'accent': '#ff7f0e',
        'text': '#2c3e50',
        'background': '#ffffff'
    },
    'gray': {
        'primary': '#7f7f7f',
        'secondary': '#c7c7c7',
        'accent': '#d62728',
        'text': '#2c3e50',
        'background': '#ffffff'
    },
    'black': {
        'primary': '#2c3e50',
        'secondary': '#95a5a6',
        'accent': '#e74c3c',
        'text': '#2c3e50',
        'background': '#ffffff'
    }
}

# Font configurations
FONT_CONFIGS = {
    'modern': {
        'primary': 'Calibri',
        'secondary': 'Arial',
        'sizes': {
            'heading': 14,
            'subheading': 12,
            'body': 11,
            'small': 10
        }
    },
    'classic': {
        'primary': 'Times New Roman',
        'secondary': 'Georgia',
        'sizes': {
            'heading': 14,
            'subheading': 12,
            'body': 11,
            'small': 10
        }
    },
    'clean': {
        'primary': 'Arial',
        'secondary': 'Helvetica',
        'sizes': {
            'heading': 13,
            'subheading': 11,
            'body': 10,
            'small': 9
        }
    },
    'professional': {
        'primary': 'Helvetica',
        'secondary': 'Arial',
        'sizes': {
            'heading': 14,
            'subheading': 12,
            'body': 11,
            'small': 10
        }
    }
}

# Export formats configuration
EXPORT_FORMATS = {
    'docx': {
        'extension': '.docx',
        'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'description': 'Microsoft Word Document'
    },
    'pdf': {
        'extension': '.pdf',
        'mime_type': 'application/pdf',
        'description': 'Portable Document Format'
    },
    'html': {
        'extension': '.html',
        'mime_type': 'text/html',
        'description': 'HTML Web Page'
    },
    'txt': {
        'extension': '.txt',
        'mime_type': 'text/plain',
        'description': 'Plain Text File'
    }
}

# Validation rules
VALIDATION_RULES = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'[\+]?[\d\s\-\(\)]{10,}',
    'linkedin': r'linkedin\.com/in/[\w\-]+',
    'github': r'github\.com/[\w\-]+',
    'website': r'https?://[\w\.-]+\.[a-zA-Z]{2,}/?.*'
}

# Error messages
ERROR_MESSAGES = {
    'file_too_large': 'File size exceeds maximum limit of {max_size}MB',
    'unsupported_format': 'Unsupported file format. Please use: {formats}',
    'ai_service_unavailable': 'AI service is currently unavailable. Please try again later.',
    'invalid_email': 'Please enter a valid email address',
    'invalid_phone': 'Please enter a valid phone number',
    'missing_required_field': 'This field is required',
    'parsing_error': 'Error parsing the document. Please check the file format.',
    'network_error': 'Network connection error. Please check your internet connection.'
}

# Success messages
SUCCESS_MESSAGES = {
    'file_uploaded': 'File uploaded successfully!',
    'analysis_complete': 'Resume analysis completed successfully!',
    'report_generated': 'Report generated successfully!',
    'settings_saved': 'Settings saved successfully!',
    'export_ready': 'Export ready for download!',
    'customization_applied': 'Customization applied successfully!'
}