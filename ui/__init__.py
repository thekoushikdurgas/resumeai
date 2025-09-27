"""
UI Package for Resume/CV AI Application
Comprehensive user interface components and modules.

This package provides:
- Main application layout and navigation
- Feature-specific tabs and pages
- Reusable UI components
- Styling and theme management
- Responsive design utilities

Author: Resume AI Team
Created: 2024
"""

# Import main UI components
from .app_layout import AppLayout
from .sidebar import Sidebar

# Import tab components
from .tabs.analysis_tab import AnalysisTab
from .tabs.job_matching_tab import JobMatchingTab
from .tabs.enhancement_tab import EnhancementTab
from .tabs.ats_checker_tab import ATSCheckerTab
from .tabs.builder_tab import BuilderTab
from .tabs.templates_tab import TemplatesTab
from .tabs.insights_tab import InsightsTab
from .tabs.customization_tab import CustomizationTab

# Import reusable components
from .components.file_uploader import FileUploader
from .components.progress_tracker import ProgressTracker
from .components.metrics_display import MetricsDisplay
from .components.charts import Charts
from .components.data_tables import DataTables
from .components.forms import Forms
from .components.modals import Modals
from .components.alerts import Alerts
from .components.buttons import Buttons
from .components.cards import Cards
from .components.resume_preview import ResumePreview
from .components.score_display import ScoreDisplay

# Import styling
from .styles.css_styles import CSSStyles
from .styles.themes import Themes
from .styles.animations import Animations
from .styles.responsive import Responsive

__all__ = [
    # Main layout
    'AppLayout',
    'Sidebar', 
    
    # Tabs
    'AnalysisTab',
    'JobMatchingTab',
    'EnhancementTab',
    'ATSCheckerTab',
    'BuilderTab',
    'TemplatesTab',
    'InsightsTab',
    'CustomizationTab',
    
    # Components
    'FileUploader',
    'ProgressTracker',
    'MetricsDisplay',
    'Charts',
    'DataTables',
    'Forms',
    'Modals',
    'Alerts',
    'Buttons',
    'Cards',
    'ResumePreview',
    'ScoreDisplay',
    
    # Styling
    'CSSStyles',
    'Themes',
    'Animations',
    'Responsive'
]
