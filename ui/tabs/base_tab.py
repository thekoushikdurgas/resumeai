"""
Base Tab Class for Resume/CV AI Application
Provides common functionality for all tabs.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
from typing import Dict, Any, Optional
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("base_tab")

class BaseTab:
    """
    Base tab class with common functionality.
    
    This class provides common functionality that all tabs can inherit from,
    including error handling, logging, and basic rendering capabilities.
    """
    
    def __init__(self, title: str, description: str = ""):
        """
        Initialize the base tab.
        
        Args:
            title (str): Tab title
            description (str): Tab description
        """
        self.title = title
        self.description = description
        logger.debug(f"Initialized tab: {title}")
    
    def render(self):
        """
        Render the tab content.
        
        This method should be overridden by subclasses to provide
        specific tab functionality.
        """
        try:
            st.title(self.title)
            if self.description:
                st.write(self.description)
            
            # Default content
            st.info("This tab is under development. Please use the main navigation.")
            
        except Exception as e:
            logger.error(f"Failed to render tab '{self.title}': {e}")
            st.error(f"Error rendering {self.title}: {e}")
    
    def get_tab_info(self) -> Dict[str, Any]:
        """
        Get tab information.
        
        Returns:
            Dict[str, Any]: Tab information
        """
        return {
            "title": self.title,
            "description": self.description,
            "type": self.__class__.__name__
        }
