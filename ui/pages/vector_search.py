"""
Vector Search Page for Resume/CV AI Application
Handles vector-based search functionality for resumes and job descriptions.

This module provides:
- Vector-based semantic search
- Resume and job description search
- Similarity matching
- Search filters and options
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import streamlit as st
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("vector_search_page")

def render():
    """
    Render the vector search page with comprehensive logging.
    
    This function renders the vector search page including search interface,
    filters, and results display for semantic search across resumes and jobs.
    
    Raises:
        Exception: If page rendering fails
    """
    try:
        logger.info("Rendering vector search page")
        start_time = time.time()
        
        # Get app instance from session state
        app = st.session_state.get('app')
        if not app:
            st.error("Application not initialized. Please refresh the page.")
            return
        
        # Page header
        st.title("🔍 Vector Search")
        st.markdown("Search through resumes and job descriptions using semantic similarity.")
        
        # Check if vector database is available
        if not hasattr(app, 'vector_db') or not app.vector_db:
            st.error("Vector database not available. Please ensure the application is properly initialized.")
            return
        
        # Search interface
        st.header("Search Interface")
        
        # Search type selection
        search_type = st.radio(
            "Search Type:",
            ["Resumes", "Job Descriptions", "Both"],
            horizontal=True,
            help="Select what type of content to search through"
        )
        
        # Search query
        search_query = st.text_area(
            "Search Query:",
            placeholder="Enter keywords, skills, job requirements, or any text to search for...",
            height=100,
            help="Enter your search terms. The system will find semantically similar content."
        )
        
        # Search options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_results = st.number_input(
                "Max Results:",
                min_value=1,
                max_value=100,
                value=10,
                help="Maximum number of results to return"
            )
        
        with col2:
            similarity_threshold = st.slider(
                "Similarity Threshold:",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                help="Minimum similarity score for results"
            )
        
        with col3:
            include_metadata = st.checkbox(
                "Include Metadata",
                value=True,
                help="Include additional metadata in search results"
            )
        
        # Search button
        if st.button("🔍 Search", type="primary", use_container_width=True):
            if not search_query.strip():
                st.warning("Please enter a search query.")
                return
            
            try:
                logger.info(f"Performing vector search: '{search_query[:50]}...'")
                
                # Show loading spinner
                with st.spinner("Searching through vector database..."):
                    # Perform search based on type
                    results = []
                    
                    if search_type in ["Resumes", "Both"]:
                        resume_results = _search_resumes(
                            app.vector_db, 
                            search_query, 
                            max_results, 
                            similarity_threshold
                        )
                        results.extend(resume_results)
                    
                    if search_type in ["Job Descriptions", "Both"]:
                        job_results = _search_jobs(
                            app.vector_db, 
                            search_query, 
                            max_results, 
                            similarity_threshold
                        )
                        results.extend(job_results)
                    
                    # Sort results by similarity score
                    results.sort(key=lambda x: x.get('similarity', 0), reverse=True)
                    
                    # Limit results
                    results = results[:max_results]
                
                # Display results
                if results:
                    st.success(f"Found {len(results)} results")
                    _display_search_results(results, include_metadata)
                else:
                    st.info("No results found. Try adjusting your search query or similarity threshold.")
                
            except Exception as search_error:
                logger.error(f"Vector search failed: {search_error}")
                st.error(f"Search failed: {str(search_error)}")
        
        # Search history and saved searches
        _render_search_history()
        
        # Performance metrics
        render_time = time.time() - start_time
        logger.info(f"Vector search page rendered successfully in {render_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Failed to render vector search page: {e}")
        st.error(f"Failed to load vector search page: {str(e)}")

def _search_resumes(vector_db, query: str, max_results: int, threshold: float) -> List[Dict]:
    """Search resumes using vector similarity."""
    try:
        # This would use the vector database to search resumes
        # For now, return mock data
        logger.debug(f"Searching resumes with query: {query[:50]}...")
        
        # Mock results - replace with actual vector search
        results = [
            {
                'type': 'resume',
                'title': 'Software Engineer Resume',
                'content': 'Experienced software engineer with 5+ years in Python, React, and AWS...',
                'similarity': 0.85,
                'metadata': {
                    'experience_years': 5,
                    'skills': ['Python', 'React', 'AWS', 'Docker'],
                    'location': 'San Francisco, CA'
                }
            }
        ]
        
        return results
        
    except Exception as e:
        logger.error(f"Resume search failed: {e}")
        return []

def _search_jobs(vector_db, query: str, max_results: int, threshold: float) -> List[Dict]:
    """Search job descriptions using vector similarity."""
    try:
        # This would use the vector database to search jobs
        # For now, return mock data
        logger.debug(f"Searching jobs with query: {query[:50]}...")
        
        # Mock results - replace with actual vector search
        results = [
            {
                'type': 'job',
                'title': 'Senior Python Developer',
                'content': 'We are looking for a senior Python developer with experience in Django, FastAPI...',
                'similarity': 0.78,
                'metadata': {
                    'company': 'TechCorp Inc.',
                    'location': 'Remote',
                    'salary_range': '$120k - $150k',
                    'experience_required': '5+ years'
                }
            }
        ]
        
        return results
        
    except Exception as e:
        logger.error(f"Job search failed: {e}")
        return []

def _display_search_results(results: List[Dict], include_metadata: bool):
    """Display search results in a formatted way."""
    try:
        for i, result in enumerate(results):
            with st.expander(f"Result {i+1}: {result.get('title', 'Untitled')} (Score: {result.get('similarity', 0):.3f})"):
                
                # Content
                st.write("**Content:**")
                st.write(result.get('content', 'No content available'))
                
                # Similarity score
                similarity = result.get('similarity', 0)
                st.metric("Similarity Score", f"{similarity:.3f}")
                
                # Metadata
                if include_metadata and result.get('metadata'):
                    st.write("**Metadata:**")
                    metadata = result['metadata']
                    
                    # Display metadata in columns
                    cols = st.columns(min(len(metadata), 3))
                    for j, (key, value) in enumerate(metadata.items()):
                        with cols[j % 3]:
                            st.caption(f"**{key.replace('_', ' ').title()}:** {value}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View Details", key=f"view_{i}"):
                        st.session_state[f"view_details_{i}"] = True
                
                with col2:
                    if st.button("Export", key=f"export_{i}"):
                        st.info("Export functionality coming soon!")
                
                with col3:
                    if st.button("Save", key=f"save_{i}"):
                        st.info("Save functionality coming soon!")
                
                # Show details if requested
                if st.session_state.get(f"view_details_{i}", False):
                    st.json(result)
                    
    except Exception as e:
        logger.error(f"Failed to display search results: {e}")
        st.error("Failed to display search results")

def _render_search_history():
    """Render search history and saved searches section."""
    try:
        st.header("Search History & Saved Searches")
        
        # Search history (mock data)
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        
        if st.session_state.search_history:
            st.write("**Recent Searches:**")
            for i, search in enumerate(st.session_state.search_history[-5:]):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {search}")
                with col2:
                    if st.button("Re-run", key=f"rerun_{i}"):
                        # Re-run search logic here
                        st.info("Re-running search...")
        
        # Saved searches
        st.write("**Saved Searches:**")
        st.info("Save search functionality coming soon! You'll be able to save frequently used searches for quick access.")
        
    except Exception as e:
        logger.error(f"Failed to render search history: {e}")
        st.warning("Search history unavailable")
