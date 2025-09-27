"""
Animations Module for Resume/CV AI Application
CSS animations and transitions for enhanced user experience.

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class Animations:
    """Animations component for CSS animations and transitions."""
    
    def __init__(self):
        """Initialize animations component."""
        self.animation_styles = {
            'fade_in': """
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                .fade-in {
                    animation: fadeIn 0.5s ease-in;
                }
            """,
            'slide_in_left': """
                @keyframes slideInLeft {
                    from { transform: translateX(-100%); }
                    to { transform: translateX(0); }
                }
                .slide-in-left {
                    animation: slideInLeft 0.5s ease-out;
                }
            """,
            'slide_in_right': """
                @keyframes slideInRight {
                    from { transform: translateX(100%); }
                    to { transform: translateX(0); }
                }
                .slide-in-right {
                    animation: slideInRight 0.5s ease-out;
                }
            """,
            'bounce': """
                @keyframes bounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-10px); }
                    60% { transform: translateY(-5px); }
                }
                .bounce {
                    animation: bounce 1s infinite;
                }
            """,
            'pulse': """
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
                .pulse {
                    animation: pulse 2s infinite;
                }
            """,
            'rotate': """
                @keyframes rotate {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
                .rotate {
                    animation: rotate 2s linear infinite;
                }
            """
        }
    
    def get_animation_css(self, animation_name: str) -> str:
        """
        Get CSS for a specific animation.
        
        Args:
            animation_name: Name of the animation
            
        Returns:
            CSS string for the animation
        """
        try:
            return self.animation_styles.get(animation_name, "")
        except Exception as e:
            logger.error(f"Error getting animation CSS: {e}")
            return ""
    
    def get_all_animations_css(self) -> str:
        """
        Get CSS for all animations.
        
        Returns:
            Combined CSS string for all animations
        """
        try:
            return "\n".join(self.animation_styles.values())
        except Exception as e:
            logger.error(f"Error getting all animations CSS: {e}")
            return ""
    
    def apply_animation(self, element_class: str, animation_name: str) -> str:
        """
        Apply animation to an element class.
        
        Args:
            element_class: CSS class name
            animation_name: Name of the animation to apply
            
        Returns:
            CSS string with animation applied
        """
        try:
            if animation_name not in self.animation_styles:
                logger.warning(f"Animation '{animation_name}' not found")
                return ""
            
            # Create a custom class that combines the element class with animation
            custom_class = f"{element_class}-{animation_name}"
            animation_css = self.animation_styles[animation_name]
            
            # Add the custom class definition
            custom_definition = f".{custom_class} {{ {animation_css.split('{')[1].split('}')[0]} }}"
            
            return f"{animation_css}\n{custom_definition}"
        except Exception as e:
            logger.error(f"Error applying animation: {e}")
            return ""
    
    def render_animation_styles(self) -> None:
        """
        Render animation styles to the page.
        """
        try:
            css = self.get_all_animations_css()
            if css:
                st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
                logger.debug("Animation styles rendered successfully")
        except Exception as e:
            logger.error(f"Error rendering animation styles: {e}")
    
    def get_available_animations(self) -> List[str]:
        """
        Get list of available animations.
        
        Returns:
            List of animation names
        """
        try:
            return list(self.animation_styles.keys())
        except Exception as e:
            logger.error(f"Error getting available animations: {e}")
            return []
