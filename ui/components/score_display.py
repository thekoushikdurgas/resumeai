"""
Score Display Component for Resume/CV AI Application
Score visualization and display components.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ScoreDisplay:
    """Score display component for visualizing scores and metrics."""
    
    def __init__(self):
        """Initialize score display component."""
        pass
    
    def render_radar_chart(self, 
                          scores: Dict[str, float],
                          title: str = "Score Analysis",
                          max_score: float = 100.0,
                          key: str = "radar_chart") -> None:
        """
        Render a radar chart for scores.
        
        Args:
            scores: Dictionary of category to score
            title: Chart title
            max_score: Maximum possible score
            key: Unique key for the widget
        """
        try:
            if not scores:
                st.info("No scores available for radar chart")
                return
            
            # Prepare data
            categories = list(scores.keys())
            values = list(scores.values())
            
            # Create radar chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Scores',
                line_color='rgb(32, 201, 151)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max_score]
                    )),
                showlegend=True,
                title=title
            )
            
            st.plotly_chart(fig, use_container_width=True, key=key)
            logger.debug(f"Radar chart rendered: {title}")
        except Exception as e:
            logger.error(f"Error rendering radar chart: {e}")
            st.error(f"Error creating radar chart: {e}")
    
    def render_score_bar(self, 
                        score: float,
                        max_score: float = 100.0,
                        label: str = "Score",
                        key: str = "score_bar") -> None:
        """
        Render a score bar.
        
        Args:
            score: Current score
            max_score: Maximum possible score
            label: Label for the score
            key: Unique key for the widget
        """
        try:
            percentage = (score / max_score) * 100
            
            st.metric(
                label=label,
                value=f"{score:.1f}/{max_score}",
                delta=None
            )
            
            st.progress(percentage / 100, key=key)
            
            # Color coding
            if percentage >= 80:
                st.success("Excellent!")
            elif percentage >= 60:
                st.info("Good")
            elif percentage >= 40:
                st.warning("Needs improvement")
            else:
                st.error("Requires attention")
            
            logger.debug(f"Score bar rendered: {score}/{max_score}")
        except Exception as e:
            logger.error(f"Error rendering score bar: {e}")
            st.error(f"Error creating score bar: {e}")
    
    def render_score_comparison(self, 
                               scores: Dict[str, Dict[str, float]],
                               title: str = "Score Comparison",
                               key: str = "score_comparison") -> None:
        """
        Render a score comparison chart.
        
        Args:
            scores: Dictionary of category to scores
            title: Chart title
            key: Unique key for the widget
        """
        try:
            if not scores:
                st.info("No scores available for comparison")
                return
            
            # Create comparison chart
            fig = go.Figure()
            
            for category, score_data in scores.items():
                fig.add_trace(go.Bar(
                    name=category,
                    x=list(score_data.keys()),
                    y=list(score_data.values())
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Categories",
                yaxis_title="Scores",
                barmode='group'
            )
            
            st.plotly_chart(fig, use_container_width=True, key=key)
            logger.debug(f"Score comparison rendered: {title}")
        except Exception as e:
            logger.error(f"Error rendering score comparison: {e}")
            st.error(f"Error creating score comparison: {e}")
