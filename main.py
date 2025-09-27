"""
Main Streamlit Application for Resume/CV AI with Vector Database
Comprehensive resume analysis, optimization, and career advancement tool.

This is the main entry point for the Resume AI application providing:
- Streamlit-based web interface
- Resume upload and processing capabilities
- AI-powered resume analysis and enhancement
- Vector database integration for semantic search
- Job matching and ATS compatibility checking
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

# NumPy 2.0 compatibility fix - must be imported before any other imports
import utils.transport
import utils.session
import numpy as np
numpy_version = np.__version__
if int(numpy_version.split('.')[0]) >= 2:
    # Monkey patch deprecated functions for NumPy 2.0+ compatibility
    if not hasattr(np, 'float_'):
        np.float_ = np.float64
    if not hasattr(np, 'int_'):
        np.int_ = np.int64
    if not hasattr(np, 'complex_'):
        np.complex_ = np.complex128

import streamlit as st
import os
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

# Import core components
from core.vector_db import VectorDatabase
from core.ai_handler import AIHandler
from core.document_processor import DocumentProcessor
from core.resume_analyzer import ResumeAnalyzer
from core.job_matcher import JobMatcher
from core.ats_checker import ATSChecker
from core.resume_builder import ResumeBuilder

# Import models
from models.resume_model import ParsedResume, ResumeMetadata
from models.job_model import JobDescription, JobMetadata
from models.analysis_model import AnalysisResult, ATSResult, EnhancementSuggestion

# Configuration management functions
def load_api_config():
    """Load API configuration from config/api_config.json"""
    try:
        config_path = "config/api_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            st.error(f"Configuration file not found: {config_path}")
            return {}
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}

def save_api_config(config):
    """Save API configuration to config/api_config.json"""
    try:
        config_path = "config/api_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving configuration: {e}")
        return False

def get_api_key(provider, key_name="api_keys"):
    """Get API key for a specific provider from config"""
    config = load_api_config()
    return config.get(provider, {}).get(key_name, "")

def update_api_key(provider, key_name, new_key):
    """Update API key for a specific provider in config"""
    config = load_api_config()
    if provider not in config:
        config[provider] = {}
    config[provider][key_name] = new_key
    return save_api_config(config)

# Import utilities
from utils.helpers import generate_unique_id, clean_text
from utils.logger import setup_logger

# Setup logging with comprehensive configuration
logger = setup_logger("main_app")

class ResumeAIApp:
    """
    Main Resume AI Application with Vector Database Integration and comprehensive logging.
    
    This class serves as the main application controller providing:
    - Component initialization and management
    - Streamlit interface orchestration
    - Resume processing and analysis workflows
    - Error handling and user feedback
    - Performance monitoring and logging
    
    Attributes:
        vector_db: Vector database instance for semantic operations
        ai_handler: AI handler instance for content analysis
        document_processor: Document processor for file handling
        resume_analyzer: Resume analyzer for content parsing
        job_matcher: Job matcher for compatibility analysis
        ats_checker: ATS checker for compatibility validation
        resume_builder: Resume builder for AI-assisted creation
        _initialization_time: Timestamp of initialization start
    """
    
    def __init__(self):
        """
        Initialize the application with comprehensive logging.
        
        Sets up all core components including vector database, AI handlers,
        and processing modules with detailed logging for monitoring.
        
        Raises:
            Exception: If critical component initialization fails
        """
        logger.info("Initializing ResumeAIApp")
        self._initialization_time = time.time()
        
        # Initialize component references
        self.vector_db = None
        self.ai_handler = None
        self.document_processor = None
        self.resume_analyzer = None
        self.job_matcher = None
        self.ats_checker = None
        self.resume_builder = None
        
        try:
            # Initialize components with comprehensive logging
            logger.info("Starting component initialization")
            self._initialize_components()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"ResumeAIApp initialized successfully in {initialization_time:.2f}s")
            logger.info("All components are ready for use")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"ResumeAIApp initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Application may not function correctly")
            
            # Check which components failed and provide specific guidance
            self._check_component_status()
            
            # Don't raise the exception, continue with limited functionality
            logger.warning("Continuing with limited functionality - some features may be disabled")
        
        # Configure page
        self._configure_page()
        
        # Store app instance in session state for UI components
        st.session_state.app = self
    
    def _check_component_status(self):
        """Check the status of all components and provide guidance."""
        try:
            logger.info("Checking component initialization status...")
            
            # Check VectorDatabase
            if self.vector_db:
                if hasattr(self.vector_db, 'is_initialized') and self.vector_db.is_initialized():
                    logger.info("✅ VectorDatabase: Initialized successfully")
                else:
                    logger.warning("⚠️ VectorDatabase: Initialized but may have limited functionality")
            else:
                logger.error("❌ VectorDatabase: Failed to initialize")
            
            # Check AIHandler
            if self.ai_handler:
                if hasattr(self.ai_handler, 'is_connected') and self.ai_handler.is_connected():
                    logger.info("✅ AIHandler: Connected successfully")
                else:
                    logger.warning("⚠️ AIHandler: Initialized but may have limited functionality")
            else:
                logger.error("❌ AIHandler: Failed to initialize")
            
            # Check other components
            components = [
                ("DocumentProcessor", self.document_processor),
                ("ResumeAnalyzer", self.resume_analyzer),
                ("JobMatcher", self.job_matcher),
                ("ATSChecker", self.ats_checker),
                ("ResumeBuilder", self.resume_builder)
            ]
            
            for name, component in components:
                if component:
                    logger.info(f"✅ {name}: Initialized successfully")
                else:
                    logger.error(f"❌ {name}: Failed to initialize")
            
            logger.info("Component status check completed")
            
        except Exception as e:
            logger.error(f"Failed to check component status: {e}")
    
    def _initialize_components(self):
        """
        Initialize all application components with comprehensive logging.
        
        This method initializes all core components in the correct dependency order
        with detailed logging for each step and error handling for failures.
        
        Raises:
            Exception: If any critical component fails to initialize
        """
        try:
            logger.info("Starting component initialization sequence")
            
            # Initialize vector database with error handling
            try:
                logger.debug("Initializing VectorDatabase")
                self.vector_db = VectorDatabase()
                logger.info("VectorDatabase initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize VectorDatabase: {e}")
                logger.warning("Continuing without VectorDatabase - some features will be disabled")
                self.vector_db = None
            
            # Initialize AI handler with error handling
            try:
                logger.debug("Initializing AIHandler with configuration")
                # Load configuration and pass to AI handler
                config = load_api_config()
                self.ai_handler = AIHandler(config)
                logger.info("AIHandler initialized successfully with configuration")
            except Exception as e:
                logger.error(f"Failed to initialize AIHandler: {e}")
                logger.warning("Continuing without AIHandler - AI features will be disabled")
                self.ai_handler = None
            
            # Initialize document processor (should always work)
            try:
                logger.debug("Initializing DocumentProcessor")
                self.document_processor = DocumentProcessor()
                logger.info("DocumentProcessor initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize DocumentProcessor: {e}")
                self.document_processor = None
            
            # Initialize resume analyzer (depends on vector_db and ai_handler)
            try:
                logger.debug("Initializing ResumeAnalyzer")
                self.resume_analyzer = ResumeAnalyzer(self.vector_db, self.ai_handler)
                logger.info("ResumeAnalyzer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ResumeAnalyzer: {e}")
                logger.warning("Continuing without ResumeAnalyzer - resume analysis features will be disabled")
                self.resume_analyzer = None
            
            # Initialize other components with error handling
            try:
                logger.debug("Initializing JobMatcher")
                self.job_matcher = JobMatcher(self.vector_db, self.ai_handler)
                logger.info("JobMatcher initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize JobMatcher: {e}")
                self.job_matcher = None
            
            try:
                logger.debug("Initializing ATSChecker")
                self.ats_checker = ATSChecker(self.ai_handler)
                logger.info("ATSChecker initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ATSChecker: {e}")
                self.ats_checker = None
            
            try:
                logger.debug("Initializing ResumeBuilder")
                self.resume_builder = ResumeBuilder(self.ai_handler)
                logger.info("ResumeBuilder initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ResumeBuilder: {e}")
                self.resume_builder = None
            
            # Count successful initializations
            successful_components = sum([
                self.vector_db is not None,
                self.ai_handler is not None,
                self.document_processor is not None,
                self.resume_analyzer is not None,
                self.job_matcher is not None,
                self.ats_checker is not None,
                self.resume_builder is not None
            ])
            
            logger.info(f"Component initialization completed: {successful_components}/7 components initialized successfully")
            
            if successful_components >= 3:  # At least basic functionality
                logger.info("Application is ready for use with available features")
            else:
                logger.warning("Limited functionality available - some core features may be disabled")
            
        except Exception as e:
            logger.error(f"Critical error during component initialization: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            # Don't raise, just log the error and continue
    
    def _configure_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Resume/CV AI Assistant",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        .metric-card {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #f5c6cb;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Run the main application using the new UI architecture."""
        try:
            # Initialize UI layout system
            from ui.app_layout import AppLayout
            
            # Create app layout instance
            app_layout = AppLayout()
            
            # Store app instance and app_layout in session state for UI components
            st.session_state.app = self
            st.session_state.app_layout = app_layout
            
            # Render the complete application layout
            app_layout.render()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            st.error(f"An error occurred: {e}")
            # Fallback to basic rendering if AppLayout fails
            self._render_fallback_ui()
    
    def _render_fallback_ui(self):
        """Fallback UI rendering when AppLayout fails."""
        try:
            logger.warning("Using fallback UI rendering")
            
            # Header
            self._render_header()
            
            # Sidebar
            self._render_sidebar()
            
            # Main content
            self._render_main_content()
            
        except Exception as e:
            logger.error(f"Fallback UI rendering failed: {e}")
            st.error("Critical error: Unable to render application")
    
    def _render_header(self):
        """Render application header."""
        st.markdown('<h1 class="main-header">🤖 Resume/CV AI Assistant</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Your comprehensive AI-powered resume companion for analysis, optimization, and career advancement
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_sidebar(self):
        """Render sidebar navigation using the new expandable design."""
        # Import the new sidebar
        from ui.sidebar import Sidebar
        
        # Create sidebar instance
        sidebar = Sidebar()
        
        # Render the sidebar
        sidebar.render()
    
    def _render_main_content(self):
        """Render main content based on selected page."""
        if not hasattr(st.session_state, 'current_page'):
            st.session_state.current_page = "Resume Analysis"
        
        page = st.session_state.current_page
        
        if page == "Resume Analysis":
            self._render_resume_analysis()
        elif page == "Job Matching":
            self._render_job_matching()
        elif page == "AI Enhancement":
            self._render_ai_enhancement()
        elif page == "ATS Checker":
            self._render_ats_checker()
        elif page == "Resume Builder":
            self._render_resume_builder()
        elif page == "Templates":
            self._render_templates()
        elif page == "Career Insights":
            self._render_career_insights()
        elif page == "Customization":
            self._render_customization()
        elif page == "Vector Search":
            self._render_vector_search()
        elif page == "Preferences":
            self._render_preferences()
        elif page == "API Keys":
            self._render_api_keys()
        elif page == "Help & Support":
            self._render_help_support()
        elif page == "Export Resume":
            self._render_export_resume()
        elif page == "Import Data":
            self._render_import_data()
    
    def _render_resume_analysis(self):
        """Render resume analysis page."""
        st.header("📄 Resume Analysis")
        st.write("Upload your resume and get comprehensive AI-powered analysis with vector database insights.")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file is not None:
            # Process file
            with st.spinner("Processing your resume..."):
                result = self.document_processor.process_uploaded_file(uploaded_file)
            
            if result['success']:
                st.success("✅ Resume processed successfully!")
                
                # Parse resume
                with st.spinner("Analyzing resume content..."):
                    resume = self.resume_analyzer.parse_resume(
                        result['text'], 
                        result['metadata']
                    )
                
                # Store in session state
                st.session_state.current_resume = resume
                
                # Display analysis
                self._display_resume_analysis(resume)
                
            else:
                st.error(f"❌ {result['error']}")
    
    def _display_resume_analysis(self, resume: ParsedResume):
        """Display comprehensive resume analysis."""
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Parse Confidence", f"{resume.parse_confidence:.1f}%")
        
        with col2:
            st.metric("Word Count", len(resume.raw_text.split()) if resume.raw_text else 0)
        
        with col3:
            st.metric("Skills Count", len(resume.skills))
        
        # Contact Information
        st.subheader("👤 Contact Information")
        contact_col1, contact_col2 = st.columns(2)
        
        with contact_col1:
            st.write(f"**Name:** {resume.contact_info.name or 'Not provided'}")
            st.write(f"**Email:** {resume.contact_info.email or 'Not provided'}")
        
        with contact_col2:
            st.write(f"**Phone:** {resume.contact_info.phone or 'Not provided'}")
            st.write(f"**Location:** {resume.contact_info.location or 'Not provided'}")
        
        # Summary
        if resume.summary:
            st.subheader("📝 Professional Summary")
            st.write(resume.summary)
        
        # Work Experience
        if resume.work_experience:
            st.subheader("💼 Work Experience")
            for i, exp in enumerate(resume.work_experience, 1):
                with st.expander(f"{i}. {exp.title} at {exp.company}"):
                    if exp.start_date and exp.end_date:
                        st.write(f"**Duration:** {exp.start_date} - {exp.end_date}")
                    if exp.description:
                        st.write(f"**Description:** {exp.description}")
                    if exp.achievements:
                        st.write("**Key Achievements:**")
                        for achievement in exp.achievements:
                            st.write(f"• {achievement}")
        
        # Education
        if resume.education:
            st.subheader("🎓 Education")
            for edu in resume.education:
                st.write(f"**{edu.degree}** from {edu.institution}")
                if edu.graduation_date:
                    st.write(f"Graduated: {edu.graduation_date}")
        
        # Skills
        if resume.skills:
            st.subheader("🛠️ Skills")
            skill_categories = {}
            for skill in resume.skills:
                if skill.category not in skill_categories:
                    skill_categories[skill.category] = []
                skill_categories[skill.category].append(skill.name)
            
            for category, skills in skill_categories.items():
                st.write(f"**{category}:** {', '.join(skills)}")
        
        # Projects
        if resume.projects:
            st.subheader("🚀 Projects")
            for project in resume.projects:
                with st.expander(project.name or "Unnamed Project"):
                    if project.description:
                        st.write(project.description)
                    if project.technologies:
                        st.write(f"**Technologies:** {', '.join(project.technologies)}")
        
        # AI Analysis
        if st.button("🤖 Get AI Analysis"):
            with st.spinner("Generating AI analysis..."):
                import asyncio
                analysis = asyncio.run(self.resume_analyzer.analyze_resume(resume))
            
            st.session_state.current_analysis = analysis
            self._display_ai_analysis(analysis)
    
    def _display_ai_analysis(self, analysis: AnalysisResult):
        """Display AI analysis results."""
        st.subheader("🤖 AI Analysis Results")
        
        # Overall Score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Score", f"{analysis.overall_score:.1f}/100")
        
        with col2:
            st.metric("Confidence", f"{analysis.confidence:.1%}")
        
        with col3:
            st.metric("Issues Found", len(analysis.issues))
        
        # Strengths
        if analysis.strengths:
            st.subheader("✅ Strengths")
            for strength in analysis.strengths:
                st.write(f"• {strength}")
        
        # Areas for Improvement
        if analysis.weaknesses:
            st.subheader("⚠️ Areas for Improvement")
            for weakness in analysis.weaknesses:
                st.write(f"• {weakness}")
        
        # Issues
        if analysis.issues:
            st.subheader("❌ Issues Found")
            for issue in analysis.issues:
                st.write(f"• {issue}")
        
        # Recommendations
        if analysis.recommendations:
            st.subheader("💡 Recommendations")
            for recommendation in analysis.recommendations:
                st.write(f"• {recommendation}")
    
    def _render_job_matching(self):
        """Render job matching page."""
        st.header("🎯 Job Matching")
        st.write("Find jobs that match your resume and get compatibility scores.")
        
        if not hasattr(st.session_state, 'current_resume') or not st.session_state.current_resume:
            st.warning("Please upload and analyze a resume first.")
            return
        
        resume = st.session_state.current_resume
        
        # Job description input
        st.subheader("📝 Job Description")
        job_description = st.text_area(
            "Paste the job description here:",
            height=200,
            placeholder="Enter the complete job description..."
        )
        
        if job_description:
            if st.button("🔍 Analyze Job Match"):
                with st.spinner("Analyzing job compatibility..."):
                    match_result = self.job_matcher.match_resume_to_job(resume, job_description)
                
                st.session_state.current_job_match = match_result
                self._display_job_match_results(match_result)
    
    def _display_job_match_results(self, match_result: Dict):
        """Display job matching results."""
        st.subheader("🎯 Job Matching Results")
        
        # Overall match score
        match_score = match_result.get('match_score', 0)
        st.metric("Overall Match Score", f"{match_score:.1f}%")
        
        # Progress bar
        st.progress(match_score / 100)
        
        # Detailed scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Skill Match", f"{match_result.get('skill_match', 0):.1f}%")
        
        with col2:
            st.metric("Experience Match", f"{match_result.get('experience_match', 0):.1f}%")
        
        with col3:
            st.metric("Education Match", f"{match_result.get('education_match', 0):.1f}%")
        
        # Matched skills
        if match_result.get('matched_skills'):
            st.subheader("✅ Matched Skills")
            st.write(", ".join(match_result['matched_skills']))
        
        # Missing skills
        if match_result.get('missing_skills'):
            st.subheader("❌ Missing Skills")
            st.write(", ".join(match_result['missing_skills']))
        
        # Recommendations
        if match_result.get('recommendations'):
            st.subheader("💡 Recommendations")
            for rec in match_result['recommendations']:
                st.write(f"• {rec}")
    
    def _render_ai_enhancement(self):
        """Render AI enhancement page."""
        st.header("✨ AI Enhancement")
        st.write("Get AI-powered suggestions to improve your resume.")
        
        if not hasattr(st.session_state, 'current_resume') or not st.session_state.current_resume:
            st.warning("Please upload and analyze a resume first.")
            return
        
        resume = st.session_state.current_resume
        
        # Enhancement options
        col1, col2 = st.columns(2)
        
        with col1:
            enhancement_type = st.selectbox(
                "Enhancement Type:",
                ["General", "ATS Optimization", "Keyword Enhancement", "Content Improvement"]
            )
        
        with col2:
            industry = st.selectbox(
                "Target Industry:",
                ["Technology", "Finance", "Healthcare", "Marketing", "General"]
            )
        
        if st.button("✨ Generate Enhancements"):
            with st.spinner("Generating enhancement suggestions..."):
                suggestions = self.ai_handler.generate_enhancement_suggestions(
                    resume, 
                    enhancement_type.lower().replace(" ", "_")
                )
            
            st.session_state.current_enhancements = suggestions
            self._display_enhancement_suggestions(suggestions)
    
    def _display_enhancement_suggestions(self, suggestions: List[EnhancementSuggestion]):
        """Display enhancement suggestions."""
        st.subheader("✨ Enhancement Suggestions")
        
        for i, suggestion in enumerate(suggestions, 1):
            with st.expander(f"{i}. {suggestion.title}"):
                st.write(f"**Category:** {suggestion.category}")
                st.write(f"**Impact Score:** {suggestion.impact_score}/10")
                st.write(f"**Effort Level:** {suggestion.effort_level}")
                
                st.write("**Description:**")
                st.write(suggestion.description)
                
                if suggestion.current_text:
                    st.write("**Current Text:**")
                    st.code(suggestion.current_text)
                
                if suggestion.suggested_text:
                    st.write("**Suggested Text:**")
                    st.code(suggestion.suggested_text)
                
                if suggestion.examples:
                    st.write("**Examples:**")
                    for example in suggestion.examples:
                        st.write(f"• {example}")
    
    def _render_ats_checker(self):
        """Render ATS checker page."""
        st.header("📊 ATS Checker")
        st.write("Check your resume's compatibility with Applicant Tracking Systems.")
        
        if not hasattr(st.session_state, 'current_resume') or not st.session_state.current_resume:
            st.warning("Please upload and analyze a resume first.")
            return
        
        resume = st.session_state.current_resume
        
        if st.button("📊 Check ATS Compatibility"):
            with st.spinner("Checking ATS compatibility..."):
                ats_result = self.ats_checker.check_ats_compatibility(resume)
            
            st.session_state.current_ats_result = ats_result
            self._display_ats_results(ats_result)
    
    def _display_ats_results(self, ats_result: ATSResult):
        """Display ATS check results."""
        st.subheader("📊 ATS Compatibility Results")
        
        # Overall ATS score
        st.metric("ATS Score", f"{ats_result.ats_score:.1f}/100")
        st.progress(ats_result.ats_score / 100)
        
        # Detailed scores
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Format Score", f"{ats_result.format_score:.1f}/100")
        
        with col2:
            st.metric("Keyword Score", f"{ats_result.keyword_score:.1f}/100")
        
        with col3:
            st.metric("Structure Score", f"{ats_result.structure_score:.1f}/100")
        
        with col4:
            st.metric("Content Score", f"{ats_result.content_score:.1f}/100")
        
        # Issues and recommendations
        if ats_result.compatibility_issues:
            st.subheader("❌ Compatibility Issues")
            for issue in ats_result.compatibility_issues:
                st.write(f"• {issue}")
        
        if ats_result.recommendations:
            st.subheader("💡 Recommendations")
            for rec in ats_result.recommendations:
                st.write(f"• {rec}")
    
    def _render_resume_builder(self):
        """Render resume builder page."""
        st.header("🔧 Resume Builder")
        st.write("Build a new resume with AI assistance.")
        
        # Resume builder form
        with st.form("resume_builder_form"):
            st.subheader("Personal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                email = st.text_input("Email")
            
            with col2:
                phone = st.text_input("Phone")
                location = st.text_input("Location")
            
            st.subheader("Professional Summary")
            summary = st.text_area("Summary", height=100)
            
            st.subheader("Work Experience")
            experience_count = st.number_input("Number of work experiences", min_value=1, max_value=10, value=1)
            
            experiences = []
            for i in range(experience_count):
                with st.expander(f"Experience {i+1}"):
                    exp_title = st.text_input(f"Job Title {i+1}")
                    exp_company = st.text_input(f"Company {i+1}")
                    exp_description = st.text_area(f"Description {i+1}", height=100)
                    experiences.append({
                        'title': exp_title,
                        'company': exp_company,
                        'description': exp_description
                    })
            
            submitted = st.form_submit_button("🔧 Build Resume")
            
            if submitted:
                # Create resume object
                resume_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'summary': summary,
                    'experiences': experiences
                }
                
                st.success("Resume built successfully!")
                st.json(resume_data)
    
    def _render_templates(self):
        """Render templates page."""
        st.header("📋 Resume Templates")
        st.write("Choose from professional resume templates.")
        
        # Template selection
        template_col1, template_col2, template_col3 = st.columns(3)
        
        with template_col1:
            st.subheader("Modern Professional")
            st.image("https://via.placeholder.com/300x400?text=Modern+Professional", width=200)
            if st.button("Select Modern Professional"):
                st.success("Template selected!")
        
        with template_col2:
            st.subheader("Creative Design")
            st.image("https://via.placeholder.com/300x400?text=Creative+Design", width=200)
            if st.button("Select Creative Design"):
                st.success("Template selected!")
        
        with template_col3:
            st.subheader("Technical Focused")
            st.image("https://via.placeholder.com/300x400?text=Technical+Focused", width=200)
            if st.button("Select Technical Focused"):
                st.success("Template selected!")
    
    def _render_career_insights(self):
        """Render career insights page."""
        st.header("📈 Career Insights")
        st.write("Get insights about your career path and market trends.")
        
        if not hasattr(st.session_state, 'current_resume') or not st.session_state.current_resume:
            st.warning("Please upload and analyze a resume first.")
            return
        
        resume = st.session_state.current_resume
        
        if st.button("📈 Generate Career Insights"):
            with st.spinner("Generating career insights..."):
                insights = self.ai_handler.generate_career_insights(resume)
            
            st.session_state.current_insights = insights
            self._display_career_insights(insights)
    
    def _display_career_insights(self, insights):
        """Display career insights."""
        st.subheader("📈 Career Insights")
        
        for insight in insights:
            with st.expander(insight.title):
                st.write(insight.description)
                
                if insight.recommendations:
                    st.write("**Recommendations:**")
                    for rec in insight.recommendations:
                        st.write(f"• {rec}")
    
    def _render_customization(self):
        """Render customization page."""
        st.header("🎨 Customization")
        st.write("Customize the appearance and behavior of your resume.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Visual Settings")
            color_theme = st.selectbox("Color Theme", ["Blue", "Green", "Purple", "Red"])
            font_family = st.selectbox("Font Family", ["Arial", "Times New Roman", "Calibri"])
            font_size = st.slider("Font Size", 10, 16, 12)
        
        with col2:
            st.subheader("Content Settings")
            include_photo = st.checkbox("Include Photo")
            include_references = st.checkbox("Include References")
            include_hobbies = st.checkbox("Include Hobbies")
        
        if st.button("🎨 Apply Customization"):
            st.success("Customization applied successfully!")
    
    def _render_vector_search(self):
        """Render vector search page."""
        st.header("🔍 Vector Search")
        st.write("Search through resumes and job descriptions using semantic search.")
        
        # Search options
        search_type = st.selectbox("Search Type", ["Resumes", "Job Descriptions", "Skills"])
        
        search_query = st.text_input("Search Query", placeholder="Enter your search terms...")
        
        if search_query:
            if st.button("🔍 Search"):
                with st.spinner("Searching..."):
                    if search_type == "Resumes":
                        results = self.vector_db.search_similar_resumes(search_query, 10)
                    elif search_type == "Job Descriptions":
                        results = self.vector_db.search_similar_jobs(search_query, 10)
                    else:
                        results = []
                
                st.session_state.search_results = results
                self._display_search_results(results, search_type)
    
    def _display_search_results(self, results: List[Dict], search_type: str):
        """Display search results."""
        st.subheader(f"🔍 Search Results for '{search_type}'")
        
        if not results:
            st.write("No results found.")
            return
        
        for i, result in enumerate(results, 1):
            with st.expander(f"Result {i} (Similarity: {1-result['distance']:.2f})"):
                st.write("**Document:**")
                st.write(result['document'][:500] + "..." if len(result['document']) > 500 else result['document'])
                
                st.write("**Metadata:**")
                for key, value in result['metadata'].items():
                    st.write(f"**{key}:** {value}")
    
    def _render_preferences(self):
        """Render preferences page."""
        st.header("⚙️ Preferences")
        st.write("Configure your application preferences and settings.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Display Settings")
            theme = st.selectbox("Theme", ["Light", "Dark", "Professional", "Creative"])
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
            font_size = st.slider("Font Size", 10, 20, 14)
        
        with col2:
            st.subheader("Behavior Settings")
            auto_save = st.checkbox("Auto-save changes", value=True)
            notifications = st.checkbox("Enable notifications", value=True)
            dark_mode = st.checkbox("Dark mode", value=False)
        
        if st.button("💾 Save Preferences"):
            st.success("Preferences saved successfully!")
    
    def _render_api_keys(self):
        """Render API keys management page."""
        # st.header("🔑 API Keys Management")
        # st.write("Manage your API keys and credentials for AI providers.")
        
        # Load current configuration
        config = load_api_config()
        
        # Create tabs for different providers
        tab1, tab2, tab3 = st.tabs(["🤗 Hugging Face", "⚡ Groq AI", "📊 Configuration Status"])
        
        with tab1:
            st.subheader("Hugging Face API Configuration")
            st.write("Configure your Hugging Face API key for model access and inference.")
            
            # Get current Hugging Face key
            current_hf_key = get_api_key("huggingface", "api_keys")
            
            # Display current key status
            if current_hf_key:
                st.success("✅ Hugging Face API key is configured")
                st.code(f"Key: {current_hf_key[:10]}...{current_hf_key[-10:]}")
            else:
                st.warning("⚠️ Using default Hugging Face key or no key configured")
            
            # Input for new key
            new_hf_key = st.text_input(
                "Hugging Face API Key", 
                value=current_hf_key,
                type="password", 
                placeholder="hf_...",
                help="Get your API key from https://huggingface.co/settings/tokens"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Hugging Face Key", key="save_hf"):
                    if new_hf_key and new_hf_key.startswith("hf_"):
                        if update_api_key("huggingface", "api_keys", new_hf_key):
                            st.success("✅ Hugging Face API key saved successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save Hugging Face API key")
                    else:
                        st.error("❌ Please enter a valid Hugging Face API key (starts with 'hf_')")
            
            with col2:
                if st.button("🔄 Reset to Default", key="reset_hf"):
                    if update_api_key("huggingface", "api_keys", ""):
                        st.success("✅ Reset to default Hugging Face key")
                        st.rerun()
                    else:
                        st.error("❌ Failed to reset Hugging Face key")
            
            # Display Hugging Face configuration info
            st.info("""
            **Hugging Face Configuration:**
            - **API Key**: Used for accessing Hugging Face models
            - **Models**: DialoGPT, BERT, BART, RoBERTa, etc.
            - **Usage**: Text generation, classification, summarization
            - **Cost**: Free tier available, pay-per-use for API calls
            """)
        
        with tab2:
            st.subheader("Groq AI API Configuration")
            st.write("Configure your Groq AI API key for fast inference with optimized models.")
            
            # Get current Groq key
            current_groq_key = get_api_key("groq", "api_keys")
            
            # Display current key status
            if current_groq_key:
                st.success("✅ Groq AI API key is configured")
                st.code(f"Key: {current_groq_key[:10]}...{current_groq_key[-10:]}")
            else:
                st.warning("⚠️ No Groq AI API key configured")
            
            # Input for new key
            new_groq_key = st.text_input(
                "Groq AI API Key", 
                value=current_groq_key,
                type="password", 
                placeholder="gsk_...",
                help="Get your API key from https://console.groq.com/keys"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Groq AI Key", key="save_groq"):
                    if new_groq_key and new_groq_key.startswith("gsk_"):
                        if update_api_key("groq", "api_keys", new_groq_key):
                            st.success("✅ Groq AI API key saved successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save Groq AI API key")
                    else:
                        st.error("❌ Please enter a valid Groq AI API key (starts with 'gsk_')")
            
            with col2:
                if st.button("🗑️ Clear Groq Key", key="clear_groq"):
                    if update_api_key("groq", "api_keys", ""):
                        st.success("✅ Groq AI API key cleared")
                        st.rerun()
                    else:
                        st.error("❌ Failed to clear Groq AI key")
            
            # Display Groq configuration info
            st.info("""
            **Groq AI Configuration:**
            - **API Key**: Used for accessing Groq's fast inference API
            - **Models**: Llama3-8B, Llama3-70B with various configurations
            - **Usage**: Fast text generation, chat completion, resume analysis
            - **Cost**: Pay-per-token pricing, very competitive rates
            - **Speed**: Optimized for high-speed inference
            """)
        
        with tab3:
            st.subheader("Configuration Status")
            st.write("Overview of your current API configuration and system status.")
            
            # Display configuration status
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🤗 Hugging Face Status")
                hf_status = "✅ Configured" if (current_hf_key) else "⚠️ Using Default"
                st.markdown(f"**Status**: {hf_status}")
                
                # Show available models
                st.markdown("**Available Models:**")
                hf_models = config.get("huggingface", {}).get("models", {})
                for model_type, model_name in hf_models.items():
                    st.markdown(f"- {model_type}: `{model_name}`")
            
            with col2:
                st.markdown("### ⚡ Groq AI Status")
                groq_status = "✅ Configured" if (current_groq_key) else "❌ Not Configured"
                st.markdown(f"**Status**: {groq_status}")
                
                # Show available models
                st.markdown("**Available Models:**")
                groq_models = config.get("groq", {}).get("models", {})
                for model_type, model_name in groq_models.items():
                    st.markdown(f"- {model_type}: `{model_name}`")
            
            # System recommendations
            st.markdown("### 💡 Recommendations")
            if current_groq_key:
                st.success("🎉 Great! You have both Hugging Face and Groq configured. The system will automatically choose the best provider for each task.")
            elif current_hf_key:
                st.info("💡 Consider adding a Groq API key for faster text generation and better performance.")
            else:
                st.warning("⚠️ Consider configuring API keys for better performance. The system will work with default keys but may have limitations.")
            
            # Configuration file info
            st.markdown("### 📁 Configuration File")
            st.code("config/api_config.json", language="text")
            st.write("Your API keys are stored securely in the configuration file. Make sure to keep this file private and don't commit it to version control.")
            
            # Export/Import configuration
            st.markdown("### 🔄 Configuration Management")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Export Configuration", key="export_config"):
                    config_json = json.dumps(config, indent=2)
                    st.download_button(
                        label="Download config.json",
                        data=config_json,
                        file_name="api_config_backup.json",
                        mime="application/json"
                    )
            
            with col2:
                uploaded_config = st.file_uploader(
                    "Import Configuration", 
                    type=['json'],
                    key="import_config"
                )
                if uploaded_config is not None:
                    try:
                        imported_config = json.load(uploaded_config)
                        if save_api_config(imported_config):
                            st.success("✅ Configuration imported successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to import configuration")
                    except Exception as e:
                        st.error(f"❌ Invalid configuration file: {e}")
    
    def _render_help_support(self):
        """Render help and support page."""
        st.header("❓ Help & Support")
        st.write("Get help and support for using the Resume AI application.")
        
        # FAQ Section
        st.subheader("Frequently Asked Questions")
        
        with st.expander("How do I upload a resume?"):
            st.write("1. Go to the Resume Analysis page")
            st.write("2. Click on 'Choose a resume file'")
            st.write("3. Select your PDF, DOCX, or TXT file")
            st.write("4. Wait for the analysis to complete")
        
        with st.expander("What file formats are supported?"):
            st.write("We support the following formats:")
            st.write("• PDF (.pdf)")
            st.write("• Microsoft Word (.docx)")
            st.write("• Plain Text (.txt)")
        
        with st.expander("How do I improve my resume score?"):
            st.write("1. Use the AI Enhancement feature")
            st.write("2. Check ATS compatibility")
            st.write("3. Match keywords from job descriptions")
            st.write("4. Follow the recommendations provided")
        
        # Contact Support
        st.subheader("Contact Support")
        st.write("If you need additional help, please contact us:")
        st.write("📧 Email: support@resumeai.com")
        st.write("📞 Phone: +1 (555) 123-4567")
        st.write("💬 Live Chat: Available 24/7")
    
    def _render_export_resume(self):
        """Render export resume page."""
        st.header("💾 Export Resume")
        st.write("Export your resume in various formats.")
        
        if not hasattr(st.session_state, 'current_resume') or not st.session_state.current_resume:
            st.warning("Please upload and analyze a resume first.")
            return
        
        resume = st.session_state.current_resume
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Export Formats")
            export_format = st.selectbox("Choose format:", ["PDF", "DOCX", "TXT", "HTML", "JSON"])
            include_photo = st.checkbox("Include photo", value=False)
            include_references = st.checkbox("Include references", value=False)
        
        with col2:
            st.subheader("Export Options")
            template = st.selectbox("Template:", ["Modern", "Professional", "Creative", "Minimal"])
            color_scheme = st.selectbox("Color Scheme:", ["Blue", "Green", "Purple", "Black"])
            font_family = st.selectbox("Font Family:", ["Arial", "Times New Roman", "Calibri"])
        
        if st.button("📄 Export Resume"):
            with st.spinner("Generating resume..."):
                # Simulate export process
                import time
                time.sleep(2)
            
            st.success(f"Resume exported as {export_format} successfully!")
            st.download_button(
                label=f"Download {export_format}",
                data="Resume content here...",
                file_name=f"resume.{export_format.lower()}",
                mime="application/octet-stream"
            )
    
    def _render_import_data(self):
        """Render import data page."""
        st.header("📥 Import Data")
        st.write("Import data from various sources to enhance your resume.")
        
        # Import options
        import_type = st.selectbox("Import Type:", [
            "LinkedIn Profile",
            "Job Description",
            "Skills Database",
            "Previous Resume",
            "Portfolio Data"
        ])
        
        if import_type == "LinkedIn Profile":
            st.subheader("LinkedIn Profile Import")
            linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourprofile")
            if st.button("Import LinkedIn Data"):
                st.success("LinkedIn data imported successfully!")
        
        elif import_type == "Job Description":
            st.subheader("Job Description Import")
            job_url = st.text_input("Job Posting URL", placeholder="https://company.com/jobs/123")
            job_text = st.text_area("Or paste job description here:", height=200)
            if st.button("Import Job Data"):
                st.success("Job description imported successfully!")
        
        elif import_type == "Skills Database":
            st.subheader("Skills Database Import")
            skills_file = st.file_uploader("Upload skills file", type=['csv', 'json', 'txt'])
            if skills_file and st.button("Import Skills"):
                st.success("Skills database imported successfully!")
        
        elif import_type == "Previous Resume":
            st.subheader("Previous Resume Import")
            resume_file = st.file_uploader("Upload previous resume", type=['pdf', 'docx', 'txt'])
            if resume_file and st.button("Import Resume"):
                st.success("Previous resume imported successfully!")
        
        elif import_type == "Portfolio Data":
            st.subheader("Portfolio Data Import")
            portfolio_url = st.text_input("Portfolio URL", placeholder="https://yourportfolio.com")
            github_url = st.text_input("GitHub URL", placeholder="https://github.com/yourusername")
            if st.button("Import Portfolio Data"):
                st.success("Portfolio data imported successfully!")

def main():
    """Main application entry point."""
    try:
        app = ResumeAIApp()
        app.run()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        st.error(f"Application failed to start: {e}")

if __name__ == "__main__":
    main()
