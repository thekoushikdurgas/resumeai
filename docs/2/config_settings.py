# Configuration Settings - Main Application Configuration
# config/settings.py

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

@dataclass
class AppConfig:
    """Main application configuration"""
    
    # Application Information
    APP_TITLE: str = "Resume/CV AI Assistant"
    APP_SUBTITLE: str = "Your comprehensive AI-powered resume companion for analysis, optimization, and career advancement"
    VERSION: str = "1.0.0"
    
    # Page Configuration
    PAGE_ICON: str = "📄"
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    
    # File Configuration
    MAX_FILE_SIZE_MB: int = 10
    SUPPORTED_FORMATS: List[str] = None
    UPLOAD_DIR: str = "uploads"
    TEMP_DIR: str = "temp"
    CACHE_DIR: str = "cache"
    LOGS_DIR: str = "logs"
    
    # Database Configuration (if using database)
    DATABASE_URL: Optional[str] = None
    USE_DATABASE: bool = False
    
    # External Services
    ANALYTICS_ENABLED: bool = True
    EMAIL_NOTIFICATIONS: bool = False
    
    # Security Settings
    SESSION_TIMEOUT_MINUTES: int = 60
    MAX_SESSIONS_PER_USER: int = 3
    
    # Performance Settings
    CACHE_ENABLED: bool = True
    CACHE_TTL_MINUTES: int = 30
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = True
    
    def __post_init__(self):
        """Initialize default values and environment variables"""
        
        # Set supported formats if not provided
        if self.SUPPORTED_FORMATS is None:
            self.SUPPORTED_FORMATS = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
        
        # Load from environment variables
        self.load_from_environment()
        
        # Create directories
        self.create_directories()
        
        # Set debug mode based on environment
        if self.ENVIRONMENT == "production":
            self.DEBUG = False
    
    def load_from_environment(self):
        """Load configuration from environment variables"""
        
        self.APP_TITLE = os.getenv("APP_TITLE", self.APP_TITLE)
        self.VERSION = os.getenv("APP_VERSION", self.VERSION)
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", self.ENVIRONMENT)
        
        # File settings
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", self.MAX_FILE_SIZE_MB))
        
        # Database settings
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.USE_DATABASE = os.getenv("USE_DATABASE", "false").lower() == "true"
        
        # Feature flags
        self.ANALYTICS_ENABLED = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
        self.EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true"
        self.CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        
        # Performance settings
        self.CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", self.CACHE_TTL_MINUTES))
        self.SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", self.SESSION_TIMEOUT_MINUTES))
    
    def create_directories(self):
        """Create necessary directories"""
        
        directories = [
            self.UPLOAD_DIR,
            self.TEMP_DIR, 
            self.CACHE_DIR,
            self.LOGS_DIR,
            "data/exports",
            "data/templates", 
            "data/samples"
        ]
        
        for directory in directories:
            dir_path = PROJECT_ROOT / directory
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_max_file_size_bytes(self) -> int:
        """Get maximum file size in bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

@dataclass
class UIConfig:
    """UI/UX configuration settings"""
    
    # Theme Configuration
    PRIMARY_COLOR: str = "#1f77b4"
    SECONDARY_COLOR: str = "#ff7f0e"
    BACKGROUND_COLOR: str = "#ffffff"
    TEXT_COLOR: str = "#2c3e50"
    SUCCESS_COLOR: str = "#28a745"
    WARNING_COLOR: str = "#ffc107"
    ERROR_COLOR: str = "#dc3545"
    
    # Layout Settings
    SIDEBAR_WIDTH: int = 300
    MAIN_CONTENT_PADDING: str = "1rem"
    HEADER_HEIGHT: str = "80px"
    
    # Typography
    FONT_FAMILY: str = "Inter, sans-serif"
    HEADER_FONT_SIZE: str = "2.5rem"
    BODY_FONT_SIZE: str = "1rem"
    
    # Icons and Emojis
    HEADER_ICON: str = "🤖"
    
    TAB_ICONS: Dict[str, str] = None
    
    # Animation Settings
    TRANSITION_DURATION: str = "0.3s"
    HOVER_EFFECTS: bool = True
    
    # Component Settings
    CHART_HEIGHT: int = 400
    METRICS_COLUMNS: int = 4
    FORM_INPUT_HEIGHT: str = "40px"
    
    # Responsive Breakpoints
    MOBILE_BREAKPOINT: str = "768px"
    TABLET_BREAKPOINT: str = "1024px"
    
    def __post_init__(self):
        """Initialize default values"""
        
        if self.TAB_ICONS is None:
            self.TAB_ICONS = {
                'analysis': '📄',
                'job_matching': '🎯',
                'enhancement': '✨',
                'ats_checker': '📊',
                'builder': '🔧',
                'templates': '📋',
                'insights': '📈',
                'customization': '🎨'
            }
        
        # Load theme from environment
        self.load_theme_from_environment()
    
    def load_theme_from_environment(self):
        """Load theme colors from environment"""
        
        self.PRIMARY_COLOR = os.getenv("UI_PRIMARY_COLOR", self.PRIMARY_COLOR)
        self.SECONDARY_COLOR = os.getenv("UI_SECONDARY_COLOR", self.SECONDARY_COLOR)
        self.BACKGROUND_COLOR = os.getenv("UI_BACKGROUND_COLOR", self.BACKGROUND_COLOR)
        
        # Load font settings
        self.FONT_FAMILY = os.getenv("UI_FONT_FAMILY", self.FONT_FAMILY)
    
    @property
    def theme(self) -> Dict[str, str]:
        """Get theme dictionary"""
        return {
            'primary': self.PRIMARY_COLOR,
            'secondary': self.SECONDARY_COLOR,
            'background': self.BACKGROUND_COLOR,
            'text': self.TEXT_COLOR,
            'success': self.SUCCESS_COLOR,
            'warning': self.WARNING_COLOR,
            'error': self.ERROR_COLOR,
            'font_family': self.FONT_FAMILY
        }

@dataclass
class FeatureConfig:
    """Feature flags and configuration"""
    
    # Core Features
    RESUME_ANALYSIS_ENABLED: bool = True
    JOB_MATCHING_ENABLED: bool = True
    AI_ENHANCEMENT_ENABLED: bool = True
    ATS_CHECKER_ENABLED: bool = True
    RESUME_BUILDER_ENABLED: bool = True
    TEMPLATES_ENABLED: bool = True
    CAREER_INSIGHTS_ENABLED: bool = True
    CUSTOMIZATION_ENABLED: bool = True
    
    # Advanced Features
    BATCH_PROCESSING_ENABLED: bool = False
    COLLABORATIVE_EDITING: bool = False
    REAL_TIME_COLLABORATION: bool = False
    ADVANCED_ANALYTICS: bool = False
    
    # Export Features
    PDF_EXPORT_ENABLED: bool = True
    DOCX_EXPORT_ENABLED: bool = True
    HTML_EXPORT_ENABLED: bool = True
    JSON_EXPORT_ENABLED: bool = True
    
    # Integration Features
    LINKEDIN_INTEGRATION: bool = False
    GITHUB_INTEGRATION: bool = False
    GOOGLE_DRIVE_INTEGRATION: bool = False
    DROPBOX_INTEGRATION: bool = False
    
    # AI Features
    MULTIPLE_AI_MODELS: bool = True
    CUSTOM_AI_PROMPTS: bool = True
    AI_MODEL_COMPARISON: bool = False
    
    def __post_init__(self):
        """Load feature flags from environment"""
        self.load_from_environment()
    
    def load_from_environment(self):
        """Load feature flags from environment variables"""
        
        # Core features
        self.RESUME_ANALYSIS_ENABLED = self._get_bool_env("FEATURE_RESUME_ANALYSIS", self.RESUME_ANALYSIS_ENABLED)
        self.JOB_MATCHING_ENABLED = self._get_bool_env("FEATURE_JOB_MATCHING", self.JOB_MATCHING_ENABLED)
        self.AI_ENHANCEMENT_ENABLED = self._get_bool_env("FEATURE_AI_ENHANCEMENT", self.AI_ENHANCEMENT_ENABLED)
        
        # Advanced features
        self.BATCH_PROCESSING_ENABLED = self._get_bool_env("FEATURE_BATCH_PROCESSING", self.BATCH_PROCESSING_ENABLED)
        self.ADVANCED_ANALYTICS = self._get_bool_env("FEATURE_ADVANCED_ANALYTICS", self.ADVANCED_ANALYTICS)
        
        # Integration features
        self.LINKEDIN_INTEGRATION = self._get_bool_env("FEATURE_LINKEDIN", self.LINKEDIN_INTEGRATION)
        self.GITHUB_INTEGRATION = self._get_bool_env("FEATURE_GITHUB", self.GITHUB_INTEGRATION)
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean value from environment"""
        return os.getenv(key, str(default)).lower() == "true"
    
    def get_enabled_features(self) -> List[str]:
        """Get list of enabled features"""
        enabled = []
        
        for attr_name in dir(self):
            if attr_name.endswith('_ENABLED') and getattr(self, attr_name):
                feature_name = attr_name.replace('_ENABLED', '').replace('_', ' ').title()
                enabled.append(feature_name)
        
        return enabled

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    
    # Authentication
    REQUIRE_AUTH: bool = False
    AUTH_PROVIDER: str = "local"  # local, oauth, saml
    SESSION_ENCRYPTION: bool = True
    
    # API Security
    RATE_LIMITING_ENABLED: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60
    API_KEY_REQUIRED: bool = False
    
    # File Security
    VIRUS_SCANNING_ENABLED: bool = False
    FILE_TYPE_VALIDATION: bool = True
    CONTENT_VALIDATION: bool = True
    
    # Data Protection
    DATA_ENCRYPTION_AT_REST: bool = False
    DATA_RETENTION_DAYS: int = 30
    GDPR_COMPLIANCE: bool = True
    
    # Logging and Monitoring
    SECURITY_LOGGING: bool = True
    AUDIT_TRAIL: bool = True
    SUSPICIOUS_ACTIVITY_DETECTION: bool = False
    
    def __post_init__(self):
        """Load security settings from environment"""
        self.load_from_environment()
    
    def load_from_environment(self):
        """Load security configuration from environment"""
        
        self.REQUIRE_AUTH = os.getenv("SECURITY_REQUIRE_AUTH", "false").lower() == "true"
        self.AUTH_PROVIDER = os.getenv("SECURITY_AUTH_PROVIDER", self.AUTH_PROVIDER)
        self.RATE_LIMITING_ENABLED = os.getenv("SECURITY_RATE_LIMITING", "true").lower() == "true"
        self.MAX_REQUESTS_PER_MINUTE = int(os.getenv("SECURITY_MAX_REQUESTS", self.MAX_REQUESTS_PER_MINUTE))
        
        # Data protection
        self.DATA_RETENTION_DAYS = int(os.getenv("SECURITY_DATA_RETENTION", self.DATA_RETENTION_DAYS))
        self.GDPR_COMPLIANCE = os.getenv("SECURITY_GDPR", "true").lower() == "true"

