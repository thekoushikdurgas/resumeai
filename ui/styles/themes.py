"""
Themes Module for Resume/CV AI Application
Handles theme management and customization.

This module provides:
- Theme management system
- Theme customization
- Theme switching
- Theme persistence
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("themes")

class Themes:
    """
    Theme management system with comprehensive logging.
    
    This class provides theme management including theme switching,
    customization, persistence, and dynamic theme generation for the
    Resume/CV AI application.
    
    Key Features:
    - Theme management system
    - Theme customization
    - Theme switching
    - Theme persistence
    - Comprehensive logging
    
    Attributes:
        _initialization_time (float): Timestamp of initialization start
        _themes (Dict[str, Dict]): Available themes
        _current_theme (str): Current active theme
        _theme_history (List[str]): Theme switching history
    """
    
    def __init__(self):
        """Initialize themes with comprehensive logging."""
        logger.info("Initializing Themes")
        self._initialization_time = datetime.now()
        
        # Initialize themes
        self._themes = {}
        
        # Initialize current theme
        self._current_theme = 'light'
        
        # Initialize theme history
        self._theme_history = []
        
        try:
            # Setup default themes
            logger.debug("Setting up default themes")
            self._setup_default_themes()
            
            # Load user preferences
            logger.debug("Loading user preferences")
            self._load_user_preferences()
            
            logger.info("Themes initialized successfully")
            logger.info(f"Current theme: {self._current_theme}")
            
        except Exception as e:
            logger.error(f"Themes initialization failed: {e}")
            logger.error("Theme management may not function correctly")
            raise
    
    def _setup_default_themes(self):
        """Setup default themes."""
        try:
            # Light theme
            self._themes['light'] = {
                'name': 'Light',
                'description': 'Clean and bright theme',
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'background_color': '#ffffff',
                'text_color': '#212529',
                'border_color': '#dee2e6',
                'accent_color': '#17a2b8',
                'success_color': '#28a745',
                'warning_color': '#ffc107',
                'danger_color': '#dc3545',
                'info_color': '#17a2b8'
            }
            
            # Dark theme
            self._themes['dark'] = {
                'name': 'Dark',
                'description': 'Dark theme for low-light environments',
                'primary_color': '#0d6efd',
                'secondary_color': '#adb5bd',
                'background_color': '#212529',
                'text_color': '#ffffff',
                'border_color': '#495057',
                'accent_color': '#20c997',
                'success_color': '#198754',
                'warning_color': '#fd7e14',
                'danger_color': '#dc3545',
                'info_color': '#0dcaf0'
            }
            
            # Professional theme
            self._themes['professional'] = {
                'name': 'Professional',
                'description': 'Professional theme for business use',
                'primary_color': '#2c3e50',
                'secondary_color': '#7f8c8d',
                'background_color': '#ffffff',
                'text_color': '#2c3e50',
                'border_color': '#bdc3c7',
                'accent_color': '#3498db',
                'success_color': '#27ae60',
                'warning_color': '#f39c12',
                'danger_color': '#e74c3c',
                'info_color': '#9b59b6'
            }
            
            # Creative theme
            self._themes['creative'] = {
                'name': 'Creative',
                'description': 'Creative theme with vibrant colors',
                'primary_color': '#e74c3c',
                'secondary_color': '#f39c12',
                'background_color': '#ffffff',
                'text_color': '#2c3e50',
                'border_color': '#ecf0f1',
                'accent_color': '#9b59b6',
                'success_color': '#2ecc71',
                'warning_color': '#f1c40f',
                'danger_color': '#e67e22',
                'info_color': '#1abc9c'
            }
            
            logger.debug(f"Setup {len(self._themes)} default themes")
            
        except Exception as e:
            logger.error(f"Failed to setup default themes: {e}")
            raise
    
    def _load_user_preferences(self):
        """Load user theme preferences."""
        try:
            # Get theme from session state
            if 'theme' in st.session_state:
                self._current_theme = st.session_state.theme
                logger.debug(f"Loaded theme from session state: {self._current_theme}")
            
            # Validate theme exists
            if self._current_theme not in self._themes:
                logger.warning(f"Theme '{self._current_theme}' not found, falling back to 'light'")
                self._current_theme = 'light'
                st.session_state.theme = 'light'
            
        except Exception as e:
            logger.error(f"Failed to load user preferences: {e}")
            self._current_theme = 'light'
    
    def apply_theme(self, theme_name: str):
        """
        Apply a theme to the application.
        
        Args:
            theme_name (str): Name of the theme to apply
        """
        try:
            if theme_name in self._themes:
                # Update current theme
                self._current_theme = theme_name
                
                # Update session state
                st.session_state.theme = theme_name
                
                # Add to history
                self._theme_history.append(theme_name)
                
                # Apply theme styles
                self._apply_theme_styles(theme_name)
                
                logger.info(f"Theme '{theme_name}' applied successfully")
            else:
                logger.warning(f"Theme '{theme_name}' not found")
                self.apply_theme('light')  # Fallback to light theme
                
        except Exception as e:
            logger.error(f"Failed to apply theme '{theme_name}': {e}")
            self.apply_theme('light')  # Fallback to light theme
    
    def _apply_theme_styles(self, theme_name: str):
        """Apply theme-specific styles."""
        try:
            theme = self._themes[theme_name]
            
            theme_css = f"""
            <style>
            :root {{
                --primary-color: {theme['primary_color']};
                --secondary-color: {theme['secondary_color']};
                --background-color: {theme['background_color']};
                --text-color: {theme['text_color']};
                --border-color: {theme['border_color']};
                --accent-color: {theme['accent_color']};
                --success-color: {theme['success_color']};
                --warning-color: {theme['warning_color']};
                --danger-color: {theme['danger_color']};
                --info-color: {theme['info_color']};
            }}
            
            .main-container {{
                background-color: var(--background-color);
                color: var(--text-color);
            }}
            
            .nav-item.current {{
                background-color: var(--primary-color);
                color: white;
            }}
            
            .sidebar-header h2 {{
                color: var(--primary-color);
            }}
            
            .success-message {{
                color: var(--success-color);
            }}
            
            .warning-message {{
                color: var(--warning-color);
            }}
            
            .error-message {{
                color: var(--danger-color);
            }}
            
            .info-message {{
                color: var(--info-color);
            }}
            </style>
            """
            
            st.markdown(theme_css, unsafe_allow_html=True)
            logger.debug(f"Theme styles applied for '{theme_name}'")
            
        except Exception as e:
            logger.error(f"Failed to apply theme styles for '{theme_name}': {e}")
    
    def get_current_theme(self) -> str:
        """
        Get current active theme.
        
        Returns:
            str: Current theme name
        """
        return self._current_theme
    
    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """
        Get theme information.
        
        Args:
            theme_name (str): Name of the theme
            
        Returns:
            Dict[str, Any]: Theme information
        """
        try:
            if theme_name in self._themes:
                return self._themes[theme_name]
            else:
                logger.warning(f"Theme '{theme_name}' not found")
                return {}
        except Exception as e:
            logger.error(f"Failed to get theme info for '{theme_name}': {e}")
            return {}
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available themes.
        
        Returns:
            List[str]: List of available theme names
        """
        try:
            return list(self._themes.keys())
        except Exception as e:
            logger.error(f"Failed to get available themes: {e}")
            return ['light']
    
    def get_theme_history(self) -> List[str]:
        """
        Get theme switching history.
        
        Returns:
            List[str]: List of theme names in chronological order
        """
        try:
            return self._theme_history.copy()
        except Exception as e:
            logger.error(f"Failed to get theme history: {e}")
            return []
    
    def create_custom_theme(self, theme_name: str, theme_config: Dict[str, Any]):
        """
        Create a custom theme.
        
        Args:
            theme_name (str): Name of the custom theme
            theme_config (Dict[str, Any]): Theme configuration
        """
        try:
            # Validate theme configuration
            required_keys = ['name', 'description', 'primary_color', 'secondary_color', 
                           'background_color', 'text_color', 'border_color']
            
            for key in required_keys:
                if key not in theme_config:
                    raise ValueError(f"Missing required theme key: {key}")
            
            # Add custom theme
            self._themes[theme_name] = theme_config
            
            logger.info(f"Custom theme '{theme_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create custom theme '{theme_name}': {e}")
            raise
    
    def delete_custom_theme(self, theme_name: str):
        """
        Delete a custom theme.
        
        Args:
            theme_name (str): Name of the theme to delete
        """
        try:
            # Don't allow deletion of default themes
            default_themes = ['light', 'dark', 'professional', 'creative']
            if theme_name in default_themes:
                raise ValueError(f"Cannot delete default theme: {theme_name}")
            
            if theme_name in self._themes:
                del self._themes[theme_name]
                logger.info(f"Custom theme '{theme_name}' deleted successfully")
            else:
                logger.warning(f"Theme '{theme_name}' not found")
                
        except Exception as e:
            logger.error(f"Failed to delete custom theme '{theme_name}': {e}")
            raise
    
    def get_themes_info(self) -> Dict[str, Any]:
        """
        Get themes information and statistics.
        
        Returns:
            Dict[str, Any]: Themes information
        """
        try:
            return {
                "themes_count": len(self._themes),
                "available_themes": self.get_available_themes(),
                "current_theme": self.get_current_theme(),
                "theme_history": self.get_theme_history(),
                "initialization_time": self._initialization_time.isoformat(),
                "themes_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get themes info: {e}")
            return {
                "error": str(e),
                "themes_timestamp": datetime.now().isoformat()
            }
