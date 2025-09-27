"""
Resume Preview Component for Resume/CV AI Application
Resume preview and display components.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ResumePreview:
    """Resume preview component for displaying resume content."""
    
    def __init__(self):
        """Initialize resume preview component."""
        pass
    
    def render_resume_summary(self, 
                             resume_data: Dict[str, Any],
                             key: str = "resume_summary") -> None:
        """
        Render a resume summary.
        
        Args:
            resume_data: Resume data dictionary
            key: Unique key for the widget
        """
        try:
            if not resume_data:
                st.info("No resume data available")
                return
            
            st.subheader("📄 Resume Summary")
            
            # Basic info
            if "contact_info" in resume_data:
                contact = resume_data["contact_info"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {contact.get('name', 'N/A')}")
                    st.write(f"**Email:** {contact.get('email', 'N/A')}")
                with col2:
                    st.write(f"**Phone:** {contact.get('phone', 'N/A')}")
                    st.write(f"**Location:** {contact.get('location', 'N/A')}")
            
            # Experience
            if "experience" in resume_data:
                st.subheader("💼 Experience")
                for exp in resume_data["experience"]:
                    st.write(f"**{exp.get('title', 'N/A')}** at {exp.get('company', 'N/A')}")
                    st.write(f"*{exp.get('duration', 'N/A')}*")
                    if exp.get('description'):
                        st.write(exp['description'])
                    st.write("---")
            
            # Education
            if "education" in resume_data:
                st.subheader("🎓 Education")
                for edu in resume_data["education"]:
                    st.write(f"**{edu.get('degree', 'N/A')}** - {edu.get('institution', 'N/A')}")
                    st.write(f"*{edu.get('year', 'N/A')}*")
                    st.write("---")
            
            # Skills
            if "skills" in resume_data:
                st.subheader("🛠️ Skills")
                skills = resume_data["skills"]
                if isinstance(skills, list):
                    st.write(", ".join(skills))
                else:
                    st.write(str(skills))
            
            logger.debug("Resume summary rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering resume summary: {e}")
            st.error(f"Error displaying resume summary: {e}")
    
    def render_analysis_results(self, 
                               analysis_data: Dict[str, Any],
                               key: str = "analysis_results") -> None:
        """
        Render analysis results.
        
        Args:
            analysis_data: Analysis results dictionary
            key: Unique key for the widget
        """
        try:
            if not analysis_data:
                st.info("No analysis results available")
                return
            
            st.subheader("📊 Analysis Results")
            
            # Overall score
            if "overall_score" in analysis_data:
                score = analysis_data["overall_score"]
                st.metric("Overall Score", f"{score:.1f}/100")
            
            # Detailed scores
            if "scores" in analysis_data:
                scores = analysis_data["scores"]
                for category, score in scores.items():
                    st.metric(category.replace("_", " ").title(), f"{score:.1f}/100")
            
            # Recommendations
            if "recommendations" in analysis_data:
                st.subheader("💡 Recommendations")
                for rec in analysis_data["recommendations"]:
                    st.write(f"• {rec}")
            
            logger.debug("Analysis results rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering analysis results: {e}")
            st.error(f"Error displaying analysis results: {e}")
