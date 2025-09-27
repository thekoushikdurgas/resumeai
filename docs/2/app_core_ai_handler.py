# AI Handler - Core AI Integration Module
# app/core/ai_handler.py

import streamlit as st
from typing import Dict, List, Optional, Union, Any
import json
import logging
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import torch

# AI Service Imports - Hugging Face Only
try:
    from transformers import (
        AutoTokenizer, 
        AutoModelForCausalLM, 
        AutoModelForSequenceClassification,
        AutoModelForQuestionAnswering,
        AutoModelForSeq2SeqLM,
        pipeline
    )
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    st.error(f"Missing Hugging Face dependencies: {e}")

from config.ai_config import AIConfig
from app.utils.logger import get_logger
from app.models.analysis_model import AnalysisResult, AIResponse

logger = get_logger(__name__)

class AIHandler:
    """Central AI handler for all AI model interactions using Hugging Face models."""
    
    def __init__(self, config: AIConfig):
        """Initialize AI handler with Hugging Face configuration"""
        self.config = config
        self.available_models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.setup_ai_services()
    
    def setup_ai_services(self):
        """Setup and configure Hugging Face AI services"""
        
        # Hugging Face Setup
        try:
            if self.config.HUGGINGFACE_API_KEY:
                os.environ['HUGGINGFACE_HUB_TOKEN'] = self.config.HUGGINGFACE_API_KEY
                
                # Initialize text generation pipeline
                self.text_generation_pipeline = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-medium",
                    device=0 if self.device == "cuda" else -1
                )
                
                # Initialize text classification pipeline
                self.text_classification_pipeline = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=0 if self.device == "cuda" else -1
                )
                
                # Initialize summarization pipeline
                self.summarization_pipeline = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=0 if self.device == "cuda" else -1
                )
                
                # Initialize question answering pipeline
                self.qa_pipeline = pipeline(
                    "question-answering",
                    model="distilbert-base-cased-distilled-squad",
                    device=0 if self.device == "cuda" else -1
                )
                
                # Initialize sentiment analysis pipeline
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    device=0 if self.device == "cuda" else -1
                )
                
                # Initialize embedding model
                self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                
                self.available_models['huggingface'] = True
                logger.info("Hugging Face models configured successfully")
            else:
                self.available_models['huggingface'] = False
                logger.warning("Hugging Face API key not provided")
        except Exception as e:
            self.available_models['huggingface'] = False
            logger.error(f"Failed to setup Hugging Face: {e}")
    
    def is_connected(self) -> bool:
        """Check if any AI service is available"""
        return any(self.available_models.values())
    
    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        return [model for model, available in self.available_models.items() if available]
    
    async def generate_response(
        self, 
        prompt: str, 
        context: str = "", 
        model: str = "text_generation",
        max_tokens: int = None,
        temperature: float = None
    ) -> AIResponse:
        """Generate AI response using Hugging Face models"""
        
        # Set defaults
        if max_tokens is None:
            max_tokens = getattr(self.config, 'DEFAULT_MAX_TOKENS', 2000)
        if temperature is None:
            temperature = getattr(self.config, 'DEFAULT_TEMPERATURE', 0.7)
        
        # Validate model availability
        if not self.available_models.get('huggingface', False):
            raise ValueError("Hugging Face models are not available")
        
        # Prepare full prompt
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        try:
            # Generate response using Hugging Face pipeline
            response = await self._generate_huggingface_response(full_prompt, max_tokens, temperature)
            
            return AIResponse(
                content=response,
                model="huggingface",
                success=True,
                tokens_used=len(response.split()) * 1.3,  # Approximation
                timestamp=datetime.now()
            )
        
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return AIResponse(
                content=f"AI service temporarily unavailable: {str(e)}",
                model="huggingface",
                success=False,
                error=str(e)
            )
    
    async def _generate_huggingface_response(
        self, 
        prompt: str, 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate response using Hugging Face text generation pipeline"""
        
        try:
            # Configure generation parameters
            generation_kwargs = {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "do_sample": True,
                "pad_token_id": self.text_generation_pipeline.tokenizer.eos_token_id
            }
            
            # Generate response
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.text_generation_pipeline(prompt, **generation_kwargs)
            )
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            elif isinstance(result, dict):
                return result.get('generated_text', '')
            else:
                return str(result)
        
        except Exception as e:
            logger.error(f"Hugging Face generation error: {e}")
            raise
    
    # Specialized AI functions for different use cases
    
    async def analyze_resume_content(self, resume_text: str) -> AnalysisResult:
        """Analyze resume content using AI"""
        
        prompt = f"""
        Analyze the following resume and provide a comprehensive assessment:
        
        Resume:
        {resume_text}
        
        Please provide analysis in JSON format with the following structure:
        {{
            "overall_score": <score 0-100>,
            "strengths": ["strength1", "strength2", ...],
            "weaknesses": ["weakness1", "weakness2", ...],
            "suggestions": ["suggestion1", "suggestion2", ...],
            "ats_compatibility": <score 0-100>,
            "keyword_density": <score 0-100>,
            "readability": <score 0-100>,
            "structure": <score 0-100>
        }}
        """
        
        context = "You are an expert resume analyst with 15+ years of experience in recruitment and career counseling."
        
        response = await self.generate_response(prompt, context, model="text_generation")
        
        try:
            # Parse JSON response
            analysis_data = json.loads(response.content)
            
            return AnalysisResult(
                overall_score=analysis_data.get("overall_score", 0),
                strengths=analysis_data.get("strengths", []),
                weaknesses=analysis_data.get("weaknesses", []),
                suggestions=analysis_data.get("suggestions", []),
                ats_compatibility=analysis_data.get("ats_compatibility", 0),
                keyword_density=analysis_data.get("keyword_density", 0),
                readability=analysis_data.get("readability", 0),
                structure=analysis_data.get("structure", 0)
            )
        
        except json.JSONDecodeError:
            logger.error("Failed to parse AI analysis response as JSON")
            return AnalysisResult(
                overall_score=0,
                suggestions=["Unable to analyze resume - please try again"]
            )
    
    async def match_job_requirements(self, resume_text: str, job_description: str) -> Dict:
        """Match resume against job requirements"""
        
        prompt = f"""
        Compare this resume against the job description and provide a detailed matching analysis:
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Provide analysis in JSON format:
        {{
            "match_percentage": <0-100>,
            "matched_skills": ["skill1", "skill2", ...],
            "missing_skills": ["skill1", "skill2", ...],
            "experience_alignment": <0-100>,
            "education_alignment": <0-100>,
            "recommendations": ["rec1", "rec2", ...],
            "keyword_matches": ["keyword1", "keyword2", ...],
            "gap_analysis": "detailed analysis of gaps"
        }}
        """
        
        context = "You are an expert job matching specialist who helps candidates optimize their resumes for specific positions."
        
        response = await self.generate_response(prompt, context)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"match_percentage": 0, "error": "Failed to analyze job match"}
    
    async def enhance_resume_section(self, section_content: str, section_type: str, target_role: str = "") -> str:
        """Enhance specific resume section with AI"""
        
        prompt = f"""
        Enhance the following {section_type} section for a resume:
        
        Current content:
        {section_content}
        
        Target role: {target_role if target_role else "General professional role"}
        
        Requirements:
        - Use action verbs and quantifiable achievements
        - Optimize for ATS scanning
        - Maintain professional tone
        - Focus on impact and results
        - Include relevant keywords
        
        Provide only the enhanced content, no explanations.
        """
        
        context = f"You are an expert resume writer specializing in {section_type} optimization."
        
        response = await self.generate_response(prompt, context)
        return response.content
    
    async def check_ats_compatibility(self, resume_text: str) -> Dict:
        """Check ATS compatibility and provide recommendations"""
        
        prompt = f"""
        Analyze this resume for ATS (Applicant Tracking System) compatibility:
        
        Resume:
        {resume_text}
        
        Provide analysis in JSON format:
        {{
            "ats_score": <0-100>,
            "formatting_issues": ["issue1", "issue2", ...],
            "keyword_optimization": <0-100>,
            "section_recognition": <0-100>,
            "recommendations": ["rec1", "rec2", ...],
            "critical_fixes": ["fix1", "fix2", ...]
        }}
        """
        
        context = "You are an ATS system expert who understands how applicant tracking systems parse and rank resumes."
        
        response = await self.generate_response(prompt, context)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"ats_score": 0, "error": "Failed to analyze ATS compatibility"}
    
    async def generate_professional_summary(self, experience_data: Dict, target_role: str = "") -> str:
        """Generate professional summary based on experience"""
        
        prompt = f"""
        Create a compelling professional summary based on the following information:
        
        Experience data: {json.dumps(experience_data, indent=2)}
        Target role: {target_role if target_role else "Professional role"}
        
        Requirements:
        - 3-4 sentences maximum
        - Highlight key achievements and years of experience
        - Include relevant skills and expertise
        - Quantify results where possible
        - Professional and confident tone
        
        Provide only the professional summary text.
        """
        
        context = "You are an expert career counselor who writes compelling professional summaries."
        
        response = await self.generate_response(prompt, context)
        return response.content.strip()
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using sentence transformer"""
        try:
            if not self.embedding_model:
                raise ValueError("Embedding model not loaded")
            
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            if not self.embedding_model:
                raise ValueError("Embedding model not loaded")
            
            # Generate embeddings
            embedding1 = self.embedding_model.encode(text1)
            embedding2 = self.embedding_model.encode(text2)
            
            # Calculate cosine similarity
            import numpy as np
            similarity = np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    def get_usage_stats(self) -> Dict:
        """Get AI service usage statistics"""
        # This would track usage across sessions in a real implementation
        return {
            "total_requests": getattr(self, '_total_requests', 0),
            "successful_requests": getattr(self, '_successful_requests', 0),
            "failed_requests": getattr(self, '_failed_requests', 0),
            "available_models": self.get_available_models(),
            "device": self.device
        }
    
    def clear_cache(self):
        """Clear AI response cache"""
        # Implementation for clearing cached responses
        if hasattr(self, '_response_cache'):
            self._response_cache.clear()
            logger.info("AI response cache cleared")