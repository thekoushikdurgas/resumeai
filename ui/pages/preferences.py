"""
Preferences Page for Resume/CV AI Application
Handles user preferences and application settings.

This module provides:
- User preference management
- Application settings configuration
- Theme and appearance customization
- Notification preferences
- Data privacy settings
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
logger = setup_logger("preferences_page")

def render():
    """
    Render the preferences page with comprehensive logging.
    
    This function renders the preferences page including user settings,
    application configuration, and customization options.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering preferences page")
        start_time = time.time()
        
        # Page header
        st.title("⚙️ Preferences")
        st.markdown("Configure your application preferences and settings.")
        
        # General preferences
        _render_general_preferences()
        
        # Appearance preferences
        _render_appearance_preferences()
        
        # Notification preferences
        _render_notification_preferences()
        
        # Privacy preferences
        _render_privacy_preferences()
        
        # Advanced preferences
        _render_advanced_preferences()
        
        # Save preferences
        _render_save_preferences()
        
        rendering_time = time.time() - start_time
        logger.info(f"Preferences page rendered in {rendering_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render preferences page: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        st.error(f"Page rendering error: {e}")

def _render_general_preferences():
    """Render general preferences section."""
    try:
        st.markdown("### 🔧 General Preferences")
        
        # Application settings
        st.markdown("#### 📱 Application Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "Language:",
                ["English", "Spanish", "French", "German", "Chinese", "Japanese"],
                help="Select your preferred language"
            )
            
            timezone = st.selectbox(
                "Timezone:",
                ["UTC", "EST", "PST", "CST", "MST", "GMT", "CET", "JST"],
                help="Select your timezone"
            )
            
            date_format = st.selectbox(
                "Date Format:",
                ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD", "DD-MM-YYYY"],
                help="Select your preferred date format"
            )
        
        with col2:
            currency = st.selectbox(
                "Currency:",
                ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY"],
                help="Select your preferred currency"
            )
            
            units = st.selectbox(
                "Units:",
                ["Metric", "Imperial"],
                help="Select your preferred unit system"
            )
            
            auto_save = st.checkbox(
                "Auto-save changes",
                value=True,
                help="Automatically save your work"
            )
        
        # User interface settings
        st.markdown("#### 🖥️ User Interface Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            show_tooltips = st.checkbox(
                "Show tooltips",
                value=True,
                help="Display helpful tooltips"
            )
            
            enable_animations = st.checkbox(
                "Enable animations",
                value=True,
                help="Enable smooth animations and transitions"
            )
            
            compact_mode = st.checkbox(
                "Compact mode",
                value=False,
                help="Use compact layout for smaller screens"
            )
        
        with col2:
            show_breadcrumbs = st.checkbox(
                "Show breadcrumbs",
                value=True,
                help="Display navigation breadcrumbs"
            )
            
            show_page_numbers = st.checkbox(
                "Show page numbers",
                value=False,
                help="Display page numbers in documents"
            )
            
            confirm_actions = st.checkbox(
                "Confirm destructive actions",
                value=True,
                help="Ask for confirmation before destructive actions"
            )
        
    except Exception as e:
        logger.error(f"Failed to render general preferences: {e}")
        st.error(f"General preferences error: {e}")

def _render_appearance_preferences():
    """Render appearance preferences section."""
    try:
        st.markdown("### 🎨 Appearance Preferences")
        
        # Theme settings
        st.markdown("#### 🌓 Theme Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "Theme:",
                ["Light", "Dark", "Auto"],
                help="Select your preferred theme"
            )
            
            accent_color = st.color_picker(
                "Accent Color:",
                value="#007bff",
                help="Choose your accent color"
            )
            
            font_size = st.selectbox(
                "Font Size:",
                ["Small", "Medium", "Large"],
                help="Select font size"
            )
        
        with col2:
            font_family = st.selectbox(
                "Font Family:",
                ["System Default", "Arial", "Times New Roman", "Calibri", "Georgia"],
                help="Select font family"
            )
            
            sidebar_width = st.slider(
                "Sidebar Width:",
                min_value=200,
                max_value=400,
                value=300,
                step=50,
                help="Adjust sidebar width"
            )
        
        # Layout settings
        st.markdown("#### 📐 Layout Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            content_width = st.selectbox(
                "Content Width:",
                ["Narrow", "Medium", "Wide", "Full"],
                help="Choose content area width"
            )
            
            show_page_titles = st.checkbox(
                "Show page titles",
                value=True,
                help="Display page titles in content area"
            )
        
        with col2:
            sidebar_position = st.selectbox(
                "Sidebar Position:",
                ["Left", "Right"],
                help="Choose sidebar position"
            )
            
            show_status_bar = st.checkbox(
                "Show status bar",
                value=True,
                help="Display status bar at bottom"
            )
        
    except Exception as e:
        logger.error(f"Failed to render appearance preferences: {e}")
        st.error(f"Appearance preferences error: {e}")

def _render_notification_preferences():
    """Render notification preferences section."""
    try:
        st.markdown("### 🔔 Notification Preferences")
        
        # Notification settings
        st.markdown("#### 📢 Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            enable_notifications = st.checkbox(
                "Enable notifications",
                value=True,
                help="Enable system notifications"
            )
            
            email_notifications = st.checkbox(
                "Email notifications",
                value=False,
                help="Send notifications via email"
            )
            
            browser_notifications = st.checkbox(
                "Browser notifications",
                value=True,
                help="Show browser notifications"
            )
        
        with col2:
            notification_sound = st.checkbox(
                "Notification sound",
                value=False,
                help="Play sound for notifications"
            )
            
            desktop_notifications = st.checkbox(
                "Desktop notifications",
                value=False,
                help="Show desktop notifications"
            )
        
        # Notification types
        st.markdown("#### 📋 Notification Types")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notify_analysis_complete = st.checkbox(
                "Analysis complete",
                value=True,
                help="Notify when resume analysis is complete"
            )
            
            notify_export_ready = st.checkbox(
                "Export ready",
                value=True,
                help="Notify when export is ready"
            )
            
            notify_import_complete = st.checkbox(
                "Import complete",
                value=True,
                help="Notify when data import is complete"
            )
        
        with col2:
            notify_updates = st.checkbox(
                "Application updates",
                value=False,
                help="Notify about application updates"
            )
            
            notify_errors = st.checkbox(
                "Error notifications",
                value=True,
                help="Notify about errors and issues"
            )
            
            notify_reminders = st.checkbox(
                "Reminders",
                value=False,
                help="Send reminder notifications"
            )
        
        # Notification frequency
        st.markdown("#### ⏰ Notification Frequency")
        
        notification_frequency = st.selectbox(
            "How often to send notifications:",
            ["Immediate", "Every 5 minutes", "Every 15 minutes", "Every hour", "Daily"],
            help="Choose notification frequency"
        )
        
    except Exception as e:
        logger.error(f"Failed to render notification preferences: {e}")
        st.error(f"Notification preferences error: {e}")

def _render_privacy_preferences():
    """Render privacy preferences section."""
    try:
        st.markdown("### 🔒 Privacy Preferences")
        
        # Data collection
        st.markdown("#### 📊 Data Collection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            collect_usage_data = st.checkbox(
                "Collect usage data",
                value=True,
                help="Help improve the app by sharing anonymous usage data"
            )
            
            collect_performance_data = st.checkbox(
                "Collect performance data",
                value=True,
                help="Share performance metrics to improve app speed"
            )
            
            collect_error_reports = st.checkbox(
                "Collect error reports",
                value=True,
                help="Automatically send error reports for debugging"
            )
        
        with col2:
            collect_feature_usage = st.checkbox(
                "Collect feature usage",
                value=False,
                help="Track which features you use most"
            )
            
            allow_analytics = st.checkbox(
                "Allow analytics",
                value=True,
                help="Enable analytics tracking"
            )
        
        # Data retention
        st.markdown("#### 💾 Data Retention")
        
        data_retention_period = st.selectbox(
            "Keep data for:",
            ["30 days", "90 days", "1 year", "Forever"],
            help="How long to keep your data"
        )
        
        auto_delete_temp_files = st.checkbox(
            "Auto-delete temporary files",
            value=True,
            help="Automatically delete temporary files"
        )
        
        # Privacy controls
        st.markdown("#### 🛡️ Privacy Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            anonymize_data = st.checkbox(
                "Anonymize data",
                value=True,
                help="Remove personal identifiers from collected data"
            )
            
            encrypt_local_data = st.checkbox(
                "Encrypt local data",
                value=True,
                help="Encrypt data stored locally"
            )
        
        with col2:
            share_with_third_parties = st.checkbox(
                "Share with third parties",
                value=False,
                help="Allow sharing data with third-party services"
            )
            
            allow_data_export = st.checkbox(
                "Allow data export",
                value=True,
                help="Allow exporting your data"
            )
        
    except Exception as e:
        logger.error(f"Failed to render privacy preferences: {e}")
        st.error(f"Privacy preferences error: {e}")

def _render_advanced_preferences():
    """Render advanced preferences section."""
    try:
        st.markdown("### ⚡ Advanced Preferences")
        
        # Performance settings
        st.markdown("#### 🚀 Performance Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cache_size = st.slider(
                "Cache Size (MB):",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Maximum cache size in megabytes"
            )
            
            max_concurrent_operations = st.number_input(
                "Max Concurrent Operations:",
                min_value=1,
                max_value=10,
                value=3,
                help="Maximum number of concurrent operations"
            )
        
        with col2:
            enable_caching = st.checkbox(
                "Enable caching",
                value=True,
                help="Enable data caching for better performance"
            )
            
            preload_data = st.checkbox(
                "Preload data",
                value=False,
                help="Preload frequently used data"
            )
        
        # Debug settings
        st.markdown("#### 🐛 Debug Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            debug_mode = st.checkbox(
                "Debug mode",
                value=False,
                help="Enable debug mode for troubleshooting"
            )
            
            verbose_logging = st.checkbox(
                "Verbose logging",
                value=False,
                help="Enable detailed logging"
            )
        
        with col2:
            show_debug_info = st.checkbox(
                "Show debug info",
                value=False,
                help="Display debug information in UI"
            )
            
            log_to_file = st.checkbox(
                "Log to file",
                value=True,
                help="Save logs to file"
            )
        
        # API settings
        st.markdown("#### 🔌 API Settings")
        
        api_timeout = st.number_input(
            "API Timeout (seconds):",
            min_value=5,
            max_value=300,
            value=30,
            help="Timeout for API requests"
        )
        
        retry_failed_requests = st.checkbox(
            "Retry failed requests",
            value=True,
            help="Automatically retry failed API requests"
        )
        
        max_retries = st.number_input(
            "Max Retries:",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum number of retry attempts"
        )
        
    except Exception as e:
        logger.error(f"Failed to render advanced preferences: {e}")
        st.error(f"Advanced preferences error: {e}")

def _render_save_preferences():
    """Render save preferences section."""
    try:
        st.markdown("### 💾 Save Preferences")
        
        # Save options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save All Preferences", type="primary", use_container_width=True):
                _save_preferences()
        
        with col2:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                _reset_preferences()
        
        with col3:
            if st.button("📥 Export Preferences", use_container_width=True):
                _export_preferences()
        
        # Import preferences
        st.markdown("#### 📤 Import Preferences")
        
        uploaded_file = st.file_uploader(
            "Choose preferences file:",
            type=['json'],
            help="Upload a previously exported preferences file"
        )
        
        if uploaded_file is not None:
            if st.button("📥 Import Preferences"):
                _import_preferences(uploaded_file)
        
    except Exception as e:
        logger.error(f"Failed to render save preferences: {e}")
        st.error(f"Save preferences error: {e}")

def _save_preferences():
    """Save all preferences."""
    try:
        logger.info("Saving user preferences")
        
        # Collect all preferences
        preferences = {
            'language': 'English',  # Get from UI
            'timezone': 'UTC',
            'date_format': 'MM/DD/YYYY',
            'currency': 'USD',
            'units': 'Metric',
            'auto_save': True,
            'theme': 'Light',
            'accent_color': '#007bff',
            'font_size': 'Medium',
            'enable_notifications': True,
            'collect_usage_data': True,
            'debug_mode': False,
            'cache_size': 100,
            'api_timeout': 30,
            'saved_at': datetime.now().isoformat()
        }
        
        # Store in session state
        st.session_state.preferences = preferences
        
        st.success("🎉 Preferences saved successfully!")
        
    except Exception as e:
        logger.error(f"Failed to save preferences: {e}")
        st.error(f"Failed to save preferences: {e}")

def _reset_preferences():
    """Reset preferences to defaults."""
    try:
        logger.info("Resetting preferences to defaults")
        
        # Reset to default values
        default_preferences = {
            'language': 'English',
            'timezone': 'UTC',
            'date_format': 'MM/DD/YYYY',
            'currency': 'USD',
            'units': 'Metric',
            'auto_save': True,
            'theme': 'Light',
            'accent_color': '#007bff',
            'font_size': 'Medium',
            'enable_notifications': True,
            'collect_usage_data': True,
            'debug_mode': False,
            'cache_size': 100,
            'api_timeout': 30,
            'reset_at': datetime.now().isoformat()
        }
        
        st.session_state.preferences = default_preferences
        
        st.success("🔄 Preferences reset to defaults!")
        st.rerun()
        
    except Exception as e:
        logger.error(f"Failed to reset preferences: {e}")
        st.error(f"Failed to reset preferences: {e}")

def _export_preferences():
    """Export preferences to file."""
    try:
        logger.info("Exporting preferences")
        
        preferences = st.session_state.get('preferences', {})
        
        import json
        preferences_json = json.dumps(preferences, indent=2)
        
        st.download_button(
            label="📥 Download Preferences",
            data=preferences_json,
            file_name="preferences.json",
            mime="application/json"
        )
        
        st.success("Preferences exported successfully!")
        
    except Exception as e:
        logger.error(f"Failed to export preferences: {e}")
        st.error(f"Failed to export preferences: {e}")

def _import_preferences(uploaded_file):
    """Import preferences from file."""
    try:
        logger.info("Importing preferences from file")
        
        import json
        preferences = json.load(uploaded_file)
        
        # Validate preferences
        required_keys = ['language', 'timezone', 'theme']
        if all(key in preferences for key in required_keys):
            st.session_state.preferences = preferences
            st.success("🎉 Preferences imported successfully!")
            st.rerun()
        else:
            st.error("Invalid preferences file format")
        
    except Exception as e:
        logger.error(f"Failed to import preferences: {e}")
        st.error(f"Failed to import preferences: {e}")

def get_preferences_info() -> Dict[str, Any]:
    """
    Get preferences page information and statistics.
    
    Returns:
        Dict[str, Any]: Preferences page information
    """
    try:
        preferences = st.session_state.get('preferences', {})
        return {
            "page_name": "Preferences",
            "preferences_saved": len(preferences) > 0,
            "preferences_count": len(preferences),
            "last_saved": preferences.get('saved_at', 'Never'),
            "page_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get preferences info: {e}")
        return {
            "error": str(e),
            "page_timestamp": datetime.now().isoformat()
        }
