"""
Pages Module for Resume/CV AI Application
Handles page rendering and management.

This module provides:
- Page rendering system
- Page management
- Page routing
- Page caching
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("pages")

class PageManager:
    """
    Page management system with comprehensive logging.
    
    This class provides page management including page registration,
    routing, caching, and rendering for the Resume/CV AI application.
    
    Key Features:
    - Page rendering system
    - Page management
    - Page routing
    - Page caching
    - Comprehensive logging
    
    Attributes:
        _initialization_time (float): Timestamp of initialization start
        _pages (Dict[str, Callable]): Registered pages
        _page_cache (Dict[str, Any]): Page content cache
        _page_history (List[str]): Page navigation history
    """
    
    def __init__(self):
        """Initialize page manager with comprehensive logging."""
        logger.info("Initializing Page Manager")
        self._initialization_time = datetime.now()
        
        # Initialize pages
        self._pages = {}
        
        # Initialize page cache with TTL
        self._page_cache = {}
        self._cache_ttl = 300  # 5 minutes
        self._cache_timestamps = {}
        
        # Initialize page history
        self._page_history = []
        
        try:
            # Register default pages
            logger.debug("Registering default pages")
            self._register_default_pages()
            
            logger.info("Page Manager initialized successfully")
            logger.info(f"Registered {len(self._pages)} pages")
            
        except Exception as e:
            logger.error(f"Page Manager initialization failed: {e}")
            logger.error("Page management may not function correctly")
            raise
    
    def _register_default_pages(self):
        """Register default pages."""
        try:
            # Import page modules
            from . import (
                resume_analysis,
                job_matching,
                ai_enhancement,
                ats_checker,
                resume_builder,
                templates,
                career_insights,
                customization,
                vector_search,
                export_resume,
                import_data,
                preferences,
                api_keys,
                help_support,
                linkedin_job_scraper
            )
            
            # Register pages
            self._pages = {
                "📄 Resume Analysis": resume_analysis.render,
                "🎯 Job Matching": job_matching.render,
                "✨ AI Enhancement": ai_enhancement.render,
                "📊 ATS Checker": ats_checker.render,
                "🔧 Resume Builder": resume_builder.render,
                "📋 Templates": templates.render,
                "📈 Career Insights": career_insights.render,
                "🎨 Customization": customization.render,
                "Vector Search": vector_search.render,
                "Export Resume": export_resume.render,
                "Import Data": import_data.render,
                "Preferences": preferences.render,
                "API Keys": api_keys.render,
                "Help & Support": help_support.render,
                "🔍 LinkedIn Job Scraper": linkedin_job_scraper.main
            }
            
            logger.debug(f"Registered {len(self._pages)} default pages")
            
        except Exception as e:
            logger.warning(f"Failed to register default pages: {e}")
            # Create fallback pages
            self._create_fallback_pages()
    
    def _create_fallback_pages(self):
        """Create fallback pages when imports fail."""
        try:
            self._pages = {
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
                "Help & Support": self._fallback_help_support,
                "🔍 LinkedIn Job Scraper": self._fallback_linkedin_job_scraper
            }
            logger.info("Created fallback pages")
        except Exception as e:
            logger.error(f"Failed to create fallback pages: {e}")
            self._pages = {}
    
    def _fallback_resume_analysis(self):
        """Fallback resume analysis page."""
        import streamlit as st
        st.title("📄 Resume Analysis")
        st.info("Resume analysis feature is being loaded...")
        st.markdown("Please wait while we initialize the resume analysis module.")
    
    def _fallback_job_matching(self):
        """Fallback job matching page."""
        import streamlit as st
        st.title("🎯 Job Matching")
        st.info("Job matching feature is being loaded...")
        st.markdown("Please wait while we initialize the job matching module.")
    
    def _fallback_ai_enhancement(self):
        """Fallback AI enhancement page."""
        import streamlit as st
        st.title("✨ AI Enhancement")
        st.info("AI enhancement feature is being loaded...")
        st.markdown("Please wait while we initialize the AI enhancement module.")
    
    def _fallback_ats_checker(self):
        """Fallback ATS checker page."""
        import streamlit as st
        st.title("📊 ATS Checker")
        st.info("ATS checker feature is being loaded...")
        st.markdown("Please wait while we initialize the ATS checker module.")
    
    def _fallback_resume_builder(self):
        """Fallback resume builder page."""
        import streamlit as st
        st.title("🔧 Resume Builder")
        st.info("Resume builder feature is being loaded...")
        st.markdown("Please wait while we initialize the resume builder module.")
    
    def _fallback_templates(self):
        """Fallback templates page."""
        import streamlit as st
        st.title("📋 Templates")
        st.info("Templates feature is being loaded...")
        st.markdown("Please wait while we initialize the templates module.")
    
    def _fallback_career_insights(self):
        """Fallback career insights page."""
        import streamlit as st
        st.title("📈 Career Insights")
        st.info("Career insights feature is being loaded...")
        st.markdown("Please wait while we initialize the career insights module.")
    
    def _fallback_customization(self):
        """Fallback customization page."""
        import streamlit as st
        st.title("🎨 Customization")
        st.info("Customization feature is being loaded...")
        st.markdown("Please wait while we initialize the customization module.")
    
    def _fallback_vector_search(self):
        """Fallback vector search page."""
        import streamlit as st
        st.title("🔍 Vector Search")
        st.info("Vector search feature is being loaded...")
        st.markdown("Please wait while we initialize the vector search module.")
    
    def _fallback_export_resume(self):
        """Fallback export resume page."""
        import streamlit as st
        st.title("💾 Export Resume")
        st.info("Export resume feature is being loaded...")
        st.markdown("Please wait while we initialize the export resume module.")
    
    def _fallback_import_data(self):
        """Fallback import data page."""
        import streamlit as st
        st.title("📥 Import Data")
        st.info("Import data feature is being loaded...")
        st.markdown("Please wait while we initialize the import data module.")
    
    def _fallback_preferences(self):
        """Fallback preferences page."""
        import streamlit as st
        st.title("⚙️ Preferences")
        st.info("Preferences feature is being loaded...")
        st.markdown("Please wait while we initialize the preferences module.")
    
    def _fallback_api_keys(self):
        """Fallback API keys page."""
        import streamlit as st
        st.title("🔑 API Keys")
        st.info("API keys feature is being loaded...")
        st.markdown("Please wait while we initialize the API keys module.")
    
    def _fallback_help_support(self):
        """Fallback help & support page."""
        import streamlit as st
        st.title("❓ Help & Support")
        st.info("Help & support feature is being loaded...")
        st.markdown("Please wait while we initialize the help & support module.")
    
    def _fallback_linkedin_job_scraper(self):
        """Fallback LinkedIn job scraper page."""
        import streamlit as st
        st.title("🔍 LinkedIn Job Scraper")
        st.info("LinkedIn job scraper feature is being loaded...")
        st.markdown("Please wait while we initialize the LinkedIn job scraper module.")
    
    def register_page(self, page_name: str, page_handler: Callable):
        """
        Register a new page.
        
        Args:
            page_name (str): Name of the page
            page_handler (Callable): Function to handle page rendering
        """
        try:
            self._pages[page_name] = page_handler
            logger.info(f"Page '{page_name}' registered successfully")
        except Exception as e:
            logger.error(f"Failed to register page '{page_name}': {e}")
    
    def unregister_page(self, page_name: str):
        """
        Unregister a page.
        
        Args:
            page_name (str): Name of the page to unregister
        """
        try:
            if page_name in self._pages:
                del self._pages[page_name]
                logger.info(f"Page '{page_name}' unregistered successfully")
            else:
                logger.warning(f"Page '{page_name}' not found")
        except Exception as e:
            logger.error(f"Failed to unregister page '{page_name}': {e}")
    
    def render_page(self, page_name: str):
        """
        Render a specific page.
        
        Args:
            page_name (str): Name of the page to render
        """
        try:
            if page_name in self._pages:
                # Add to history
                self._page_history.append(page_name)
                
                # Render page
                self._pages[page_name]()
                logger.debug(f"Page '{page_name}' rendered successfully")
            else:
                logger.warning(f"Page '{page_name}' not found")
                self._render_error_page(page_name)
        except Exception as e:
            logger.error(f"Failed to render page '{page_name}': {e}")
            self._render_error_page(page_name, str(e))
    
    def _render_error_page(self, page_name: str, error_message: str = None):
        """Render error page."""
        try:
            import streamlit as st
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
            
        except Exception as e:
            logger.error(f"Failed to render error page: {e}")
    
    def get_available_pages(self) -> List[str]:
        """
        Get list of available pages.
        
        Returns:
            List[str]: List of available page names
        """
        try:
            return list(self._pages.keys())
        except Exception as e:
            logger.error(f"Failed to get available pages: {e}")
            return []
    
    def get_page_history(self) -> List[str]:
        """
        Get page navigation history.
        
        Returns:
            List[str]: List of page names in chronological order
        """
        try:
            return self._page_history.copy()
        except Exception as e:
            logger.error(f"Failed to get page history: {e}")
            return []
    
    def get_page_manager_info(self) -> Dict[str, Any]:
        """
        Get page manager information and statistics.
        
        Returns:
            Dict[str, Any]: Page manager information
        """
        try:
            return {
                "pages_count": len(self._pages),
                "available_pages": self.get_available_pages(),
                "page_history": self.get_page_history(),
                "cache_size": len(self._page_cache),
                "cache_ttl": self._cache_ttl,
                "initialization_time": self._initialization_time.isoformat(),
                "page_manager_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get page manager info: {e}")
            return {
                "error": str(e),
                "page_manager_timestamp": datetime.now().isoformat()
            }
    
    def clear_cache(self):
        """Clear the page cache."""
        try:
            self._page_cache.clear()
            self._cache_timestamps.clear()
            logger.info("Page cache cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear page cache: {e}")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information."""
        try:
            return {
                "cache_size": len(self._page_cache),
                "cache_ttl": self._cache_ttl,
                "cached_pages": list(self._page_cache.keys()),
                "cache_timestamps": self._cache_timestamps
            }
        except Exception as e:
            logger.error(f"Failed to get cache info: {e}")
            return {"error": str(e)}

# Create global page manager instance
page_manager = PageManager()

# Export page manager functions
def register_page(page_name: str, page_handler: Callable):
    """Register a new page."""
    page_manager.register_page(page_name, page_handler)

def unregister_page(page_name: str):
    """Unregister a page."""
    page_manager.unregister_page(page_name)

def render_page(page_name: str):
    """Render a specific page."""
    page_manager.render_page(page_name)

def get_available_pages() -> List[str]:
    """Get list of available pages."""
    return page_manager.get_available_pages()

def get_page_history() -> List[str]:
    """Get page navigation history."""
    return page_manager.get_page_history()

def get_page_manager_info() -> Dict[str, Any]:
    """Get page manager information and statistics."""
    return page_manager.get_page_manager_info()
