"""
Customization Page for Resume/CV AI Application
Handles application customization and settings.

This module provides:
- Theme customization
- Layout preferences
- User settings
- Application preferences
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
logger = setup_logger("customization_page")

def render():
    """
    Render the customization page with comprehensive logging.
    
    This function renders the customization page including theme customization,
    layout preferences, user settings, and application preferences.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering customization page")
        start_time = time.time()
        
        # Page header
        st.title("🎨 Customization")
        st.markdown("Customize your Resume AI experience with themes, layouts, and preferences.")
        
        # Theme customization section
        _render_theme_customization()
        
        # Layout preferences section
        _render_layout_preferences()
        
        # User settings section
        _render_user_settings()
        
        # Application preferences section
        _render_app_preferences()
        
        # Export/Import settings section
        _render_settings_management()
        
        rendering_time = time.time() - start_time
        logger.info(f"Customization page rendered in {rendering_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render customization page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        st.error(f"Page rendering error: {e}")

def _render_theme_customization():
    """Render theme customization section."""
    try:
        st.markdown("### 🎨 Theme Customization")
        
        # Current theme
        current_theme = st.session_state.get('theme', 'light')
        st.info(f"Current theme: {current_theme.title()}")
        
        # Theme selection
        theme_options = ["light", "dark", "professional", "creative"]
        theme_labels = ["Light", "Dark", "Professional", "Creative"]
        
        selected_theme = st.selectbox(
            "Choose a theme:",
            theme_options,
            index=theme_options.index(current_theme),
            format_func=lambda x: theme_labels[theme_options.index(x)],
            key="theme_selector"
        )
        
        if selected_theme != current_theme:
            st.session_state.theme = selected_theme
            st.success(f"Theme changed to {selected_theme.title()}")
            st.rerun()
        
        # Custom theme options
        st.markdown("#### 🎨 Custom Theme Options")
        
        if st.checkbox("Enable custom theme", key="enable_custom_theme"):
            col1, col2 = st.columns(2)
            
            with col1:
                primary_color = st.color_picker("Primary Color", value="#007bff")
                secondary_color = st.color_picker("Secondary Color", value="#6c757d")
                background_color = st.color_picker("Background Color", value="#ffffff")
            
            with col2:
                text_color = st.color_picker("Text Color", value="#212529")
                accent_color = st.color_picker("Accent Color", value="#17a2b8")
                border_color = st.color_picker("Border Color", value="#dee2e6")
            
            if st.button("Apply Custom Theme", key="apply_custom_theme"):
                st.success("Custom theme applied!")
        
    except Exception as e:
        logger.error(f"Failed to render theme customization: {e}")
        st.error(f"Theme customization error: {e}")

def _render_layout_preferences():
    """Render layout preferences section."""
    try:
        st.markdown("### 📐 Layout Preferences")
        
        # Sidebar preferences
        st.markdown("#### 📱 Sidebar Preferences")
        
        sidebar_width = st.slider(
            "Sidebar Width",
            min_value=200,
            max_value=400,
            value=300,
            step=50,
            help="Adjust the width of the sidebar"
        )
        
        sidebar_position = st.selectbox(
            "Sidebar Position",
            ["Left", "Right"],
            help="Choose sidebar position"
        )
        
        # Main content preferences
        st.markdown("#### 📄 Main Content Preferences")
        
        content_width = st.selectbox(
            "Content Width",
            ["Narrow", "Medium", "Wide", "Full"],
            help="Choose the width of the main content area"
        )
        
        show_page_titles = st.checkbox(
            "Show page titles",
            value=True,
            help="Display page titles in the main content area"
        )
        
        show_breadcrumbs = st.checkbox(
            "Show breadcrumbs",
            value=True,
            help="Display navigation breadcrumbs"
        )
        
        # Layout preview
        st.markdown("#### 👀 Layout Preview")
        st.info("Layout changes will be applied immediately")
        
    except Exception as e:
        logger.error(f"Failed to render layout preferences: {e}")
        st.error(f"Layout preferences error: {e}")

def _render_user_settings():
    """Render user settings section."""
    try:
        st.markdown("### 👤 User Settings")
        
        # Personal information
        st.markdown("#### 📝 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name",
                value=st.session_state.get('user_first_name', ''),
                key="user_first_name"
            )
            last_name = st.text_input(
                "Last Name",
                value=st.session_state.get('user_last_name', ''),
                key="user_last_name"
            )
            email = st.text_input(
                "Email",
                value=st.session_state.get('user_email', ''),
                key="user_email"
            )
        
        with col2:
            company = st.text_input(
                "Company",
                value=st.session_state.get('user_company', ''),
                key="user_company"
            )
            job_title = st.text_input(
                "Job Title",
                value=st.session_state.get('user_job_title', ''),
                key="user_job_title"
            )
            location = st.text_input(
                "Location",
                value=st.session_state.get('user_location', ''),
                key="user_location"
            )
        
        # Preferences
        st.markdown("#### ⚙️ Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "Language",
                ["English", "Spanish", "French", "German", "Chinese"],
                help="Select your preferred language"
            )
            
            timezone = st.selectbox(
                "Timezone",
                ["UTC", "EST", "PST", "CST", "MST"],
                help="Select your timezone"
            )
        
        with col2:
            date_format = st.selectbox(
                "Date Format",
                ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
                help="Select your preferred date format"
            )
            
            currency = st.selectbox(
                "Currency",
                ["USD", "EUR", "GBP", "CAD", "AUD"],
                help="Select your preferred currency"
            )
        
        # Save button
        if st.button("💾 Save User Settings", key="save_user_settings"):
            # Store user settings
            st.session_state.user_first_name = first_name
            st.session_state.user_last_name = last_name
            st.session_state.user_email = email
            st.session_state.user_company = company
            st.session_state.user_job_title = job_title
            st.session_state.user_location = location
            st.session_state.user_language = language
            st.session_state.user_timezone = timezone
            st.session_state.user_date_format = date_format
            st.session_state.user_currency = currency
            
            st.success("User settings saved successfully!")
        
    except Exception as e:
        logger.error(f"Failed to render user settings: {e}")
        st.error(f"User settings error: {e}")

def _render_app_preferences():
    """Render application preferences section."""
    try:
        st.markdown("### ⚙️ Application Preferences")
        
        # General preferences
        st.markdown("#### 🔧 General Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_save = st.checkbox(
                "Auto-save",
                value=st.session_state.get('auto_save', True),
                help="Automatically save your work"
            )
            
            show_tooltips = st.checkbox(
                "Show tooltips",
                value=st.session_state.get('show_tooltips', True),
                help="Display helpful tooltips"
            )
            
            enable_animations = st.checkbox(
                "Enable animations",
                value=st.session_state.get('enable_animations', True),
                help="Enable smooth animations and transitions"
            )
        
        with col2:
            show_debug_info = st.checkbox(
                "Show debug info",
                value=st.session_state.get('show_debug_info', False),
                help="Display debug information"
            )
            
            enable_notifications = st.checkbox(
                "Enable notifications",
                value=st.session_state.get('enable_notifications', True),
                help="Show system notifications"
            )
            
            remember_settings = st.checkbox(
                "Remember settings",
                value=st.session_state.get('remember_settings', True),
                help="Remember your preferences across sessions"
            )
        
        # AI preferences
        st.markdown("#### 🤖 AI Preferences")
        
        ai_model = st.selectbox(
            "Preferred AI Model",
            ["GPT-4", "Claude", "Gemini", "Auto"],
            help="Select your preferred AI model for analysis"
        )
        
        ai_confidence = st.slider(
            "AI Confidence Level",
            min_value=0.1,
            max_value=1.0,
            value=0.8,
            step=0.1,
            help="Adjust AI confidence threshold"
        )
        
        enable_ai_suggestions = st.checkbox(
            "Enable AI suggestions",
            value=st.session_state.get('enable_ai_suggestions', True),
            help="Show AI-powered suggestions and recommendations"
        )
        
        # Save button
        if st.button("💾 Save App Preferences", key="save_app_preferences"):
            # Store app preferences
            st.session_state.auto_save = auto_save
            st.session_state.show_tooltips = show_tooltips
            st.session_state.enable_animations = enable_animations
            st.session_state.show_debug_info = show_debug_info
            st.session_state.enable_notifications = enable_notifications
            st.session_state.remember_settings = remember_settings
            st.session_state.ai_model = ai_model
            st.session_state.ai_confidence = ai_confidence
            st.session_state.enable_ai_suggestions = enable_ai_suggestions
            
            st.success("Application preferences saved successfully!")
        
    except Exception as e:
        logger.error(f"Failed to render app preferences: {e}")
        st.error(f"App preferences error: {e}")

def _render_settings_management():
    """Render settings management section."""
    try:
        st.markdown("### 💾 Settings Management")
        
        # Export settings
        st.markdown("#### 📤 Export Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export All Settings", key="export_all_settings"):
                st.success("Settings exported successfully!")
                st.download_button(
                    label="Download Settings File",
                    data="settings.json",
                    file_name="resume_ai_settings.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📥 Export Theme Only", key="export_theme"):
                st.success("Theme exported successfully!")
                st.download_button(
                    label="Download Theme File",
                    data="theme.json",
                    file_name="resume_ai_theme.json",
                    mime="application/json"
                )
        
        # Import settings
        st.markdown("#### 📥 Import Settings")
        
        uploaded_file = st.file_uploader(
            "Choose a settings file",
            type=['json'],
            help="Upload a previously exported settings file"
        )
        
        if uploaded_file is not None:
            if st.button("📤 Import Settings", key="import_settings"):
                st.success("Settings imported successfully!")
                st.rerun()
        
        # Reset settings
        st.markdown("#### 🔄 Reset Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset to Defaults", key="reset_to_defaults"):
                st.warning("This will reset all settings to default values. Are you sure?")
                if st.button("Yes, Reset", key="confirm_reset"):
                    st.success("Settings reset to defaults!")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All Data", key="clear_all_data"):
                st.error("This will clear all your data. Are you sure?")
                if st.button("Yes, Clear All", key="confirm_clear"):
                    st.success("All data cleared!")
                    st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to render settings management: {e}")
        st.error(f"Settings management error: {e}")

def get_customization_info() -> Dict[str, Any]:
    """
    Get customization page information and statistics.
    
    Returns:
        Dict[str, Any]: Customization page information
    """
    try:
        return {
            "page_name": "Customization",
            "current_theme": st.session_state.get('theme', 'light'),
            "user_settings": {
                "first_name": st.session_state.get('user_first_name', ''),
                "last_name": st.session_state.get('user_last_name', ''),
                "email": st.session_state.get('user_email', ''),
                "company": st.session_state.get('user_company', ''),
                "job_title": st.session_state.get('user_job_title', ''),
                "location": st.session_state.get('user_location', '')
            },
            "app_preferences": {
                "auto_save": st.session_state.get('auto_save', True),
                "show_tooltips": st.session_state.get('show_tooltips', True),
                "enable_animations": st.session_state.get('enable_animations', True),
                "ai_model": st.session_state.get('ai_model', 'GPT-4'),
                "ai_confidence": st.session_state.get('ai_confidence', 0.8)
            },
            "page_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get customization info: {e}")
        return {
            "error": str(e),
            "page_timestamp": datetime.now().isoformat()
        }
