"""
ATS Checker Tab for Resume/CV AI Application
Handles ATS checking functionality.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from .base_tab import BaseTab

class ATSCheckerTab(BaseTab):
    """Tab for ATS checking functionality."""
    
    def __init__(self):
        super().__init__("ATS Checker", "Check ATS compatibility")
    
    def render(self):
        """Render the ATS checker tab."""
        st.title("📊 ATS Checker")
        st.write("This tab provides ATS checking functionality.")
        st.info("Please use the main navigation to access ATS checker features.")
