"""
Data Tables Component for Resume/CV AI Application
Data table display and manipulation components.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class DataTables:
    """Data tables component for displaying tabular data."""
    
    def __init__(self):
        """Initialize data tables component."""
        pass
    
    def render_dataframe(self, 
                        data: pd.DataFrame,
                        title: str = "Data Table",
                        height: int = 400,
                        key: str = "data_table") -> None:
        """
        Render a DataFrame as a table.
        
        Args:
            data: Pandas DataFrame to display
            title: Table title
            height: Table height in pixels
            key: Unique key for the widget
        """
        try:
            if data.empty:
                st.info("No data available")
                return
            
            st.subheader(title)
            st.dataframe(
                data,
                height=height,
                use_container_width=True,
                key=key
            )
            logger.debug(f"Rendered DataFrame with {len(data)} rows")
        except Exception as e:
            logger.error(f"Error rendering DataFrame: {e}")
            st.error(f"Error displaying data table: {e}")
    
    def render_metrics_table(self, 
                            metrics: Dict[str, Any],
                            title: str = "Metrics",
                            key: str = "metrics_table") -> None:
        """
        Render metrics as a table.
        
        Args:
            metrics: Dictionary of metric name to value
            title: Table title
            key: Unique key for the widget
        """
        try:
            if not metrics:
                st.info("No metrics available")
                return
            
            # Convert to DataFrame
            df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
            
            st.subheader(title)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                key=key
            )
            logger.debug(f"Rendered metrics table with {len(metrics)} items")
        except Exception as e:
            logger.error(f"Error rendering metrics table: {e}")
            st.error(f"Error displaying metrics table: {e}")
