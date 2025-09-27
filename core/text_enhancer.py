"""
Text Enhancement Module for Resume/CV AI Application
Handles AI-powered text improvement and content optimization.

This module provides:
- AI-powered text enhancement and improvement
- Content optimization for different industries
- Grammar and language improvement
- Achievement quantification assistance
- Professional tone enhancement
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import re
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json

from models.resume_model import ParsedResume, WorkExperience
from models.analysis_model import EnhancementSuggestion
from core.ai_handler import AIHandler
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("text_enhancer")

class TextEnhancer:
    """
    Advanced text enhancement and optimization with comprehensive logging.
    
    This class provides sophisticated text improvement capabilities including
    AI-powered content enhancement, industry-specific optimization, grammar
    improvement, and achievement quantification assistance.
    
    Key Features:
    - AI-powered text enhancement and improvement
    - Industry-specific content optimization
    - Grammar and language improvement
    - Achievement quantification assistance
    - Professional tone enhancement
    - Comprehensive logging and error handling
    
    Attributes:
        ai_handler (AIHandler): AI handler instance for content analysis
        enhancement_templates (Dict): Templates for different enhancement types
        industry_guidelines (Dict): Industry-specific writing guidelines
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, ai_handler: AIHandler):
        """
        Initialize the TextEnhancer with comprehensive logging.
        
        Args:
            ai_handler (AIHandler): AI handler instance for content analysis
            
        Raises:
            Exception: If TextEnhancer initialization fails
        """
        logger.info("Initializing TextEnhancer")
        self._initialization_time = time.time()
        
        # Initialize AI handler
        self.ai_handler = ai_handler
        
        # Initialize enhancement templates and guidelines
        self.enhancement_templates = {}
        self.industry_guidelines = {}
        
        try:
            # Load enhancement templates and guidelines
            logger.debug("Loading enhancement templates and guidelines")
            self._load_enhancement_templates()
            self._load_industry_guidelines()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"TextEnhancer initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.enhancement_templates)} enhancement templates")
            logger.info(f"Loaded {len(self.industry_guidelines)} industry guidelines")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"TextEnhancer initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Text enhancement may not function correctly")
            raise
    
    def _load_enhancement_templates(self):
        """Load enhancement templates for different content types."""
        self.enhancement_templates = {
            "professional_summary": {
                "template": "Experienced {role} with {years} years of expertise in {skills}. Proven track record of {achievements}. Skilled in {technologies} with strong background in {industry}.",
                "guidelines": [
                    "Keep it concise (2-3 sentences)",
                    "Include years of experience",
                    "Mention key skills and technologies",
                    "Highlight major achievements",
                    "Use action verbs and quantifiable results"
                ]
            },
            "work_experience": {
                "template": "• {action_verb} {achievement} resulting in {quantifiable_result}",
                "guidelines": [
                    "Start with strong action verbs",
                    "Include quantifiable achievements",
                    "Focus on results and impact",
                    "Use industry-specific terminology",
                    "Keep bullet points concise but impactful"
                ]
            },
            "skills_section": {
                "template": "{category}: {skills_list}",
                "guidelines": [
                    "Group related skills together",
                    "List most relevant skills first",
                    "Include both technical and soft skills",
                    "Use industry-standard terminology",
                    "Keep the list scannable"
                ]
            },
            "education": {
                "template": "{degree} in {field} - {institution} ({year})",
                "guidelines": [
                    "Include degree, field, institution, and year",
                    "List in reverse chronological order",
                    "Include relevant coursework or projects",
                    "Add honors or achievements if applicable"
                ]
            }
        }
    
    def _load_industry_guidelines(self):
        """Load industry-specific writing guidelines."""
        self.industry_guidelines = {
            "technology": {
                "tone": "Technical and innovative",
                "keywords": ["developed", "implemented", "architected", "optimized", "scaled"],
                "focus_areas": ["technical skills", "project outcomes", "technologies used"],
                "avoid": ["buzzwords without context", "vague descriptions"]
            },
            "finance": {
                "tone": "Professional and analytical",
                "keywords": ["analyzed", "managed", "optimized", "increased", "reduced"],
                "focus_areas": ["financial metrics", "ROI", "risk management", "compliance"],
                "avoid": ["unsubstantiated claims", "vague financial terms"]
            },
            "healthcare": {
                "tone": "Compassionate and precise",
                "keywords": ["improved", "enhanced", "delivered", "managed", "coordinated"],
                "focus_areas": ["patient outcomes", "quality improvement", "regulatory compliance"],
                "avoid": ["medical jargon without explanation", "unverified claims"]
            },
            "marketing": {
                "tone": "Creative and results-driven",
                "keywords": ["increased", "launched", "developed", "optimized", "generated"],
                "focus_areas": ["campaign results", "brand growth", "customer acquisition"],
                "avoid": ["vague metrics", "unsubstantiated growth claims"]
            },
            "sales": {
                "tone": "Achievement-oriented and persuasive",
                "keywords": ["exceeded", "generated", "increased", "closed", "expanded"],
                "focus_areas": ["revenue growth", "client relationships", "sales targets"],
                "avoid": ["unrealistic claims", "vague performance metrics"]
            }
        }
    
    def enhance_text(self, text: str, enhancement_type: str, industry: str = None, context: Dict[str, Any] = None) -> EnhancementSuggestion:
        """
        Enhance text content using AI with comprehensive logging.
        
        Args:
            text (str): Text content to enhance
            enhancement_type (str): Type of enhancement (summary, experience, skills, etc.)
            industry (str): Target industry for optimization
            context (Dict[str, Any]): Additional context for enhancement
            
        Returns:
            EnhancementSuggestion: Enhancement suggestion with improved text
            
        Raises:
            Exception: If text enhancement fails
        """
        try:
            logger.debug(f"Enhancing text (type: {enhancement_type}, industry: {industry})")
            start_time = time.time()
            
            # Get industry guidelines
            guidelines = self.industry_guidelines.get(industry, {}) if industry else {}
            
            # Generate enhancement prompt
            prompt = self._create_enhancement_prompt(text, enhancement_type, industry, guidelines, context)
            
            # Get AI enhancement
            enhanced_text = self.ai_handler.generate_text(
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            # Calculate improvement metrics
            improvement_score = self._calculate_improvement_score(text, enhanced_text, enhancement_type)
            
            # Generate enhancement suggestion
            suggestion = EnhancementSuggestion(
                title=f"Enhanced {enhancement_type.replace('_', ' ').title()}",
                category=enhancement_type,
                current_text=text,
                suggested_text=enhanced_text,
                impact_score=improvement_score,
                effort_level="Low",
                description=f"AI-enhanced version optimized for {industry or 'general'} industry",
                examples=self._get_enhancement_examples(enhancement_type),
                reasoning=self._generate_enhancement_reasoning(text, enhanced_text, guidelines)
            )
            
            enhancement_time = time.time() - start_time
            logger.info(f"Text enhancement completed in {enhancement_time:.2f}s")
            logger.info(f"Improvement score: {improvement_score}/10")
            
            return suggestion
            
        except Exception as e:
            logger.error(f"Failed to enhance text: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return EnhancementSuggestion(
                title="Enhancement Failed",
                category=enhancement_type,
                current_text=text,
                suggested_text=text,
                impact_score=0,
                effort_level="High",
                description="Enhancement failed due to an error",
                examples=[],
                reasoning="Unable to generate enhancement due to technical error"
            )
    
    def _create_enhancement_prompt(self, text: str, enhancement_type: str, industry: str, guidelines: Dict, context: Dict) -> str:
        """Create enhancement prompt for AI."""
        base_prompt = f"""
        Please enhance the following {enhancement_type} text to make it more professional, impactful, and ATS-friendly.
        
        Original text:
        {text}
        
        Enhancement requirements:
        - Make it more concise and impactful
        - Use strong action verbs
        - Include quantifiable achievements where possible
        - Ensure ATS compatibility
        - Maintain professional tone
        """
        
        if industry and guidelines:
            base_prompt += f"""
        
        Industry-specific requirements for {industry}:
        - Tone: {guidelines.get('tone', 'Professional')}
        - Preferred keywords: {', '.join(guidelines.get('keywords', []))}
        - Focus areas: {', '.join(guidelines.get('focus_areas', []))}
        - Avoid: {', '.join(guidelines.get('avoid', []))}
        """
        
        if context:
            base_prompt += f"""
        
        Additional context:
        {json.dumps(context, indent=2)}
        """
        
        base_prompt += """
        
        Please provide the enhanced version that:
        1. Is more compelling and professional
        2. Uses industry-appropriate language
        3. Includes quantifiable results where possible
        4. Is optimized for ATS systems
        5. Maintains the original meaning while improving impact
        
        Enhanced text:
        """
        
        return base_prompt
    
    def _calculate_improvement_score(self, original: str, enhanced: str, enhancement_type: str) -> int:
        """Calculate improvement score (1-10) for enhanced text."""
        try:
            score = 5  # Base score
            
            # Length improvement (not too short, not too long)
            original_length = len(original.split())
            enhanced_length = len(enhanced.split())
            
            if enhancement_type == "professional_summary":
                if 20 <= enhanced_length <= 50:  # Good length for summary
                    score += 1
            elif enhancement_type == "work_experience":
                if 10 <= enhanced_length <= 25:  # Good length for bullet point
                    score += 1
            
            # Action verb usage
            action_verbs = ["achieved", "developed", "implemented", "managed", "led", "created", "improved", "increased", "reduced", "optimized"]
            enhanced_action_verbs = sum(1 for verb in action_verbs if verb in enhanced.lower())
            if enhanced_action_verbs > 0:
                score += min(2, enhanced_action_verbs)
            
            # Quantifiable results
            quantifiable_patterns = [r'\d+%', r'\$\d+', r'\d+x', r'\d+ years', r'\d+ people', r'\d+ projects']
            enhanced_quantifiable = sum(1 for pattern in quantifiable_patterns if re.search(pattern, enhanced))
            if enhanced_quantifiable > 0:
                score += min(2, enhanced_quantifiable)
            
            # Professional language
            professional_words = ["strategic", "comprehensive", "innovative", "collaborative", "proven", "expertise", "proficiency"]
            enhanced_professional = sum(1 for word in professional_words if word in enhanced.lower())
            if enhanced_professional > 0:
                score += 1
            
            return min(10, max(1, score))
            
        except Exception as e:
            logger.warning(f"Failed to calculate improvement score: {e}")
            return 5
    
    def _get_enhancement_examples(self, enhancement_type: str) -> List[str]:
        """Get examples for enhancement type."""
        examples = {
            "professional_summary": [
                "Before: 'Experienced software developer with good skills.'",
                "After: 'Senior Software Developer with 5+ years of expertise in full-stack development, delivering scalable solutions that increased system performance by 40%.'"
            ],
            "work_experience": [
                "Before: 'Worked on various projects and helped improve things.'",
                "After: '• Architected and implemented microservices solution, reducing API response time by 60% and improving system scalability.'"
            ],
            "skills_section": [
                "Before: 'Good at programming and problem solving'",
                "After: 'Technical Skills: Python, Java, React, AWS, Docker, Kubernetes, SQL, Git'"
            ]
        }
        
        return examples.get(enhancement_type, [])
    
    def _generate_enhancement_reasoning(self, original: str, enhanced: str, guidelines: Dict) -> str:
        """Generate reasoning for enhancement suggestions."""
        reasoning_parts = []
        
        # Length improvement
        original_words = len(original.split())
        enhanced_words = len(enhanced.split())
        if enhanced_words > original_words:
            reasoning_parts.append(f"Expanded from {original_words} to {enhanced_words} words for better detail")
        elif enhanced_words < original_words:
            reasoning_parts.append(f"Condensed from {original_words} to {enhanced_words} words for conciseness")
        
        # Action verb improvement
        action_verbs = ["achieved", "developed", "implemented", "managed", "led", "created", "improved", "increased", "reduced", "optimized"]
        original_verbs = sum(1 for verb in action_verbs if verb in original.lower())
        enhanced_verbs = sum(1 for verb in action_verbs if verb in enhanced.lower())
        if enhanced_verbs > original_verbs:
            reasoning_parts.append(f"Increased action verbs from {original_verbs} to {enhanced_verbs}")
        
        # Quantifiable results
        quantifiable_patterns = [r'\d+%', r'\$\d+', r'\d+x', r'\d+ years', r'\d+ people', r'\d+ projects']
        original_quantifiable = sum(1 for pattern in quantifiable_patterns if re.search(pattern, original))
        enhanced_quantifiable = sum(1 for pattern in quantifiable_patterns if re.search(pattern, enhanced))
        if enhanced_quantifiable > original_quantifiable:
            reasoning_parts.append(f"Added {enhanced_quantifiable - original_quantifiable} quantifiable metrics")
        
        # Industry-specific improvements
        if guidelines:
            tone = guidelines.get('tone', '')
            if tone:
                reasoning_parts.append(f"Adjusted tone to be more {tone}")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "General improvements for clarity and impact"
    
    def enhance_resume_section(self, resume: ParsedResume, section: str, industry: str = None) -> List[EnhancementSuggestion]:
        """
        Enhance specific resume section with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume object to enhance
            section (str): Section to enhance (summary, experience, skills, education)
            industry (str): Target industry for optimization
            
        Returns:
            List[EnhancementSuggestion]: List of enhancement suggestions
        """
        try:
            logger.debug(f"Enhancing resume section: {section}")
            start_time = time.time()
            
            suggestions = []
            
            if section == "summary" and resume.summary:
                suggestion = self.enhance_text(
                    text=resume.summary,
                    enhancement_type="professional_summary",
                    industry=industry,
                    context={"years_experience": len(resume.work_experience)}
                )
                suggestions.append(suggestion)
            
            elif section == "experience" and resume.work_experience:
                for i, exp in enumerate(resume.work_experience):
                    if exp.description:
                        suggestion = self.enhance_text(
                            text=exp.description,
                            enhancement_type="work_experience",
                            industry=industry,
                            context={
                                "job_title": exp.title,
                                "company": exp.company,
                                "duration": f"{exp.start_date} - {exp.end_date}" if exp.start_date and exp.end_date else "Unknown"
                            }
                        )
                        suggestion.title = f"Enhanced Experience: {exp.title} at {exp.company}"
                        suggestions.append(suggestion)
            
            elif section == "skills" and resume.skills:
                # Group skills by category
                skills_by_category = {}
                for skill in resume.skills:
                    category = skill.subcategory or skill.category.value
                    if category not in skills_by_category:
                        skills_by_category[category] = []
                    skills_by_category[category].append(skill.name)
                
                for category, skills_list in skills_by_category.items():
                    skills_text = f"{category}: {', '.join(skills_list)}"
                    suggestion = self.enhance_text(
                        text=skills_text,
                        enhancement_type="skills_section",
                        industry=industry,
                        context={"category": category, "skill_count": len(skills_list)}
                    )
                    suggestion.title = f"Enhanced Skills: {category}"
                    suggestions.append(suggestion)
            
            elif section == "education" and resume.education:
                for edu in resume.education:
                    education_text = f"{edu.degree} in {edu.field} - {edu.institution}"
                    if edu.graduation_date:
                        education_text += f" ({edu.graduation_date})"
                    
                    suggestion = self.enhance_text(
                        text=education_text,
                        enhancement_type="education",
                        industry=industry,
                        context={
                            "degree": edu.degree,
                            "field": edu.field,
                            "institution": edu.institution
                        }
                    )
                    suggestion.title = f"Enhanced Education: {edu.degree}"
                    suggestions.append(suggestion)
            
            enhancement_time = time.time() - start_time
            logger.info(f"Resume section enhancement completed in {enhancement_time:.2f}s")
            logger.info(f"Generated {len(suggestions)} enhancement suggestions")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to enhance resume section: {e}")
            return []
    
    def enhance_achievements(self, achievements: List[str], industry: str = None) -> List[EnhancementSuggestion]:
        """
        Enhance achievement statements with quantifiable results.
        
        Args:
            achievements (List[str]): List of achievement statements
            industry (str): Target industry for optimization
            
        Returns:
            List[EnhancementSuggestion]: List of enhanced achievement suggestions
        """
        try:
            logger.debug(f"Enhancing {len(achievements)} achievements")
            start_time = time.time()
            
            suggestions = []
            
            for i, achievement in enumerate(achievements):
                if not achievement.strip():
                    continue
                
                # Create context for achievement enhancement
                context = {
                    "achievement_number": i + 1,
                    "total_achievements": len(achievements),
                    "original_achievement": achievement
                }
                
                suggestion = self.enhance_text(
                    text=achievement,
                    enhancement_type="work_experience",  # Use work experience template for achievements
                    industry=industry,
                    context=context
                )
                suggestion.title = f"Enhanced Achievement #{i + 1}"
                suggestion.description = "AI-enhanced achievement with quantifiable results and stronger impact"
                suggestions.append(suggestion)
            
            enhancement_time = time.time() - start_time
            logger.info(f"Achievement enhancement completed in {enhancement_time:.2f}s")
            logger.info(f"Enhanced {len(suggestions)} achievements")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to enhance achievements: {e}")
            return []
    
    def get_enhancement_summary(self, suggestions: List[EnhancementSuggestion]) -> Dict[str, Any]:
        """
        Get summary of enhancement suggestions.
        
        Args:
            suggestions (List[EnhancementSuggestion]): List of enhancement suggestions
            
        Returns:
            Dict[str, Any]: Enhancement summary with statistics
        """
        try:
            logger.debug("Generating enhancement summary")
            
            if not suggestions:
                return {
                    "total_suggestions": 0,
                    "average_impact_score": 0,
                    "categories": {},
                    "high_impact_suggestions": 0,
                    "summary_timestamp": datetime.now().isoformat()
                }
            
            # Calculate statistics
            total_suggestions = len(suggestions)
            average_impact_score = sum(s.impact_score for s in suggestions) / total_suggestions
            high_impact_suggestions = sum(1 for s in suggestions if s.impact_score >= 8)
            
            # Categorize suggestions
            categories = {}
            for suggestion in suggestions:
                category = suggestion.category
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            # Get top suggestions
            top_suggestions = sorted(suggestions, key=lambda x: x.impact_score, reverse=True)[:5]
            
            summary = {
                "total_suggestions": total_suggestions,
                "average_impact_score": round(average_impact_score, 2),
                "high_impact_suggestions": high_impact_suggestions,
                "categories": categories,
                "top_suggestions": [
                    {
                        "title": s.title,
                        "impact_score": s.impact_score,
                        "category": s.category
                    }
                    for s in top_suggestions
                ],
                "summary_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Enhancement summary generated: {total_suggestions} suggestions")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate enhancement summary: {e}")
            return {
                "total_suggestions": 0,
                "average_impact_score": 0,
                "categories": {},
                "high_impact_suggestions": 0,
                "summary_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
