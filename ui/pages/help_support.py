"""
Help & Support Page for Resume/CV AI Application
Handles help documentation and support functionality.

This module provides:
- Help documentation and guides
- FAQ and troubleshooting
- Contact support options
- Video tutorials and examples
- Community resources
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("help_support_page")

def render():
    """
    Render the help & support page with comprehensive logging.
    
    This function renders the help & support page including documentation,
    FAQ, contact options, and community resources.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering help & support page")
        start_time = time.time()
        
        # Page header
        st.title("❓ Help & Support")
        st.markdown("Get help, find answers, and connect with our support team.")
        
        # Quick help sections
        _render_quick_help()
        
        # Documentation sections
        _render_documentation()
        
        # FAQ section
        _render_faq()
        
        # Video tutorials
        _render_video_tutorials()
        
        # Contact support
        _render_contact_support()
        
        # Community resources
        _render_community_resources()
        
        rendering_time = time.time() - start_time
        logger.info(f"Help & support page rendered in {rendering_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render help & support page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        st.error(f"Page rendering error: {e}")

def _render_quick_help():
    """Render quick help section."""
    try:
        st.markdown("### 🚀 Quick Help")
        
        # Common tasks
        st.markdown("#### 📋 Common Tasks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 How to upload a resume", use_container_width=True):
                st.session_state.show_upload_help = True
                st.rerun()
            
            if st.button("🔍 How to use job matching", use_container_width=True):
                st.session_state.show_job_matching_help = True
                st.rerun()
            
            if st.button("✨ How to enhance your resume", use_container_width=True):
                st.session_state.show_enhancement_help = True
                st.rerun()
        
        with col2:
            if st.button("📊 How to check ATS compatibility", use_container_width=True):
                st.session_state.show_ats_help = True
                st.rerun()
            
            if st.button("🔧 How to build a new resume", use_container_width=True):
                st.session_state.show_builder_help = True
                st.rerun()
            
            if st.button("💾 How to export your resume", use_container_width=True):
                st.session_state.show_export_help = True
                st.rerun()
        
        # Show specific help content
        if st.session_state.get('show_upload_help'):
            _render_upload_help()
        
        if st.session_state.get('show_job_matching_help'):
            _render_job_matching_help()
        
        if st.session_state.get('show_enhancement_help'):
            _render_enhancement_help()
        
        if st.session_state.get('show_ats_help'):
            _render_ats_help()
        
        if st.session_state.get('show_builder_help'):
            _render_builder_help()
        
        if st.session_state.get('show_export_help'):
            _render_export_help()
        
    except Exception as e:
        logger.error(f"Failed to render quick help: {e}")
        st.error(f"Quick help error: {e}")

def _render_upload_help():
    """Render upload help content."""
    try:
        st.markdown("#### 📄 Resume Upload Guide")
        
        st.markdown("""
        **Step 1: Prepare Your Resume**
        - Ensure your resume is in PDF, DOCX, or TXT format
        - File size should be under 10MB
        - Make sure the text is readable and not scanned
        
        **Step 2: Upload Your Resume**
        - Go to the Resume Analysis page
        - Click "Choose a resume file"
        - Select your resume file from your computer
        
        **Step 3: Wait for Processing**
        - The system will automatically process your file
        - This usually takes 10-30 seconds
        - You'll see a success message when complete
        
        **Step 4: Review Results**
        - Check the analysis results
        - Review any errors or warnings
        - Make corrections if needed
        """)
        
        if st.button("❌ Close Help", key="close_upload_help"):
            st.session_state.show_upload_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render upload help: {e}")
        st.error(f"Upload help error: {e}")

def _render_job_matching_help():
    """Render job matching help content."""
    try:
        st.markdown("#### 🎯 Job Matching Guide")
        
        st.markdown("""
        **Step 1: Analyze Your Resume**
        - First, upload and analyze your resume
        - Make sure the analysis is complete
        
        **Step 2: Upload Job Description**
        - Go to the Job Matching page
        - Upload a job description file (PDF, DOCX, TXT)
        - Or paste the job description text
        
        **Step 3: Run Matching Analysis**
        - Click "Analyze Match" button
        - Wait for the analysis to complete
        
        **Step 4: Review Results**
        - Check your compatibility score
        - Review skills match analysis
        - See recommendations for improvement
        """)
        
        if st.button("❌ Close Help", key="close_job_matching_help"):
            st.session_state.show_job_matching_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render job matching help: {e}")
        st.error(f"Job matching help error: {e}")

def _render_enhancement_help():
    """Render enhancement help content."""
    try:
        st.markdown("#### ✨ AI Enhancement Guide")
        
        st.markdown("""
        **Step 1: Analyze Your Resume**
        - Upload and analyze your resume first
        - The AI needs to understand your content
        
        **Step 2: Choose Enhancement Types**
        - Text Enhancement: Improve writing quality
        - Keyword Optimization: Add relevant keywords
        - ATS Optimization: Improve ATS compatibility
        - Content Structure: Reorganize sections
        
        **Step 3: Select Enhancement Level**
        - Conservative: Minor improvements
        - Moderate: Balanced changes
        - Aggressive: Major rewrites
        
        **Step 4: Apply Enhancements**
        - Click "Start AI Enhancement"
        - Review the suggestions
        - Apply the changes you like
        """)
        
        if st.button("❌ Close Help", key="close_enhancement_help"):
            st.session_state.show_enhancement_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render enhancement help: {e}")
        st.error(f"Enhancement help error: {e}")

def _render_ats_help():
    """Render ATS help content."""
    try:
        st.markdown("#### 📊 ATS Checker Guide")
        
        st.markdown("""
        **Step 1: Analyze Your Resume**
        - Upload and analyze your resume first
        
        **Step 2: Select ATS Systems**
        - Choose which ATS systems to check against
        - Common options: Workday, BambooHR, Greenhouse
        
        **Step 3: Choose Check Level**
        - Basic: Format and structure only
        - Standard: Includes keywords and content
        - Comprehensive: Full analysis with recommendations
        
        **Step 4: Review ATS Score**
        - Check your overall ATS compatibility score
        - Review format, keyword, and structure scores
        - Follow the recommendations for improvement
        """)
        
        if st.button("❌ Close Help", key="close_ats_help"):
            st.session_state.show_ats_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render ATS help: {e}")
        st.error(f"ATS help error: {e}")

def _render_builder_help():
    """Render builder help content."""
    try:
        st.markdown("#### 🔧 Resume Builder Guide")
        
        st.markdown("""
        **Step 1: Personal Information**
        - Enter your basic contact information
        - Add professional summary
        - Specify target job title
        
        **Step 2: Choose Template**
        - Select from professional templates
        - Preview different designs
        - Choose one that fits your style
        
        **Step 3: Add Content**
        - Enter your work experience
        - Add education information
        - List your skills
        
        **Step 4: AI Enhancement**
        - Apply AI improvements
        - Optimize content
        - Finalize your resume
        
        **Step 5: Export**
        - Download in your preferred format
        - Save as draft if needed
        """)
        
        if st.button("❌ Close Help", key="close_builder_help"):
            st.session_state.show_builder_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render builder help: {e}")
        st.error(f"Builder help error: {e}")

def _render_export_help():
    """Render export help content."""
    try:
        st.markdown("#### 💾 Export Guide")
        
        st.markdown("""
        **Step 1: Analyze Your Resume**
        - Make sure your resume is analyzed and enhanced
        
        **Step 2: Choose Export Format**
        - PDF: Professional, print-ready
        - DOCX: Editable Microsoft Word format
        - HTML: Web-friendly format
        - TXT: Plain text format
        
        **Step 3: Customize Export**
        - Adjust layout options
        - Choose color scheme
        - Set security options
        
        **Step 4: Download**
        - Click "Export Now"
        - Wait for processing
        - Download your resume file
        """)
        
        if st.button("❌ Close Help", key="close_export_help"):
            st.session_state.show_export_help = False
            st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render export help: {e}")
        st.error(f"Export help error: {e}")

def _render_documentation():
    """Render documentation section."""
    try:
        st.markdown("### 📚 Documentation")
        
        # Documentation categories
        doc_categories = {
            "Getting Started": [
                "Quick Start Guide",
                "Account Setup",
                "First Resume Upload",
                "Understanding the Interface"
            ],
            "Features": [
                "Resume Analysis",
                "Job Matching",
                "AI Enhancement",
                "ATS Checking",
                "Resume Building",
                "Export Options"
            ],
            "Advanced": [
                "API Integration",
                "Custom Templates",
                "Bulk Operations",
                "Data Import/Export"
            ],
            "Troubleshooting": [
                "Common Issues",
                "File Format Problems",
                "Performance Issues",
                "Error Messages"
            ]
        }
        
        # Display documentation in tabs
        tabs = st.tabs(list(doc_categories.keys()))
        
        for i, (category, topics) in enumerate(doc_categories.items()):
            with tabs[i]:
                st.markdown(f"#### {category}")
                
                for topic in topics:
                    with st.expander(f"📖 {topic}", expanded=False):
                        st.markdown(f"**{topic} Documentation**")
                        st.write(f"Detailed documentation for {topic.lower()} will be displayed here.")
                        st.write("This section will contain step-by-step instructions, examples, and best practices.")
                        
                        # Mock content
                        if "Quick Start" in topic:
                            st.markdown("""
                            **Quick Start Steps:**
                            1. Sign up for an account
                            2. Upload your resume
                            3. Run analysis
                            4. Get AI enhancements
                            5. Export your improved resume
                            """)
        
    except Exception as e:
        logger.error(f"Failed to render documentation: {e}")
        st.error(f"Documentation error: {e}")

def _render_faq():
    """Render FAQ section."""
    try:
        st.markdown("### ❓ Frequently Asked Questions")
        
        # FAQ categories
        faq_data = {
            "General": [
                {
                    "question": "What file formats are supported?",
                    "answer": "We support PDF, DOCX, DOC, TXT, and RTF files. Maximum file size is 10MB."
                },
                {
                    "question": "Is my data secure?",
                    "answer": "Yes, all data is encrypted and stored securely. We never share your personal information."
                },
                {
                    "question": "How accurate is the AI analysis?",
                    "answer": "Our AI analysis is highly accurate, but we recommend reviewing all suggestions before applying them."
                }
            ],
            "Technical": [
                {
                    "question": "Why is my resume not uploading?",
                    "answer": "Check that your file is in a supported format and under 10MB. Also ensure the file is not password-protected."
                },
                {
                    "question": "How long does analysis take?",
                    "answer": "Most resumes are analyzed within 30 seconds. Larger files or complex formatting may take longer."
                },
                {
                    "question": "Can I use the app offline?",
                    "answer": "No, the app requires an internet connection for AI processing and cloud storage."
                }
            ],
            "Billing": [
                {
                    "question": "Is there a free trial?",
                    "answer": "Yes, we offer a free tier with limited features. Premium plans provide full access."
                },
                {
                    "question": "How does billing work?",
                    "answer": "We offer monthly and annual subscription plans. You can cancel anytime."
                },
                {
                    "question": "What payment methods do you accept?",
                    "answer": "We accept all major credit cards, PayPal, and bank transfers."
                }
            ]
        }
        
        # Display FAQ in tabs
        tabs = st.tabs(list(faq_data.keys()))
        
        for i, (category, questions) in enumerate(faq_data.items()):
            with tabs[i]:
                st.markdown(f"#### {category} Questions")
                
                for j, qa in enumerate(questions):
                    with st.expander(f"Q: {qa['question']}", expanded=False):
                        st.write(qa['answer'])
        
        # Search FAQ
        st.markdown("#### 🔍 Search FAQ")
        search_term = st.text_input("Search for a question:", placeholder="Enter keywords...")
        
        if search_term:
            st.info(f"Searching for: '{search_term}' - Results will be displayed here")
        
    except Exception as e:
        logger.error(f"Failed to render FAQ: {e}")
        st.error(f"FAQ error: {e}")

def _render_video_tutorials():
    """Render video tutorials section."""
    try:
        st.markdown("### 🎥 Video Tutorials")
        
        # Tutorial categories
        tutorials = {
            "Getting Started": [
                {
                    "title": "Welcome to Resume AI",
                    "duration": "5:30",
                    "description": "Introduction to the platform and basic features"
                },
                {
                    "title": "Uploading Your First Resume",
                    "duration": "3:45",
                    "description": "Step-by-step guide to uploading and analyzing resumes"
                }
            ],
            "Advanced Features": [
                {
                    "title": "AI Enhancement Deep Dive",
                    "duration": "8:15",
                    "description": "Learn how to use AI enhancement features effectively"
                },
                {
                    "title": "Job Matching Strategies",
                    "duration": "6:20",
                    "description": "Best practices for job matching and optimization"
                }
            ],
            "Tips & Tricks": [
                {
                    "title": "ATS Optimization Tips",
                    "duration": "4:50",
                    "description": "Make your resume ATS-friendly with these tips"
                },
                {
                    "title": "Export and Formatting",
                    "duration": "3:30",
                    "description": "Export your resume in the perfect format"
                }
            ]
        }
        
        # Display tutorials
        for category, video_list in tutorials.items():
            st.markdown(f"#### {category}")
            
            for video in video_list:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"🎥 **{video['title']}**")
                    st.write(video['description'])
                
                with col2:
                    st.write(f"⏱️ {video['duration']}")
                
                with col3:
                    if st.button("▶️ Watch", key=f"watch_{video['title']}"):
                        st.info(f"Opening video: {video['title']}")
        
        # Tutorial requests
        st.markdown("#### 📝 Request a Tutorial")
        st.write("Can't find what you're looking for? Request a tutorial!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tutorial_topic = st.text_input("What topic would you like a tutorial on?")
        
        with col2:
            tutorial_difficulty = st.selectbox("Difficulty Level:", ["Beginner", "Intermediate", "Advanced"])
        
        if st.button("📤 Submit Request", key="submit_tutorial_request"):
            st.success("Thank you! We'll consider your tutorial request.")
        
    except Exception as e:
        logger.error(f"Failed to render video tutorials: {e}")
        st.error(f"Video tutorials error: {e}")

def _render_contact_support():
    """Render contact support section."""
    try:
        st.markdown("### 📞 Contact Support")
        
        # Support options
        st.markdown("#### 💬 Get in Touch")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📧 Email Support**")
            st.write("For detailed questions and issues:")
            st.code("support@resumeai.com")
            
            if st.button("📧 Send Email", key="send_email"):
                st.info("Opening your email client...")
            
            st.markdown("**💬 Live Chat**")
            st.write("For immediate assistance:")
            
            if st.button("💬 Start Chat", key="start_chat"):
                st.info("Live chat will be available during business hours (9 AM - 6 PM EST)")
        
        with col2:
            st.markdown("**📞 Phone Support**")
            st.write("For urgent issues:")
            st.code("+1 (555) 123-4567")
            
            if st.button("📞 Call Now", key="call_support"):
                st.info("Phone support available Monday-Friday, 9 AM - 6 PM EST")
            
            st.markdown("**🎫 Support Ticket**")
            st.write("Create a support ticket for tracking:")
            
            if st.button("🎫 Create Ticket", key="create_ticket"):
                st.session_state.show_ticket_form = True
                st.rerun()
        
        # Support ticket form
        if st.session_state.get('show_ticket_form'):
            _render_support_ticket_form()
        
        # Response times
        st.markdown("#### ⏱️ Response Times")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Email Support", "24 hours", "Average")
        
        with col2:
            st.metric("Live Chat", "5 minutes", "During hours")
        
        with col3:
            st.metric("Phone Support", "Immediate", "During hours")
        
    except Exception as e:
        logger.error(f"Failed to render contact support: {e}")
        st.error(f"Contact support error: {e}")

def _render_support_ticket_form():
    """Render support ticket form."""
    try:
        st.markdown("#### 🎫 Create Support Ticket")
        
        with st.form("support_ticket_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name*", required=True)
                email = st.text_input("Email Address*", required=True)
                priority = st.selectbox("Priority*", ["Low", "Medium", "High", "Urgent"])
            
            with col2:
                issue_type = st.selectbox("Issue Type*", [
                    "Technical Issue",
                    "Billing Question",
                    "Feature Request",
                    "Bug Report",
                    "General Question"
                ])
                subject = st.text_input("Subject*", required=True)
            
            description = st.text_area(
                "Description*",
                placeholder="Please describe your issue in detail...",
                required=True
            )
            
            attachments = st.file_uploader(
                "Attachments (optional)",
                accept_multiple_files=True,
                help="Upload screenshots or files that might help"
            )
            
            submitted = st.form_submit_button("🎫 Submit Ticket", type="primary")
            
            if submitted:
                if name and email and subject and description:
                    st.success("✅ Support ticket submitted successfully!")
                    st.info("We'll get back to you within 24 hours.")
                    st.session_state.show_ticket_form = False
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
    except Exception as e:
        logger.error(f"Failed to render support ticket form: {e}")
        st.error(f"Support ticket form error: {e}")

def _render_community_resources():
    """Render community resources section."""
    try:
        st.markdown("### 🌐 Community Resources")
        
        # Community links
        st.markdown("#### 🔗 Community Links")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💬 Community Forum**")
            st.write("Connect with other users, share tips, and get help:")
            st.write("🌐 [community.resumeai.com](https://community.resumeai.com)")
            
            if st.button("💬 Visit Forum", key="visit_forum"):
                st.info("Opening community forum...")
            
            st.markdown("**📱 Social Media**")
            st.write("Follow us for updates and tips:")
            st.write("🐦 Twitter: @ResumeAI")
            st.write("📘 Facebook: /ResumeAI")
            st.write("📸 Instagram: @resumeai")
        
        with col2:
            st.markdown("**📚 Knowledge Base**")
            st.write("Comprehensive guides and articles:")
            st.write("🌐 [help.resumeai.com](https://help.resumeai.com)")
            
            if st.button("📚 Visit Knowledge Base", key="visit_kb"):
                st.info("Opening knowledge base...")
            
            st.markdown("**🎓 Learning Center**")
            st.write("Free courses and tutorials:")
            st.write("🌐 [learn.resumeai.com](https://learn.resumeai.com)")
            
            if st.button("🎓 Visit Learning Center", key="visit_learning"):
                st.info("Opening learning center...")
        
        # Community stats
        st.markdown("#### 📊 Community Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Forum Members", "12,456", "234")
        
        with col2:
            st.metric("Articles", "1,234", "56")
        
        with col3:
            st.metric("Tutorials", "89", "12")
        
        with col4:
            st.metric("Active Users", "3,456", "123")
        
        # Newsletter signup
        st.markdown("#### 📧 Newsletter")
        st.write("Stay updated with the latest features and tips!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            newsletter_email = st.text_input("Email Address:", placeholder="your@email.com")
        
        with col2:
            if st.button("📧 Subscribe", key="subscribe_newsletter"):
                if newsletter_email:
                    st.success("✅ Subscribed to newsletter!")
                else:
                    st.error("Please enter your email address")
        
    except Exception as e:
        logger.error(f"Failed to render community resources: {e}")
        st.error(f"Community resources error: {e}")

def get_help_support_info() -> Dict[str, Any]:
    """
    Get help & support page information and statistics.
    
    Returns:
        Dict[str, Any]: Help & support page information
    """
    try:
        return {
            "page_name": "Help & Support",
            "help_sections_viewed": len([k for k in st.session_state.keys() if k.startswith('show_') and st.session_state[k]]),
            "ticket_form_shown": st.session_state.get('show_ticket_form', False),
            "page_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get help & support info: {e}")
        return {
            "error": str(e),
            "page_timestamp": datetime.now().isoformat()
        }
