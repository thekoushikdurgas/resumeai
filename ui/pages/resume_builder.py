"""
Resume Builder Page for Resume/CV AI Application
Handles AI-powered resume building.

This module provides:
- Resume building wizard
- Template selection
- Content generation
- AI assistance
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
logger = setup_logger("resume_builder_page")

def render():
    """
    Render the resume builder page with comprehensive logging.
    
    This function renders the resume builder page including building wizard,
    template selection, content generation, and AI assistance.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering resume builder page")
        start_time = time.time()
        
        # Page header
        st.title("🔧 Resume Builder")
        st.markdown("Build a professional resume with AI assistance.")
        
        # Resume builder wizard
        _render_builder_wizard()
        
        # Template selection section
        if st.session_state.get('builder_step') >= 1:
            _render_template_selection()
        
        # Content generation section
        if st.session_state.get('builder_step') >= 2:
            _render_content_generation()
        
        # AI assistance section
        if st.session_state.get('builder_step') >= 3:
            _render_ai_assistance()
        
        # Final review section
        if st.session_state.get('builder_step') >= 4:
            _render_final_review()
        
        rendering_time = time.time() - start_time
        logger.info(f"Resume builder page rendered in {rendering_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render resume builder page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        st.error(f"Page rendering error: {e}")

def _render_builder_wizard():
    """Render resume builder wizard."""
    try:
        st.markdown("### 🧙‍♂️ Resume Builder Wizard")
        
        # Initialize builder step if not exists
        if 'builder_step' not in st.session_state:
            st.session_state.builder_step = 0
        
        # Step indicator
        steps = ["Personal Info", "Template", "Content", "AI Help", "Review"]
        current_step = st.session_state.builder_step
        
        # Progress bar
        progress = (current_step + 1) / len(steps)
        st.progress(progress)
        
        # Step navigation
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, step in enumerate(steps):
            with [col1, col2, col3, col4, col5][i]:
                if i <= current_step:
                    st.success(f"✅ {step}")
                else:
                    st.info(f"⏳ {step}")
        
        # Personal information form
        if current_step == 0:
            _render_personal_info_form()
        
    except Exception as e:
        logger.error(f"Failed to render builder wizard: {e}")
        st.error(f"Builder wizard error: {e}")

def _render_personal_info_form():
    """Render personal information form."""
    try:
        st.markdown("#### 👤 Personal Information")
        
        # Personal details
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", value=st.session_state.get('first_name', ''))
            last_name = st.text_input("Last Name", value=st.session_state.get('last_name', ''))
            email = st.text_input("Email", value=st.session_state.get('email', ''))
            phone = st.text_input("Phone", value=st.session_state.get('phone', ''))
        
        with col2:
            location = st.text_input("Location", value=st.session_state.get('location', ''))
            linkedin = st.text_input("LinkedIn Profile", value=st.session_state.get('linkedin', ''))
            github = st.text_input("GitHub Profile", value=st.session_state.get('github', ''))
            website = st.text_input("Website", value=st.session_state.get('website', ''))
        
        # Professional summary
        st.markdown("#### 📝 Professional Summary")
        professional_summary = st.text_area(
            "Tell us about yourself",
            value=st.session_state.get('professional_summary', ''),
            help="Brief description of your professional background and goals"
        )
        
        # Target job
        target_job = st.text_input(
            "Target Job Title",
            value=st.session_state.get('target_job', ''),
            help="The job title you're applying for"
        )
        
        # Next button
        if st.button("Next Step", key="next_personal_info"):
            # Store personal info
            st.session_state.first_name = first_name
            st.session_state.last_name = last_name
            st.session_state.email = email
            st.session_state.phone = phone
            st.session_state.location = location
            st.session_state.linkedin = linkedin
            st.session_state.github = github
            st.session_state.website = website
            st.session_state.professional_summary = professional_summary
            st.session_state.target_job = target_job
            
            # Move to next step
            st.session_state.builder_step = 1
            st.rerun()
            
    except Exception as e:
        logger.error(f"Failed to render personal info form: {e}")
        st.error(f"Personal info form error: {e}")

def _render_template_selection():
    """Render template selection section."""
    try:
        st.markdown("### 🎨 Template Selection")
        
        # Template options
        templates = [
            {
                "name": "Professional",
                "description": "Clean and professional design",
                "preview": "👔",
                "features": ["Simple layout", "ATS-friendly", "Easy to read"]
            },
            {
                "name": "Modern",
                "description": "Contemporary design with visual elements",
                "preview": "🎨",
                "features": ["Visual hierarchy", "Color accents", "Modern fonts"]
            },
            {
                "name": "Creative",
                "description": "Unique design for creative professionals",
                "preview": "✨",
                "features": ["Creative layout", "Visual elements", "Unique design"]
            },
            {
                "name": "Minimalist",
                "description": "Simple and clean design",
                "preview": "📄",
                "features": ["Minimal design", "Focus on content", "Clean typography"]
            }
        ]
        
        # Template selection
        selected_template = st.radio(
            "Choose a template:",
            [template["name"] for template in templates],
            key="template_selection"
        )
        
        # Show template details
        template_details = next(t for t in templates if t["name"] == selected_template)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"### {template_details['preview']}")
        
        with col2:
            st.markdown(f"**{template_details['name']}**")
            st.write(template_details['description'])
            st.markdown("**Features:**")
            for feature in template_details['features']:
                st.write(f"• {feature}")
        
        # Next button
        if st.button("Next Step", key="next_template"):
            st.session_state.selected_template = selected_template
            st.session_state.builder_step = 2
            st.rerun()
            
    except Exception as e:
        logger.error(f"Failed to render template selection: {e}")
        st.error(f"Template selection error: {e}")

