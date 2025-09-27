"""
Cards Component for Resume/CV AI Application
Card-based UI components for content display.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class Cards:
    """Cards component for displaying content in card format."""
    
    def __init__(self):
        """Initialize cards component."""
        pass
    
    def render_info_card(self, 
                        title: str,
                        content: str,
                        icon: str = "📄",
                        key: str = "info_card") -> None:
        """
        Render an info card.
        
        Args:
            title: Card title
            content: Card content
            icon: Icon to display
            key: Unique key for the widget
        """
        try:
            with st.container():
                st.markdown(f"### {icon} {title}")
                st.markdown(content)
                st.markdown("---")
            
            logger.debug(f"Info card rendered: {title}")
        except Exception as e:
            logger.error(f"Error rendering info card: {e}")
            st.error(f"Error creating info card: {e}")
    
    def render_metric_card(self, 
                          title: str,
                          value: str,
                          delta: Optional[str] = None,
                          icon: str = "📊",
                          key: str = "metric_card") -> None:
        """
        Render a metric card.
        
        Args:
            title: Card title
            value: Metric value
            delta: Change indicator
            icon: Icon to display
            key: Unique key for the widget
        """
        try:
            with st.container():
                st.markdown(f"### {icon} {title}")
                st.metric(
                    label="",
                    value=value,
                    delta=delta
                )
                st.markdown("---")
            
            logger.debug(f"Metric card rendered: {title}")
        except Exception as e:
            logger.error(f"Error rendering metric card: {e}")
            st.error(f"Error creating metric card: {e}")
    
    def render_card_grid(self, 
                        cards: List[Dict[str, Any]],
                        columns: int = 3,
                        key: str = "card_grid") -> None:
        """
        Render a grid of cards.
        
        Args:
            cards: List of card configurations
            columns: Number of columns
            key: Unique key for the widget
        """
        try:
            if not cards:
                st.info("No cards to display")
                return
            
            # Create columns
            cols = st.columns(columns)
            
            # Render cards
            for i, card in enumerate(cards):
                with cols[i % columns]:
                    if card.get("type") == "metric":
                        self.render_metric_card(
                            title=card.get("title", ""),
                            value=card.get("value", ""),
                            delta=card.get("delta"),
                            icon=card.get("icon", "📊"),
                            key=f"{key}_{i}"
                        )
                    else:
                        self.render_info_card(
                            title=card.get("title", ""),
                            content=card.get("content", ""),
                            icon=card.get("icon", "📄"),
                            key=f"{key}_{i}"
                        )
            
            logger.debug(f"Card grid rendered with {len(cards)} cards")
        except Exception as e:
            logger.error(f"Error rendering card grid: {e}")
            st.error(f"Error creating card grid: {e}")
