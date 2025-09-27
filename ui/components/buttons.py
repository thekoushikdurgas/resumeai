"""
Buttons Component for Resume/CV AI Application
Interactive button components.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)

class Buttons:
    """Buttons component for interactive elements."""
    
    def __init__(self):
        """Initialize buttons component."""
        pass
    
    def render_primary_button(self, 
                             label: str,
                             callback: Optional[Callable] = None,
                             key: str = "primary_button") -> bool:
        """
        Render a primary button.
        
        Args:
            label: Button label
            callback: Function to call when clicked
            key: Unique key for the widget
            
        Returns:
            True if clicked, False otherwise
        """
        try:
            clicked = st.button(
                label,
                type="primary",
                key=key
            )
            
            if clicked and callback:
                callback()
            
            logger.debug(f"Primary button rendered: {label}")
            return clicked
        except Exception as e:
            logger.error(f"Error rendering primary button: {e}")
            st.error(f"Error creating button: {e}")
            return False
    
    def render_secondary_button(self, 
                               label: str,
                               callback: Optional[Callable] = None,
                               key: str = "secondary_button") -> bool:
        """
        Render a secondary button.
        
        Args:
            label: Button label
            callback: Function to call when clicked
            key: Unique key for the widget
            
        Returns:
            True if clicked, False otherwise
        """
        try:
            clicked = st.button(
                label,
                type="secondary",
                key=key
            )
            
            if clicked and callback:
                callback()
            
            logger.debug(f"Secondary button rendered: {label}")
            return clicked
        except Exception as e:
            logger.error(f"Error rendering secondary button: {e}")
            st.error(f"Error creating button: {e}")
            return False
    
    def render_button_group(self, 
                           buttons: List[Dict[str, Any]],
                           key: str = "button_group") -> Optional[str]:
        """
        Render a group of buttons.
        
        Args:
            buttons: List of button configurations
            key: Unique key for the widget
            
        Returns:
            Key of clicked button or None
        """
        try:
            if not buttons:
                st.warning("No buttons to display")
                return None
            
            # Create columns for buttons
            cols = st.columns(len(buttons))
            
            clicked_key = None
            for i, button_config in enumerate(buttons):
                with cols[i]:
                    if st.button(
                        button_config.get("label", f"Button {i}"),
                        type=button_config.get("type", "secondary"),
                        key=f"{key}_{i}"
                    ):
                        clicked_key = button_config.get("key", f"button_{i}")
                        if button_config.get("callback"):
                            button_config["callback"]()
            
            logger.debug(f"Button group rendered with {len(buttons)} buttons")
            return clicked_key
        except Exception as e:
            logger.error(f"Error rendering button group: {e}")
            st.error(f"Error creating button group: {e}")
            return None
