"""
Configuration Settings for Resume/CV AI Application
Handles application configuration and settings management.

This module provides:
- Application configuration
- Environment-specific settings
- Feature flags
- Configuration validation
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("config_settings")

class Settings:
    """
    Application settings class with comprehensive logging.
    
    This class provides configuration management including environment-specific
    settings, feature flags, and configuration validation for the Resume/CV
    AI application.
    
    Key Features:
    - Application configuration
    - Environment-specific settings
    - Feature flags
    - Configuration validation
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _settings (Dict[str, Any]): Application settings
        _environment (str): Current environment
    """
    
    def __init__(self, environment: str = None):
        """
        Initialize settings with comprehensive logging.
        
        Args:
            environment (str): Environment name (dev, staging, prod)
        """
        logger.info("Initializing Settings")
        self._initialization_time = datetime.now()
        
        # Set environment
        self._environment = environment or os.getenv('ENVIRONMENT', 'dev')
        
        # Initialize settings
        self._settings = {}
        
        try:
            # Load base settings
            self._load_base_settings()
            
            # Load environment-specific settings
            self._load_environment_settings()
            
            # Load feature flags
            self._load_feature_flags()
            
            logger.info("Settings initialized successfully")
            logger.info(f"Environment: {self._environment}")
            
        except Exception as e:
            logger.error(f"Settings initialization failed: {e}")
            raise
    
    def _load_base_settings(self):
        """Load base application settings."""
        try:
            self._settings = {
                # Application settings
                'app_name': 'Resume AI',
                'app_version': '1.0.0',
                'app_description': 'AI-powered resume analysis and optimization platform',
                'debug': self._environment == 'dev',
                'environment': self._environment,
                
                # Server settings
                'host': '0.0.0.0',
                'port': int(os.getenv('PORT', 8501)),
                'reload': self._environment == 'dev',
                
                # Database settings
                'database_url': os.getenv('DATABASE_URL', 'sqlite:///resume_ai.db'),
                'database_pool_size': int(os.getenv('DATABASE_POOL_SIZE', 10)),
                'database_max_overflow': int(os.getenv('DATABASE_MAX_OVERFLOW', 20)),
                
                # AI settings
                'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
                'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                'google_api_key': os.getenv('GOOGLE_API_KEY', ''),
                'ai_model_default': os.getenv('AI_MODEL_DEFAULT', 'gpt-4'),
                'ai_temperature': float(os.getenv('AI_TEMPERATURE', 0.7)),
                'ai_max_tokens': int(os.getenv('AI_MAX_TOKENS', 4096)),
                
                # File settings
                'upload_dir': os.getenv('UPLOAD_DIR', 'uploads'),
                'temp_dir': os.getenv('TEMP_DIR', 'temp'),
                'export_dir': os.getenv('EXPORT_DIR', 'exports'),
                'max_file_size': int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024)),  # 10MB
                'allowed_file_types': ['.pdf', '.docx', '.doc', '.txt', '.rtf'],
                
                # Cache settings
                'cache_type': os.getenv('CACHE_TYPE', 'memory'),
                'cache_ttl': int(os.getenv('CACHE_TTL', 3600)),  # 1 hour
                'cache_max_size': int(os.getenv('CACHE_MAX_SIZE', 1000)),
                
                # Logging settings
                'log_level': os.getenv('LOG_LEVEL', 'INFO'),
                'log_file': os.getenv('LOG_FILE', 'logs/app.log'),
                'log_max_size': int(os.getenv('LOG_MAX_SIZE', 10 * 1024 * 1024)),  # 10MB
                'log_backup_count': int(os.getenv('LOG_BACKUP_COUNT', 5)),
                
                # Security settings
                'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-here'),
                'jwt_secret': os.getenv('JWT_SECRET', 'your-jwt-secret-here'),
                'jwt_expiration': int(os.getenv('JWT_EXPIRATION', 3600)),  # 1 hour
                'cors_origins': os.getenv('CORS_ORIGINS', '*').split(','),
                
                # Rate limiting
                'rate_limit_enabled': os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true',
                'rate_limit_requests': int(os.getenv('RATE_LIMIT_REQUESTS', 100)),
                'rate_limit_window': int(os.getenv('RATE_LIMIT_WINDOW', 3600)),  # 1 hour
                
                # Email settings
                'smtp_host': os.getenv('SMTP_HOST', ''),
                'smtp_port': int(os.getenv('SMTP_PORT', 587)),
                'smtp_username': os.getenv('SMTP_USERNAME', ''),
                'smtp_password': os.getenv('SMTP_PASSWORD', ''),
                'smtp_use_tls': os.getenv('SMTP_USE_TLS', 'true').lower() == 'true',
                
                # Notification settings
                'notifications_enabled': os.getenv('NOTIFICATIONS_ENABLED', 'true').lower() == 'true',
                'email_notifications': os.getenv('EMAIL_NOTIFICATIONS', 'true').lower() == 'true',
                'push_notifications': os.getenv('PUSH_NOTIFICATIONS', 'false').lower() == 'true',
                
                # Analytics settings
                'analytics_enabled': os.getenv('ANALYTICS_ENABLED', 'false').lower() == 'true',
                'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', ''),
                'mixpanel_token': os.getenv('MIXPANEL_TOKEN', ''),
                
                # Monitoring settings
                'monitoring_enabled': os.getenv('MONITORING_ENABLED', 'false').lower() == 'true',
                'sentry_dsn': os.getenv('SENTRY_DSN', ''),
                'health_check_interval': int(os.getenv('HEALTH_CHECK_INTERVAL', 300)),  # 5 minutes
                
                # Performance settings
                'worker_processes': int(os.getenv('WORKER_PROCESSES', 1)),
                'worker_threads': int(os.getenv('WORKER_THREADS', 4)),
                'request_timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),  # 30 seconds
                
                # Feature settings
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
                    'monitoring': False
                }
            }
            
            logger.debug("Base settings loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load base settings: {e}")
            raise
    
    def _load_environment_settings(self):
        """Load environment-specific settings."""
        try:
            if self._environment == 'dev':
                self._settings.update({
                    'debug': True,
                    'reload': True,
                    'log_level': 'DEBUG',
                    'cors_origins': ['http://localhost:3000', 'http://localhost:8501'],
                    'rate_limit_enabled': False,
                    'monitoring_enabled': False,
                    'analytics_enabled': False
                })
            elif self._environment == 'staging':
                self._settings.update({
                    'debug': False,
                    'reload': False,
                    'log_level': 'INFO',
                    'cors_origins': ['https://staging.resumeai.com'],
                    'rate_limit_enabled': True,
                    'monitoring_enabled': True,
                    'analytics_enabled': True
                })
            elif self._environment == 'prod':
                self._settings.update({
                    'debug': False,
                    'reload': False,
                    'log_level': 'WARNING',
                    'cors_origins': ['https://resumeai.com'],
                    'rate_limit_enabled': True,
                    'monitoring_enabled': True,
                    'analytics_enabled': True
                })
            
            logger.debug(f"Environment-specific settings loaded for {self._environment}")
            
        except Exception as e:
            logger.error(f"Failed to load environment settings: {e}")
            raise
    
    def _load_feature_flags(self):
        """Load feature flags."""
        try:
            # Feature flags can be overridden by environment variables
            feature_flags = {
                'resume_analysis': os.getenv('FEATURE_RESUME_ANALYSIS', 'true').lower() == 'true',
                'job_matching': os.getenv('FEATURE_JOB_MATCHING', 'true').lower() == 'true',
                'ai_enhancement': os.getenv('FEATURE_AI_ENHANCEMENT', 'true').lower() == 'true',
                'ats_checker': os.getenv('FEATURE_ATS_CHECKER', 'true').lower() == 'true',
                'resume_builder': os.getenv('FEATURE_RESUME_BUILDER', 'true').lower() == 'true',
                'templates': os.getenv('FEATURE_TEMPLATES', 'true').lower() == 'true',
                'career_insights': os.getenv('FEATURE_CAREER_INSIGHTS', 'true').lower() == 'true',
                'export': os.getenv('FEATURE_EXPORT', 'true').lower() == 'true',
                'notifications': os.getenv('FEATURE_NOTIFICATIONS', 'true').lower() == 'true',
                'analytics': os.getenv('FEATURE_ANALYTICS', 'false').lower() == 'true',
                'monitoring': os.getenv('FEATURE_MONITORING', 'false').lower() == 'true'
            }
            
            self._settings['features'].update(feature_flags)
            
            logger.debug("Feature flags loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load feature flags: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get setting value by key.
        
        Args:
            key (str): Setting key
            default (Any): Default value if key not found
            
        Returns:
            Any: Setting value
        """
        try:
            return self._settings.get(key, default)
        except Exception as e:
            logger.error(f"Failed to get setting '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any):
        """
        Set setting value by key.
        
        Args:
            key (str): Setting key
            value (Any): Setting value
        """
        try:
            self._settings[key] = value
            logger.debug(f"Setting '{key}' updated")
        except Exception as e:
            logger.error(f"Failed to set setting '{key}': {e}")
    
    def get_feature_flag(self, feature: str) -> bool:
        """
        Get feature flag value.
        
        Args:
            feature (str): Feature name
            
        Returns:
            bool: Feature flag value
        """
        try:
            return self._settings.get('features', {}).get(feature, False)
        except Exception as e:
            logger.error(f"Failed to get feature flag '{feature}': {e}")
            return False
    
    def set_feature_flag(self, feature: str, enabled: bool):
        """
        Set feature flag value.
        
        Args:
            feature (str): Feature name
            enabled (bool): Feature enabled status
        """
        try:
            if 'features' not in self._settings:
                self._settings['features'] = {}
            
            self._settings['features'][feature] = enabled
            logger.debug(f"Feature flag '{feature}' set to {enabled}")
        except Exception as e:
            logger.error(f"Failed to set feature flag '{feature}': {e}")
    
    def validate_settings(self) -> Dict[str, Any]:
        """
        Validate application settings.
        
        Returns:
            Dict[str, Any]: Validation result
        """
        try:
            validation_result = {
                'valid': True,
                'errors': [],
                'warnings': []
            }
            
            # Validate required settings
            required_settings = [
                'app_name',
                'app_version',
                'database_url',
                'secret_key'
            ]
            
            for setting in required_settings:
                if not self._settings.get(setting):
                    validation_result['errors'].append(f"Required setting '{setting}' is missing")
                    validation_result['valid'] = False
            
            # Validate API keys if features are enabled
            if self.get_feature_flag('ai_enhancement'):
                if not self._settings.get('openai_api_key') and not self._settings.get('anthropic_api_key'):
                    validation_result['warnings'].append("No AI API keys configured")
            
            # Validate file settings
            if self._settings.get('max_file_size', 0) <= 0:
                validation_result['errors'].append("Invalid max_file_size setting")
                validation_result['valid'] = False
            
            # Validate port
            port = self._settings.get('port', 0)
            if not isinstance(port, int) or port <= 0 or port > 65535:
                validation_result['errors'].append("Invalid port setting")
                validation_result['valid'] = False
            
            logger.info(f"Settings validation completed: {validation_result['valid']}")
            return validation_result
            
        except Exception as e:
            logger.error(f"Failed to validate settings: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': []
            }
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all settings.
        
        Returns:
            Dict[str, Any]: All settings
        """
        return self._settings.copy()
    
    def get_settings_info(self) -> Dict[str, Any]:
        """
        Get settings information and statistics.
        
        Returns:
            Dict[str, Any]: Settings information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "environment": self._environment,
                "settings_count": len(self._settings),
                "feature_flags_count": len(self._settings.get('features', {})),
                "enabled_features": [k for k, v in self._settings.get('features', {}).items() if v],
                "validation_result": self.validate_settings(),
                "settings_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get settings info: {e}")
            return {
                "error": str(e),
                "settings_timestamp": datetime.now().isoformat()
            }

# Create global settings instance
settings = Settings()

# Export commonly used functions
get_setting = settings.get
set_setting = settings.set
get_feature_flag = settings.get_feature_flag
set_feature_flag = settings.set_feature_flag
validate_settings = settings.validate_settings
