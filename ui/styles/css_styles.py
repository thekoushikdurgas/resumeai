"""
CSS Styles Module for Resume/CV AI Application
Handles CSS styling and theme management.

This module provides:
- CSS styling system
- Theme management
- Responsive design
- Component styling
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
logger = setup_logger("css_styles")

class CSSStyles:
    """
    CSS styling system with comprehensive logging.
    
    This class provides CSS styling including themes, responsive design,
    component styling, and dynamic style generation for the Resume/CV AI
    application.
    
    Key Features:
    - CSS styling system
    - Theme management
    - Responsive design
    - Component styling
    - Comprehensive logging
    
    Attributes:
        _initialization_time (float): Timestamp of initialization start
        _styles_cache (Dict[str, str]): CSS styles cache
        _theme_styles (Dict[str, Dict]): Theme-specific styles
    """
    
    def __init__(self):
        """Initialize CSS styles with comprehensive logging."""
        logger.info("Initializing CSS Styles")
        self._initialization_time = datetime.now()
        
        # Initialize styles cache
        self._styles_cache = {}
        
        # Initialize theme styles
        self._theme_styles = {}
        
        try:
            # Setup base styles
            logger.debug("Setting up base styles")
            self._setup_base_styles()
            
            # Setup theme styles
            logger.debug("Setting up theme styles")
            self._setup_theme_styles()
            
            logger.info("CSS Styles initialized successfully")
            
        except Exception as e:
            logger.error(f"CSS Styles initialization failed: {e}")
            logger.error("Styling may not function correctly")
            raise
    
    def _setup_base_styles(self):
        """Setup base CSS styles."""
        try:
            base_styles = """
            <style>
            /* Base Styles */
            .main-container {
                padding: 1rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .sidebar-header {
                text-align: center;
                padding: 1rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .sidebar-header h2 {
                margin: 0;
                color: #2c3e50;
                font-size: 1.5rem;
            }
            
            .nav-item {
                padding: 0.5rem;
                margin: 0.25rem 0;
                border-radius: 0.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .nav-item:hover {
                background-color: #f0f0f0;
                transform: translateX(5px);
            }
            
            .nav-item.current {
                background-color: #007bff;
                color: white;
            }
            
            .nav-icon {
                margin-right: 0.5rem;
                font-size: 1.2rem;
            }
            
            .nav-title {
                font-weight: 500;
            }
            
            /* Page Item Styles */
            .page-item {
                padding: 0.5rem;
                margin: 0.25rem 0;
                border-radius: 0.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                width: 100%;
                border: none;
                background: transparent;
                text-align: left;
            }
            
            .page-item:hover {
                background-color: #f0f0f0;
                transform: translateX(5px);
            }
            
            .page-item.current {
                background-color: #007bff;
                color: white;
                font-weight: 600;
            }
            
            .page-icon {
                margin-right: 0.5rem;
                font-size: 1.1rem;
                min-width: 1.5rem;
            }
            
            .page-title {
                font-weight: 500;
                flex: 1;
            }
            
            /* Expander Styles */
            .streamlit-expander {
                border: 1px solid #e0e0e0;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
            }
            
            .streamlit-expanderHeader {
                background-color: #f8f9fa;
                border-radius: 0.5rem 0.5rem 0 0;
                padding: 0.75rem;
                font-weight: 600;
                color: #2c3e50;
            }
            
            .streamlit-expanderContent {
                padding: 0.5rem;
            }
            
            /* Sidebar Expander Custom Styles */
            .sidebar-expander {
                margin: 0.5rem 0;
                border: 1px solid #e0e0e0;
                border-radius: 0.5rem;
                overflow: hidden;
            }
            
            .sidebar-expander-header {
                background-color: #f8f9fa;
                padding: 0.75rem;
                font-weight: 600;
                color: #2c3e50;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .sidebar-expander-content {
                padding: 0.5rem;
                background-color: white;
            }
            
            .error-page {
                text-align: center;
                padding: 2rem;
                background-color: #f8f9fa;
                border-radius: 0.5rem;
                margin: 2rem 0;
            }
            
            .critical-error {
                text-align: center;
                padding: 2rem;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 0.5rem;
                margin: 2rem 0;
            }
            
            .sidebar-footer {
                text-align: center;
                padding: 1rem 0;
                border-top: 1px solid #e0e0e0;
                margin-top: auto;
            }
            
            .sidebar-footer p {
                margin: 0.25rem 0;
                color: #6c757d;
                font-size: 0.875rem;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .main-container {
                    padding: 0.5rem;
                }
                
                .sidebar-header h2 {
                    font-size: 1.25rem;
                }
            }
            </style>
            """
            
            self._styles_cache['base'] = base_styles
            logger.debug("Base styles setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup base styles: {e}")
            raise
    
    def _setup_theme_styles(self):
        """Setup theme-specific styles."""
        try:
            # Light theme
            self._theme_styles['light'] = {
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'background_color': '#ffffff',
                'text_color': '#212529',
                'border_color': '#dee2e6'
            }
            
            # Dark theme
            self._theme_styles['dark'] = {
                'primary_color': '#0d6efd',
                'secondary_color': '#adb5bd',
                'background_color': '#212529',
                'text_color': '#ffffff',
                'border_color': '#495057'
            }
            
            # Professional theme
            self._theme_styles['professional'] = {
                'primary_color': '#2c3e50',
                'secondary_color': '#7f8c8d',
                'background_color': '#ffffff',
                'text_color': '#2c3e50',
                'border_color': '#bdc3c7'
            }
            
            # Creative theme
            self._theme_styles['creative'] = {
                'primary_color': '#e74c3c',
                'secondary_color': '#f39c12',
                'background_color': '#ffffff',
                'text_color': '#2c3e50',
                'border_color': '#ecf0f1'
            }
            
            logger.debug(f"Setup {len(self._theme_styles)} theme styles")
            
        except Exception as e:
            logger.error(f"Failed to setup theme styles: {e}")
            raise
    
    def apply_base_styles(self):
        """Apply base styles to the application."""
        try:
            if 'base' in self._styles_cache:
                st.markdown(self._styles_cache['base'], unsafe_allow_html=True)
                logger.debug("Base styles applied")
            else:
                logger.warning("Base styles not found in cache")
        except Exception as e:
            logger.error(f"Failed to apply base styles: {e}")
    
    def apply_theme(self, theme_name: str):
        """
        Apply theme styles to the application.
        
        Args:
            theme_name (str): Name of the theme to apply
        """
        try:
            if theme_name in self._theme_styles:
                theme = self._theme_styles[theme_name]
                
                theme_css = f"""
                <style>
                :root {{
                    --primary-color: {theme['primary_color']};
                    --secondary-color: {theme['secondary_color']};
                    --background-color: {theme['background_color']};
                    --text-color: {theme['text_color']};
                    --border-color: {theme['border_color']};
                }}
                
                .main-container {{
                    background-color: var(--background-color);
                    color: var(--text-color);
                }}
                
                .nav-item.current {{
                    background-color: var(--primary-color);
                }}
                
                .sidebar-header h2 {{
                    color: var(--primary-color);
                }}
                </style>
                """
                
                st.markdown(theme_css, unsafe_allow_html=True)
                logger.info(f"Theme '{theme_name}' applied successfully")
            else:
                logger.warning(f"Theme '{theme_name}' not found")
                self.apply_theme('light')  # Fallback to light theme
                
        except Exception as e:
            logger.error(f"Failed to apply theme '{theme_name}': {e}")
            self.apply_theme('light')  # Fallback to light theme
    
    def get_theme_styles(self, theme_name: str) -> Dict[str, str]:
        """
        Get theme styles.
        
        Args:
            theme_name (str): Name of the theme
            
        Returns:
            Dict[str, str]: Theme styles
        """
        try:
            if theme_name in self._theme_styles:
                return self._theme_styles[theme_name]
            else:
                logger.warning(f"Theme '{theme_name}' not found")
                return self._theme_styles['light']
        except Exception as e:
            logger.error(f"Failed to get theme styles for '{theme_name}': {e}")
            return self._theme_styles['light']
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available themes.
        
        Returns:
            List[str]: List of available theme names
        """
        try:
            return list(self._theme_styles.keys())
        except Exception as e:
            logger.error(f"Failed to get available themes: {e}")
            return ['light']
    
    def add_custom_style(self, style_name: str, css_content: str):
        """
        Add custom CSS style.
        
        Args:
            style_name (str): Name of the style
            css_content (str): CSS content
        """
        try:
            self._styles_cache[style_name] = css_content
            logger.info(f"Custom style '{style_name}' added")
        except Exception as e:
            logger.error(f"Failed to add custom style '{style_name}': {e}")
    
    def apply_custom_style(self, style_name: str):
        """
        Apply custom CSS style.
        
        Args:
            style_name (str): Name of the style to apply
        """
        try:
            if style_name in self._styles_cache:
                st.markdown(self._styles_cache[style_name], unsafe_allow_html=True)
                logger.debug(f"Custom style '{style_name}' applied")
            else:
                logger.warning(f"Custom style '{style_name}' not found")
        except Exception as e:
            logger.error(f"Failed to apply custom style '{style_name}': {e}")
    
    def get_css_styles_info(self) -> Dict[str, Any]:
        """
        Get CSS styles information and statistics.
        
        Returns:
            Dict[str, Any]: CSS styles information
        """
        try:
            return {
                "themes_count": len(self._theme_styles),
                "available_themes": self.get_available_themes(),
                "custom_styles_count": len(self._styles_cache),
                "custom_styles": list(self._styles_cache.keys()),
                "initialization_time": self._initialization_time.isoformat(),
                "css_styles_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get CSS styles info: {e}")
            return {
                "error": str(e),
                "css_styles_timestamp": datetime.now().isoformat()
            }
