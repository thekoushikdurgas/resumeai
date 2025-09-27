"""
Job Matching Tab for Resume/CV AI Application
Handles job matching functionality.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from .base_tab import BaseTab

class JobMatchingTab(BaseTab):
    """Tab for job matching functionality."""
    
    def __init__(self):
        super().__init__("Job Matching", "Match your resume with job descriptions")
    
    def render(self):
        """Render the job matching tab."""
        st.title("🎯 Job Matching")
        st.write("This tab provides job matching functionality.")
        st.info("Please use the main navigation to access job matching features.")
