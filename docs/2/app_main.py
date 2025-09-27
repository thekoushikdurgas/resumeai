# Main Streamlit Application Entry Point
# app/main.py - Resume/CV AI Application

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import core modules
from app.core.ai_handler import AIHandler
from app.core.document_processor import DocumentProcessor
from app.core.resume_analyzer import ResumeAnalyzer
from app.core.job_matcher import JobMatcher
from app.core.ats_checker import ATSChecker
from app.core.resume_builder import ResumeBuilder

# Import UI components
from app.ui.sidebar import render_sidebar
from app.ui.tabs.analysis_tab import AnalysisTab
from app.ui.tabs.job_matching_tab import JobMatchingTab
from app.ui.tabs.enhancement_tab import EnhancementTab
from app.ui.tabs.ats_checker_tab import ATSCheckerTab
from app.ui.tabs.builder_tab import BuilderTab
from app.ui.tabs.templates_tab import TemplatesTab
from app.ui.tabs.insights_tab import InsightsTab
from app.ui.tabs.customization_tab import CustomizationTab
from app.ui.styles.css import apply_custom_styles

# Import configuration
from config.settings import AppConfig, UIConfig
from config.ai_config import AIConfig

# Import utilities
from app.utils.logger import setup_logger
from app.utils.cache_manager import CacheManager
from app.utils.helpers import initialize_session_state

# Initialize logging
logger = setup_logger(__name__)

class ResumeAIApp:
    """Main Resume AI Application Class"""
    
    def __init__(self):
        """Initialize the Resume AI application"""
        self.config = AppConfig()
        self.ui_config = UIConfig()
        self.ai_config = AIConfig()
        
        # Initialize core components
        self.ai_handler = AIHandler(self.ai_config)
        self.document_processor = DocumentProcessor()
        self.resume_analyzer = ResumeAnalyzer(self.ai_handler)
        self.job_matcher = JobMatcher(self.ai_handler)
        self.ats_checker = ATSChecker()
        self.resume_builder = ResumeBuilder(self.ai_handler)
        
        # Initialize cache manager
        self.cache_manager = CacheManager()
        
        # Initialize UI components
        self.tabs = {
            'analysis': AnalysisTab(self.resume_analyzer, self.document_processor),
            'job_matching': JobMatchingTab(self.job_matcher),
            'enhancement': EnhancementTab(self.ai_handler),
            'ats_checker': ATSCheckerTab(self.ats_checker),
            'builder': BuilderTab(self.resume_builder),
            'templates': TemplatesTab(),
            'insights': InsightsTab(),
            'customization': CustomizationTab()
        }
    
    def configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=self.config.APP_TITLE,
            page_icon=self.config.PAGE_ICON,
            layout=self.config.LAYOUT,
            initial_sidebar_state=self.config.SIDEBAR_STATE,
            menu_items={
                'Get Help': 'https://github.com/your-repo/resumeai/issues',
                'Report a bug': 'https://github.com/your-repo/resumeai/issues/new',
                'About': f"Resume AI v{self.config.VERSION} - AI-powered resume optimization"
            }
        )
    
    def apply_styling(self):
        """Apply custom CSS styling"""
        apply_custom_styles(self.ui_config.theme)
    
    def render_header(self):
        """Render application header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="main-header">
                <h1>{self.ui_config.HEADER_ICON} {self.config.APP_TITLE}</h1>
                <p class="subtitle">{self.config.APP_SUBTITLE}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display version and status
        with st.sidebar:
            st.caption(f"Version {self.config.VERSION}")
            if self.ai_handler.is_connected():
                st.success("🤖 AI Services Connected")
            else:
                st.warning("⚠️ AI Services Limited")
    
    def render_main_content(self):
        """Render main application content with tabs"""
        
        # Create tab labels with icons
        tab_labels = [
            f"{self.ui_config.TAB_ICONS['analysis']} Resume Analysis",
            f"{self.ui_config.TAB_ICONS['job_matching']} Job Matching",
            f"{self.ui_config.TAB_ICONS['enhancement']} AI Enhancement",
            f"{self.ui_config.TAB_ICONS['ats_checker']} ATS Checker",
            f"{self.ui_config.TAB_ICONS['builder']} Resume Builder",
            f"{self.ui_config.TAB_ICONS['templates']} Templates",
            f"{self.ui_config.TAB_ICONS['insights']} Career Insights",
            f"{self.ui_config.TAB_ICONS['customization']} Customization"
        ]
        
        # Create tabs
        tabs = st.tabs(tab_labels)
        
        # Render each tab
        with tabs[0]:
            self.tabs['analysis'].render()
        
        with tabs[1]:
            self.tabs['job_matching'].render()
        
        with tabs[2]:
            self.tabs['enhancement'].render()
        
        with tabs[3]:
            self.tabs['ats_checker'].render()
        
        with tabs[4]:
            self.tabs['builder'].render()
        
        with tabs[5]:
            self.tabs['templates'].render()
        
        with tabs[6]:
            self.tabs['insights'].render()
        
        with tabs[7]:
            self.tabs['customization'].render()
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📊 Statistics**")
            if 'analysis_history' in st.session_state:
                st.write(f"Resumes analyzed: {len(st.session_state.analysis_history)}")
            else:
                st.write("Resumes analyzed: 0")
        
        with col2:
            st.markdown("**🔗 Resources**")
            st.markdown("[Documentation](https://docs.example.com) | [Support](https://support.example.com)")
        
        with col3:
            st.markdown("**ℹ️ About**")
            st.markdown(f"Resume AI © 2025 | Made with ❤️ using Streamlit")
    
    def handle_errors(self, error: Exception):
        """Handle application errors"""
        logger.error(f"Application error: {str(error)}", exc_info=True)
        
        st.error("🚨 An error occurred")
        
        with st.expander("Error Details"):
            st.code(str(error))
            st.write("Please try refreshing the page or contact support if the issue persists.")
    
    def run(self):
        """Run the main application"""
        try:
            # Initialize session state
            initialize_session_state()
            
            # Configure page
            self.configure_page()
            
            # Apply styling
            self.apply_styling()
            
            # Render sidebar
            render_sidebar(self.config, self.cache_manager)
            
            # Render main content
            self.render_header()
            self.render_main_content()
            self.render_footer()
            
            logger.info("Application rendered successfully")
            
        except Exception as e:
            self.handle_errors(e)

# Application entry point
def main():
    """Main function to run the application"""
    app = ResumeAIApp()
    app.run()

if __name__ == "__main__":
    main()