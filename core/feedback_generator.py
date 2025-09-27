"""
Feedback Generator Module for Resume/CV AI Application
Handles AI-powered feedback generation and recommendations.

This module provides:
- AI-powered feedback generation
- Personalized recommendations
- Industry-specific advice
- Actionable improvement suggestions
- Feedback categorization and prioritization
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json

from models.resume_model import ParsedResume
from models.analysis_model import AnalysisResult, EnhancementSuggestion, FeedbackItem
from core.ai_handler import AIHandler
from core.scoring_engine import ScoringEngine
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("feedback_generator")

class FeedbackGenerator:
    """
    Advanced feedback generator with comprehensive logging.
    
    This class provides sophisticated feedback generation capabilities including
    AI-powered analysis, personalized recommendations, industry-specific advice,
    and actionable improvement suggestions.
    
    Key Features:
    - AI-powered feedback generation
    - Personalized recommendations
    - Industry-specific advice
    - Actionable improvement suggestions
    - Feedback categorization and prioritization
    - Comprehensive logging and error handling
    
    Attributes:
        ai_handler (AIHandler): AI handler instance for content analysis
        scoring_engine (ScoringEngine): Scoring engine for evaluation
        feedback_templates (Dict): Templates for different feedback types
        industry_guidelines (Dict): Industry-specific feedback guidelines
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, ai_handler: AIHandler, scoring_engine: ScoringEngine):
        """
        Initialize the FeedbackGenerator with comprehensive logging.
        
        Args:
            ai_handler (AIHandler): AI handler instance for content analysis
            scoring_engine (ScoringEngine): Scoring engine for evaluation
            
        Raises:
            Exception: If FeedbackGenerator initialization fails
        """
        logger.info("Initializing FeedbackGenerator")
        self._initialization_time = time.time()
        
        # Initialize dependencies
        self.ai_handler = ai_handler
        self.scoring_engine = scoring_engine
        
        # Initialize feedback templates and guidelines
        self.feedback_templates = {}
        self.industry_guidelines = {}
        
        try:
            # Load feedback templates and guidelines
            logger.debug("Loading feedback templates and guidelines")
            self._load_feedback_templates()
            self._load_industry_guidelines()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"FeedbackGenerator initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.feedback_templates)} feedback templates")
            logger.info(f"Loaded {len(self.industry_guidelines)} industry guidelines")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"FeedbackGenerator initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Feedback generation may not function correctly")
            raise
    
    def _load_feedback_templates(self):
        """Load feedback templates for different categories."""
        self.feedback_templates = {
            "content_quality": {
                "excellent": "Your content quality is excellent with clear, professional writing and strong impact.",
                "good": "Your content quality is good but could benefit from more specific details and quantifiable results.",
                "needs_improvement": "Your content quality needs improvement. Focus on adding specific achievements and professional language."
            },
            "ats_compatibility": {
                "excellent": "Your resume is highly ATS-compatible with proper formatting and keyword usage.",
                "good": "Your resume has good ATS compatibility but could benefit from more action verbs and keywords.",
                "needs_improvement": "Your resume needs ATS improvements. Focus on formatting, keywords, and action verbs."
            },
            "skills_relevance": {
                "excellent": "Your skills section is comprehensive and highly relevant to your target industry.",
                "good": "Your skills section is good but could include more industry-specific skills.",
                "needs_improvement": "Your skills section needs enhancement. Add more relevant technical and soft skills."
            },
            "experience_quality": {
                "excellent": "Your work experience is well-presented with strong achievements and quantifiable results.",
                "good": "Your work experience is good but could benefit from more detailed descriptions and metrics.",
                "needs_improvement": "Your work experience needs improvement. Add more detail, action verbs, and quantifiable results."
            },
            "format_structure": {
                "excellent": "Your resume format and structure are professional and well-organized.",
                "good": "Your resume format is good but could benefit from better organization and consistency.",
                "needs_improvement": "Your resume format needs improvement. Focus on consistent formatting and clear structure."
            }
        }
    
    def _load_industry_guidelines(self):
        """Load industry-specific feedback guidelines."""
        self.industry_guidelines = {
            "technology": {
                "focus_areas": ["technical skills", "project outcomes", "technologies used", "certifications"],
                "keywords": ["developed", "implemented", "architected", "optimized", "scaled"],
                "metrics": ["performance improvements", "user growth", "system efficiency", "code quality"],
                "advice": "Emphasize technical achievements, quantify impact, and highlight relevant technologies."
            },
            "finance": {
                "focus_areas": ["financial metrics", "ROI", "risk management", "compliance", "analytics"],
                "keywords": ["analyzed", "managed", "optimized", "increased", "reduced"],
                "metrics": ["revenue growth", "cost savings", "risk reduction", "compliance rates"],
                "advice": "Focus on financial impact, risk management, and regulatory compliance achievements."
            },
            "healthcare": {
                "focus_areas": ["patient outcomes", "quality improvement", "regulatory compliance", "team collaboration"],
                "keywords": ["improved", "enhanced", "delivered", "managed", "coordinated"],
                "metrics": ["patient satisfaction", "quality scores", "efficiency gains", "safety improvements"],
                "advice": "Emphasize patient care, quality improvements, and regulatory compliance achievements."
            },
            "marketing": {
                "focus_areas": ["campaign results", "brand growth", "customer acquisition", "digital metrics"],
                "keywords": ["increased", "launched", "developed", "optimized", "generated"],
                "metrics": ["conversion rates", "engagement", "lead generation", "brand awareness"],
                "advice": "Highlight campaign performance, brand impact, and customer acquisition results."
            },
            "sales": {
                "focus_areas": ["revenue growth", "client relationships", "sales targets", "market expansion"],
                "keywords": ["exceeded", "generated", "increased", "closed", "expanded"],
                "metrics": ["sales targets", "revenue growth", "client retention", "market share"],
                "advice": "Emphasize sales achievements, revenue impact, and client relationship building."
            }
        }
    
    def generate_comprehensive_feedback(self, resume: ParsedResume, analysis_result: AnalysisResult, 
                                      industry: str = None, job_description: str = None) -> List[FeedbackItem]:
        """
        Generate comprehensive feedback for resume with detailed analysis.
        
        Args:
            resume (ParsedResume): Resume to analyze
            analysis_result (AnalysisResult): Analysis results from scoring engine
            industry (str): Target industry for feedback
            job_description (str): Job description for context (optional)
            
        Returns:
            List[FeedbackItem]: Comprehensive feedback items
            
        Raises:
            Exception: If feedback generation fails
        """
        try:
            logger.debug("Generating comprehensive feedback")
            start_time = time.time()
            
            feedback_items = []
            
            # Generate feedback for each scoring category
            if analysis_result.scoring_metrics:
                metrics = analysis_result.scoring_metrics
                
                # Content Quality Feedback
                content_feedback = self._generate_category_feedback(
                    "content_quality", metrics.content_quality, resume, industry
                )
                feedback_items.extend(content_feedback)
                
                # ATS Compatibility Feedback
                ats_feedback = self._generate_category_feedback(
                    "ats_compatibility", metrics.ats_compatibility, resume, industry
                )
                feedback_items.extend(ats_feedback)
                
                # Skills Relevance Feedback
                skills_feedback = self._generate_category_feedback(
                    "skills_relevance", metrics.skills_relevance, resume, industry
                )
                feedback_items.extend(skills_feedback)
                
                # Experience Quality Feedback
                experience_feedback = self._generate_category_feedback(
                    "experience_quality", metrics.experience_quality, resume, industry
                )
                feedback_items.extend(experience_feedback)
                
                # Format Structure Feedback
                format_feedback = self._generate_category_feedback(
                    "format_structure", metrics.format_structure, resume, industry
                )
                feedback_items.extend(format_feedback)
            
            # Generate AI-powered insights
            ai_insights = self._generate_ai_insights(resume, analysis_result, industry, job_description)
            feedback_items.extend(ai_insights)
            
            # Generate industry-specific recommendations
            if industry:
                industry_feedback = self._generate_industry_feedback(resume, industry)
                feedback_items.extend(industry_feedback)
            
            # Generate job-specific feedback
            if job_description:
                job_feedback = self._generate_job_specific_feedback(resume, job_description)
                feedback_items.extend(job_feedback)
            
            # Sort feedback by priority
            feedback_items.sort(key=lambda x: x.priority, reverse=True)
            
            generation_time = time.time() - start_time
            logger.info(f"Comprehensive feedback generated in {generation_time:.2f}s")
            logger.info(f"Generated {len(feedback_items)} feedback items")
            
            return feedback_items
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive feedback: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return []
    
    def _generate_category_feedback(self, category: str, score: float, resume: ParsedResume, 
                                   industry: str = None) -> List[FeedbackItem]:
        """Generate feedback for a specific scoring category."""
        try:
            feedback_items = []
            
            # Determine feedback level based on score
            if score >= 80:
                level = "excellent"
                priority = 3
            elif score >= 60:
                level = "good"
                priority = 2
            else:
                level = "needs_improvement"
                priority = 1
            
            # Get base feedback message
            base_message = self.feedback_templates[category][level]
            
            # Generate specific recommendations
            recommendations = self._get_category_recommendations(category, score, resume, industry)
            
            # Create feedback item
            feedback_item = FeedbackItem(
                category=category,
                title=f"{category.replace('_', ' ').title()} Feedback",
                message=base_message,
                priority=priority,
                recommendations=recommendations,
                score=score,
                improvement_potential=100 - score
            )
            
            feedback_items.append(feedback_item)
            
            # Add specific suggestions if score is low
            if score < 60:
                specific_suggestions = self._get_specific_suggestions(category, resume, industry)
                for suggestion in specific_suggestions:
                    suggestion_item = FeedbackItem(
                        category=category,
                        title=suggestion["title"],
                        message=suggestion["message"],
                        priority=1,
                        recommendations=suggestion["recommendations"],
                        score=score,
                        improvement_potential=suggestion["improvement_potential"]
                    )
                    feedback_items.append(suggestion_item)
            
            return feedback_items
            
        except Exception as e:
            logger.warning(f"Failed to generate category feedback for {category}: {e}")
            return []
    
    def _get_category_recommendations(self, category: str, score: float, resume: ParsedResume, 
                                     industry: str = None) -> List[str]:
        """Get specific recommendations for a category."""
        recommendations = []
        
        if category == "content_quality":
            if score < 60:
                recommendations.extend([
                    "Add a compelling professional summary",
                    "Include quantifiable achievements in work experience",
                    "Use stronger action verbs throughout",
                    "Add more specific details and metrics"
                ])
            elif score < 80:
                recommendations.extend([
                    "Enhance content with more specific achievements",
                    "Add more quantifiable results",
                    "Improve professional language and tone"
                ])
        
        elif category == "ats_compatibility":
            if score < 60:
                recommendations.extend([
                    "Use more ATS-friendly keywords",
                    "Improve formatting and structure",
                    "Add more action verbs",
                    "Ensure consistent bullet point formatting"
                ])
            elif score < 80:
                recommendations.extend([
                    "Optimize keyword density",
                    "Improve section headers",
                    "Add more industry-specific terms"
                ])
        
        elif category == "skills_relevance":
            if score < 60:
                recommendations.extend([
                    "Add more relevant technical skills",
                    "Include industry-specific skills",
                    "Balance technical and soft skills",
                    "Add certifications and training"
                ])
            elif score < 80:
                recommendations.extend([
                    "Add more industry-specific skills",
                    "Include recent technologies",
                    "Add relevant certifications"
                ])
        
        elif category == "experience_quality":
            if score < 60:
                recommendations.extend([
                    "Add detailed descriptions for each role",
                    "Include quantifiable achievements",
                    "Use strong action verbs",
                    "Add more specific responsibilities"
                ])
            elif score < 80:
                recommendations.extend([
                    "Add more quantifiable results",
                    "Include more specific achievements",
                    "Improve action verb usage"
                ])
        
        elif category == "format_structure":
            if score < 60:
                recommendations.extend([
                    "Improve overall formatting consistency",
                    "Add proper section headers",
                    "Use consistent bullet points",
                    "Improve contact information formatting"
                ])
            elif score < 80:
                recommendations.extend([
                    "Improve formatting consistency",
                    "Enhance section organization",
                    "Add more professional formatting"
                ])
        
        return recommendations[:3]  # Limit to top 3 recommendations
    
    def _get_specific_suggestions(self, category: str, resume: ParsedResume, industry: str = None) -> List[Dict[str, Any]]:
        """Get specific improvement suggestions for a category."""
        suggestions = []
        
        if category == "content_quality":
            if not resume.summary or len(resume.summary.strip()) < 50:
                suggestions.append({
                    "title": "Add Professional Summary",
                    "message": "Your resume lacks a compelling professional summary",
                    "recommendations": [
                        "Write a 2-3 sentence summary highlighting your key strengths",
                        "Include years of experience and key skills",
                        "Mention your most significant achievement"
                    ],
                    "improvement_potential": 20
                })
        
        elif category == "ats_compatibility":
            resume_text = self._get_resume_text(resume)
            action_verbs_count = sum(1 for verb in ["achieved", "developed", "implemented", "managed", "led"] 
                                   if verb in resume_text.lower())
            
            if action_verbs_count < 3:
                suggestions.append({
                    "title": "Add More Action Verbs",
                    "message": "Your resume needs more action verbs to strengthen descriptions",
                    "recommendations": [
                        "Start bullet points with action verbs like 'achieved', 'developed', 'implemented'",
                        "Use past tense for completed work",
                        "Avoid weak verbs like 'responsible for' or 'involved in'"
                    ],
                    "improvement_potential": 15
                })
        
        elif category == "skills_relevance":
            if not resume.skills or len(resume.skills) < 5:
                suggestions.append({
                    "title": "Expand Skills Section",
                    "message": "Your skills section needs more comprehensive coverage",
                    "recommendations": [
                        "Add technical skills relevant to your field",
                        "Include soft skills like leadership and communication",
                        "Add certifications and training programs"
                    ],
                    "improvement_potential": 25
                })
        
        return suggestions
    
    def _get_resume_text(self, resume: ParsedResume) -> str:
        """Get combined text from resume for analysis."""
        text_parts = []
        
        if resume.summary:
            text_parts.append(resume.summary)
        
        for exp in resume.work_experience:
            if exp.description:
                text_parts.append(exp.description)
        
        return " ".join(text_parts)
    
    def _generate_ai_insights(self, resume: ParsedResume, analysis_result: AnalysisResult, 
                             industry: str = None, job_description: str = None) -> List[FeedbackItem]:
        """Generate AI-powered insights and recommendations."""
        try:
            insights = []
            
            # Create AI prompt for insights
            prompt = self._create_ai_insights_prompt(resume, analysis_result, industry, job_description)
            
            # Get AI insights
            ai_response = self.ai_handler.generate_text(
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            # Parse AI response into feedback items
            if ai_response:
                insight_item = FeedbackItem(
                    category="ai_insights",
                    title="AI-Powered Insights",
                    message=ai_response,
                    priority=2,
                    recommendations=self._extract_recommendations_from_ai(ai_response),
                    score=analysis_result.overall_score,
                    improvement_potential=100 - analysis_result.overall_score
                )
                insights.append(insight_item)
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate AI insights: {e}")
            return []
    
    def _create_ai_insights_prompt(self, resume: ParsedResume, analysis_result: AnalysisResult, 
                                  industry: str = None, job_description: str = None) -> str:
        """Create prompt for AI insights generation."""
        prompt = f"""
        Analyze this resume and provide specific, actionable feedback for improvement.
        
        Resume Summary:
        - Overall Score: {analysis_result.overall_score}/100
        - Strengths: {', '.join(analysis_result.strengths[:3]) if analysis_result.strengths else 'None identified'}
        - Weaknesses: {', '.join(analysis_result.weaknesses[:3]) if analysis_result.weaknesses else 'None identified'}
        
        """
        
        if industry:
            prompt += f"Target Industry: {industry}\n"
        
        if job_description:
            prompt += f"Job Description Context: {job_description[:200]}...\n"
        
        prompt += """
        
        Please provide:
        1. Specific areas for improvement
        2. Actionable recommendations
        3. Industry-specific advice
        4. Priority areas to focus on
        
        Keep the feedback constructive, specific, and actionable.
        """
        
        return prompt
    
    def _extract_recommendations_from_ai(self, ai_response: str) -> List[str]:
        """Extract recommendations from AI response."""
        try:
            # Simple extraction of recommendations (could be more sophisticated)
            recommendations = []
            lines = ai_response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                    # Clean up the recommendation
                    rec = re.sub(r'^\d+\.\s*|^[-•]\s*', '', line)
                    if rec and len(rec) > 10:
                        recommendations.append(rec)
            
            return recommendations[:5]  # Limit to top 5
            
        except Exception as e:
            logger.warning(f"Failed to extract recommendations from AI response: {e}")
            return []
    
    def _generate_industry_feedback(self, resume: ParsedResume, industry: str) -> List[FeedbackItem]:
        """Generate industry-specific feedback."""
        try:
            if industry.lower() not in self.industry_guidelines:
                return []
            
            guidelines = self.industry_guidelines[industry.lower()]
            feedback_items = []
            
            # Check for industry-specific focus areas
            resume_text = self._get_resume_text(resume).lower()
            
            focus_areas_covered = sum(1 for area in guidelines["focus_areas"] 
                                    if any(word in resume_text for word in area.split()))
            
            if focus_areas_covered < len(guidelines["focus_areas"]) / 2:
                feedback_item = FeedbackItem(
                    category="industry_specific",
                    title=f"{industry} Industry Focus",
                    message=f"Your resume could better align with {industry} industry standards",
                    priority=2,
                    recommendations=[
                        f"Emphasize {guidelines['advice']}",
                        f"Focus on {', '.join(guidelines['focus_areas'][:3])}",
                        f"Use industry keywords like {', '.join(guidelines['keywords'][:3])}"
                    ],
                    score=50,
                    improvement_potential=50
                )
                feedback_items.append(feedback_item)
            
            return feedback_items
            
        except Exception as e:
            logger.warning(f"Failed to generate industry feedback: {e}")
            return []
    
    def _generate_job_specific_feedback(self, resume: ParsedResume, job_description: str) -> List[FeedbackItem]:
        """Generate job-specific feedback based on job description."""
        try:
            feedback_items = []
            
            # Extract keywords from job description
            job_keywords = extract_keywords(job_description)
            resume_text = self._get_resume_text(resume).lower()
            
            # Check keyword alignment
            matching_keywords = [kw for kw in job_keywords if kw.lower() in resume_text]
            keyword_match_percentage = (len(matching_keywords) / len(job_keywords)) * 100 if job_keywords else 0
            
            if keyword_match_percentage < 50:
                feedback_item = FeedbackItem(
                    category="job_specific",
                    title="Job Description Alignment",
                    message="Your resume could better align with the job requirements",
                    priority=1,
                    recommendations=[
                        "Include more keywords from the job description",
                        "Emphasize relevant skills and experience",
                        "Tailor your summary to match the job requirements"
                    ],
                    score=keyword_match_percentage,
                    improvement_potential=100 - keyword_match_percentage
                )
                feedback_items.append(feedback_item)
            
            return feedback_items
            
        except Exception as e:
            logger.warning(f"Failed to generate job-specific feedback: {e}")
            return []
    
    def generate_feedback_summary(self, feedback_items: List[FeedbackItem]) -> Dict[str, Any]:
        """
        Generate summary of feedback items.
        
        Args:
            feedback_items (List[FeedbackItem]): List of feedback items
            
        Returns:
            Dict[str, Any]: Feedback summary with statistics
        """
        try:
            logger.debug("Generating feedback summary")
            
            if not feedback_items:
                return {
                    "total_feedback_items": 0,
                    "high_priority_items": 0,
                    "categories": {},
                    "average_improvement_potential": 0,
                    "summary_timestamp": datetime.now().isoformat()
                }
            
            # Calculate statistics
            total_items = len(feedback_items)
            high_priority_items = sum(1 for item in feedback_items if item.priority == 1)
            average_improvement_potential = sum(item.improvement_potential for item in feedback_items) / total_items
            
            # Categorize feedback
            categories = {}
            for item in feedback_items:
                category = item.category
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            # Get top recommendations
            all_recommendations = []
            for item in feedback_items:
                all_recommendations.extend(item.recommendations)
            
            # Count recommendation frequency
            rec_counts = {}
            for rec in all_recommendations:
                rec_counts[rec] = rec_counts.get(rec, 0) + 1
            
            # Get top 5 most common recommendations
            top_recommendations = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            summary = {
                "total_feedback_items": total_items,
                "high_priority_items": high_priority_items,
                "categories": categories,
                "average_improvement_potential": round(average_improvement_potential, 1),
                "top_recommendations": [rec for rec, count in top_recommendations],
                "summary_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Feedback summary generated: {total_items} items")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate feedback summary: {e}")
            return {
                "total_feedback_items": 0,
                "high_priority_items": 0,
                "categories": {},
                "average_improvement_potential": 0,
                "summary_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
