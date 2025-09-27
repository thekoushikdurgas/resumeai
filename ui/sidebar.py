"""
Sidebar Module for Resume/CV AI Application
Handles sidebar navigation and settings with expandable sections.

This module provides:
- Sidebar navigation menu with expandable sections
- User settings and preferences
- Quick actions and shortcuts
- Status indicators and information
- Page item management system
- Comprehensive logging and error handling

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
logger = setup_logger("sidebar")

class PageItem:
    """
    Page item class for managing individual page items in expandable sections.
    
    This class provides:
    - Page item management
    - Click handling
    - State management
    - Visual representation
    """
    
    def __init__(self, title: str, page_handler: Callable = None, default: bool = False, 
                 icon: str = "", description: str = ""):
        """
        Initialize a page item.
        
        Args:
            title (str): Display title of the page item
            page_handler (Callable): Function to call when item is clicked
            default (bool): Whether this is the default page
            icon (str): Icon to display with the item
            description (str): Description text for the item
        """
        self.title = title
        self.page_handler = page_handler
        self.default = default
        self.icon = icon
        self.description = description
        self.key = f"page_item_{title.lower().replace(' ', '_')}"
    
    def render(self, is_current: bool = False):
        """
        Render the page item.
        
        Args:
            is_current (bool): Whether this is the current page
        """
        try:
            # Create button with appropriate styling
            button_text = f"{self.icon} {self.title}" if self.icon else self.title
            button_color = "primary" if is_current else "secondary"
            # if is_current:
            #     # Show current page with different styling
            #     st.markdown(f"""
            #     <div class="page-item current">
            #         <span class="page-icon">{self.icon}</span>
            #         <span class="page-title">{self.title}</span>
            #     </div>
            #     """, unsafe_allow_html=True)
                
            #     if self.description:
            #         st.caption(self.description)
            # else:
            # Create clickable button
            if st.button(button_text, key=self.key, use_container_width=True, type=button_color):
                if self.page_handler:
                    self.page_handler()
                else:
                    # Default behavior - set current page
                    st.session_state.current_page = self.title
                    st.rerun()
                        
        except Exception as e:
            logger.error(f"Failed to render page item '{self.title}': {e}")

