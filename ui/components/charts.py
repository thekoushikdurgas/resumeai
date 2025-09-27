"""
Charts Component for Resume/CV AI Application
Data visualization components using Plotly.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Charts:
    """Charts component for data visualization."""
    
    def __init__(self):
        """Initialize charts component."""
        pass
    
    def render_bar_chart(self, 
                        data: Dict[str, float],
                        title: str = "Bar Chart",
                        x_label: str = "Category",
                        y_label: str = "Value",
                        key: str = "bar_chart") -> None:
        """
        Render a bar chart.
        
        Args:
            data: Dictionary of category to value
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            key: Unique key for the widget
        """
        try:
            if not data:
                st.info("No data available for chart")
                return
            
            # Create DataFrame
            df = pd.DataFrame(list(data.items()), columns=[x_label, y_label])
            
            # Create bar chart
            fig = px.bar(
                df, 
                x=x_label, 
                y=y_label,
                title=title,
                labels={x_label: x_label, y_label: y_label}
            )
            
            # Update layout
            fig.update_layout(
                xaxis_tickangle=-45,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key=key)
            logger.debug(f"Rendered bar chart: {title}")
        except Exception as e:
            logger.error(f"Error rendering bar chart: {e}")
            st.error(f"Error creating bar chart: {e}")
    
    def render_pie_chart(self, 
                        data: Dict[str, float],
                        title: str = "Pie Chart",
                        key: str = "pie_chart") -> None:
        """
        Render a pie chart.
        
        Args:
            data: Dictionary of label to value
            title: Chart title
            key: Unique key for the widget
        """
        try:
            if not data:
                st.info("No data available for chart")
                return
            
            # Create pie chart
            fig = px.pie(
                values=list(data.values()),
                names=list(data.keys()),
                title=title
            )
            
            st.plotly_chart(fig, use_container_width=True, key=key)
            logger.debug(f"Rendered pie chart: {title}")
        except Exception as e:
            logger.error(f"Error rendering pie chart: {e}")
            st.error(f"Error creating pie chart: {e}")
    
    def render_line_chart(self, 
                         data: Dict[str, List[float]],
                         title: str = "Line Chart",
                         x_label: str = "X",
                         y_label: str = "Y",
                         key: str = "line_chart") -> None:
        """
        Render a line chart.
        
        Args:
            data: Dictionary of series name to list of values
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            key: Unique key for the widget
        """
        try:
            if not data:
                st.info("No data available for chart")
                return
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create line chart
            fig = px.line(
                df,
                title=title,
                labels={"index": x_label, "value": y_label}
            )
            
            st.plotly_chart(fig, use_container_width=True, key=key)
            logger.debug(f"Rendered line chart: {title}")
        except Exception as e:
            logger.error(f"Error rendering line chart: {e}")
            st.error(f"Error creating line chart: {e}")
