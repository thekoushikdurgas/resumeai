"""
Career Advisor Module for Resume/CV AI Application
Handles career guidance and professional development recommendations.

This module provides:
- Career path analysis and recommendations
- Industry trend analysis
- Skills development guidance
- Salary insights and benchmarking
- Professional development planning
- Comprehensive logging and error handling

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json

from models.resume_model import ParsedResume, Skill, SkillCategory
from models.analysis_model import CareerInsight, CareerRecommendation
from core.ai_handler import AIHandler
from core.scoring_engine import ScoringEngine
from utils.helpers import clean_text, extract_keywords
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("career_advisor")

class CareerAdvisor:
    """
    Advanced career advisor with comprehensive logging.
    
    This class provides sophisticated career guidance capabilities including
    career path analysis, industry trend insights, skills development
    recommendations, and professional development planning.
    
    Key Features:
    - Career path analysis and recommendations
    - Industry trend analysis
    - Skills development guidance
    - Salary insights and benchmarking
    - Professional development planning
    - Comprehensive logging and error handling
    
    Attributes:
        ai_handler (AIHandler): AI handler instance for content analysis
        scoring_engine (ScoringEngine): Scoring engine for evaluation
        career_paths (Dict): Career path templates and progressions
        industry_trends (Dict): Industry trend data and insights
        salary_data (Dict): Salary benchmarking data
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, ai_handler: AIHandler, scoring_engine: ScoringEngine):
        """
        Initialize the CareerAdvisor with comprehensive logging.
        
        Args:
            ai_handler (AIHandler): AI handler instance for content analysis
            scoring_engine (ScoringEngine): Scoring engine for evaluation
            
        Raises:
            Exception: If CareerAdvisor initialization fails
        """
        logger.info("Initializing CareerAdvisor")
        self._initialization_time = time.time()
        
        # Initialize dependencies
        self.ai_handler = ai_handler
        self.scoring_engine = scoring_engine
        
        # Initialize career guidance data
        self.career_paths = {}
        self.industry_trends = {}
        self.salary_data = {}
        self.skills_roadmap = {}
        
        try:
            # Load career guidance data
            logger.debug("Loading career guidance data")
            self._load_career_paths()
            self._load_industry_trends()
            self._load_salary_data()
            self._load_skills_roadmap()
            
            initialization_time = time.time() - self._initialization_time
            logger.info(f"CareerAdvisor initialized successfully in {initialization_time:.2f}s")
            logger.info(f"Loaded {len(self.career_paths)} career paths")
            logger.info(f"Loaded {len(self.industry_trends)} industry trends")
            logger.info(f"Loaded {len(self.salary_data)} salary benchmarks")
            
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"CareerAdvisor initialization failed after {initialization_time:.2f}s: {e}")
            logger.error("Career guidance may not function correctly")
            raise
    
    def _load_career_paths(self):
        """Load career path templates and progressions."""
        self.career_paths = {
            "technology": {
                "entry_level": ["Junior Developer", "Software Engineer I", "Associate Developer"],
                "mid_level": ["Software Engineer II", "Senior Developer", "Tech Lead"],
                "senior_level": ["Senior Software Engineer", "Principal Engineer", "Staff Engineer"],
                "leadership": ["Engineering Manager", "Director of Engineering", "VP of Engineering"],
                "specializations": ["Frontend", "Backend", "Full Stack", "DevOps", "Data Science", "AI/ML"]
            },
            "finance": {
                "entry_level": ["Financial Analyst", "Junior Accountant", "Investment Analyst"],
                "mid_level": ["Senior Financial Analyst", "Senior Accountant", "Portfolio Manager"],
                "senior_level": ["Finance Manager", "Senior Portfolio Manager", "Risk Manager"],
                "leadership": ["CFO", "Director of Finance", "VP of Finance"],
                "specializations": ["Investment Banking", "Corporate Finance", "Risk Management", "Accounting"]
            },
            "healthcare": {
                "entry_level": ["Nurse", "Medical Assistant", "Lab Technician"],
                "mid_level": ["Senior Nurse", "Nurse Practitioner", "Physician Assistant"],
                "senior_level": ["Nurse Manager", "Clinical Director", "Medical Director"],
                "leadership": ["Chief Nursing Officer", "Chief Medical Officer", "VP of Clinical Operations"],
                "specializations": ["Emergency Medicine", "Pediatrics", "Surgery", "Mental Health"]
            },
            "marketing": {
                "entry_level": ["Marketing Coordinator", "Digital Marketing Specialist", "Content Creator"],
                "mid_level": ["Marketing Manager", "Digital Marketing Manager", "Brand Manager"],
                "senior_level": ["Senior Marketing Manager", "Marketing Director", "Head of Marketing"],
                "leadership": ["CMO", "VP of Marketing", "Chief Growth Officer"],
                "specializations": ["Digital Marketing", "Brand Management", "Content Marketing", "Growth Marketing"]
            }
        }
    
    def _load_industry_trends(self):
        """Load industry trend data and insights."""
        self.industry_trends = {
            "technology": {
                "growth_rate": 15.2,
                "hot_skills": ["AI/ML", "Cloud Computing", "Cybersecurity", "DevOps", "Data Science"],
                "emerging_roles": ["AI Engineer", "Cloud Architect", "DevSecOps Engineer", "Data Engineer"],
                "salary_trends": "Increasing",
                "job_market": "High demand",
                "future_outlook": "Very positive with continued growth expected"
            },
            "finance": {
                "growth_rate": 8.5,
                "hot_skills": ["FinTech", "Blockchain", "Data Analytics", "Risk Management", "Compliance"],
                "emerging_roles": ["FinTech Analyst", "Blockchain Developer", "Quantitative Analyst", "Risk Analyst"],
                "salary_trends": "Stable with bonuses",
                "job_market": "Moderate demand",
                "future_outlook": "Stable with growth in FinTech"
            },
            "healthcare": {
                "growth_rate": 12.8,
                "hot_skills": ["Telemedicine", "Health Informatics", "AI in Healthcare", "Patient Care", "Regulatory"],
                "emerging_roles": ["Health Informatics Specialist", "Telemedicine Coordinator", "AI Healthcare Analyst"],
                "salary_trends": "Increasing",
                "job_market": "High demand",
                "future_outlook": "Very positive due to aging population"
            },
            "marketing": {
                "growth_rate": 10.3,
                "hot_skills": ["Digital Marketing", "Marketing Automation", "Data Analytics", "Content Marketing", "SEO/SEM"],
                "emerging_roles": ["Marketing Automation Specialist", "Growth Hacker", "Content Strategist", "SEO Specialist"],
                "salary_trends": "Increasing",
                "job_market": "High demand",
                "future_outlook": "Positive with digital transformation"
            }
        }
    
    def _load_salary_data(self):
        """Load salary benchmarking data."""
        self.salary_data = {
            "technology": {
                "entry_level": {"min": 60000, "max": 85000, "median": 72000},
                "mid_level": {"min": 85000, "max": 130000, "median": 105000},
                "senior_level": {"min": 130000, "max": 180000, "median": 155000},
                "leadership": {"min": 180000, "max": 300000, "median": 240000}
            },
            "finance": {
                "entry_level": {"min": 50000, "max": 70000, "median": 60000},
                "mid_level": {"min": 70000, "max": 110000, "median": 90000},
                "senior_level": {"min": 110000, "max": 160000, "median": 135000},
                "leadership": {"min": 160000, "max": 250000, "median": 205000}
            },
            "healthcare": {
                "entry_level": {"min": 45000, "max": 65000, "median": 55000},
                "mid_level": {"min": 65000, "max": 95000, "median": 80000},
                "senior_level": {"min": 95000, "max": 140000, "median": 117500},
                "leadership": {"min": 140000, "max": 220000, "median": 180000}
            },
            "marketing": {
                "entry_level": {"min": 40000, "max": 60000, "median": 50000},
                "mid_level": {"min": 60000, "max": 90000, "median": 75000},
                "senior_level": {"min": 90000, "max": 130000, "median": 110000},
                "leadership": {"min": 130000, "max": 200000, "median": 165000}
            }
        }
    
    def _load_skills_roadmap(self):
        """Load skills development roadmap data."""
        self.skills_roadmap = {
            "technology": {
                "foundational": ["Programming Fundamentals", "Data Structures", "Algorithms", "Version Control"],
                "intermediate": ["Framework Knowledge", "Database Design", "API Development", "Testing"],
                "advanced": ["System Design", "Cloud Architecture", "DevOps", "Security"],
                "leadership": ["Team Management", "Project Management", "Technical Strategy", "Mentoring"]
            },
            "finance": {
                "foundational": ["Financial Analysis", "Accounting Principles", "Excel", "Financial Modeling"],
                "intermediate": ["Risk Management", "Investment Analysis", "Regulatory Compliance", "Data Analysis"],
                "advanced": ["Portfolio Management", "Derivatives", "Quantitative Analysis", "FinTech"],
                "leadership": ["Team Leadership", "Strategic Planning", "Stakeholder Management", "Risk Strategy"]
            },
            "healthcare": {
                "foundational": ["Medical Knowledge", "Patient Care", "Healthcare Systems", "Medical Terminology"],
                "intermediate": ["Clinical Procedures", "Healthcare Technology", "Regulatory Compliance", "Quality Improvement"],
                "advanced": ["Healthcare Informatics", "Telemedicine", "AI in Healthcare", "Population Health"],
                "leadership": ["Clinical Leadership", "Healthcare Management", "Policy Development", "Team Coordination"]
            },
            "marketing": {
                "foundational": ["Marketing Principles", "Digital Marketing", "Content Creation", "Analytics"],
                "intermediate": ["Campaign Management", "SEO/SEM", "Social Media", "Marketing Automation"],
                "advanced": ["Growth Marketing", "Data Science", "AI in Marketing", "Brand Strategy"],
                "leadership": ["Marketing Strategy", "Team Leadership", "Budget Management", "Stakeholder Relations"]
            }
        }
    
    def analyze_career_path(self, resume: ParsedResume, target_industry: str = None) -> List[CareerInsight]:
        """
        Analyze career path and provide insights with comprehensive logging.
        
        Args:
            resume (ParsedResume): Resume to analyze
            target_industry (str): Target industry for analysis (optional)
            
        Returns:
            List[CareerInsight]: Career path insights and recommendations
            
        Raises:
            Exception: If career path analysis fails
        """
        try:
            logger.debug("Analyzing career path")
            start_time = time.time()
            
            insights = []
            
            # Determine current career level
            current_level = self._determine_career_level(resume)
            
            # Analyze career progression
            progression_insight = self._analyze_career_progression(resume, current_level, target_industry)
            if progression_insight:
                insights.append(progression_insight)
            
            # Analyze skills alignment
            skills_insight = self._analyze_skills_alignment(resume, target_industry)
            if skills_insight:
                insights.append(skills_insight)
            
            # Analyze industry trends
            trends_insight = self._analyze_industry_trends(resume, target_industry)
            if trends_insight:
                insights.append(trends_insight)
            
            # Generate career recommendations
            recommendations = self._generate_career_recommendations(resume, current_level, target_industry)
            for rec in recommendations:
                insights.append(rec)
            
            analysis_time = time.time() - start_time
            logger.info(f"Career path analysis completed in {analysis_time:.2f}s")
            logger.info(f"Generated {len(insights)} career insights")
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to analyze career path: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return []
    
    def _determine_career_level(self, resume: ParsedResume) -> str:
        """Determine current career level based on resume."""
        try:
            # Analyze work experience
            exp_count = len(resume.work_experience) if resume.work_experience else 0
            
            # Analyze job titles for level indicators
            level_indicators = {
                "entry": ["junior", "associate", "assistant", "coordinator", "specialist"],
                "mid": ["senior", "lead", "manager", "analyst", "consultant"],
                "senior": ["principal", "staff", "director", "head", "chief"],
                "leadership": ["vp", "vice president", "ceo", "cto", "cfo", "cmo"]
            }
            
            if exp_count == 0:
                return "entry"
            
            # Check job titles for level indicators
            for exp in resume.work_experience:
                if exp.title:
                    title_lower = exp.title.lower()
                    for level, indicators in level_indicators.items():
                        if any(indicator in title_lower for indicator in indicators):
                            return level
            
            # Fallback to experience count
            if exp_count <= 2:
                return "entry"
            elif exp_count <= 5:
                return "mid"
            elif exp_count <= 10:
                return "senior"
            else:
                return "leadership"
                
        except Exception as e:
            logger.warning(f"Failed to determine career level: {e}")
            return "mid"
    
    def _analyze_career_progression(self, resume: ParsedResume, current_level: str, target_industry: str = None) -> Optional[CareerInsight]:
        """Analyze career progression and next steps."""
        try:
            if not target_industry or target_industry.lower() not in self.career_paths:
                return None
            
            career_path = self.career_paths[target_industry.lower()]
            
            # Get next level positions
            level_mapping = {
                "entry": "mid_level",
                "mid": "senior_level", 
                "senior": "leadership",
                "leadership": "leadership"
            }
            
            next_level = level_mapping.get(current_level, "mid_level")
            next_positions = career_path.get(next_level, [])
            
            if not next_positions:
                return None
            
            # Generate progression insight
            insight = CareerInsight(
                title="Career Progression Analysis",
                description=f"Based on your current level ({current_level}), here are potential next steps in {target_industry}",
                category="career_progression",
                priority=2,
                recommendations=[
                    f"Consider targeting {next_positions[0]} positions",
                    f"Develop skills relevant to {next_level.replace('_', ' ')} roles",
                    f"Gain experience in {', '.join(career_path.get('specializations', [])[:3])}"
                ],
                industry=target_industry,
                confidence=0.8
            )
            
            return insight
            
        except Exception as e:
            logger.warning(f"Failed to analyze career progression: {e}")
            return None
    
    def _analyze_skills_alignment(self, resume: ParsedResume, target_industry: str = None) -> Optional[CareerInsight]:
        """Analyze skills alignment with industry requirements."""
        try:
            if not target_industry or target_industry.lower() not in self.skills_roadmap:
                return None
            
            skills_roadmap = self.skills_roadmap[target_industry.lower()]
            resume_skills = [skill.name.lower() for skill in resume.skills] if resume.skills else []
            
            # Check skills alignment
            foundational_skills = skills_roadmap.get("foundational", [])
            intermediate_skills = skills_roadmap.get("intermediate", [])
            advanced_skills = skills_roadmap.get("advanced", [])
            
            foundational_covered = sum(1 for skill in foundational_skills 
                                     if any(rs in skill.lower() or skill.lower() in rs for rs in resume_skills))
            intermediate_covered = sum(1 for skill in intermediate_skills 
                                     if any(rs in skill.lower() or skill.lower() in rs for rs in resume_skills))
            advanced_covered = sum(1 for skill in advanced_skills 
                                 if any(rs in skill.lower() or skill.lower() in rs for rs in resume_skills))
            
            # Generate recommendations
            recommendations = []
            if foundational_covered < len(foundational_skills) * 0.7:
                recommendations.append(f"Strengthen foundational skills: {', '.join(foundational_skills[:3])}")
            
            if intermediate_covered < len(intermediate_skills) * 0.5:
                recommendations.append(f"Develop intermediate skills: {', '.join(intermediate_skills[:3])}")
            
            if advanced_covered < len(advanced_skills) * 0.3:
                recommendations.append(f"Consider advanced skills: {', '.join(advanced_skills[:3])}")
            
            if not recommendations:
                recommendations.append("Your skills are well-aligned with industry requirements")
            
            insight = CareerInsight(
                title="Skills Alignment Analysis",
                description=f"Analysis of your skills against {target_industry} industry requirements",
                category="skills_alignment",
                priority=1,
                recommendations=recommendations,
                industry=target_industry,
                confidence=0.9
            )
            
            return insight
            
        except Exception as e:
            logger.warning(f"Failed to analyze skills alignment: {e}")
            return None
    
    def _analyze_industry_trends(self, resume: ParsedResume, target_industry: str = None) -> Optional[CareerInsight]:
        """Analyze industry trends and opportunities."""
        try:
            if not target_industry or target_industry.lower() not in self.industry_trends:
                return None
            
            trends = self.industry_trends[target_industry.lower()]
            
            # Generate trend insights
            recommendations = [
                f"Industry growth rate: {trends['growth_rate']}% annually",
                f"Hot skills to develop: {', '.join(trends['hot_skills'][:3])}",
                f"Emerging roles: {', '.join(trends['emerging_roles'][:2])}",
                f"Job market outlook: {trends['job_market']}"
            ]
            
            insight = CareerInsight(
                title="Industry Trends Analysis",
                description=f"Current trends and opportunities in {target_industry}",
                category="industry_trends",
                priority=2,
                recommendations=recommendations,
                industry=target_industry,
                confidence=0.85
            )
            
            return insight
            
        except Exception as e:
            logger.warning(f"Failed to analyze industry trends: {e}")
            return None
    
    def _generate_career_recommendations(self, resume: ParsedResume, current_level: str, target_industry: str = None) -> List[CareerInsight]:
        """Generate specific career recommendations."""
        try:
            recommendations = []
            
            # Skills development recommendation
            skills_rec = CareerInsight(
                title="Skills Development Plan",
                description="Recommended skills to develop for career advancement",
                category="skills_development",
                priority=1,
                recommendations=[
                    "Identify skill gaps in your current role",
                    "Take online courses or certifications",
                    "Practice new skills through projects",
                    "Seek mentorship or coaching"
                ],
                industry=target_industry,
                confidence=0.8
            )
            recommendations.append(skills_rec)
            
            # Networking recommendation
            networking_rec = CareerInsight(
                title="Professional Networking",
                description="Build your professional network for career opportunities",
                category="networking",
                priority=2,
                recommendations=[
                    "Join industry professional associations",
                    "Attend conferences and networking events",
                    "Connect with professionals on LinkedIn",
                    "Participate in online communities and forums"
                ],
                industry=target_industry,
                confidence=0.7
            )
            recommendations.append(networking_rec)
            
            # Experience building recommendation
            experience_rec = CareerInsight(
                title="Experience Building",
                description="Ways to gain relevant experience for career advancement",
                category="experience_building",
                priority=1,
                recommendations=[
                    "Take on challenging projects at work",
                    "Volunteer for cross-functional teams",
                    "Consider side projects or freelance work",
                    "Seek opportunities to lead initiatives"
                ],
                industry=target_industry,
                confidence=0.8
            )
            recommendations.append(experience_rec)
            
            return recommendations
            
        except Exception as e:
            logger.warning(f"Failed to generate career recommendations: {e}")
            return []
    
    def get_salary_insights(self, resume: ParsedResume, target_industry: str = None, location: str = None) -> Dict[str, Any]:
        """
        Get salary insights and benchmarking data.
        
        Args:
            resume (ParsedResume): Resume to analyze
            target_industry (str): Target industry for salary data
            location (str): Location for salary adjustment (optional)
            
        Returns:
            Dict[str, Any]: Salary insights and benchmarking data
        """
        try:
            logger.debug("Generating salary insights")
            start_time = time.time()
            
            if not target_industry or target_industry.lower() not in self.salary_data:
                return {"error": "Salary data not available for this industry"}
            
            # Determine career level
            current_level = self._determine_career_level(resume)
            
            # Get salary data
            salary_data = self.salary_data[target_industry.lower()]
            level_salaries = salary_data.get(f"{current_level}_level", salary_data["mid_level"])
            
            # Apply location adjustment if provided
            location_multiplier = self._get_location_multiplier(location) if location else 1.0
            
            adjusted_salaries = {
                "min": int(level_salaries["min"] * location_multiplier),
                "max": int(level_salaries["max"] * location_multiplier),
                "median": int(level_salaries["median"] * location_multiplier)
            }
            
            # Generate insights
            insights = {
                "current_level": current_level,
                "industry": target_industry,
                "salary_range": adjusted_salaries,
                "location": location,
                "location_multiplier": location_multiplier,
                "recommendations": self._generate_salary_recommendations(adjusted_salaries, current_level),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            analysis_time = time.time() - start_time
            logger.info(f"Salary insights generated in {analysis_time:.2f}s")
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate salary insights: {e}")
            return {
                "error": str(e),
                "analysis_timestamp": datetime.now().isoformat()
            }
    
    def _get_location_multiplier(self, location: str) -> float:
        """Get salary multiplier based on location."""
        # Simplified location multipliers (in practice, this would be more comprehensive)
        location_multipliers = {
            "san francisco": 1.4,
            "new york": 1.3,
            "seattle": 1.2,
            "boston": 1.15,
            "austin": 1.1,
            "chicago": 1.05,
            "denver": 1.0,
            "atlanta": 0.95,
            "dallas": 0.9,
            "phoenix": 0.85
        }
        
        location_lower = location.lower()
        for city, multiplier in location_multipliers.items():
            if city in location_lower:
                return multiplier
        
        return 1.0  # Default multiplier
    
    def _generate_salary_recommendations(self, salary_range: Dict[str, int], current_level: str) -> List[str]:
        """Generate salary-related recommendations."""
        recommendations = []
        
        median_salary = salary_range["median"]
        
        if current_level == "entry":
            recommendations.append(f"Entry-level salary range: ${salary_range['min']:,} - ${salary_range['max']:,}")
            recommendations.append("Focus on gaining experience and skills for salary growth")
        elif current_level == "mid":
            recommendations.append(f"Mid-level salary range: ${salary_range['min']:,} - ${salary_range['max']:,}")
            recommendations.append("Consider specialization or leadership roles for higher compensation")
        elif current_level == "senior":
            recommendations.append(f"Senior-level salary range: ${salary_range['min']:,} - ${salary_range['max']:,}")
            recommendations.append("Leverage expertise and leadership skills for maximum compensation")
        else:
            recommendations.append(f"Leadership salary range: ${salary_range['min']:,} - ${salary_range['max']:,}")
            recommendations.append("Focus on strategic impact and team leadership for compensation growth")
        
        recommendations.append(f"Median salary for your level: ${median_salary:,}")
        
        return recommendations
    
    def generate_career_plan(self, resume: ParsedResume, target_industry: str, time_horizon: str = "1 year") -> Dict[str, Any]:
        """
        Generate comprehensive career development plan.
        
        Args:
            resume (ParsedResume): Resume to analyze
            target_industry (str): Target industry for career plan
            time_horizon (str): Time horizon for the plan (1 year, 3 years, 5 years)
            
        Returns:
            Dict[str, Any]: Comprehensive career development plan
        """
        try:
            logger.debug(f"Generating career plan for {time_horizon}")
            start_time = time.time()
            
            # Analyze current state
            current_level = self._determine_career_level(resume)
            career_insights = self.analyze_career_path(resume, target_industry)
            salary_insights = self.get_salary_insights(resume, target_industry)
            
            # Generate timeline-based plan
            plan_phases = self._generate_plan_phases(current_level, target_industry, time_horizon)
            
            # Generate action items
            action_items = self._generate_action_items(resume, target_industry, time_horizon)
            
            # Generate success metrics
            success_metrics = self._generate_success_metrics(current_level, target_industry, time_horizon)
            
            career_plan = {
                "target_industry": target_industry,
                "time_horizon": time_horizon,
                "current_level": current_level,
                "career_insights": [insight.dict() for insight in career_insights],
                "salary_insights": salary_insights,
                "plan_phases": plan_phases,
                "action_items": action_items,
                "success_metrics": success_metrics,
                "plan_timestamp": datetime.now().isoformat()
            }
            
            analysis_time = time.time() - start_time
            logger.info(f"Career plan generated in {analysis_time:.2f}s")
            
            return career_plan
            
        except Exception as e:
            logger.error(f"Failed to generate career plan: {e}")
            return {
                "error": str(e),
                "plan_timestamp": datetime.now().isoformat()
            }
    
    def _generate_plan_phases(self, current_level: str, target_industry: str, time_horizon: str) -> List[Dict[str, Any]]:
        """Generate career plan phases based on time horizon."""
        phases = []
        
        if time_horizon == "1 year":
            phases = [
                {
                    "phase": "Immediate (0-3 months)",
                    "focus": "Skill assessment and gap identification",
                    "goals": ["Complete skills assessment", "Identify 2-3 key skill gaps", "Start learning plan"]
                },
                {
                    "phase": "Short-term (3-6 months)",
                    "focus": "Skill development and experience building",
                    "goals": ["Complete online courses", "Apply new skills in projects", "Update resume"]
                },
                {
                    "phase": "Medium-term (6-12 months)",
                    "focus": "Career advancement preparation",
                    "goals": ["Network with industry professionals", "Apply for new roles", "Prepare for interviews"]
                }
            ]
        elif time_horizon == "3 years":
            phases = [
                {
                    "phase": "Year 1",
                    "focus": "Foundation building",
                    "goals": ["Master core skills", "Gain relevant experience", "Build professional network"]
                },
                {
                    "phase": "Year 2",
                    "focus": "Specialization and advancement",
                    "goals": ["Develop expertise in chosen area", "Take on leadership roles", "Earn certifications"]
                },
                {
                    "phase": "Year 3",
                    "focus": "Senior role preparation",
                    "goals": ["Lead major projects", "Mentor junior colleagues", "Target senior positions"]
                }
            ]
        else:  # 5 years
            phases = [
                {
                    "phase": "Years 1-2",
                    "focus": "Foundation and growth",
                    "goals": ["Build strong foundation", "Gain diverse experience", "Develop leadership skills"]
                },
                {
                    "phase": "Years 3-4",
                    "focus": "Specialization and leadership",
                    "goals": ["Become subject matter expert", "Lead teams and projects", "Build industry reputation"]
                },
                {
                    "phase": "Year 5",
                    "focus": "Senior leadership preparation",
                    "goals": ["Target executive roles", "Develop strategic thinking", "Build external network"]
                }
            ]
        
        return phases
    
    def _generate_action_items(self, resume: ParsedResume, target_industry: str, time_horizon: str) -> List[Dict[str, Any]]:
        """Generate specific action items for career development."""
        action_items = []
        
        # Skills development actions
        action_items.append({
            "category": "Skills Development",
            "priority": "High",
            "action": "Complete skills assessment",
            "timeline": "1 month",
            "description": "Identify current skills and gaps for target industry"
        })
        
        action_items.append({
            "category": "Skills Development",
            "priority": "High",
            "action": "Take relevant online courses",
            "timeline": "3 months",
            "description": "Enroll in courses for identified skill gaps"
        })
        
        # Networking actions
        action_items.append({
            "category": "Networking",
            "priority": "Medium",
            "action": "Join professional associations",
            "timeline": "2 months",
            "description": "Join industry-specific professional organizations"
        })
        
        action_items.append({
            "category": "Networking",
            "priority": "Medium",
            "action": "Attend industry events",
            "timeline": "Ongoing",
            "description": "Regularly attend conferences and networking events"
        })
        
        # Experience building actions
        action_items.append({
            "category": "Experience Building",
            "priority": "High",
            "action": "Take on challenging projects",
            "timeline": "Ongoing",
            "description": "Volunteer for projects that stretch your skills"
        })
        
        action_items.append({
            "category": "Experience Building",
            "priority": "Medium",
            "action": "Seek mentorship",
            "timeline": "2 months",
            "description": "Find a mentor in your target industry"
        })
        
        return action_items
    
    def _generate_success_metrics(self, current_level: str, target_industry: str, time_horizon: str) -> List[Dict[str, Any]]:
        """Generate success metrics for career development."""
        metrics = []
        
        # Skills metrics
        metrics.append({
            "metric": "Skills Development",
            "target": "Complete 3-5 new skills",
            "measurement": "Number of skills learned",
            "timeline": "6 months"
        })
        
        # Experience metrics
        metrics.append({
            "metric": "Project Leadership",
            "target": "Lead 2-3 major projects",
            "measurement": "Number of projects led",
            "timeline": "1 year"
        })
        
        # Network metrics
        metrics.append({
            "metric": "Professional Network",
            "target": "Connect with 50+ industry professionals",
            "measurement": "LinkedIn connections",
            "timeline": "1 year"
        })
        
        # Career advancement metrics
        if current_level in ["entry", "mid"]:
            metrics.append({
                "metric": "Career Advancement",
                "target": "Promotion or new role",
                "measurement": "Job level increase",
                "timeline": "1-2 years"
            })
        
        return metrics
