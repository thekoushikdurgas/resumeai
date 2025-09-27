#!/usr/bin/env python3
"""
Demo script showing the new expandable sidebar design.
This demonstrates how the new sidebar works with expandable sections.
"""

import streamlit as st

# Configure the page
st.set_page_config(
    page_title="New Sidebar Demo",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def demo_sidebar():
    """Demonstrate the new sidebar design."""
    
    # Custom CSS for the demo
    st.markdown("""
    <style>
    .demo-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .demo-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    
    .page-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        width: 100%;
        border: none;
        background: transparent;
        text-align: left;
    }
    
    .page-item:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    
    .page-item.current {
        background-color: #007bff;
        color: white;
        font-weight: 600;
    }
    
    .page-icon {
        margin-right: 0.5rem;
        font-size: 1.1rem;
        min-width: 1.5rem;
    }
    
    .page-title {
        font-weight: 500;
        flex: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Demo header
    st.markdown("""
    <div class="demo-header">
        <h1>🧪 New Expandable Sidebar Design Demo</h1>
        <p>This demonstrates the new sidebar with expandable sections similar to the reference design</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🎯 New Sidebar Features")
        
        # Simulate the new sidebar structure
        st.markdown("""
        <div class="demo-section">
            <h4>✨ APPS</h4>
            <div class="page-item current">
                <span class="page-icon">📄</span>
                <span class="page-title">Resume Analysis</span>
            </div>
            <div class="page-item">
                <span class="page-icon">🎯</span>
                <span class="page-title">Job Matching</span>
            </div>
            <div class="page-item">
                <span class="page-icon">✨</span>
                <span class="page-title">AI Enhancement</span>
            </div>
            <div class="page-item">
                <span class="page-icon">📈</span>
                <span class="page-title">Career Insights</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="demo-section">
            <h4>🛠 COMPONENTS</h4>
            <div class="page-item">
                <span class="page-icon">📊</span>
                <span class="page-title">ATS Checker</span>
            </div>
            <div class="page-item">
                <span class="page-icon">🔧</span>
                <span class="page-title">Resume Builder</span>
            </div>
            <div class="page-item">
                <span class="page-icon">📋</span>
                <span class="page-title">Templates</span>
            </div>
            <div class="page-item">
                <span class="page-icon">🎨</span>
                <span class="page-title">Customization</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="demo-section">
            <h4>🔧 TOOLS</h4>
            <div class="page-item">
                <span class="page-icon">🔍</span>
                <span class="page-title">Vector Search</span>
            </div>
            <div class="page-item">
                <span class="page-icon">💾</span>
                <span class="page-title">Export Resume</span>
            </div>
            <div class="page-item">
                <span class="page-icon">📥</span>
                <span class="page-title">Import Data</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="demo-section">
            <h4>⚙️ SETTINGS</h4>
            <div class="page-item">
                <span class="page-icon">⚙️</span>
                <span class="page-title">Preferences</span>
            </div>
            <div class="page-item">
                <span class="page-icon">🔑</span>
                <span class="page-title">API Keys</span>
            </div>
            <div class="page-item">
                <span class="page-icon">❓</span>
                <span class="page-title">Help & Support</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 Implementation Details")
        
        st.markdown("""
        #### Key Features Implemented:
        
        1. **Expandable Sections**: Similar to the reference design with `st.expander()`
        2. **Page Items**: Custom `PageItem` class for individual navigation items
        3. **Page Object**: `Page` class with `item()` method similar to the reference
        4. **Organized Groups**: Logical grouping of features into sections
        5. **Modern Styling**: Clean, professional CSS styling
        6. **Interactive Elements**: Hover effects and current page highlighting
        
        #### Code Structure:
        
        ```python
        # PageItem class for individual items
        class PageItem:
            def __init__(self, title, page_handler=None, default=False, icon="", description=""):
                # Implementation details...
        
        # Page class for managing sections
        class Page:
            def item(self, title, page_handler=None, default=False, icon="", description=""):
                # Similar to reference design's page.item()
        
        # Sidebar with expandable sections
        class Sidebar:
            def _render_expandable_navigation(self):
                for section_title, page_items in self.navigation_sections.items():
                    with st.expander(section_title, expanded=True):
                        for page_item in page_items:
                            page_item.render(is_current=is_current)
        ```
        
        #### Navigation Sections:
        
        - **✨ APPS**: Core application features (Resume Analysis, Job Matching, etc.)
        - **🛠 COMPONENTS**: Analysis and building tools (ATS Checker, Resume Builder, etc.)
        - **🔧 TOOLS**: Utility features (Vector Search, Export, Import)
        - **⚙️ SETTINGS**: Configuration and support (Preferences, API Keys, Help)
        """)
        
        st.markdown("### 🎨 Styling Features")
        
        st.markdown("""
        - **Responsive Design**: Works on different screen sizes
        - **Hover Effects**: Smooth transitions and visual feedback
        - **Current Page Highlighting**: Clear indication of active page
        - **Icon Support**: Emoji icons for better visual appeal
        - **Consistent Spacing**: Professional layout with proper margins
        - **Theme Support**: Ready for light/dark theme switching
        """)
        
        st.markdown("### 🚀 Usage Example")
        
        st.code("""
# Create sidebar instance
sidebar = Sidebar()

# Add custom page items
page = Page(sidebar, "Custom Section")
page.item("My Feature", icon="⭐", description="A custom feature")

# Render the sidebar
sidebar.render()
        """, language="python")

if __name__ == "__main__":
    demo_sidebar()
