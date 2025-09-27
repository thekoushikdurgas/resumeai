"""
Resume/CV AI Application with Vector Database Integration
A comprehensive Streamlit application for resume analysis, optimization, and career advancement.
"""

__version__ = "1.0.0"
__author__ = "Resume AI Team"
__description__ = "AI-powered resume analysis and optimization with vector database support"

# Import main components
from core.vector_db import VectorDatabase
from core.ai_handler import AIHandler
from core.document_processor import DocumentProcessor
from core.resume_analyzer import ResumeAnalyzer
from core.job_matcher import JobMatcher
from core.ats_checker import ATSChecker
from core.resume_builder import ResumeBuilder

__all__ = [
    "VectorDatabase",
    "AIHandler", 
    "DocumentProcessor",
    "ResumeAnalyzer",
    "JobMatcher",
    "ATSChecker",
    "ResumeBuilder"
]
