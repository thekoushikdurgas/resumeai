"""
Main Content Module for Resume/CV AI Application
Handles main content area rendering and page management.

This module provides:
- Main content area rendering
- Page management and routing
- Content loading and caching
- Error handling and fallbacks
- Comprehensive logging and monitoring

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from .styles.css_styles import CSSStyles
from .styles.themes import Themes
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("main_content")

class MainContent:
    """
    Main content area component with comprehensive logging.
    
    This class provides the main content area including page management,
    content rendering, error handling, and performance monitoring for
    the Resume/CV AI application.
    
    Key Features:
    - Main content area rendering
    - Page management and routing
    - Content loading and caching
    - Error handling and fallbacks
    - Comprehensive logging and monitoring
    
    Attributes:
        css_styles (CSSStyles): CSS styling manager
        themes (Themes): Theme management system
        page_handlers (Dict[str, Callable]): Dictionary of page handlers
        content_cache (Dict[str, Any]): Content caching system
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize the MainContent with comprehensive logging.
        
        Raises:
            Exception: If MainContent initialization fails
        """
        logger.info("Initializing MainContent")
        self._initialization_time = time.time()
        
        # Initialize styling components
        self.css_styles = CSSStyles()
        self.themes = Themes()
        
        # Initialize page handlers
        self.page_handlers = {}
        
        # Initialize content cache
        self.content_cache = {}
        
        try:
            # Setup page handlers
            logger.debug("Setting up page handlers")
            self._setup_page_handlers()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"MainContent initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.page_handlers)} page handlers")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"MainContent initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Main content area may not function correctly")
            raise
    
    def _setup_page_handlers(self):
        """Setup page handlers for different sections."""
        try:
            # Use PageManager instead of duplicating page management
            from .pages import page_manager
            
            # Get page handlers from PageManager
            self.page_handlers = page_manager._pages.copy()
            
            logger.debug(f"Setup {len(self.page_handlers)} page handlers from PageManager")
        except Exception as e:
            logger.warning(f"Failed to setup page handlers: {e}")
            # Create fallback handlers
            self._create_fallback_handlers()
    
    def _create_fallback_handlers(self):
        """Create fallback page handlers."""
        try:
            self.page_handlers = {
                "📄 Resume Analysis": self._fallback_resume_analysis,
                "🎯 Job Matching": self._fallback_job_matching,
                "✨ AI Enhancement": self._fallback_ai_enhancement,
                "📊 ATS Checker": self._fallback_ats_checker,
                "🔧 Resume Builder": self._fallback_resume_builder,
                "📋 Templates": self._fallback_templates,
                "📈 Career Insights": self._fallback_career_insights,
                "🎨 Customization": self._fallback_customization,
                "Vector Search": self._fallback_vector_search,
                "Export Resume": self._fallback_export_resume,
                "Import Data": self._fallback_import_data,
                "Preferences": self._fallback_preferences,
                "API Keys": self._fallback_api_keys,
                "Help & Support": self._fallback_help_support
            }
            logger.info("Created fallback page handlers")
        except Exception as e:
            logger.error(f"Failed to create fallback handlers: {e}")
            self.page_handlers = {}
    
    def render(self):
        """
        Render the main content area with comprehensive logging.
        
        Raises:
            Exception: If main content rendering fails
        """
        try:
            logger.debug("Rendering main content area")
            start_time = time.time()
            
            # Get current page
            current_page = st.session_state.get('current_page', "📄 Resume Analysis")
            logger.debug(f"Rendering page: {current_page}")
            
            # Check if page handler exists
            if current_page in self.page_handlers:
                # Render page content
                self._render_page_content(current_page)
            else:
                # Render error page
                self._render_error_page(current_page)
            
            rendering_time = time.time() - start_time
            logger.debug(f"Main content rendered in {rendering_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to render main content: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            self._render_error_fallback(e)
    
    def _render_page_content(self, page_name: str):
        """Render specific page content."""
        try:
            # Get page handler
            page_handler = self.page_handlers[page_name]
            
            # Check cache first
            cache_key = f"page_{page_name}_{st.session_state.get('page_version', 0)}"
            if cache_key in self.content_cache:
                logger.debug(f"Using cached content for {page_name}")
                cached_content = self.content_cache[cache_key]
                st.markdown(cached_content, unsafe_allow_html=True)
                return
            
            # Render page content
            logger.debug(f"Rendering fresh content for {page_name}")
            page_handler()
            
            # Cache the rendered content (simplified for now)
            self.content_cache[cache_key] = f"<div>Content for {page_name}</div>"
            
        except Exception as e:
            logger.error(f"Failed to render page content for {page_name}: {e}")
            self._render_error_page(page_name, str(e))
    
    def _render_error_page(self, page_name: str, error_message: str = None):
        """Render error page."""
        try:
            st.error(f"❌ Error loading page: {page_name}")
            
            if error_message:
                st.error(f"Error details: {error_message}")
            
            st.markdown("""
            <div class="error-page">
                <h2>⚠️ Page Error</h2>
                <p>The requested page could not be loaded.</p>
                <p>Please try refreshing the page or contact support if the problem persists.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show retry button
            if st.button("🔄 Retry", key="retry_page"):
                st.rerun()
            
        except Exception as e:
            logger.error(f"Failed to render error page: {e}")
            st.error("Critical error: Unable to render error page")
    
    def _render_error_fallback(self, error: Exception):
        """Render error fallback when main content fails."""
        try:
            st.error("❌ Critical Error: Unable to render main content")
            st.error(f"Error: {str(error)}")
            
            st.markdown("""
            <div class="critical-error">
                <h2>🚨 Critical Error</h2>
                <p>The application encountered a critical error and cannot continue.</p>
                <p>Please refresh the page or contact support.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show emergency actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Refresh Page", key="emergency_refresh"):
                    st.rerun()
            
            with col2:
                if st.button("📧 Contact Support", key="emergency_support"):
                    st.info("Please contact support with the error details above.")
            
        except Exception as e:
            logger.critical(f"Failed to render error fallback: {e}")
            st.write("Critical system failure. Please contact support.")
    
    def _fallback_resume_analysis(self):
        """Fallback resume analysis page."""
        st.title("📄 Resume Analysis")
        st.info("Resume analysis feature is being loaded...")
        st.markdown("Please wait while we initialize the resume analysis module.")
    
    def _fallback_job_matching(self):
        """Fallback job matching page."""
        st.title("🎯 Job Matching")
        st.info("Job matching feature is being loaded...")
        st.markdown("Please wait while we initialize the job matching module.")
    
    def _fallback_ai_enhancement(self):
        """Fallback AI enhancement page."""
        st.title("✨ AI Enhancement")
        st.info("AI enhancement feature is being loaded...")
        st.markdown("Please wait while we initialize the AI enhancement module.")
    
    def _fallback_ats_checker(self):
        """Fallback ATS checker page."""
        st.title("📊 ATS Checker")
        st.info("ATS checker feature is being loaded...")
        st.markdown("Please wait while we initialize the ATS checker module.")
    
    def _fallback_resume_builder(self):
        """Fallback resume builder page."""
        st.title("🔧 Resume Builder")
        st.info("Resume builder feature is being loaded...")
        st.markdown("Please wait while we initialize the resume builder module.")
    
    def _fallback_templates(self):
        """Fallback templates page."""
        st.title("📋 Templates")
        st.info("Templates feature is being loaded...")
        st.markdown("Please wait while we initialize the templates module.")
    
    def _fallback_career_insights(self):
        """Fallback career insights page."""
        st.title("📈 Career Insights")
        st.info("Career insights feature is being loaded...")
        st.markdown("Please wait while we initialize the career insights module.")
    
    def _fallback_customization(self):
        """Fallback customization page."""
        st.title("🎨 Customization")
        st.info("Customization feature is being loaded...")
        st.markdown("Please wait while we initialize the customization module.")
    
    def _fallback_vector_search(self):
        """Fallback vector search page."""
        st.title("🔍 Vector Search")
        st.info("Vector search feature is being loaded...")
        st.markdown("Please wait while we initialize the vector search module.")
    
    def _fallback_export_resume(self):
        """Fallback export resume page."""
        st.title("💾 Export Resume")
        st.info("Export resume feature is being loaded...")
        st.markdown("Please wait while we initialize the export resume module.")
    
    def _fallback_import_data(self):
        """Fallback import data page."""
        st.title("📥 Import Data")
        st.info("Import data feature is being loaded...")
        st.markdown("Please wait while we initialize the import data module.")
    
    def _fallback_preferences(self):
        """Fallback preferences page."""
        st.title("⚙️ Preferences")
        st.info("Preferences feature is being loaded...")
        st.markdown("Please wait while we initialize the preferences module.")
    
    def _fallback_api_keys(self):
        """Fallback API keys page."""
        st.title("🔑 API Keys")
        st.info("API keys feature is being loaded...")
        st.markdown("Please wait while we initialize the API keys module.")
    
    def _fallback_help_support(self):
        """Fallback help & support page."""
        st.title("❓ Help & Support")
        st.info("Help & support feature is being loaded...")
        st.markdown("Please wait while we initialize the help & support module.")
    
    def add_page_handler(self, page_name: str, handler: Callable):
        """
        Add a new page handler.
        
        Args:
            page_name (str): Name of the page
            handler (Callable): Function to handle page rendering
        """
        try:
            self.page_handlers[page_name] = handler
            logger.info(f"Added page handler for: {page_name}")
        except Exception as e:
            logger.error(f"Failed to add page handler for {page_name}: {e}")
    
    def remove_page_handler(self, page_name: str):
        """
        Remove a page handler.
        
        Args:
            page_name (str): Name of the page to remove
        """
        try:
            if page_name in self.page_handlers:
                del self.page_handlers[page_name]
                logger.info(f"Removed page handler for: {page_name}")
            else:
                logger.warning(f"Page handler not found: {page_name}")
        except Exception as e:
            logger.error(f"Failed to remove page handler for {page_name}: {e}")
    
    def clear_cache(self):
        """Clear content cache."""
        try:
            self.content_cache.clear()
            logger.info("Content cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
    
    def get_page_handlers(self) -> Dict[str, Callable]:
        """
        Get all page handlers.
        
        Returns:
            Dict[str, Callable]: Dictionary of page handlers
        """
        return self.page_handlers
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache information.
        
        Returns:
            Dict[str, Any]: Cache information
        """
        try:
            return {
                "cache_size": len(self.content_cache),
                "cache_keys": list(self.content_cache.keys()),
                "cache_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get cache info: {e}")
            return {"error": str(e)}
    
    def get_main_content_info(self) -> Dict[str, Any]:
        """
        Get main content information and statistics.
        
        Returns:
            Dict[str, Any]: Main content information
        """
        try:
            return {
                "page_handlers_count": len(self.page_handlers),
                "current_page": st.session_state.get('current_page', "📄 Resume Analysis"),
                "cache_info": self.get_cache_info(),
                "initialization_time": self._initialization_time,
                "main_content_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get main content info: {e}")
            return {
                "error": str(e),
                "main_content_timestamp": datetime.now().isoformat()
            }