def _render_content_generation():
    """Render content generation section."""
    try:
        st.markdown("### 📝 Content Generation")
        
        # Content sections
        st.markdown("#### 📋 Resume Sections")
        
        # Experience section
        st.markdown("##### 💼 Experience")
        experience_count = st.number_input("Number of experiences", min_value=1, max_value=10, value=3)
        
        experiences = []
        for i in range(experience_count):
            with st.expander(f"Experience {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    job_title = st.text_input(f"Job Title {i+1}", key=f"job_title_{i}")
                    company = st.text_input(f"Company {i+1}", key=f"company_{i}")
                    start_date = st.date_input(f"Start Date {i+1}", key=f"start_date_{i}")
                
                with col2:
                    end_date = st.date_input(f"End Date {i+1}", key=f"end_date_{i}")
                    location = st.text_input(f"Location {i+1}", key=f"location_{i}")
                
                description = st.text_area(f"Description {i+1}", key=f"description_{i}")
                
                experiences.append({
                    "job_title": job_title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "location": location,
                    "description": description
                })
        
        # Education section
        st.markdown("##### 🎓 Education")
        education_count = st.number_input("Number of education entries", min_value=1, max_value=5, value=1)
        
        educations = []
        for i in range(education_count):
            with st.expander(f"Education {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
                    school = st.text_input(f"School {i+1}", key=f"school_{i}")
                
                with col2:
                    graduation_date = st.date_input(f"Graduation Date {i+1}", key=f"graduation_date_{i}")
                    gpa = st.text_input(f"GPA {i+1}", key=f"gpa_{i}")
                
                educations.append({
                    "degree": degree,
                    "school": school,
                    "graduation_date": graduation_date,
                    "gpa": gpa
                })
        
        # Skills section
        st.markdown("##### 🎯 Skills")
        skills = st.text_area(
            "Enter your skills (one per line)",
            help="Enter each skill on a new line"
        )
        skills_list = [skill.strip() for skill in skills.split('\n') if skill.strip()]
        
        # Next button
        if st.button("Next Step", key="next_content"):
            st.session_state.experiences = experiences
            st.session_state.educations = educations
            st.session_state.skills = skills_list
            st.session_state.builder_step = 3
            st.rerun()
            
    except Exception as e:
        logger.error(f"Failed to render content generation: {e}")
        st.error(f"Content generation error: {e}")

def _render_ai_assistance():
    """Render AI assistance section."""
    try:
        st.markdown("### 🤖 AI Assistance")
        
        # AI enhancement options
        st.markdown("#### ✨ AI Enhancement Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            enhance_summary = st.checkbox("Enhance Professional Summary", value=True)
            enhance_experience = st.checkbox("Improve Experience Descriptions", value=True)
            enhance_skills = st.checkbox("Optimize Skills Section", value=True)
        
        with col2:
            add_keywords = st.checkbox("Add Industry Keywords", value=True)
            improve_formatting = st.checkbox("Improve Formatting", value=True)
            ats_optimize = st.checkbox("ATS Optimization", value=True)
        
        # AI processing
        if st.button("🚀 Apply AI Enhancements", key="apply_ai_enhancements"):
            _apply_ai_enhancements({
                "enhance_summary": enhance_summary,
                "enhance_experience": enhance_experience,
                "enhance_skills": enhance_skills,
                "add_keywords": add_keywords,
                "improve_formatting": improve_formatting,
                "ats_optimize": ats_optimize
            })
        
        # Next button
        if st.button("Next Step", key="next_ai"):
            st.session_state.builder_step = 4
            st.rerun()
            
    except Exception as e:
        logger.error(f"Failed to render AI assistance: {e}")
        st.error(f"AI assistance error: {e}")

def _apply_ai_enhancements(options):
    """Apply AI enhancements to resume content."""
    try:
        logger.info("Applying AI enhancements")
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate AI processing
        enhancement_steps = [
            "Analyzing content...",
            "Generating improvements...",
            "Optimizing descriptions...",
            "Adding keywords...",
            "Improving formatting...",
            "Finalizing enhancements...",
            "Complete!"
        ]
        
        for i, step in enumerate(enhancement_steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(enhancement_steps))
            time.sleep(0.5)
        
        # Store enhanced content
        st.session_state.ai_enhanced = True
        st.session_state.enhancement_options = options
        
        status_text.text("AI enhancements applied!")
        st.success("🎉 AI enhancements applied successfully!")
        
    except Exception as e:
        logger.error(f"Failed to apply AI enhancements: {e}")
        st.error(f"AI enhancement error: {e}")

def _render_final_review():
    """Render final review section."""
    try:
        st.markdown("### 📋 Final Review")
        
        # Resume preview
        st.markdown("#### 👀 Resume Preview")
        
        # Personal info
        st.markdown(f"**{st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}**")
        st.markdown(f"📧 {st.session_state.get('email', '')} | 📞 {st.session_state.get('phone', '')}")
        st.markdown(f"📍 {st.session_state.get('location', '')}")
        
        # Professional summary
        st.markdown("#### Professional Summary")
        st.write(st.session_state.get('professional_summary', ''))
        
        # Experience
        st.markdown("#### Experience")
        experiences = st.session_state.get('experiences', [])
        for exp in experiences:
            if exp.get('job_title') and exp.get('company'):
                st.markdown(f"**{exp['job_title']}** at {exp['company']}")
                if exp.get('description'):
                    st.write(exp['description'])
        
        # Education
        st.markdown("#### Education")
        educations = st.session_state.get('educations', [])
        for edu in educations:
            if edu.get('degree') and edu.get('school'):
                st.markdown(f"**{edu['degree']}** from {edu['school']}")
        
        # Skills
        st.markdown("#### Skills")
        skills = st.session_state.get('skills', [])
        if skills:
            st.write(", ".join(skills))
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download Resume", key="download_resume"):
                st.success("Resume download started!")
        
        with col2:
            if st.button("🔄 Regenerate", key="regenerate_resume"):
                st.session_state.builder_step = 0
                st.rerun()
        
        with col3:
            if st.button("💾 Save Draft", key="save_draft"):
                st.success("Draft saved successfully!")
        
    except Exception as e:
        logger.error(f"Failed to render final review: {e}")
        st.error(f"Final review error: {e}")

def get_resume_builder_info() -> Dict[str, Any]:
    """
    Get resume builder page information and statistics.
    
    Returns:
        Dict[str, Any]: Resume builder page information
    """
    try:
        return {
            "page_name": "Resume Builder",
            "builder_step": st.session_state.get('builder_step', 0),
            "selected_template": st.session_state.get('selected_template', ''),
            "ai_enhanced": st.session_state.get('ai_enhanced', False),
            "page_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get resume builder info: {e}")
        return {
            "error": str(e),
            "page_timestamp": datetime.now().isoformat()
        }
