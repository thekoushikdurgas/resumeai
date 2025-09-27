"""
Forms Component for Resume/CV AI Application
Form input components and validation.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)

class Forms:
    """Forms component for user input and validation."""
    
    def __init__(self):
        """Initialize forms component."""
        pass
    
    def render_text_input(self, 
                         label: str,
                         value: str = "",
                         help_text: str = "",
                         required: bool = False,
                         key: str = "text_input") -> str:
        """
        Render a text input field.
        
        Args:
            label: Field label
            value: Default value
            help_text: Help text
            required: Whether field is required
            key: Unique key for the widget
            
        Returns:
            Entered text value
        """
        try:
            if required and not value:
                value = st.text_input(
                    label=f"{label} *",
                    value=value,
                    help=help_text,
                    key=key
                )
            else:
                value = st.text_input(
                    label=label,
                    value=value,
                    help=help_text,
                    key=key
                )
            
            logger.debug(f"Text input rendered: {label}")
            return value
        except Exception as e:
            logger.error(f"Error rendering text input: {e}")
            st.error(f"Error creating text input: {e}")
            return ""
    
    def render_selectbox(self, 
                        label: str,
                        options: List[str],
                        index: int = 0,
                        help_text: str = "",
                        key: str = "selectbox") -> str:
        """
        Render a select box.
        
        Args:
            label: Field label
            options: List of options
            index: Default selected index
            help_text: Help text
            key: Unique key for the widget
            
        Returns:
            Selected option
        """
        try:
            if not options:
                st.warning("No options available")
                return ""
            
            selected = st.selectbox(
                label=label,
                options=options,
                index=index,
                help=help_text,
                key=key
            )
            
            logger.debug(f"Selectbox rendered: {label}")
            return selected
        except Exception as e:
            logger.error(f"Error rendering selectbox: {e}")
            st.error(f"Error creating selectbox: {e}")
            return ""
    
    def render_multiselect(self, 
                          label: str,
                          options: List[str],
                          default: List[str] = None,
                          help_text: str = "",
                          key: str = "multiselect") -> List[str]:
        """
        Render a multi-select box.
        
        Args:
            label: Field label
            options: List of options
            default: Default selected options
            help_text: Help text
            key: Unique key for the widget
            
        Returns:
            List of selected options
        """
        try:
            if default is None:
                default = []
            
            selected = st.multiselect(
                label=label,
                options=options,
                default=default,
                help=help_text,
                key=key
            )
            
            logger.debug(f"Multiselect rendered: {label}")
            return selected
        except Exception as e:
            logger.error(f"Error rendering multiselect: {e}")
            st.error(f"Error creating multiselect: {e}")
            return []
