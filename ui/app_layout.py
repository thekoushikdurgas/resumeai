"""
Main Application Layout Module for Resume/CV AI Application
Handles the overall application layout and navigation structure.

This module provides:
- Main application layout management
- Navigation structure and routing
- Page state management
- Responsive layout handling
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from .sidebar import Sidebar
from .tabs.analysis_tab import AnalysisTab
from .tabs.job_matching_tab import JobMatchingTab
from .tabs.enhancement_tab import EnhancementTab
from .tabs.ats_checker_tab import ATSCheckerTab
from .tabs.builder_tab import BuilderTab
from .tabs.templates_tab import TemplatesTab
from .tabs.insights_tab import InsightsTab
from .tabs.customization_tab import CustomizationTab
from .styles.css_styles import CSSStyles
from .styles.themes import Themes
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("app_layout")

class AppLayout:
    """
    Main application layout manager with comprehensive logging.
    
    This class provides the overall application structure including
    navigation, page routing, state management, and responsive design
    for the Resume/CV AI application.
    
    Key Features:
    - Main application layout management
    - Navigation structure and routing
    - Page state management
    - Responsive layout handling
    - Comprehensive logging and error handling
    
    Attributes:
        sidebar (Sidebar): Sidebar navigation component
        tabs (Dict): Dictionary of available tabs
        css_styles (CSSStyles): CSS styling manager
        themes (Themes): Theme management system
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize the AppLayout with comprehensive logging.
        
        Raises:
            Exception: If AppLayout initialization fails
        """
        logger.info("Initializing AppLayout")
        self._initialization_time = time.time()
        
        # Initialize components
        self.sidebar = None
        self.css_styles = None
        self.themes = None
        
        # Component loading optimization
        self._components_loaded = False
        self._lazy_components = {}
        
        try:
            # Initialize styling components
            logger.debug("Initializing styling components")
            self.css_styles = CSSStyles()
            self.themes = Themes()
            
            # Initialize UI components with lazy loading
            logger.debug("Initializing UI components with lazy loading")
            self._initialize_ui_components()
            
            # Tabs are now handled by PageManager
            logger.debug("Using PageManager for page rendering")
            
            # Setup page configuration
            logger.debug("Setting up page configuration")
            self._setup_page_config()
            
            # Apply initial styling
            logger.debug("Applying initial styling")
            self._apply_initial_styling()
            
            # Apply responsive design
            logger.debug("Applying responsive design")
            self._apply_responsive_design()
            
            # Apply animations
            logger.debug("Applying animations")
            self._apply_animations()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"AppLayout initialized successfully in {initialization_time:.2f}s")
            logger.info("Using PageManager for page rendering")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"AppLayout initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Application layout may not function correctly")
            raise
    
    
    def _setup_page_config(self):
        """Setup Streamlit page configuration."""
        try:
            st.set_page_config(
                page_title="Resume/CV AI Assistant",
                page_icon="🤖",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://github.com/your-repo/resumeai',
                    'Report a bug': 'https://github.com/your-repo/resumeai/issues',
                    'About': 'Resume/CV AI Assistant - AI-powered resume analysis and optimization'
                }
            )
            logger.debug("Page configuration set up successfully")
        except Exception as e:
            logger.warning(f"Failed to setup page configuration: {e}")
    
    def _apply_initial_styling(self):
        """Apply initial CSS styling to the application."""
        try:
            # Apply base CSS styles
            self.css_styles.apply_base_styles()
            
            # Apply theme
            current_theme = st.session_state.get('theme', 'light')
            self.themes.apply_theme(current_theme)
            
            logger.debug("Initial styling applied successfully")
        except Exception as e:
            logger.warning(f"Failed to apply initial styling: {e}")
    
    def _apply_responsive_design(self):
        """Apply responsive design system."""
        try:
            from ui.styles.responsive import Responsive
            
            # Initialize responsive design
            responsive = Responsive()
            
            # Apply responsive styles
            responsive.render_responsive_styles()
            
            logger.debug("Responsive design applied successfully")
        except Exception as e:
            logger.warning(f"Failed to apply responsive design: {e}")
    
    def _apply_animations(self):
        """Apply animation system."""
        try:
            from ui.styles.animations import Animations
            
            # Initialize animations
            animations = Animations()
            
            # Apply animation styles
            animations.render_animation_styles()
            
            logger.debug("Animations applied successfully")
        except Exception as e:
            logger.warning(f"Failed to apply animations: {e}")
    
    def _initialize_ui_components(self):
        """Initialize UI components with lazy loading optimization."""
        try:
            # Only initialize essential components immediately
            self.sidebar = Sidebar()
            
            # Mark components as loaded
            self._components_loaded = True
            
            logger.debug("UI components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize UI components: {e}")
            self._components_loaded = False
    
    def _get_lazy_component(self, component_name: str):
        """Get a component with lazy loading."""
        try:
            if component_name not in self._lazy_components:
                # Lazy load the component
                if component_name == "charts":
                    from ui.components.charts import Charts
                    self._lazy_components[component_name] = Charts()
                elif component_name == "forms":
                    from ui.components.forms import Forms
                    self._lazy_components[component_name] = Forms()
                elif component_name == "modals":
                    from ui.components.modals import Modals
                    self._lazy_components[component_name] = Modals()
                # Add more components as needed
                
                logger.debug(f"Lazy loaded component: {component_name}")
            
            return self._lazy_components[component_name]
        except Exception as e:
            logger.error(f"Failed to lazy load component {component_name}: {e}")
            return None
    
    def render(self):
        """
        Render the main application layout with comprehensive logging.
        
        Raises:
            Exception: If layout rendering fails
        """
        try:
            logger.debug("Rendering main application layout")
            start_time = time.time()
            
            # Initialize session state
            self._initialize_session_state()
            
            # Create main layout columns
            # col1, col2 = st.columns([1, 4])
            
            with st.sidebar:
                # Render sidebar
                self.sidebar.render()
            
            # with col2:
            #     # Render main content
            self._render_main_content()
            
            
            rendering_time = time.time() - start_time
            logger.debug(f"Main layout rendered in {rendering_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to render main application layout: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            st.error(f"Application layout error: {e}")
            raise
    
    def _initialize_session_state(self):
        """Initialize session state variables."""
        try:
            # Initialize default session state
            if 'current_page' not in st.session_state:
                st.session_state.current_page = "📄 Resume Analysis"
            
            if 'theme' not in st.session_state:
                st.session_state.theme = 'light'
            
            if 'resume_data' not in st.session_state:
                st.session_state.resume_data = None
            
            if 'job_data' not in st.session_state:
                st.session_state.job_data = None
            
            if 'analysis_results' not in st.session_state:
                st.session_state.analysis_results = None
            
            if 'user_preferences' not in st.session_state:
                st.session_state.user_preferences = {
                    'auto_save': True,
                    'notifications': True,
                    'theme': 'light',
                    'language': 'en'
                }
            
            logger.debug("Session state initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize session state: {e}")
    
    def _render_main_content(self):
        """Render the main content area based on current page."""
        try:
            current_page = st.session_state.get('current_page', "📄 Resume Analysis")
            
            # Use PageManager to render the page
            from ui.pages import render_page
            render_page(current_page)
            
        except Exception as e:
            logger.error(f"Failed to render main content: {e}")
            st.error(f"Content rendering error: {e}")
    
    def switch_page(self, page_name: str):
        """
        Switch to a different page.
        
        Args:
            page_name (str): Name of the page to switch to
        """
        try:
            available_pages = self.get_available_pages()
            if page_name in available_pages:
                st.session_state.current_page = page_name
                logger.info(f"Switched to page: {page_name}")
                st.rerun()
            else:
                logger.warning(f"Page not found: {page_name}")
                st.error(f"Page '{page_name}' not found")
        except Exception as e:
            logger.error(f"Failed to switch page: {e}")
            st.error(f"Page switch error: {e}")
    
    def get_current_page(self) -> str:
        """
        Get the current page name.
        
        Returns:
            str: Current page name
        """
        return st.session_state.get('current_page', "📄 Resume Analysis")
    
    def get_available_pages(self) -> List[str]:
        """
        Get list of available pages.
        
        Returns:
            List[str]: List of available page names
        """
        try:
            from ui.pages import get_available_pages
            return get_available_pages()
        except Exception as e:
            logger.error(f"Failed to get available pages: {e}")
            return []
    
    def apply_theme(self, theme_name: str):
        """
        Apply a specific theme to the application.
        
        Args:
            theme_name (str): Name of the theme to apply
        """
        try:
            logger.debug(f"Applying theme: {theme_name}")
            
            # Update session state
            st.session_state.theme = theme_name
            
            # Apply theme
            self.themes.apply_theme(theme_name)
            
            logger.info(f"Theme applied successfully: {theme_name}")
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_name}: {e}")
            st.error(f"Theme application error: {e}")
    
    def get_theme(self) -> str:
        """
        Get the current theme name.
        
        Returns:
            str: Current theme name
        """
        return st.session_state.get('theme', 'light')
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available themes.
        
        Returns:
            List[str]: List of available theme names
        """
        return self.themes.get_available_themes()
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """
        Update user preferences.
        
        Args:
            preferences (Dict[str, Any]): Dictionary of preferences to update
        """
        try:
            logger.debug("Updating user preferences")
            
            # Update session state
            current_preferences = st.session_state.get('user_preferences', {})
            current_preferences.update(preferences)
            st.session_state.user_preferences = current_preferences
            
            # Apply theme if changed
            if 'theme' in preferences:
                self.apply_theme(preferences['theme'])
            
            logger.info("User preferences updated successfully")
        except Exception as e:
            logger.error(f"Failed to update user preferences: {e}")
            st.error(f"Preferences update error: {e}")
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Get current user preferences.
        
        Returns:
            Dict[str, Any]: Current user preferences
        """
        return st.session_state.get('user_preferences', {})
    
    def show_loading_state(self, message: str = "Loading..."):
        """
        Show loading state with spinner.
        
        Args:
            message (str): Loading message to display
        """
        try:
            with st.spinner(message):
                time.sleep(0.1)  # Small delay to show spinner
        except Exception as e:
            logger.warning(f"Failed to show loading state: {e}")
    
    def show_error_message(self, error: str, details: str = None):
        """
        Show error message to user.
        
        Args:
            error (str): Error message to display
            details (str): Additional error details (optional)
        """
        try:
            st.error(f"❌ {error}")
            if details:
                with st.expander("Error Details"):
                    st.code(details)
        except Exception as e:
            logger.warning(f"Failed to show error message: {e}")
    
    def show_success_message(self, message: str):
        """
        Show success message to user.
        
        Args:
            message (str): Success message to display
        """
        try:
            st.success(f"✅ {message}")
        except Exception as e:
            logger.warning(f"Failed to show success message: {e}")
    
    def show_warning_message(self, message: str):
        """
        Show warning message to user.
        
        Args:
            message (str): Warning message to display
        """
        try:
            st.warning(f"⚠️ {message}")
        except Exception as e:
            logger.warning(f"Failed to show warning message: {e}")
    
    def show_info_message(self, message: str):
        """
        Show info message to user.
        
        Args:
            message (str): Info message to display
        """
        try:
            st.info(f"ℹ️ {message}")
        except Exception as e:
            logger.warning(f"Failed to show info message: {e}")
    
    def get_layout_info(self) -> Dict[str, Any]:
        """
        Get layout information and statistics.
        
        Returns:
            Dict[str, Any]: Layout information
        """
        try:
            return {
                "available_pages": self.get_available_pages(),
                "current_page": self.get_current_page(),
                "current_theme": self.get_theme(),
                "available_themes": self.get_available_themes(),
                "user_preferences": self.get_user_preferences(),
                "initialization_time": self._initialization_time,
                "layout_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get layout info: {e}")
            return {
                "error": str(e),
                "layout_timestamp": datetime.now().isoformat()
            }
