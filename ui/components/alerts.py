"""
Alerts Component for Resume/CV AI Application
Alert and notification components.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class Alerts:
    """Alerts component for notifications and messages."""
    
    def __init__(self):
        """Initialize alerts component."""
        pass
    
    def show_success(self, message: str, key: str = "success_alert") -> None:
        """
        Show a success alert.
        
        Args:
            message: Success message
            key: Unique key for the widget
        """
        try:
            st.success(message, icon="✅")
            logger.info(f"Success alert shown: {message}")
        except Exception as e:
            logger.error(f"Error showing success alert: {e}")
    
    def show_error(self, message: str, key: str = "error_alert") -> None:
        """
        Show an error alert.
        
        Args:
            message: Error message
            key: Unique key for the widget
        """
        try:
            st.error(message, icon="❌")
            logger.error(f"Error alert shown: {message}")
        except Exception as e:
            logger.error(f"Error showing error alert: {e}")
    
    def show_warning(self, message: str, key: str = "warning_alert") -> None:
        """
        Show a warning alert.
        
        Args:
            message: Warning message
            key: Unique key for the widget
        """
        try:
            st.warning(message, icon="⚠️")
            logger.warning(f"Warning alert shown: {message}")
        except Exception as e:
            logger.error(f"Error showing warning alert: {e}")
    
    def show_info(self, message: str, key: str = "info_alert") -> None:
        """
        Show an info alert.
        
        Args:
            message: Info message
            key: Unique key for the widget
        """
        try:
            st.info(message, icon="ℹ️")
            logger.info(f"Info alert shown: {message}")
        except Exception as e:
            logger.error(f"Error showing info alert: {e}")
    
    def show_custom_alert(self, 
                         message: str,
                         alert_type: str = "info",
                         icon: str = "ℹ️",
                         key: str = "custom_alert") -> None:
        """
        Show a custom alert.
        
        Args:
            message: Alert message
            alert_type: Type of alert (success, error, warning, info)
            icon: Icon to display
            key: Unique key for the widget
        """
        try:
            if alert_type == "success":
                st.success(f"{icon} {message}")
            elif alert_type == "error":
                st.error(f"{icon} {message}")
            elif alert_type == "warning":
                st.warning(f"{icon} {message}")
            else:
                st.info(f"{icon} {message}")
            
            logger.debug(f"Custom alert shown: {alert_type} - {message}")
        except Exception as e:
            logger.error(f"Error showing custom alert: {e}")
