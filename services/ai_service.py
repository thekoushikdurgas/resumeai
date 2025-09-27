"""
AI Service for Resume/CV AI Application
Handles AI model integrations and operations using Hugging Face and Groq providers.

This module provides:
- Multi-provider AI model management (Hugging Face and Groq)
- Text generation and analysis
- Embedding generation
- AI response processing
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from utils.logger import setup_logger
from core.ai_provider_handler import AIProviderHandler

# Initialize logger with module-specific name
logger = setup_logger("ai_service")

class AIService:
    """
    AI service class with multi-provider support (Hugging Face and Groq).
    
    This class provides AI model management including text generation,
    analysis, embedding generation, and response processing for the
    Resume/CV AI application using multiple AI providers.
    
    Key Features:
    - Multi-provider AI model management (Hugging Face and Groq)
    - Text generation and analysis
    - Embedding generation
    - AI response processing
    - Provider selection and fallback
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _ai_handler (AIProviderHandler): Multi-provider AI handler
        _providers (Dict[str, Any]): Available AI providers
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize AI service with multi-provider support."""
        logger.info("Initializing AI Service with multi-provider support")
        self._initialization_time = datetime.now()
        
        try:
            # Initialize multi-provider AI handler
            self._ai_handler = AIProviderHandler(config)
            
            # Get provider information
            self._providers = self._ai_handler.providers
            
            logger.info("AI Service initialized successfully")
            logger.info(f"Available providers: {list(self._providers.keys())}")
            
        except Exception as e:
            logger.error(f"AI Service initialization failed: {e}")
            raise
    
    def is_connected(self) -> bool:
        """Check if any AI provider is available and functional."""
        return self._ai_handler.is_connected()
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers."""
        return self._ai_handler.get_available_providers()
    
    async def generate_text(self, prompt: str, provider: str = 'auto', model: str = 'text_generation', 
                           max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate text using AI model.
        
        Args:
            prompt (str): Input prompt
            provider (str): AI provider to use ('auto', 'huggingface', 'groq')
            model (str): AI model to use within the provider
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature for generation
            
        Returns:
            Dict[str, Any]: Generation result
        """
        try:
            logger.info(f"Generating text with provider: {provider}, model: {model}")
            start_time = time.time()
            
            # Generate text using multi-provider handler
            generated_text = await self._ai_handler.generate_response(
                prompt=prompt,
                provider=provider,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            generation_time = time.time() - start_time
            
            result = {
                'success': True,
                'text': generated_text,
                'provider': provider,
                'model': model,
                'tokens_used': len(generated_text.split()),
                'generation_time': round(generation_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Text generation completed in {generation_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate text with provider {provider}, model {model}: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_embeddings(self, text: str) -> Dict[str, Any]:
        """
        Generate embeddings for text using sentence transformer.
        
        Args:
            text (str): Text to generate embeddings for
            
        Returns:
            Dict[str, Any]: Embedding result
        """
        try:
            logger.info(f"Generating embeddings for text of length: {len(text)}")
            start_time = time.time()
            
            # Generate embeddings using multi-provider handler
            embeddings = self._ai_handler.generate_embeddings(text)
            
            generation_time = time.time() - start_time
            
            result = {
                'success': True,
                'embeddings': embeddings,
                'text_length': len(text),
                'embedding_dimension': len(embeddings) if embeddings else 0,
                'generation_time': round(generation_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Embeddings generated in {generation_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return {'success': False, 'error': str(e)}
    
    async def analyze_text(self, text: str, analysis_type: str = 'general', 
                          provider: str = 'auto') -> Dict[str, Any]:
        """
        Analyze text using AI.
        
        Args:
            text (str): Text to analyze
            analysis_type (str): Type of analysis to perform
            provider (str): AI provider to use
            
        Returns:
            Dict[str, Any]: Analysis result
        """
        try:
            logger.info(f"Analyzing text with analysis type: {analysis_type}, provider: {provider}")
            start_time = time.time()
            
            # Create analysis prompt based on type
            if analysis_type == 'sentiment':
                prompt = f"Analyze the sentiment of the following text and provide a score from -1 (negative) to 1 (positive):\n\n{text}"
            elif analysis_type == 'keywords':
                prompt = f"Extract the most important keywords from the following text:\n\n{text}"
            elif analysis_type == 'summary':
                prompt = f"Provide a concise summary of the following text:\n\n{text}"
            else:
                prompt = f"Analyze the following text and provide insights about its content, structure, and quality:\n\n{text}"
            
            # Generate analysis using AI
            analysis_result = await self._ai_handler.generate_response(
                prompt=prompt,
                provider=provider,
                model="text_generation",
                max_tokens=500,
                temperature=0.3
            )
            
            analysis_time = time.time() - start_time
            
            result = {
                'success': True,
                'analysis_type': analysis_type,
                'text_length': len(text),
                'analysis_result': analysis_result,
                'analysis_time': round(analysis_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Text analysis completed in {analysis_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze text: {e}")
            return {'success': False, 'error': str(e)}
    
    def calculate_similarity(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            Dict[str, Any]: Similarity result
        """
        try:
            logger.info(f"Calculating similarity between texts of lengths: {len(text1)}, {len(text2)}")
            start_time = time.time()
            
            # Calculate similarity using multi-provider handler
            similarity_score = self._ai_handler.calculate_similarity(text1, text2)
            
            calculation_time = time.time() - start_time
            
            result = {
                'success': True,
                'similarity_score': similarity_score,
                'text1_length': len(text1),
                'text2_length': len(text2),
                'calculation_time': round(calculation_time, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Similarity calculation completed in {calculation_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_ai_service_info(self) -> Dict[str, Any]:
        """
        Get AI service information and statistics.
        
        Returns:
            Dict[str, Any]: AI service information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "providers_count": len(self._providers),
                "available_providers": self.get_available_providers(),
                "provider_details": {name: {"enabled": provider.get("enabled", False)} for name, provider in self._providers.items()},
                "ai_service_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get AI service info: {e}")
            return {
                "error": str(e),
                "ai_service_timestamp": datetime.now().isoformat()
            }