class Sidebar:
    """
    Sidebar navigation component with expandable sections and comprehensive logging.
    
    This class provides the sidebar navigation including expandable menu sections,
    user settings, quick actions, and status indicators for the Resume/CV AI application.
    
    Key Features:
    - Expandable sidebar navigation sections
    - Page item management system
    - User settings and preferences
    - Quick actions and shortcuts
    - Status indicators and information
    - Comprehensive logging and error handling
    
    Attributes:
        css_styles (CSSStyles): CSS styling manager
        themes (Themes): Theme management system
        navigation_sections (Dict[str, List[PageItem]]): Dictionary of navigation sections
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize the Sidebar with comprehensive logging.
        
        Raises:
            Exception: If Sidebar initialization fails
        """
        logger.info("Initializing Sidebar")
        self._initialization_time = time.time()
        
        # Initialize styling components
        self.css_styles = CSSStyles()
        self.themes = Themes()
        
        # Initialize navigation sections
        self.navigation_sections = {}
        
        try:
            # Setup navigation sections
            logger.debug("Setting up navigation sections")
            self._setup_navigation_sections()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"Sidebar initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.navigation_sections)} navigation sections")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"Sidebar initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Sidebar navigation may not function correctly")
            raise
    
    def _setup_navigation_sections(self):
        """Setup navigation sections with expandable groups."""
        try:
            # Define navigation sections with page names that match PageManager
            self.navigation_sections = {
                "✨ APPS": [
                    PageItem("Resume Analysis", icon="📄", description="Upload and analyze your resume", default=True),
                    PageItem("Job Matching", icon="🎯", description="Match your resume with job descriptions"),
                    PageItem("AI Enhancement", icon="✨", description="Get AI-powered improvement suggestions"),
                    PageItem("Career Insights", icon="📈", description="Get career guidance and insights"),
                ],
                "🛠 COMPONENTS": [
                    PageItem("ATS Checker", icon="📊", description="Check ATS compatibility"),
                    PageItem("Resume Builder", icon="🔧", description="Build a new resume with AI assistance"),
                    PageItem("Templates", icon="📋", description="Browse and use resume templates"),
                    PageItem("Customization", icon="🎨", description="Customize appearance and settings"),
                ],
                "🔧 TOOLS": [
                    PageItem("Vector Search", icon="🔍", description="Search through resumes and jobs"),
                    PageItem("Export Resume", icon="💾", description="Export resume in various formats"),
                    PageItem("Import Data", icon="📥", description="Import data from various sources"),
                ],
                "⚙️ SETTINGS": [
                    PageItem("Preferences", icon="⚙️", description="Configure application preferences"),
                    PageItem("API Keys", icon="🔑", description="Manage API keys and credentials"),
                    PageItem("Help & Support", icon="❓", description="Get help and support"),
                ]
            }
            logger.debug(f"Setup {len(self.navigation_sections)} navigation sections")
        except Exception as e:
            logger.error(f"Failed to setup navigation sections: {e}")
            self.navigation_sections = {}
    
    def render(self):
        """
        Render the sidebar with expandable sections and comprehensive logging.
        
        Raises:
            Exception: If sidebar rendering fails
        """
        try:
            logger.debug("Rendering sidebar")
            start_time = time.time()
            
            with st.sidebar:
                # # Render header
                # self._render_header()
                
                # Render breadcrumbs
                self._render_breadcrumbs()
                
                # Render user status indicators
                self._render_user_status()
                
                # Render expandable navigation sections
                self._render_expandable_navigation()
                
                # Render status indicators
                self._render_status_indicators()
                
                # Render user settings
                self._render_user_settings()
                
                # # Render footer
                # self._render_footer()
            
            rendering_time = time.time() - start_time
            logger.debug(f"Sidebar rendered in {rendering_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to render sidebar: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            st.error(f"Sidebar rendering error: {e}")
            raise
    
    # def _render_header(self):
    #     """Render sidebar header."""
    #     try:
    #         st.markdown("""
    #         <div class="sidebar-header">
    #             <h2>🤖 Resume AI</h2>
    #             <p>Your AI-powered resume assistant</p>
    #         </div>
    #         """, unsafe_allow_html=True)
            
    #         st.markdown("---")
    #     except Exception as e:
    #         logger.warning(f"Failed to render sidebar header: {e}")
    
    def _render_breadcrumbs(self):
        """Render navigation breadcrumbs."""
        try:
            # Get current page from session state
            current_page = st.session_state.get('current_page', 'Resume Analysis')
            
            if current_page:
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 0.75rem 1rem;
                    border-radius: 5px;
                    margin-bottom: 1rem;
                    border-left: 4px solid #1f77b4;
                ">
                    <span style="color: #6c757d; font-size: 0.9rem;">
                        📍 Current Page: <strong style="color: #1f77b4;">{current_page}</strong>
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            logger.warning(f"Failed to render breadcrumbs: {e}")
    
    def _render_user_status(self):
        """Render user status indicators."""
        try:
            # Check if app is available in session state
            if hasattr(st.session_state, 'app') and st.session_state.app:
                app = st.session_state.app
                
                # Create status indicators
                col1, col2 = st.columns(2)
                
                with col1:
                    # AI Status
                    if hasattr(app, 'ai_handler') and app.ai_handler:
                        st.success("🤖 AI Ready")
                    else:
                        st.error("🤖 AI Unavailable")
                    # Vector DB Status
                    if hasattr(app, 'vector_db') and app.vector_db:
                        st.success("🗄️ Vector DB Ready")
                    else:
                        st.error("🗄️ Vector DB Unavailable")
                
                with col2:
                    # Document Processor Status
                    if hasattr(app, 'document_processor') and app.document_processor:
                        st.success("📄 Document Ready")
                    else:
                        st.error("📄 Document Unavailable")
                    # Overall Status
                    components_available = sum([
                        hasattr(app, 'ai_handler') and app.ai_handler is not None,
                        hasattr(app, 'vector_db') and app.vector_db is not None,
                        hasattr(app, 'document_processor') and app.document_processor is not None,
                        hasattr(app, 'resume_analyzer') and app.resume_analyzer is not None
                    ])
                    
                    if components_available >= 3:
                        st.success(f"✅ {components_available}/4 Ready")
                    else:
                        st.warning(f"⚠️ {components_available}/4 Ready")
                
        except Exception as e:
            logger.warning(f"Failed to render user status: {e}")
    
    def _render_expandable_navigation(self):
        """Render expandable navigation sections."""
        try:
            # Get current page
            current_page = st.session_state.get('current_page', "📄 Resume Analysis")
            
            # Render each navigation section as an expander
            for section_title, page_items in self.navigation_sections.items():
                with st.expander(section_title, expanded=True):
                    for page_item in page_items:
                        # Check if this is the current page
                        is_current = page_item.title == current_page
                        
                        # Render the page item
                        page_item.render(is_current=is_current)
            
        except Exception as e:
            logger.warning(f"Failed to render expandable navigation: {e}")
    
    
    def _render_status_indicators(self):
        """Render status indicators."""
        try:
            st.markdown("---")
            st.markdown("### 📊 Status")
            
            # AI Service Status
            ai_status = self._get_ai_service_status()
            if ai_status["connected"]:
                st.success(f"🤖 AI Services: {ai_status['status']}")
            else:
                st.error(f"🤖 AI Services: {ai_status['status']}")
            
            # Resume Status
            resume_status = self._get_resume_status()
            if resume_status["loaded"]:
                st.success(f"📄 Resume: {resume_status['status']}")
            else:
                st.info(f"📄 Resume: {resume_status['status']}")
            
            # Job Status
            job_status = self._get_job_status()
            if job_status["loaded"]:
                st.success(f"🎯 Job: {job_status['status']}")
            else:
                st.info(f"🎯 Job: {job_status['status']}")
            
        except Exception as e:
            logger.warning(f"Failed to render status indicators: {e}")
    
    def _render_user_settings(self):
        """Render user settings section."""
        try:
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            
            # Theme selector
            current_theme = st.session_state.get('theme', 'light')
            theme_options = ['light', 'dark', 'professional', 'creative']
            selected_theme = st.selectbox(
                "Theme",
                theme_options,
                index=theme_options.index(current_theme),
                key="theme_selector"
            )
            
            if selected_theme != current_theme:
                st.session_state.theme = selected_theme
                # Apply theme using the app's theme system
                app_layout = st.session_state.get('app_layout')
                if app_layout:
                    app_layout.apply_theme(selected_theme)
                st.rerun()
            
            # Language selector
            current_language = st.session_state.get('user_preferences', {}).get('language', 'en')
            language_options = ['en', 'es', 'fr', 'de', 'zh']
            language_labels = ['English', 'Spanish', 'French', 'German', 'Chinese']
            selected_language = st.selectbox(
                "Language",
                language_labels,
                index=language_options.index(current_language),
                key="language_selector"
            )
            
            if selected_language != language_labels[language_options.index(current_language)]:
                new_language = language_options[language_labels.index(selected_language)]
                st.session_state.user_preferences = st.session_state.get('user_preferences', {})
                st.session_state.user_preferences['language'] = new_language
            
            # Auto-save toggle
            auto_save = st.session_state.get('user_preferences', {}).get('auto_save', True)
            new_auto_save = st.checkbox("Auto-save", value=auto_save, key="auto_save_toggle")
            
            if new_auto_save != auto_save:
                st.session_state.user_preferences = st.session_state.get('user_preferences', {})
                st.session_state.user_preferences['auto_save'] = new_auto_save
            
            # Notifications toggle
            notifications = st.session_state.get('user_preferences', {}).get('notifications', True)
            new_notifications = st.checkbox("Notifications", value=notifications, key="notifications_toggle")
            
            if new_notifications != notifications:
                st.session_state.user_preferences = st.session_state.get('user_preferences', {})
                st.session_state.user_preferences['notifications'] = new_notifications
            
        except Exception as e:
            logger.warning(f"Failed to render user settings: {e}")
    
    # def _render_footer(self):
    #     """Render sidebar footer."""
    #     try:
    #         st.markdown("---")
    #         st.markdown("""
    #         <div class="sidebar-footer">
    #             <p><small>Resume AI v1.0.0</small></p>
    #             <p><small>Powered by AI</small></p>
    #         </div>
    #         """, unsafe_allow_html=True)
    #     except Exception as e:
    #         logger.warning(f"Failed to render sidebar footer: {e}")
    
    def _handle_save_action(self):
        """Handle save action."""
        try:
            logger.debug("Handling save action")
            
            # Check if there's data to save
            if st.session_state.get('resume_data'):
                # Implement save logic here
                st.success("💾 Data saved successfully!")
            else:
                st.warning("⚠️ No data to save")
                
        except Exception as e:
            logger.error(f"Failed to handle save action: {e}")
            st.error(f"Save error: {e}")
    
    def _show_theme_selector(self):
        """Show theme selector modal."""
        try:
            with st.expander("🎨 Theme Selector", expanded=True):
                current_theme = st.session_state.get('theme', 'light')
                theme_options = ['light', 'dark', 'professional', 'creative']
                
                selected_theme = st.radio(
                    "Choose a theme:",
                    theme_options,
                    index=theme_options.index(current_theme),
                    key="theme_radio"
                )
                
                if st.button("Apply Theme", key="apply_theme"):
                    st.session_state.theme = selected_theme
                    self.themes.apply_theme(selected_theme)
                    st.rerun()
                    
        except Exception as e:
            logger.warning(f"Failed to show theme selector: {e}")
    
    def _get_ai_service_status(self) -> Dict[str, Any]:
        """Get AI service status."""
        try:
            # Check if AI handler is available in session state
            if hasattr(st.session_state, 'app') and st.session_state.app:
                app = st.session_state.app
                if hasattr(app, 'ai_handler') and app.ai_handler:
                    if hasattr(app.ai_handler, 'is_connected') and app.ai_handler.is_connected():
                        return {
                            "connected": True,
                            "status": "Connected",
                            "models": getattr(app.ai_handler, 'get_available_models', lambda: [])()
                        }
                    else:
                        return {
                            "connected": False,
                            "status": "Limited Functionality",
                            "models": []
                        }
            
            # Fallback status
            return {
                "connected": False,
                "status": "Not Available",
                "models": []
            }
        except Exception as e:
            logger.warning(f"Failed to get AI service status: {e}")
            return {
                "connected": False,
                "status": "Error",
                "models": []
            }
    
    def _get_resume_status(self) -> Dict[str, Any]:
        """Get resume status."""
        try:
            resume_data = st.session_state.get('resume_data')
            if resume_data:
                return {
                    "loaded": True,
                    "status": "Loaded",
                    "filename": resume_data.get('filename', 'Unknown')
                }
            else:
                return {
                    "loaded": False,
                    "status": "No resume loaded",
                    "filename": None
                }
        except Exception as e:
            logger.warning(f"Failed to get resume status: {e}")
            return {
                "loaded": False,
                "status": "Error",
                "filename": None
            }
    
    def _get_job_status(self) -> Dict[str, Any]:
        """Get job description status."""
        try:
            job_data = st.session_state.get('job_data')
            if job_data:
                return {
                    "loaded": True,
                    "status": "Loaded",
                    "title": job_data.get('title', 'Unknown')
                }
            else:
                return {
                    "loaded": False,
                    "status": "No job loaded",
                    "title": None
                }
        except Exception as e:
            logger.warning(f"Failed to get job status: {e}")
            return {
                "loaded": False,
                "status": "Error",
                "title": None
            }
    
    def get_navigation_sections(self) -> Dict[str, List[PageItem]]:
        """
        Get dictionary of navigation sections.
        
        Returns:
            Dict[str, List[PageItem]]: Dictionary of navigation sections
        """
        return self.navigation_sections
    
    def get_navigation_items(self) -> List[PageItem]:
        """
        Get list of all navigation items across all sections.
        
        Returns:
            List[PageItem]: List of all navigation items
        """
        all_items = []
        for section_items in self.navigation_sections.values():
            all_items.extend(section_items)
        return all_items
    
    def get_current_page(self) -> str:
        """
        Get current page name.
        
        Returns:
            str: Current page name
        """
        return st.session_state.get('current_page', "📄 Resume Analysis")
    
    def set_current_page(self, page_name: str):
        """
        Set current page name.
        
        Args:
            page_name (str): Page name to set as current
        """
        try:
            st.session_state.current_page = page_name
            logger.info(f"Current page set to: {page_name}")
        except Exception as e:
            logger.error(f"Failed to set current page: {e}")
    
    def get_sidebar_info(self) -> Dict[str, Any]:
        """
        Get sidebar information and statistics.
        
        Returns:
            Dict[str, Any]: Sidebar information
        """
        try:
            all_items = self.get_navigation_items()
            return {
                "navigation_sections_count": len(self.navigation_sections),
                "navigation_items_count": len(all_items),
                "current_page": self.get_current_page(),
                "ai_status": self._get_ai_service_status(),
                "resume_status": self._get_resume_status(),
                "job_status": self._get_job_status(),
                "user_preferences": st.session_state.get('user_preferences', {}),
                "initialization_time": self._initialization_time,
                "sidebar_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get sidebar info: {e}")
            return {
                "error": str(e),
                "sidebar_timestamp": datetime.now().isoformat()
            }
    
    def add_page_item(self, section_title: str, page_item: PageItem):
        """
        Add a page item to a specific section.
        
        Args:
            section_title (str): Title of the section to add the item to
            page_item (PageItem): Page item to add
        """
        try:
            if section_title not in self.navigation_sections:
                self.navigation_sections[section_title] = []
            
            self.navigation_sections[section_title].append(page_item)
            logger.info(f"Added page item '{page_item.title}' to section '{section_title}'")
        except Exception as e:
            logger.error(f"Failed to add page item: {e}")
    
    def remove_page_item(self, section_title: str, page_title: str):
        """
        Remove a page item from a specific section.
        
        Args:
            section_title (str): Title of the section to remove the item from
            page_title (str): Title of the page item to remove
        """
        try:
            if section_title in self.navigation_sections:
                self.navigation_sections[section_title] = [
                    item for item in self.navigation_sections[section_title] 
                    if item.title != page_title
                ]
                logger.info(f"Removed page item '{page_title}' from section '{section_title}'")
        except Exception as e:
            logger.error(f"Failed to remove page item: {e}")

# Create a page object similar to the reference design
class Page:
    """
    Page object for managing page items in a section.
    Similar to the reference design's page.item() functionality.
    """
    
    def __init__(self, sidebar: Sidebar, section_title: str):
        """
        Initialize a page object for a specific section.
        
        Args:
            sidebar (Sidebar): The sidebar instance
            section_title (str): The section title this page belongs to
        """
        self.sidebar = sidebar
        self.section_title = section_title
    
    def item(self, title: str, page_handler: Callable = None, default: bool = False, 
             icon: str = "", description: str = ""):
        """
        Add a page item to this section.
        Similar to the reference design's page.item() method.
        
        Args:
            title (str): Display title of the page item
            page_handler (Callable): Function to call when item is clicked
            default (bool): Whether this is the default page
            icon (str): Icon to display with the item
            description (str): Description text for the item
        """
        page_item = PageItem(title, page_handler, default, icon, description)
        self.sidebar.add_page_item(self.section_title, page_item)
        return page_item
