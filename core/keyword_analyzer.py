"""
Keyword Analysis Module for Resume/CV AI Application
Handles keyword extraction, analysis, and optimization for ATS compatibility.

This module provides:
- Keyword extraction from text content
- Keyword density analysis and optimization
- ATS-friendly keyword suggestions
- Industry-specific keyword mapping
- Keyword scoring and ranking
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime
import json
import os
from collections import Counter, defaultdict

from models.resume_model import ParsedResume
from models.job_model import JobDescription
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("keyword_analyzer")

class KeywordAnalyzer:
    """
    Advanced keyword analysis and optimization with comprehensive logging.
    
    This class provides sophisticated keyword analysis capabilities including
    extraction, density analysis, ATS optimization, and industry-specific
    keyword mapping for resume and job description analysis.
    
    Key Features:
    - Multi-source keyword extraction (resume, job descriptions)
    - Keyword density analysis and optimization
    - ATS-friendly keyword suggestions
    - Industry-specific keyword mapping
    - Keyword scoring and ranking algorithms
    - Comprehensive logging and error handling
    
    Attributes:
        ats_keywords_db (Dict): Database of ATS-friendly keywords
        industry_keywords (Dict): Industry-specific keyword mappings
        action_verbs (List): List of powerful action verbs
        stop_words (Set): Set of common stop words to filter
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, keywords_data_path: str = "data/skills/"):
        """
        Initialize the KeywordAnalyzer with comprehensive logging.
        
        Args:
            keywords_data_path (str): Path to keywords database files
            
        Raises:
            Exception: If keywords database initialization fails
        """
        logger.info("Initializing KeywordAnalyzer")
        self._initialization_time = time.time()
        
        # Initialize keyword databases
        self.ats_keywords_db = {}
        self.industry_keywords = {}
        self.action_verbs = []
        self.stop_words = set()
        
        try:
            # Load keyword databases
            logger.debug("Loading keyword databases")
            self._load_keyword_databases(keywords_data_path)
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"KeywordAnalyzer initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.ats_keywords_db)} ATS keyword categories")
            logger.info(f"Loaded {len(self.industry_keywords)} industry keyword mappings")
            logger.info(f"Loaded {len(self.action_verbs)} action verbs")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"KeywordAnalyzer initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Keyword analysis may not function correctly")
            raise
    
    def _load_keyword_databases(self, keywords_data_path: str):
        """
        Load keyword databases from JSON files with comprehensive logging.
        
        Args:
            keywords_data_path (str): Path to keywords database files
            
        Raises:
            Exception: If any keyword database file fails to load
        """
        try:
            logger.debug(f"Loading keyword databases from: {keywords_data_path}")
            
            # Load ATS keywords
            ats_keywords_file = os.path.join(keywords_data_path, "ats_keywords.json")
            if os.path.exists(ats_keywords_file):
                with open(ats_keywords_file, 'r', encoding='utf-8') as f:
                    self.ats_keywords_db = json.load(f)
                logger.debug(f"Loaded ATS keywords: {len(self.ats_keywords_db)} categories")
            else:
                logger.warning(f"ATS keywords file not found: {ats_keywords_file}")
                self.ats_keywords_db = self._get_default_ats_keywords()
            
            # Load industry keywords
            industry_keywords_file = os.path.join(keywords_data_path, "industry_keywords.json")
            if os.path.exists(industry_keywords_file):
                with open(industry_keywords_file, 'r', encoding='utf-8') as f:
                    self.industry_keywords = json.load(f)
                logger.debug(f"Loaded industry keywords: {len(self.industry_keywords)} industries")
            else:
                logger.warning(f"Industry keywords file not found: {industry_keywords_file}")
                self.industry_keywords = self._get_default_industry_keywords()
            
            # Load action verbs
            action_verbs_file = os.path.join(keywords_data_path, "action_verbs.json")
            if os.path.exists(action_verbs_file):
                with open(action_verbs_file, 'r', encoding='utf-8') as f:
                    action_verbs_data = json.load(f)
                    self.action_verbs = action_verbs_data.get("verbs", [])
                logger.debug(f"Loaded action verbs: {len(self.action_verbs)} verbs")
            else:
                logger.warning(f"Action verbs file not found: {action_verbs_file}")
                self.action_verbs = self._get_default_action_verbs()
            
            # Load stop words
            self.stop_words = self._get_stop_words()
            
            logger.info("Keyword databases loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load keyword databases: {e}")
            logger.error("Using default keyword databases")
            self._load_default_keywords()
    
    def _load_default_keywords(self):
        """Load default keyword databases when files are not available."""
        logger.debug("Loading default keyword databases")
        self.ats_keywords_db = self._get_default_ats_keywords()
        self.industry_keywords = self._get_default_industry_keywords()
        self.action_verbs = self._get_default_action_verbs()
        self.stop_words = self._get_stop_words()
    
    def _get_default_ats_keywords(self) -> Dict:
        """Get default ATS keywords database."""
        return {
            "Technical Skills": [
                "Python", "Java", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes",
                "Machine Learning", "Data Analysis", "Cloud Computing", "DevOps",
                "Agile", "Scrum", "Git", "CI/CD", "Microservices", "API Development"
            ],
            "Soft Skills": [
                "Leadership", "Communication", "Problem Solving", "Teamwork",
                "Project Management", "Time Management", "Adaptability", "Creativity",
                "Critical Thinking", "Decision Making", "Negotiation", "Mentoring"
            ],
            "Industry Terms": [
                "ROI", "KPI", "SLA", "SOP", "Compliance", "Regulatory", "Audit",
                "Risk Management", "Quality Assurance", "Process Improvement",
                "Stakeholder Management", "Change Management", "Strategic Planning"
            ],
            "Action Verbs": [
                "Developed", "Implemented", "Managed", "Led", "Created", "Designed",
                "Analyzed", "Improved", "Optimized", "Delivered", "Achieved",
                "Increased", "Reduced", "Streamlined", "Automated", "Coordinated"
            ]
        }
    
    def _get_default_industry_keywords(self) -> Dict:
        """Get default industry keywords mapping."""
        return {
            "Technology": [
                "Software Development", "Cloud Computing", "Data Science", "AI/ML",
                "Cybersecurity", "DevOps", "Mobile Development", "Web Development",
                "API", "Microservices", "Agile", "Scrum", "CI/CD", "Automation"
            ],
            "Finance": [
                "Financial Analysis", "Risk Management", "Investment Banking",
                "Accounting", "Trading", "Compliance", "Auditing", "Financial Modeling",
                "Portfolio Management", "Derivatives", "Equity Research", "M&A"
            ],
            "Healthcare": [
                "Medical Knowledge", "Patient Care", "Healthcare IT", "Clinical Research",
                "Regulatory Compliance", "Medical Coding", "Healthcare Analytics",
                "HIPAA", "FDA", "Clinical Trials", "Electronic Health Records"
            ],
            "Marketing": [
                "Digital Marketing", "Content Marketing", "SEO/SEM", "Social Media",
                "Brand Management", "Market Research", "Analytics", "Campaign Management",
                "Lead Generation", "Customer Acquisition", "ROI", "Conversion Rate"
            ],
            "Sales": [
                "Lead Generation", "Customer Relationship Management", "Negotiation",
                "Sales Strategy", "Account Management", "Business Development",
                "Prospecting", "Pipeline Management", "Revenue Growth", "Client Retention"
            ]
        }
    
    def _get_default_action_verbs(self) -> List[str]:
        """Get default action verbs list."""
        return [
            "Achieved", "Administered", "Analyzed", "Architected", "Built", "Collaborated",
            "Created", "Delivered", "Designed", "Developed", "Directed", "Established",
            "Executed", "Generated", "Implemented", "Improved", "Increased", "Initiated",
            "Led", "Managed", "Optimized", "Organized", "Planned", "Produced",
            "Reduced", "Resolved", "Streamlined", "Supervised", "Transformed", "Utilized"
        ]
    
    def _get_stop_words(self) -> Set[str]:
        """Get common stop words for filtering."""
        return {
            "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
            "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "will", "with",
            "i", "you", "we", "they", "me", "him", "her", "us", "them", "my", "your",
            "our", "their", "this", "these", "those", "or", "but", "if", "when", "where",
            "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
            "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "can", "could", "should", "would", "may", "might", "must"
        }
    
    def extract_keywords_from_text(self, text: str, min_length: int = 3, max_length: int = 20) -> List[Dict[str, Any]]:
        """
        Extract keywords from text content with comprehensive logging.
        
        Args:
            text (str): Text content to analyze
            min_length (int): Minimum keyword length
            max_length (int): Maximum keyword length
            
        Returns:
            List[Dict[str, Any]]: List of extracted keywords with metadata
            
        Raises:
            Exception: If keyword extraction fails
        """
        try:
            logger.debug(f"Extracting keywords from text (length: {len(text)})")
            start_time = time.time()
            
            # Clean and preprocess text
            cleaned_text = clean_text(text)
            words = re.findall(r'\b[a-zA-Z]+\b', cleaned_text.lower())
            
            # Filter words by length and stop words
            filtered_words = [
                word for word in words
                if min_length <= len(word) <= max_length
                and word not in self.stop_words
            ]
            
            # Count word frequencies
            word_counts = Counter(filtered_words)
            
            # Calculate keyword scores
            total_words = len(filtered_words)
            keywords = []
            
            for word, count in word_counts.items():
                frequency = count / total_words if total_words > 0 else 0
                
                # Calculate keyword score based on frequency and length
                score = frequency * (1 + len(word) / 10)  # Longer words get slight boost
                
                # Check if it's an action verb
                is_action_verb = word in [verb.lower() for verb in self.action_verbs]
                if is_action_verb:
                    score *= 1.5  # Boost action verbs
                
                # Check if it's an ATS keyword
                is_ats_keyword = self._is_ats_keyword(word)
                if is_ats_keyword:
                    score *= 1.3  # Boost ATS keywords
                
                keywords.append({
                    "word": word,
                    "count": count,
                    "frequency": round(frequency, 4),
                    "score": round(score, 4),
                    "is_action_verb": is_action_verb,
                    "is_ats_keyword": is_ats_keyword,
                    "length": len(word)
                })
            
            # Sort by score
            keywords.sort(key=lambda x: x["score"], reverse=True)
            
            extraction_time = time.time() - start_time
            logger.info(f"Keyword extraction completed in {extraction_time:.2f}s")
            logger.info(f"Total keywords extracted: {len(keywords)}")
            
            return keywords
            
        except Exception as e:
            logger.error(f"Failed to extract keywords from text: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return []
    
    def _is_ats_keyword(self, word: str) -> bool:
        """Check if a word is an ATS keyword."""
        word_lower = word.lower()
        for category, keywords in self.ats_keywords_db.items():
            if any(keyword.lower() == word_lower for keyword in keywords):
                return True
        return False
    
    def analyze_keyword_density(self, text: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Analyze keyword density in text content.
        
        Args:
            text (str): Text content to analyze
            target_keywords (List[str]): Specific keywords to analyze
            
        Returns:
            Dict[str, Any]: Keyword density analysis results
        """
        try:
            logger.debug("Analyzing keyword density")
            start_time = time.time()
            
            # Extract all keywords
            all_keywords = self.extract_keywords_from_text(text)
            
            # If target keywords provided, filter to those
            if target_keywords:
                target_keywords_lower = [kw.lower() for kw in target_keywords]
                filtered_keywords = [
                    kw for kw in all_keywords
                    if kw["word"] in target_keywords_lower
                ]
            else:
                filtered_keywords = all_keywords
            
            # Calculate density metrics
            total_words = len(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
            keyword_density = {}
            
            for kw in filtered_keywords:
                density = (kw["count"] / total_words) * 100 if total_words > 0 else 0
                keyword_density[kw["word"]] = {
                    "count": kw["count"],
                    "density": round(density, 2),
                    "score": kw["score"],
                    "is_action_verb": kw["is_action_verb"],
                    "is_ats_keyword": kw["is_ats_keyword"]
                }
            
            # Calculate overall metrics
            total_keyword_count = sum(kw["count"] for kw in filtered_keywords)
            overall_density = (total_keyword_count / total_words) * 100 if total_words > 0 else 0
            
            # Get top keywords
            top_keywords = sorted(
                filtered_keywords,
                key=lambda x: x["score"],
                reverse=True
            )[:10]
            
            analysis_time = time.time() - start_time
            logger.info(f"Keyword density analysis completed in {analysis_time:.2f}s")
            logger.info(f"Overall keyword density: {overall_density:.2f}%")
            
            return {
                "total_words": total_words,
                "total_keywords": len(filtered_keywords),
                "overall_density": round(overall_density, 2),
                "keyword_density": keyword_density,
                "top_keywords": [kw["word"] for kw in top_keywords],
                "action_verbs_count": sum(1 for kw in filtered_keywords if kw["is_action_verb"]),
                "ats_keywords_count": sum(1 for kw in filtered_keywords if kw["is_ats_keyword"]),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze keyword density: {e}")
            return {
                "total_words": 0,
                "total_keywords": 0,
                "overall_density": 0,
                "keyword_density": {},
                "top_keywords": [],
                "action_verbs_count": 0,
                "ats_keywords_count": 0,
                "analysis_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_keyword_suggestions(self, resume_text: str, job_text: str, industry: str = None) -> Dict[str, Any]:
        """
        Get keyword suggestions for resume optimization.
        
        Args:
            resume_text (str): Resume text content
            job_text (str): Job description text content
            industry (str): Target industry for suggestions
            
        Returns:
            Dict[str, Any]: Keyword suggestions and recommendations
        """
        try:
            logger.debug("Generating keyword suggestions")
            start_time = time.time()
            
            # Extract keywords from both texts
            resume_keywords = self.extract_keywords_from_text(resume_text)
            job_keywords = self.extract_keywords_from_text(job_text)
            
            # Get keyword sets
            resume_words = {kw["word"] for kw in resume_keywords}
            job_words = {kw["word"] for kw in job_keywords}
            
            # Find missing keywords
            missing_keywords = job_words - resume_words
            
            # Find extra keywords
            extra_keywords = resume_words - job_words
            
            # Find matching keywords
            matching_keywords = resume_words.intersection(job_words)
            
            # Get industry-specific suggestions
            industry_suggestions = []
            if industry and industry.lower() in self.industry_keywords:
                industry_keywords = self.industry_keywords[industry.lower()]
                industry_suggestions = [
                    kw for kw in industry_keywords
                    if kw.lower() not in resume_words
                ][:5]  # Top 5 industry suggestions
            
            # Get ATS keyword suggestions
            ats_suggestions = []
            for category, keywords in self.ats_keywords_db.items():
                for keyword in keywords:
                    if keyword.lower() not in resume_words and keyword.lower() in job_words:
                        ats_suggestions.append({
                            "keyword": keyword,
                            "category": category,
                            "priority": "High"
                        })
            
            # Get action verb suggestions
            action_verb_suggestions = []
            resume_action_verbs = {kw["word"] for kw in resume_keywords if kw["is_action_verb"]}
            job_action_verbs = {kw["word"] for kw in job_keywords if kw["is_action_verb"]}
            missing_action_verbs = job_action_verbs - resume_action_verbs
            
            for verb in missing_action_verbs:
                action_verb_suggestions.append({
                    "verb": verb,
                    "priority": "Medium",
                    "suggestion": f"Use '{verb}' to start bullet points in your experience section"
                })
            
            # Calculate optimization score
            match_percentage = (len(matching_keywords) / len(job_words)) * 100 if job_words else 0
            optimization_score = min(100, match_percentage + (len(ats_suggestions) * 2))
            
            analysis_time = time.time() - start_time
            logger.info(f"Keyword suggestions generated in {analysis_time:.2f}s")
            logger.info(f"Optimization score: {optimization_score:.1f}")
            
            return {
                "optimization_score": round(optimization_score, 1),
                "match_percentage": round(match_percentage, 1),
                "missing_keywords": list(missing_keywords)[:10],
                "extra_keywords": list(extra_keywords)[:10],
                "matching_keywords": list(matching_keywords),
                "industry_suggestions": industry_suggestions,
                "ats_suggestions": ats_suggestions[:10],
                "action_verb_suggestions": action_verb_suggestions[:5],
                "total_resume_keywords": len(resume_keywords),
                "total_job_keywords": len(job_keywords),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate keyword suggestions: {e}")
            return {
                "optimization_score": 0,
                "match_percentage": 0,
                "missing_keywords": [],
                "extra_keywords": [],
                "matching_keywords": [],
                "industry_suggestions": [],
                "ats_suggestions": [],
                "action_verb_suggestions": [],
                "total_resume_keywords": 0,
                "total_job_keywords": 0,
                "analysis_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def optimize_keywords_for_ats(self, text: str, target_keywords: List[str]) -> Dict[str, Any]:
        """
        Optimize text for ATS keyword matching.
        
        Args:
            text (str): Text content to optimize
            target_keywords (List[str]): Target keywords to include
            
        Returns:
            Dict[str, Any]: Optimization suggestions and results
        """
        try:
            logger.debug("Optimizing keywords for ATS")
            start_time = time.time()
            
            # Analyze current keyword density
            current_analysis = self.analyze_keyword_density(text, target_keywords)
            
            # Find missing target keywords
            missing_keywords = []
            for keyword in target_keywords:
                if keyword.lower() not in current_analysis["keyword_density"]:
                    missing_keywords.append(keyword)
            
            # Generate optimization suggestions
            suggestions = []
            
            # Suggest adding missing keywords
            for keyword in missing_keywords[:5]:  # Top 5 missing keywords
                suggestions.append({
                    "type": "add_keyword",
                    "keyword": keyword,
                    "suggestion": f"Add '{keyword}' to your resume content",
                    "priority": "High",
                    "location": "Experience section or skills section"
                })
            
            # Suggest improving keyword density
            for keyword, data in current_analysis["keyword_density"].items():
                if data["density"] < 1.0:  # Less than 1% density
                    suggestions.append({
                        "type": "increase_density",
                        "keyword": keyword,
                        "current_density": data["density"],
                        "suggestion": f"Increase usage of '{keyword}' in your resume",
                        "priority": "Medium",
                        "target_density": "1-2%"
                    })
            
            # Suggest action verb improvements
            action_verbs_in_text = [
                kw for kw, data in current_analysis["keyword_density"].items()
                if data["is_action_verb"]
            ]
            
            if len(action_verbs_in_text) < 5:
                suggestions.append({
                    "type": "add_action_verbs",
                    "suggestion": "Add more action verbs to start your bullet points",
                    "priority": "High",
                    "examples": self.action_verbs[:10]
                })
            
            # Calculate optimization potential
            optimization_potential = min(100, len(missing_keywords) * 10 + len(suggestions) * 5)
            
            analysis_time = time.time() - start_time
            logger.info(f"ATS optimization completed in {analysis_time:.2f}s")
            logger.info(f"Optimization potential: {optimization_potential}%")
            
            return {
                "optimization_potential": optimization_potential,
                "current_density": current_analysis["overall_density"],
                "missing_keywords": missing_keywords,
                "suggestions": suggestions,
                "action_verbs_count": current_analysis["action_verbs_count"],
                "ats_keywords_count": current_analysis["ats_keywords_count"],
                "optimization_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to optimize keywords for ATS: {e}")
            return {
                "optimization_potential": 0,
                "current_density": 0,
                "missing_keywords": [],
                "suggestions": [],
                "action_verbs_count": 0,
                "ats_keywords_count": 0,
                "optimization_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_keyword_report(self, resume_text: str, job_text: str = None) -> Dict[str, Any]:
        """
        Generate comprehensive keyword analysis report.
        
        Args:
            resume_text (str): Resume text content
            job_text (str): Job description text content (optional)
            
        Returns:
            Dict[str, Any]: Comprehensive keyword analysis report
        """
        try:
            logger.debug("Generating keyword analysis report")
            start_time = time.time()
            
            # Analyze resume keywords
            resume_analysis = self.analyze_keyword_density(resume_text)
            
            report = {
                "resume_analysis": resume_analysis,
                "job_analysis": None,
                "comparison": None,
                "recommendations": [],
                "overall_score": 0,
                "report_timestamp": datetime.now().isoformat()
            }
            
            # If job text provided, analyze and compare
            if job_text:
                job_analysis = self.analyze_keyword_density(job_text)
                report["job_analysis"] = job_analysis
                
                # Generate suggestions
                suggestions = self.get_keyword_suggestions(resume_text, job_text)
                report["comparison"] = suggestions
                report["overall_score"] = suggestions["optimization_score"]
                
                # Add recommendations
                if suggestions["missing_keywords"]:
                    report["recommendations"].append({
                        "type": "missing_keywords",
                        "priority": "High",
                        "message": f"Add {len(suggestions['missing_keywords'])} missing keywords",
                        "keywords": suggestions["missing_keywords"][:5]
                    })
                
                if suggestions["ats_suggestions"]:
                    report["recommendations"].append({
                        "type": "ats_keywords",
                        "priority": "High",
                        "message": f"Include {len(suggestions['ats_suggestions'])} ATS keywords",
                        "keywords": [s["keyword"] for s in suggestions["ats_suggestions"][:5]]
                    })
                
                if suggestions["action_verb_suggestions"]:
                    report["recommendations"].append({
                        "type": "action_verbs",
                        "priority": "Medium",
                        "message": f"Use more action verbs ({len(suggestions['action_verb_suggestions'])} suggestions)",
                        "verbs": [s["verb"] for s in suggestions["action_verb_suggestions"][:5]]
                    })
            else:
                # Standalone resume analysis
                report["overall_score"] = min(100, resume_analysis["overall_density"] * 10)
                
                # Add general recommendations
                if resume_analysis["action_verbs_count"] < 5:
                    report["recommendations"].append({
                        "type": "action_verbs",
                        "priority": "Medium",
                        "message": "Add more action verbs to strengthen your resume",
                        "examples": self.action_verbs[:10]
                    })
                
                if resume_analysis["ats_keywords_count"] < 10:
                    report["recommendations"].append({
                        "type": "ats_keywords",
                        "priority": "High",
                        "message": "Include more ATS-friendly keywords",
                        "examples": list(self.ats_keywords_db.keys())
                    })
            
            analysis_time = time.time() - start_time
            logger.info(f"Keyword analysis report generated in {analysis_time:.2f}s")
            logger.info(f"Overall score: {report['overall_score']}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate keyword analysis report: {e}")
            return {
                "resume_analysis": {},
                "job_analysis": None,
                "comparison": None,
                "recommendations": [],
                "overall_score": 0,
                "report_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
