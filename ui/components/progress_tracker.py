"""
Progress Tracker Component for Resume/CV AI Application
Displays progress bars and status indicators.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Progress tracking component for long-running operations."""
    
    def __init__(self):
        """Initialize progress tracker."""
        self.progress_bar = None
        self.status_text = None
    
    def start(self, 
              total_steps: int = 100,
              status_text: str = "Processing...",
              key: str = "progress_tracker") -> None:
        """
        Start progress tracking.
        
        Args:
            total_steps: Total number of steps
            status_text: Initial status text
            key: Unique key for the widget
        """
        try:
            self.progress_bar = st.progress(0, key=f"{key}_bar")
            self.status_text = st.empty()
            self.status_text.text(status_text)
            logger.info(f"Progress tracking started: {status_text}")
        except Exception as e:
            logger.error(f"Error starting progress tracker: {e}")
    
    def update(self, 
               step: int,
               status_text: Optional[str] = None,
               key: str = "progress_tracker") -> None:
        """
        Update progress.
        
        Args:
            step: Current step (0-100)
            status_text: New status text
            key: Unique key for the widget
        """
        try:
            if self.progress_bar is not None:
                self.progress_bar.progress(step)
            
            if status_text and self.status_text is not None:
                self.status_text.text(status_text)
                
            logger.debug(f"Progress updated: {step}% - {status_text}")
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
    
    def complete(self, 
                 status_text: str = "Complete!",
                 key: str = "progress_tracker") -> None:
        """
        Mark progress as complete.
        
        Args:
            status_text: Final status text
            key: Unique key for the widget
        """
        try:
            if self.progress_bar is not None:
                self.progress_bar.progress(100)
            
            if self.status_text is not None:
                self.status_text.text(status_text)
                
            logger.info(f"Progress completed: {status_text}")
        except Exception as e:
            logger.error(f"Error completing progress: {e}")
    
    def clear(self, key: str = "progress_tracker") -> None:
        """
        Clear progress display.
        
        Args:
            key: Unique key for the widget
        """
        try:
            if self.progress_bar is not None:
                self.progress_bar.empty()
            if self.status_text is not None:
                self.status_text.empty()
            logger.debug("Progress display cleared")
        except Exception as e:
            logger.error(f"Error clearing progress: {e}")
