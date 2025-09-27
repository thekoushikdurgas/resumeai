"""
Metrics Display Component for Resume/CV AI Application
Displays key metrics and statistics.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class MetricsDisplay:
    """Metrics display component for showing key statistics."""
    
    def __init__(self):
        """Initialize metrics display."""
        pass
    
    def render_metrics(self, 
                      metrics: Dict[str, Any],
                      columns: int = 3,
                      key: str = "metrics_display") -> None:
        """
        Render metrics in columns.
        
        Args:
            metrics: Dictionary of metric name to value
            columns: Number of columns to display
            key: Unique key for the widget
        """
        try:
            if not metrics:
                st.info("No metrics available")
                return
            
            # Create columns
            cols = st.columns(columns)
            
            # Display metrics
            for i, (name, value) in enumerate(metrics.items()):
                with cols[i % columns]:
                    st.metric(
                        label=name,
                        value=value,
                        key=f"{key}_{i}"
                    )
            
            logger.debug(f"Displayed {len(metrics)} metrics in {columns} columns")
        except Exception as e:
            logger.error(f"Error rendering metrics: {e}")
            st.error(f"Error displaying metrics: {e}")
    
    def render_score_card(self, 
                         title: str,
                         score: float,
                         max_score: float = 100.0,
                         description: str = "",
                         key: str = "score_card") -> None:
        """
        Render a score card.
        
        Args:
            title: Card title
            score: Current score
            max_score: Maximum possible score
            description: Description text
            key: Unique key for the widget
        """
        try:
            percentage = (score / max_score) * 100
            
            # Create score card
            with st.container():
                st.subheader(title)
                
                # Score display
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Score", f"{score:.1f}/{max_score}")
                with col2:
                    st.progress(percentage / 100)
                
                if description:
                    st.caption(description)
            
            logger.debug(f"Rendered score card: {title} - {score}/{max_score}")
        except Exception as e:
            logger.error(f"Error rendering score card: {e}")
            st.error(f"Error displaying score card: {e}")
