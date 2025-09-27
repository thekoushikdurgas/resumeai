"""
Templates Page for Resume/CV AI Application
Handles resume template management.

This module provides:
- Template browsing and selection
- Template preview
- Template customization
- Template management
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
logger = setup_logger("templates_page")

def render():
    """
    Render the templates page with comprehensive logging.
    
    This function renders the templates page including template browsing,
    selection, preview, and customization.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering templates page")
        start_time = time.time()
        
        # Page header
        st.title("📋 Resume Templates")
        st.markdown("Browse and select from our collection of professional resume templates.")
        
        # Template categories
        _render_template_categories()
        
        # Template grid
        _render_template_grid()
        
        # Template preview
        if st.session_state.get('selected_template'):
            _render_template_preview()
        
        # Template customization
        if st.session_state.get('template_customizing'):
            _render_template_customization()
        
        rendering_time = time.time() - start_time
        logger.info(f"Templates page rendered in {rendering_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render templates page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        st.error(f"Page rendering error: {e}")

def _render_template_categories():
    """Render template categories section."""
    try:
        st.markdown("### 🏷️ Template Categories")
        
        # Category selection
        categories = ["All", "Professional", "Creative", "Modern", "Minimalist", "Academic", "Technical"]
        selected_category = st.selectbox("Filter by category:", categories)
        
        # Template count
        template_count = _get_template_count(selected_category)
        st.info(f"Found {template_count} templates in '{selected_category}' category")
        
    except Exception as e:
        logger.error(f"Failed to render template categories: {e}")
        st.error(f"Template categories error: {e}")

def _get_template_count(category: str) -> int:
    """Get template count for category."""
    try:
        # Mock template counts
        counts = {
            "All": 24,
            "Professional": 8,
            "Creative": 6,
            "Modern": 4,
            "Minimalist": 3,
            "Academic": 2,
            "Technical": 1
        }
        return counts.get(category, 0)
    except Exception as e:
        logger.error(f"Failed to get template count: {e}")
        return 0

def _render_template_grid():
    """Render template grid section."""
    try:
        st.markdown("### 🎨 Available Templates")
        
        # Template data
        templates = [
            {
                "id": "prof_001",
                "name": "Classic Professional",
                "category": "Professional",
                "preview": "👔",
                "description": "Clean and traditional design perfect for corporate roles",
                "features": ["ATS-friendly", "Simple layout", "Easy to customize"],
                "popularity": 95
            },
            {
                "id": "prof_002",
                "name": "Executive Summary",
                "category": "Professional",
                "preview": "💼",
                "description": "Executive-level template with emphasis on leadership",
                "features": ["Leadership focus", "Achievement highlights", "Professional tone"],
                "popularity": 88
            },
            {
                "id": "creative_001",
                "name": "Design Portfolio",
                "category": "Creative",
                "preview": "🎨",
                "description": "Creative template for designers and artists",
                "features": ["Visual elements", "Portfolio integration", "Creative layout"],
                "popularity": 92
            },
            {
                "id": "modern_001",
                "name": "Tech Modern",
                "category": "Modern",
                "preview": "💻",
                "description": "Modern template for technology professionals",
                "features": ["Tech-focused", "Clean design", "Skills emphasis"],
                "popularity": 90
            },
            {
                "id": "minimal_001",
                "name": "Clean Minimal",
                "category": "Minimalist",
                "preview": "📄",
                "description": "Minimalist design focusing on content",
                "features": ["Minimal design", "Content focus", "Clean typography"],
                "popularity": 85
            },
            {
                "id": "academic_001",
                "name": "Academic CV",
                "category": "Academic",
                "preview": "🎓",
                "description": "Template designed for academic and research positions",
                "features": ["Publication focus", "Research emphasis", "Academic format"],
                "popularity": 78
            }
        ]
        
        # Display templates in grid
        cols = st.columns(3)
        for i, template in enumerate(templates):
            with cols[i % 3]:
                _render_template_card(template)
        
    except Exception as e:
        logger.error(f"Failed to render template grid: {e}")
        st.error(f"Template grid error: {e}")

def _render_template_card(template: Dict[str, Any]):
    """Render individual template card."""
    try:
        with st.container():
            # Template preview
            st.markdown(f"### {template['preview']} {template['name']}")
            
            # Description
            st.write(template['description'])
            
            # Features
            st.markdown("**Features:**")
            for feature in template['features']:
                st.write(f"• {feature}")
            
            # Popularity
            st.markdown(f"**Popularity:** {template['popularity']}%")
            
            # Action buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👀 Preview", key=f"preview_{template['id']}"):
                    st.session_state.selected_template = template
                    st.rerun()
            
            with col2:
                if st.button("✏️ Customize", key=f"customize_{template['id']}"):
                    st.session_state.selected_template = template
                    st.session_state.template_customizing = True
                    st.rerun()
            
            st.markdown("---")
            
    except Exception as e:
        logger.error(f"Failed to render template card: {e}")
        st.error(f"Template card error: {e}")

def _render_template_preview():
    """Render template preview section."""
    try:
        st.markdown("### 👀 Template Preview")
        
        template = st.session_state.get('selected_template')
        if not template:
            st.warning("No template selected")
            return
        
        # Template details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {template['preview']} {template['name']}")
            st.write(template['description'])
            
            # Features
            st.markdown("**Features:**")
            for feature in template['features']:
                st.write(f"• {feature}")
        
        with col2:
            st.metric("Popularity", f"{template['popularity']}%")
            st.metric("Category", template['category'])
            
            # Action buttons
            if st.button("✏️ Customize This Template", key="customize_selected"):
                st.session_state.template_customizing = True
                st.rerun()
            
            if st.button("📥 Download Template", key="download_selected"):
                st.success("Template download started!")
            
            if st.button("❌ Close Preview", key="close_preview"):
                st.session_state.selected_template = None
                st.rerun()
        
        # Template preview image (mock)
        st.markdown("#### 📄 Template Preview")
        st.image("https://via.placeholder.com/600x800/ffffff/000000?text=Template+Preview", 
                caption=f"Preview of {template['name']} template")
        
    except Exception as e:
        logger.error(f"Failed to render template preview: {e}")
        st.error(f"Template preview error: {e}")

def _render_template_customization():
    """Render template customization section."""
    try:
        st.markdown("### ✏️ Template Customization")
        
        template = st.session_state.get('selected_template')
        if not template:
            st.warning("No template selected for customization")
            return
        
        # Customization options
        st.markdown(f"#### Customizing: {template['name']}")
        
        # Color scheme
        st.markdown("##### 🎨 Color Scheme")
        color_scheme = st.selectbox(
            "Choose color scheme:",
            ["Default", "Blue", "Green", "Purple", "Orange", "Custom"],
            key="color_scheme"
        )
        
        # Font selection
        st.markdown("##### 🔤 Font Selection")
        font_family = st.selectbox(
            "Choose font family:",
            ["Arial", "Times New Roman", "Calibri", "Georgia", "Helvetica"],
            key="font_family"
        )
        
        # Layout options
        st.markdown("##### 📐 Layout Options")
        col1, col2 = st.columns(2)
        
        with col1:
            section_order = st.multiselect(
                "Section order:",
                ["Contact", "Summary", "Experience", "Education", "Skills", "Projects"],
                default=["Contact", "Summary", "Experience", "Education", "Skills"]
            )
        
        with col2:
            include_photo = st.checkbox("Include photo placeholder", value=False)
            two_column = st.checkbox("Two-column layout", value=False)
            show_borders = st.checkbox("Show section borders", value=True)
        
        # Customization preview
        st.markdown("##### 👀 Customization Preview")
        st.info("Preview will be updated based on your selections")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Customization", key="save_customization"):
                st.success("Customization saved!")
        
        with col2:
            if st.button("🔄 Reset to Default", key="reset_customization"):
                st.session_state.template_customizing = False
                st.rerun()
        
        with col3:
            if st.button("📥 Apply & Download", key="apply_download"):
                st.success("Template applied and download started!")
        
    except Exception as e:
        logger.error(f"Failed to render template customization: {e}")
        st.error(f"Template customization error: {e}")

def get_templates_info() -> Dict[str, Any]:
    """
    Get templates page information and statistics.
    
    Returns:
        Dict[str, Any]: Templates page information
    """
    try:
        return {
            "page_name": "Templates",
            "selected_template": st.session_state.get('selected_template', {}),
            "template_customizing": st.session_state.get('template_customizing', False),
            "page_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get templates info: {e}")
        return {
            "error": str(e),
            "page_timestamp": datetime.now().isoformat()
        }