@dataclass
class EmailConfig:
    """Email service configuration"""
    
    # SMTP Settings
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # Email Templates
    FROM_EMAIL: Optional[str] = None
    FROM_NAME: str = "Resume AI Assistant"
    
    # Notification Settings
    WELCOME_EMAIL_ENABLED: bool = False
    ANALYSIS_COMPLETE_EMAIL: bool = False
    ERROR_NOTIFICATION_EMAIL: bool = False
    
    def __post_init__(self):
        """Load email configuration from environment"""
        
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", self.SMTP_PORT))
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        self.FROM_EMAIL = os.getenv("FROM_EMAIL")
        self.FROM_NAME = os.getenv("FROM_NAME", self.FROM_NAME)
        
        # Feature flags
        self.WELCOME_EMAIL_ENABLED = os.getenv("EMAIL_WELCOME", "false").lower() == "true"
        self.ANALYSIS_COMPLETE_EMAIL = os.getenv("EMAIL_ANALYSIS", "false").lower() == "true"
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return all([
            self.SMTP_SERVER,
            self.SMTP_USERNAME,
            self.SMTP_PASSWORD,
            self.FROM_EMAIL
        ])

# Create configuration instances
app_config = AppConfig()
ui_config = UIConfig()
feature_config = FeatureConfig()
security_config = SecurityConfig()
email_config = EmailConfig()

# Environment-specific configuration loading
def load_environment_config(env: str = None):
    """Load environment-specific configuration"""
    
    if env is None:
        env = os.getenv("ENVIRONMENT", "development")
    
    try:
        if env == "development":
            from config.environments.development import DevelopmentConfig
            return DevelopmentConfig()
        elif env == "staging":
            from config.environments.staging import StagingConfig
            return StagingConfig()
        elif env == "production":
            from config.environments.production import ProductionConfig
            return ProductionConfig()
        else:
            return app_config
    except ImportError:
        return app_config

# Global configuration access
def get_config():
    """Get the current configuration"""
    return {
        'app': app_config,
        'ui': ui_config,
        'features': feature_config,
        'security': security_config,
        'email': email_config
    }