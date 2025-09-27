"""
Modals Component for Resume/CV AI Application
Modal dialog components for user interactions.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)

class Modals:
    """Modals component for dialog boxes and overlays."""
    
    def __init__(self):
        """Initialize modals component."""
        pass
    
    def render_confirmation_modal(self, 
                                 title: str,
                                 message: str,
                                 confirm_text: str = "Confirm",
                                 cancel_text: str = "Cancel",
                                 key: str = "confirmation_modal") -> bool:
        """
        Render a confirmation modal.
        
        Args:
            title: Modal title
            message: Confirmation message
            confirm_text: Confirm button text
            cancel_text: Cancel button text
            key: Unique key for the widget
            
        Returns:
            True if confirmed, False otherwise
        """
        try:
            # Use session state to track modal state
            if f"{key}_show" not in st.session_state:
                st.session_state[f"{key}_show"] = False
            
            # Show modal if requested
            if st.session_state[f"{key}_show"]:
                with st.container():
                    st.markdown("---")
                    st.subheader(title)
                    st.write(message)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(confirm_text, key=f"{key}_confirm"):
                            st.session_state[f"{key}_show"] = False
                            st.session_state[f"{key}_result"] = True
                            st.rerun()
                    
                    with col2:
                        if st.button(cancel_text, key=f"{key}_cancel"):
                            st.session_state[f"{key}_show"] = False
                            st.session_state[f"{key}_result"] = False
                            st.rerun()
                    st.markdown("---")
            
            # Check for result
            if f"{key}_result" in st.session_state:
                result = st.session_state[f"{key}_result"]
                del st.session_state[f"{key}_result"]
                return result
            
            return False
        except Exception as e:
            logger.error(f"Error rendering confirmation modal: {e}")
            st.error(f"Error creating confirmation modal: {e}")
            return False
    
    def show_confirmation_modal(self, key: str = "confirmation_modal") -> None:
        """
        Show a confirmation modal.
        
        Args:
            key: Unique key for the widget
        """
        try:
            st.session_state[f"{key}_show"] = True
            logger.debug(f"Confirmation modal shown: {key}")
        except Exception as e:
            logger.error(f"Error showing confirmation modal: {e}")
    
    def render_info_modal(self, 
                         title: str,
                         content: str,
                         key: str = "info_modal") -> None:
        """
        Render an info modal.
        
        Args:
            title: Modal title
            content: Modal content
            key: Unique key for the widget
        """
        try:
            # Use session state to track modal state
            if f"{key}_show" not in st.session_state:
                st.session_state[f"{key}_show"] = False
            
            # Show modal if requested
            if st.session_state[f"{key}_show"]:
                with st.container():
                    st.markdown("---")
                    st.subheader(title)
                    st.markdown(content)
                    
                    if st.button("Close", key=f"{key}_close"):
                        st.session_state[f"{key}_show"] = False
                        st.rerun()
                    st.markdown("---")
            
            logger.debug(f"Info modal rendered: {title}")
        except Exception as e:
            logger.error(f"Error rendering info modal: {e}")
            st.error(f"Error creating info modal: {e}")
    
    def show_info_modal(self, key: str = "info_modal") -> None:
        """
        Show an info modal.
        
        Args:
            key: Unique key for the widget
        """
        try:
            st.session_state[f"{key}_show"] = True
            logger.debug(f"Info modal shown: {key}")
        except Exception as e:
            logger.error(f"Error showing info modal: {e}")
