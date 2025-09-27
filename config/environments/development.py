"""
Development Environment Configuration
Configuration settings specific to the development environment.

This module provides:
- Development-specific settings
- Debug configurations
- Local development tools
- Development database settings
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import os
import logging
from typing import Dict, Any

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("dev_config")

# Development environment configuration
DEVELOPMENT_CONFIG = {
    # Application settings
    'app_name': 'Resume AI - Development',
    'debug': True,
    'reload': True,
    'environment': 'development',
    
    # Server settings
    'host': '127.0.0.1',
    'port': 8501,
    'reload_delay': 0.25,
    
    # Database settings
    'database_url': 'sqlite:///dev_resume_ai.db',
    'database_echo': True,
    'database_pool_size': 5,
    'database_max_overflow': 10,
    
    # AI settings
    'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
    'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
    'google_api_key': os.getenv('GOOGLE_API_KEY', ''),
    'ai_model_default': 'gpt-3.5-turbo',
    'ai_temperature': 0.7,
    'ai_max_tokens': 2048,
    'ai_timeout': 30,
    
    # File settings
    'upload_dir': 'dev_uploads',
    'temp_dir': 'dev_temp',
    'export_dir': 'dev_exports',
    'max_file_size': 5 * 1024 * 1024,  # 5MB for development
    'allowed_file_types': ['.pdf', '.docx', '.doc', '.txt', '.rtf'],
    
    # Cache settings
    'cache_type': 'memory',
    'cache_ttl': 1800,  # 30 minutes
    'cache_max_size': 100,
    
    # Logging settings
    'log_level': 'DEBUG',
    'log_file': 'logs/dev_app.log',
    'log_max_size': 5 * 1024 * 1024,  # 5MB
    'log_backup_count': 3,
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
    # Security settings
    'secret_key': 'dev-secret-key-change-in-production',
    'jwt_secret': 'dev-jwt-secret-change-in-production',
    'jwt_expiration': 7200,  # 2 hours
    'cors_origins': [
        'http://localhost:3000',
        'http://localhost:8501',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:8501'
    ],
    
    # Rate limiting
    'rate_limit_enabled': False,
    'rate_limit_requests': 1000,
    'rate_limit_window': 3600,
    
    # Email settings
    'smtp_host': 'localhost',
    'smtp_port': 1025,  # MailHog for development
    'smtp_username': '',
    'smtp_password': '',
    'smtp_use_tls': False,
    'email_from': 'dev@resumeai.com',
    
    # Notification settings
    'notifications_enabled': True,
    'email_notifications': True,
    'push_notifications': False,
    'notification_retention_days': 7,
    
    # Analytics settings
    'analytics_enabled': False,
    'google_analytics_id': '',
    'mixpanel_token': '',
    
    # Monitoring settings
    'monitoring_enabled': False,
    'sentry_dsn': '',
    'health_check_interval': 60,  # 1 minute
    'metrics_enabled': False,
    
    # Performance settings
    'worker_processes': 1,
    'worker_threads': 2,
    'request_timeout': 60,  # 60 seconds
    'response_timeout': 30,  # 30 seconds
    
    # Development tools
    'profiling_enabled': True,
    'debug_toolbar_enabled': True,
    'sql_debug_enabled': True,
    'api_documentation_enabled': True,
    'swagger_ui_enabled': True,
    
    # Feature flags
    'features': {
        'resume_analysis': True,
        'job_matching': True,
        'ai_enhancement': True,
        'ats_checker': True,
        'resume_builder': True,
        'templates': True,
        'career_insights': True,
        'export': True,
        'notifications': True,
        'analytics': False,
        'monitoring': False,
        'profiling': True,
        'debug_toolbar': True
    },
    
    # Development-specific settings
    'dev_tools': {
        'auto_reload': True,
        'reload_dirs': ['app', 'core', 'utils', 'services'],
        'reload_extensions': ['.py', '.json', '.yaml'],
        'debug_sql': True,
        'debug_queries': True,
        'show_sql_queries': True,
        'explain_queries': True
    },
    
    # Testing settings
    'testing': {
        'enabled': True,
        'test_database_url': 'sqlite:///test_resume_ai.db',
        'test_data_dir': 'tests/fixtures',
        'mock_external_apis': True,
        'mock_ai_responses': True,
        'test_timeout': 30
    },
    
    # Development data
    'sample_data': {
        'enabled': True,
        'load_sample_resumes': True,
        'load_sample_jobs': True,
        'load_sample_templates': True,
        'sample_data_dir': 'data/samples'
    }
}

def get_development_config() -> Dict[str, Any]:
    """
    Get development environment configuration.
    
    Returns:
        Dict[str, Any]: Development configuration
    """
    try:
        logger.info("Loading development configuration")
        return DEVELOPMENT_CONFIG
    except Exception as e:
        logger.error(f"Failed to load development configuration: {e}")
        raise

def validate_development_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate development configuration.
    
    Args:
        config (Dict[str, Any]): Configuration to validate
        
    Returns:
        Dict[str, Any]: Validation result
    """
    try:
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required settings
        required_settings = ['app_name', 'debug', 'database_url', 'secret_key']
        for setting in required_settings:
            if setting not in config:
                validation_result['errors'].append(f"Missing required setting: {setting}")
                validation_result['valid'] = False
        
        # Check debug mode
        if not config.get('debug', False):
            validation_result['warnings'].append("Debug mode is disabled in development")
        
        # Check database URL
        if 'sqlite' not in config.get('database_url', ''):
            validation_result['warnings'].append("Using non-SQLite database in development")
        
        # Check API keys
        if not config.get('openai_api_key') and not config.get('anthropic_api_key'):
            validation_result['warnings'].append("No AI API keys configured")
        
        logger.info(f"Development configuration validation completed: {validation_result['valid']}")
        return validation_result
        
    except Exception as e:
        logger.error(f"Failed to validate development configuration: {e}")
        return {
            'valid': False,
            'errors': [f"Validation error: {str(e)}"],
            'warnings': []
        }
