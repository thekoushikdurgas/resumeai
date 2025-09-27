"""
Responsive Design Module for Resume/CV AI Application
Responsive design utilities and breakpoints for different screen sizes.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class Responsive:
    """Responsive design component for handling different screen sizes."""
    
    def __init__(self):
        """Initialize responsive component."""
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200,
            'large': 1440
        }
        
        self.responsive_styles = {
            'mobile_first': """
                .mobile-first {
                    width: 100%;
                    padding: 10px;
                }
                @media (min-width: 768px) {
                    .mobile-first {
                        width: 50%;
                        padding: 20px;
                    }
                }
                @media (min-width: 1024px) {
                    .mobile-first {
                        width: 33.33%;
                        padding: 30px;
                    }
                }
            """,
            'flexible_grid': """
                .flexible-grid {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                .flexible-grid > * {
                    flex: 1 1 300px;
                    min-width: 300px;
                }
                @media (max-width: 768px) {
                    .flexible-grid > * {
                        flex: 1 1 100%;
                        min-width: 100%;
                    }
                }
            """,
            'responsive_text': """
                .responsive-text {
                    font-size: 14px;
                }
                @media (min-width: 768px) {
                    .responsive-text {
                        font-size: 16px;
                    }
                }
                @media (min-width: 1024px) {
                    .responsive-text {
                        font-size: 18px;
                    }
                }
            """,
            'responsive_columns': """
                .responsive-columns {
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 20px;
                }
                @media (min-width: 768px) {
                    .responsive-columns {
                        grid-template-columns: 1fr 1fr;
                    }
                }
                @media (min-width: 1024px) {
                    .responsive-columns {
                        grid-template-columns: 1fr 1fr 1fr;
                    }
                }
            """,
            'hide_on_mobile': """
                @media (max-width: 767px) {
                    .hide-on-mobile {
                        display: none !important;
                    }
                }
            """,
            'show_on_mobile': """
                @media (min-width: 768px) {
                    .show-on-mobile {
                        display: none !important;
                    }
                }
            """,
            'responsive_spacing': """
                .responsive-spacing {
                    margin: 10px;
                    padding: 10px;
                }
                @media (min-width: 768px) {
                    .responsive-spacing {
                        margin: 20px;
                        padding: 20px;
                    }
                }
                @media (min-width: 1024px) {
                    .responsive-spacing {
                        margin: 30px;
                        padding: 30px;
                    }
                }
            """
        }
    
    def get_breakpoint_css(self, breakpoint: str) -> str:
        """
        Get CSS for a specific breakpoint.
        
        Args:
            breakpoint: Breakpoint name (mobile, tablet, desktop, large)
            
        Returns:
            CSS string for the breakpoint
        """
        try:
            if breakpoint not in self.breakpoints:
                logger.warning(f"Breakpoint '{breakpoint}' not found")
                return ""
            
            width = self.breakpoints[breakpoint]
            return f"@media (min-width: {width}px)"
        except Exception as e:
            logger.error(f"Error getting breakpoint CSS: {e}")
            return ""
    
    def get_responsive_style(self, style_name: str) -> str:
        """
        Get CSS for a specific responsive style.
        
        Args:
            style_name: Name of the responsive style
            
        Returns:
            CSS string for the style
        """
        try:
            return self.responsive_styles.get(style_name, "")
        except Exception as e:
            logger.error(f"Error getting responsive style: {e}")
            return ""
    
    def get_all_responsive_css(self) -> str:
        """
        Get CSS for all responsive styles.
        
        Returns:
            Combined CSS string for all responsive styles
        """
        try:
            return "\n".join(self.responsive_styles.values())
        except Exception as e:
            logger.error(f"Error getting all responsive CSS: {e}")
            return ""
    
    def create_custom_breakpoint(self, name: str, width: int) -> str:
        """
        Create a custom breakpoint.
        
        Args:
            name: Name for the breakpoint
            width: Width in pixels
            
        Returns:
            CSS string for the custom breakpoint
        """
        try:
            self.breakpoints[name] = width
            return f"@media (min-width: {width}px)"
        except Exception as e:
            logger.error(f"Error creating custom breakpoint: {e}")
            return ""
    
    def get_responsive_class(self, base_class: str, breakpoint: str, properties: Dict[str, str]) -> str:
        """
        Create a responsive class with properties for a specific breakpoint.
        
        Args:
            base_class: Base CSS class name
            breakpoint: Breakpoint name
            properties: CSS properties to apply
            
        Returns:
            CSS string for the responsive class
        """
        try:
            if breakpoint not in self.breakpoints:
                logger.warning(f"Breakpoint '{breakpoint}' not found")
                return ""
            
            width = self.breakpoints[breakpoint]
            responsive_class = f"{base_class}-{breakpoint}"
            
            # Create properties string
            props = "; ".join([f"{k}: {v}" for k, v in properties.items()])
            
            css = f"""
                @media (min-width: {width}px) {{
                    .{responsive_class} {{
                        {props}
                    }}
                }}
            """
            
            return css
        except Exception as e:
            logger.error(f"Error creating responsive class: {e}")
            return ""
    
    def render_responsive_styles(self) -> None:
        """
        Render responsive styles to the page.
        """
        try:
            css = self.get_all_responsive_css()
            if css:
                st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
                logger.debug("Responsive styles rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering responsive styles: {e}")
    
    def get_available_breakpoints(self) -> List[str]:
        """
        Get list of available breakpoints.
        
        Returns:
            List of breakpoint names
        """
        try:
            return list(self.breakpoints.keys())
        except Exception as e:
            logger.error(f"Error getting available breakpoints: {e}")
            return []
    
    def get_available_styles(self) -> List[str]:
        """
        Get list of available responsive styles.
        
        Returns:
            List of style names
        """
        try:
            return list(self.responsive_styles.keys())
        except Exception as e:
            logger.error(f"Error getting available styles: {e}")
            return []
