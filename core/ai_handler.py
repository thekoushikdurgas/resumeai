"""
AI Handler Module for Resume/CV AI Application
Handles AI model integrations and provides unified interface for AI operations.

This module provides:
- Hugging Face model integration for all AI operations
- Unified interface for AI operations using Hugging Face models
- Local and API-based inference options
- Embedding generation using SentenceTransformers
- Semantic similarity calculations
- AI-powered resume analysis and enhancement

Author: Resume AI Team
Created: 2024
"""

import os
import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json
import requests
import torch

from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    AutoModelForSequenceClassification,
    AutoModelForQuestionAnswering,
    AutoModelForSeq2SeqLM,
    pipeline
)
# NumPy 2.0 compatibility fix
import numpy as np
numpy_version = np.__version__
if int(numpy_version.split('.')[0]) >= 2:
    if not hasattr(np, 'float_'):
        np.float_ = np.float64
    if not hasattr(np, 'int_'):
        np.int_ = np.int64
    if not hasattr(np, 'complex_'):
        np.complex_ = np.complex128

from sentence_transformers import SentenceTransformer

from models.resume_model import ParsedResume
from models.job_model import JobDescription
from models.analysis_model import AnalysisResult, ATSResult, EnhancementSuggestion, CareerInsight
from utils.helpers import clean_text, generate_unique_id
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("ai_handler")

class AIHandler:
    """
    Central AI handler for all AI model interactions using Hugging Face models.
    
    This class provides a unified interface for interacting with Hugging Face models
    for text generation, classification, summarization, and other AI tasks.
    
    Key Features:
    - Hugging Face model support for all AI operations
    - Local and API-based inference options
    - Embedding generation using SentenceTransformers
    - Semantic similarity calculations
    - AI-powered resume analysis and enhancement
    - Comprehensive error handling and logging
    
    Attributes:
        config (Dict): Configuration settings for AI services
        available_models (Dict): Dictionary of available AI models
        embedding_model (SentenceTransformer): Model for generating embeddings
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize AI handler with Hugging Face configuration and comprehensive logging.
        
        Args:
            config (Optional[Dict]): Configuration dictionary containing API keys
                                   and service settings. If None, uses environment
                                   variables for configuration.
        
        Raises:
            Exception: If critical AI services fail to initialize
        
        Example:
            >>> config = {
            ...     'huggingface_api_key': 'your_hf_key',
            ...     'use_local_models': True
            ... }
            >>> ai_handler = AIHandler(config)
        """
        logger.info("Initializing AIHandler with Hugging Face support")
        
        self.config = config or {}
        self.available_models = {}
        self.embedding_model = None
        self._initialization_time = time.time()
        
        # Hugging Face configuration
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or self.config.get('huggingface_api_key')
        self.use_local_models = self.config.get('use_local_models', True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            # Initialize AI services with comprehensive logging
            logger.info("Setting up Hugging Face AI service connections")
            self._setup_huggingface_services()
            logger.info("Hugging Face AI service setup completed")
            
            # Load embedding model
            logger.info("Loading embedding model for semantic operations")
            self._load_embedding_model()
            logger.info("Embedding model loaded successfully")
            
            # Log initialization summary
            initialization_time = time.time() - self._initialization_time
            available_models = list(self.available_models.keys())
            
            logger.info(f"AIHandler initialization completed in {initialization_time:.2f}s")
            logger.info(f"Available AI models: {available_models}")
            logger.info(f"Total available models: {len(self.available_models)}")
            logger.info(f"Using device: {self.device}")
            
            if not available_models:
                logger.warning("No AI models are available - configuration may be incorrect")
            else:
                logger.info("AI services are ready for use")
                
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"AIHandler initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def _setup_huggingface_services(self):
        """
        Setup Hugging Face service connections with comprehensive error handling and logging.
        
        Initializes connections to Hugging Face models for various AI tasks:
        - Text generation
        - Text classification
        - Summarization
        - Question answering
        - Sentiment analysis
        - Named entity recognition
        
        Raises:
            Exception: If critical setup errors occur
        """
        logger.debug("Starting Hugging Face service setup process")
        setup_start_time = time.time()
        
        services_configured = 0
        services_failed = 0
        
        try:
            # Set Hugging Face token
            if self.hf_api_key:
                os.environ['HUGGINGFACE_HUB_TOKEN'] = self.hf_api_key
                logger.debug("Hugging Face API key configured")
            
            # Model configurations
            model_configs = {
                'text_generation': {
                    'model_name': 'microsoft/DialoGPT-medium',
                    'task': 'text-generation',
                    'local': self.use_local_models,
                    'max_length': 1024,  # DialoGPT-medium max length
                    'truncation': True
                },
                'text_generation_long': {
                    'model_name': 'gpt2-medium',
                    'task': 'text-generation',
                    'local': self.use_local_models,
                    'max_length': 1024,  # GPT-2 medium max length
                    'truncation': True
                },
                'text_classification': {
                    'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
                    'task': 'text-classification',
                    'local': self.use_local_models
                },
                'summarization': {
                    'model_name': 'facebook/bart-large-cnn',
                    'task': 'summarization',
                    'local': self.use_local_models
                },
                'question_answering': {
                    'model_name': 'distilbert-base-cased-distilled-squad',
                    'task': 'question-answering',
                    'local': self.use_local_models
                },
                'sentiment_analysis': {
                    'model_name': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                    'task': 'sentiment-analysis',
                    'local': self.use_local_models,
                    'ignore_mismatched_sizes': True
                },
                'named_entity_recognition': {
                    'model_name': 'dbmdz/bert-large-cased-finetuned-conll03-english',
                    'task': 'ner',
                    'local': self.use_local_models,
                    'ignore_mismatched_sizes': True
                }
            }
            
            # Initialize models
            for model_name, config in model_configs.items():
                try:
                    logger.debug(f"Initializing {model_name} model: {config['model_name']}")
                    
                    if config['local']:
                        # Load model locally
                        pipeline_kwargs = {
                            'task': config['task'],
                            'model': config['model_name'],
                            'device': 0 if self.device == "cuda" else -1
                        }
                        
                        # Add ignore_mismatched_sizes if specified
                        if config.get('ignore_mismatched_sizes'):
                            pipeline_kwargs['ignore_mismatched_sizes'] = True
                        
                        pipeline_obj = pipeline(**pipeline_kwargs)
                        self.available_models[model_name] = pipeline_obj
                        logger.info(f"{model_name} model loaded locally successfully")
                        services_configured += 1  # Count successful local model loads
                    else:
                        # Use API inference
                        self.available_models[model_name] = {
                            'model_name': config['model_name'],
                            'task': config['task'],
                            'api_key': self.hf_api_key
                        }
                        logger.info(f"{model_name} model configured for API inference")
                        services_configured += 1  # Count successful API configurations
                    
                except Exception as model_error:
                    logger.error(f"Failed to initialize {model_name}: {model_error}")
                    services_failed += 1  # Only increment on actual failure
            
            # Summary logging
            setup_time = time.time() - setup_start_time
            logger.info(f"Hugging Face service setup completed in {setup_time:.2f}s")
            logger.info(f"Services configured: {services_configured}")
            logger.info(f"Services failed: {services_failed}")
            
            if not self.available_models:
                logger.error("No Hugging Face models could be configured")
                raise Exception("No AI models available")
            else:
                available_services = list(self.available_models.keys())
                logger.info(f"Available AI services: {available_services}")
                
        except Exception as e:
            setup_time = time.time() - setup_start_time
            logger.error(f"Hugging Face service setup failed after {setup_time:.2f}s: {e}")
            raise

    def _load_embedding_model(self):
        """
        Load sentence transformer model for embeddings with comprehensive logging.
        
        Uses the 'all-MiniLM-L6-v2' model which provides a good balance between
        performance and computational efficiency for semantic similarity tasks.
        
        Raises:
            Exception: If model loading fails
        """
        try:
            logger.debug("Loading SentenceTransformer embedding model")
            model_name = 'sentence-transformers/all-MiniLM-L6-v2'
            
            # Load the embedding model
            start_time = time.time()
            self.embedding_model = SentenceTransformer(model_name)
            load_time = time.time() - start_time
            
            logger.info(f"Embedding model '{model_name}' loaded successfully in {load_time:.2f}s")
            logger.debug(f"Model device: {self.embedding_model.device}")
            logger.debug(f"Model max sequence length: {self.embedding_model.max_seq_length}")
            
            # Test the model with a sample embedding
            try:
                test_text = "This is a test sentence for embedding generation."
                test_embedding = self.embedding_model.encode([test_text])
                logger.debug(f"Test embedding generated successfully, shape: {test_embedding.shape}")
            except Exception as test_error:
                logger.warning(f"Model test embedding failed: {test_error}")
                
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model '{model_name}': {e}")
            logger.error("This could be due to network issues or model download problems")
            raise
    
    def _truncate_prompt_for_model(self, prompt: str, model: str) -> str:
        """
        Truncate prompt to fit within model's token limits.
        
        Args:
            prompt (str): Original prompt
            model (str): Model name
            
        Returns:
            str: Truncated prompt that fits within model limits
        """
        try:
            # Get model configuration
            model_configs = {
                'text_generation': {
                    'model_name': 'microsoft/DialoGPT-medium',
                    'max_length': 1024,
                    'truncation': True
                },
                'text_generation_long': {
                    'model_name': 'gpt2-medium',
                    'max_length': 1024,
                    'truncation': True
                }
            }
            
            if model not in model_configs:
                logger.warning(f"No token limit configuration for model: {model}")
                return prompt
            
            config = model_configs[model]
            max_length = config.get('max_length', 1024)
            
            # Rough estimation: 1 token ≈ 4 characters for English text
            # Leave buffer for generation tokens (reserve 20% for generation)
            max_input_chars = int(max_length * 2.8)  # More conservative to leave room for generation
            
            if len(prompt) <= max_input_chars:
                logger.debug(f"Prompt length ({len(prompt)}) within limits ({max_input_chars})")
                return prompt
            
            logger.warning(f"Prompt too long ({len(prompt)} chars), truncating to {max_input_chars} chars")
            
            # Smart truncation: prioritize important sections
            # Look for key sections to preserve
            important_sections = ['experience', 'education', 'skills', 'summary', 'objective']
            
            # Try to find and preserve important sections
            truncated = prompt[:max_input_chars]
            
            # Look for section headers and try to preserve them
            for section in important_sections:
                section_start = prompt.lower().find(section)
                if section_start != -1 and section_start < max_input_chars:
                    # Try to include this section
                    section_end = prompt.find('\n', section_start + len(section) + 50)
                    if section_end != -1 and section_end < max_input_chars:
                        continue  # Section fits, keep it
            
            # Try to end at a sentence boundary
            last_period = truncated.rfind('.')
            last_newline = truncated.rfind('\n')
            last_break = max(last_period, last_newline)
            
            if last_break > max_input_chars * 0.7:  # If we can find a good break point
                truncated = truncated[:last_break + 1]
                logger.debug(f"Truncated at sentence boundary, final length: {len(truncated)}")
            else:
                logger.debug(f"Truncated at character limit, final length: {len(truncated)}")
            
            return truncated
            
        except Exception as e:
            logger.error(f"Error truncating prompt: {e}")
            # Fallback: simple truncation
            return prompt[:2000] if len(prompt) > 2000 else prompt
    
    def is_connected(self) -> bool:
        """
        Check if any AI service is available and functional.
        
        Returns:
            bool: True if at least one AI service is configured and available
        """
        is_available = len(self.available_models) > 0
        logger.debug(f"AI service availability check: {is_available}")
        
        if is_available:
            available_services = list(self.available_models.keys())
            logger.debug(f"Available services: {available_services}")
        else:
            logger.warning("No AI services are currently available")
            
        return is_available
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available AI models with logging.
        
        Returns:
            List[str]: List of available AI service names
        """
        available_models = list(self.available_models.keys())
        logger.debug(f"Retrieved available models: {available_models}")
        return available_models
    
    async def generate_response(
        self, 
        prompt: str, 
        context: str = "", 
        model: str = "text_generation",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI response using the specified Hugging Face model with comprehensive logging.
        
        This method handles AI response generation using Hugging Face models with
        detailed logging for debugging and monitoring.
        
        Args:
            prompt (str): Input prompt for the AI model
            context (str): Additional context to prepend to the prompt
            model (str): Model to use ("text_generation", "summarization", etc.)
            max_tokens (int): Maximum number of tokens to generate (default: 2000)
            temperature (float): Temperature for generation randomness (default: 0.7)
            
        Returns:
            str: Generated AI response or error message if generation fails
            
        Raises:
            ValueError: If specified model is not available
            Exception: If response generation fails
        """
        start_time = time.time()
        
        try:
            logger.info("Starting AI response generation")
            logger.debug(f"Original prompt length: {len(prompt)} characters")
            logger.debug(f"Context length: {len(context)} characters")
            logger.debug(f"Requested model: {model}")
            logger.debug(f"Max tokens: {max_tokens}, Temperature: {temperature}")
            
            # Validate inputs
            if not prompt or len(prompt.strip()) < 3:
                logger.warning("Prompt is very short or empty, may result in poor response quality")
            
            # Prepare full prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            logger.debug(f"Full prompt length: {len(full_prompt)} characters")
            
            # Check and handle token limits for text generation models
            if model in ["text_generation", "text_generation_long"]:
                full_prompt = self._truncate_prompt_for_model(full_prompt, model)
                logger.debug(f"Truncated prompt length: {len(full_prompt)} characters")
            
            # Validate model availability
            if model not in self.available_models:
                available_models = list(self.available_models.keys())
                logger.error(f"Requested model '{model}' not available")
                logger.error(f"Available models: {available_models}")
                raise ValueError(f"Model {model} not available. Available: {available_models}")
            
            logger.debug(f"Model '{model}' is available, proceeding with generation")
            
            # Generate response based on model
            logger.debug("Calling Hugging Face model for response generation")
            try:
                response = await self._generate_huggingface_response(full_prompt, model, max_tokens, temperature)
            except Exception as model_error:
                logger.warning(f"Primary model {model} failed: {model_error}")
                # Try fallback model if available
                if model == "text_generation" and "text_generation_long" in self.available_models:
                    logger.info("Attempting fallback to text_generation_long model")
                    try:
                        response = await self._generate_huggingface_response(full_prompt, "text_generation_long", max_tokens, temperature)
                    except Exception as fallback_error:
                        logger.error(f"Fallback model also failed: {fallback_error}")
                        # Try with even more aggressive truncation
                        logger.info("Attempting with more aggressive truncation")
                        try:
                            # Truncate more aggressively for fallback
                            truncated_prompt = full_prompt[:1500]  # Very aggressive truncation
                            response = await self._generate_huggingface_response(truncated_prompt, "text_generation_long", 50, temperature)
                        except Exception as final_error:
                            logger.error(f"All fallback attempts failed: {final_error}")
                            raise model_error  # Raise original error
                else:
                    raise model_error
            
            # Log response details
            generation_time = time.time() - start_time
            logger.info(f"AI response generated successfully in {generation_time:.2f}s")
            logger.info(f"Model used: {model}")
            logger.info(f"Response length: {len(response)} characters")
            logger.debug(f"Response preview: {response[:100]}{'...' if len(response) > 100 else ''}")
            
            return response
                
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"AI response generation failed after {generation_time:.2f}s: {e}")
            logger.error(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
            logger.error(f"Requested model: {model}")
            
            # Return user-friendly error message
            error_message = "I apologize, but I'm unable to generate a response at the moment. Please try again later."
            logger.info(f"Returning error message to user: {error_message}")
            return error_message
    
    async def _generate_huggingface_response(self, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """
        Generate response using Hugging Face models with comprehensive logging.
        
        Args:
            prompt (str): Input prompt for the model
            model (str): Model name to use
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Temperature for generation randomness
            
        Returns:
            str: Generated response from Hugging Face model
            
        Raises:
            Exception: If Hugging Face API call fails
        """
        start_time = time.time()
        
        try:
            logger.debug(f"Generating response using Hugging Face {model}")
            logger.debug(f"Prompt length: {len(prompt)} characters")
            logger.debug(f"Max tokens: {max_tokens}, temperature: {temperature}")
            
            model_config = self.available_models[model]
            
            if isinstance(model_config, dict) and 'api_key' in model_config:
                # Use API inference
                response = await self._call_huggingface_api(prompt, model_config, max_tokens, temperature)
            else:
                # Use local model
                response = await self._call_local_model(prompt, model_config, max_tokens, temperature)
            
            generation_time = time.time() - start_time
            logger.info(f"Hugging Face response generated in {generation_time:.2f}s")
            logger.debug(f"Response length: {len(response)} characters")
            
            return response
            
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Hugging Face API error after {generation_time:.2f}s: {e}")
            logger.error(f"Prompt length: {len(prompt)} characters")
            logger.error(f"Max tokens: {max_tokens}, Temperature: {temperature}")
            raise
    
    async def _call_huggingface_api(self, prompt: str, model_config: Dict, max_tokens: int, temperature: float) -> str:
        """
        Call Hugging Face API for inference.
        
        Args:
            prompt (str): Input prompt
            model_config (Dict): Model configuration
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature for generation
            
        Returns:
            str: Generated response
        """
        try:
            headers = {
                "Authorization": f"Bearer {model_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "return_full_text": False
                }
            }
            
            model_name = model_config['model_name']
            api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            response = requests.post(api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            elif isinstance(result, dict):
                return result.get('generated_text', '')
            else:
                return str(result)
            
        except Exception as e:
            logger.error(f"Hugging Face API call failed: {e}")
            raise
    
    async def _call_local_model(self, prompt: str, pipeline_obj, max_tokens: int, temperature: float) -> str:
        """
        Call local Hugging Face model for inference with token limit handling.
        
        Args:
            prompt (str): Input prompt
            pipeline_obj: Hugging Face pipeline object
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature for generation
            
        Returns:
            str: Generated response
        """
        try:
            # Get tokenizer to check input length
            tokenizer = pipeline_obj.tokenizer
            max_model_length = getattr(tokenizer, 'model_max_length', 1024)
            
            # Tokenize input to check length
            input_tokens = tokenizer.encode(prompt, add_special_tokens=True)
            input_length = len(input_tokens)
            
            logger.debug(f"Input token length: {input_length}, Model max: {max_model_length}")
            
            # Truncate input if necessary
            if input_length > max_model_length:
                logger.warning(f"Input too long ({input_length} tokens), truncating to {max_model_length}")
                # Truncate tokens and decode back to text
                truncated_tokens = input_tokens[:max_model_length]
                prompt = tokenizer.decode(truncated_tokens, skip_special_tokens=True)
                logger.debug(f"Truncated prompt length: {len(prompt)} characters")
            
            # Calculate available tokens for generation (reserve at least 50 tokens)
            available_tokens = max_model_length - input_length
            generation_tokens = min(max_tokens, max(50, available_tokens - 10))  # Reserve 10 tokens buffer
            
            # Configure generation parameters
            generation_kwargs = {
                "max_new_tokens": generation_tokens,
                "temperature": temperature,
                "do_sample": True,
                "pad_token_id": tokenizer.eos_token_id,
                "truncation": True,
                "return_full_text": False  # Only return generated text, not input
            }
            
            # Ensure we have minimum tokens for generation
            if generation_kwargs["max_new_tokens"] < 20:
                logger.warning(f"Very few tokens available for generation ({generation_tokens}), using minimum")
                generation_kwargs["max_new_tokens"] = 20
            
            logger.debug(f"Generation parameters: {generation_kwargs}")
            
            # Generate response
            result = pipeline_obj(prompt, **generation_kwargs)
            
            if isinstance(result, list) and len(result) > 0:
                response = result[0].get('generated_text', '')
                # Clean up the response
                if response.startswith(prompt):
                    response = response[len(prompt):].strip()
                return response
            elif isinstance(result, dict):
                response = result.get('generated_text', '')
                if response.startswith(prompt):
                    response = response[len(prompt):].strip()
                return response
            else:
                return str(result)
            
        except Exception as e:
            error_msg = str(e).lower()
            if "index out of range" in error_msg or "sequence length" in error_msg:
                logger.error(f"Token limit exceeded error: {e}")
                logger.error(f"Prompt length: {len(prompt)} characters")
                logger.error(f"Max tokens: {max_tokens}, Temperature: {temperature}")
                return "I apologize, but the input text is too long for analysis. Please try with a shorter resume or break it into smaller sections."
            else:
                logger.error(f"Local model call failed: {e}")
                logger.error(f"Prompt length: {len(prompt)} characters")
                logger.error(f"Max tokens: {max_tokens}, Temperature: {temperature}")
                raise
    
    async def analyze_resume_content(self, resume: ParsedResume) -> AnalysisResult:
        """
        Analyze resume content using AI.
        
        Args:
            resume: Parsed resume object
            
        Returns:
            Analysis result
        """
        try:
            # Create analysis prompt
            prompt = self._create_resume_analysis_prompt(resume)
            
            # Generate AI analysis
            ai_response = await self.generate_response(prompt, model="text_generation")
            
            # Parse AI response
            analysis = self._parse_analysis_response(ai_response)
            
            # Create analysis result
            result = AnalysisResult(
                analysis_id=generate_unique_id(),
                analysis_type="resume_analysis",
                overall_score=analysis.get('overall_score', 0.0),
                confidence=analysis.get('confidence', 0.0),
                issues=analysis.get('issues', []),
                recommendations=analysis.get('recommendations', []),
                strengths=analysis.get('strengths', []),
                weaknesses=analysis.get('weaknesses', []),
                metrics=analysis.get('metrics', {}),
                created_at=datetime.now()
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze resume content: {e}")
            logger.exception("Full traceback for AI analysis error:")
            return AnalysisResult(
                analysis_id=generate_unique_id(),
                analysis_type="resume_analysis",
                overall_score=0.0,
                confidence=0.0,
                issues=[f"AI analysis failed: {str(e)}"],
                recommendations=["Please try again or contact support"],
                strengths=[],
                weaknesses=["Unable to complete AI analysis"],
                metrics={},
                created_at=datetime.now()
            )
    
    async def match_job_requirements(self, resume: ParsedResume, job: JobDescription) -> Dict:
        """
        Match resume against job requirements.
        
        Args:
            resume: Parsed resume object
            job: Job description object
            
        Returns:
            Matching analysis result
        """
        try:
            # Create matching prompt
            prompt = self._create_job_matching_prompt(resume, job)
            
            # Generate AI analysis
            ai_response = await self.generate_response(prompt, model="text_generation")
            
            # Parse AI response
            match_analysis = self._parse_job_matching_response(ai_response)
            
            return match_analysis
            
        except Exception as e:
            logger.error(f"Failed to match job requirements: {e}")
            return {
                'match_score': 0.0,
                'issues': ['Matching failed due to technical error']
            }
    
    async def check_ats_compatibility(self, resume: ParsedResume) -> ATSResult:
        """
        Check ATS compatibility of resume.
        
        Args:
            resume: Parsed resume object
            
        Returns:
            ATS compatibility result
        """
        try:
            # Create ATS check prompt
            prompt = self._create_ats_check_prompt(resume)
            
            # Generate AI analysis
            ai_response = await self.generate_response(prompt, model="text_generation")
            
            # Parse AI response
            ats_analysis = self._parse_ats_response(ai_response)
            
            # Create ATS result
            result = ATSResult(
                ats_score=ats_analysis.get('ats_score', 0.0),
                format_score=ats_analysis.get('format_score', 0.0),
                keyword_score=ats_analysis.get('keyword_score', 0.0),
                structure_score=ats_analysis.get('structure_score', 0.0),
                content_score=ats_analysis.get('content_score', 0.0),
                compatibility_issues=ats_analysis.get('compatibility_issues', []),
                keyword_matches=ats_analysis.get('keyword_matches', []),
                missing_keywords=ats_analysis.get('missing_keywords', []),
                format_issues=ats_analysis.get('format_issues', []),
                structure_issues=ats_analysis.get('structure_issues', []),
                recommendations=ats_analysis.get('recommendations', [])
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to check ATS compatibility: {e}")
            return ATSResult(
                ats_score=0.0,
                compatibility_issues=["ATS check failed due to technical error"]
            )
    
    async def generate_enhancement_suggestions(self, resume: ParsedResume, focus_area: str = "general") -> List[EnhancementSuggestion]:
        """
        Generate enhancement suggestions for resume.
        
        Args:
            resume: Parsed resume object
            focus_area: Area to focus on (general, ats, keywords, etc.)
            
        Returns:
            List of enhancement suggestions
        """
        try:
            # Create enhancement prompt
            prompt = self._create_enhancement_prompt(resume, focus_area)
            
            # Generate AI analysis
            ai_response = await self.generate_response(prompt, model="text_generation")
            
            # Parse AI response
            suggestions_data = self._parse_enhancement_response(ai_response)
            
            # Create enhancement suggestions
            suggestions = []
            for suggestion_data in suggestions_data:
                suggestion = EnhancementSuggestion(
                    suggestion_id=generate_unique_id(),
                    category=suggestion_data.get('category', 'general'),
                    title=suggestion_data.get('title', 'Enhancement Suggestion'),
                    description=suggestion_data.get('description', ''),
                    current_text=suggestion_data.get('current_text'),
                    suggested_text=suggestion_data.get('suggested_text'),
                    impact_score=suggestion_data.get('impact_score', 0.0),
                    effort_level=suggestion_data.get('effort_level', 'medium'),
                    priority=suggestion_data.get('priority', 'medium'),
                    reasoning=suggestion_data.get('reasoning'),
                    examples=suggestion_data.get('examples', [])
                )
                suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to generate enhancement suggestions: {e}")
            return []
    
    async def generate_career_insights(self, resume: ParsedResume, industry: str = None) -> List[CareerInsight]:
        """
        Generate career insights based on resume.
        
        Args:
            resume: Parsed resume object
            industry: Target industry
            
        Returns:
            List of career insights
        """
        try:
            # Create career insights prompt
            prompt = self._create_career_insights_prompt(resume, industry)
            
            # Generate AI analysis
            ai_response = await self.generate_response(prompt, model="text_generation")
            
            # Parse AI response
            insights_data = self._parse_career_insights_response(ai_response)
            
            # Create career insights
            insights = []
            for insight_data in insights_data:
                insight = CareerInsight(
                    insight_id=generate_unique_id(),
                    category=insight_data.get('category', 'general'),
                    title=insight_data.get('title', 'Career Insight'),
                    description=insight_data.get('description', ''),
                    data_points=insight_data.get('data_points', {}),
                    recommendations=insight_data.get('recommendations', []),
                    confidence=insight_data.get('confidence', 0.0),
                    source=insight_data.get('source'),
                    generated_at=datetime.now(),
                    relevance_score=insight_data.get('relevance_score', 0.0)
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate career insights: {e}")
            return []
    
    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text using sentence transformer.
        
        Args:
            text: Text to generate embeddings for
            
        Returns:
            Embedding vector
        """
        try:
            if not self.embedding_model:
                raise ValueError("Embedding model not loaded")
            
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            if not self.embedding_model:
                raise ValueError("Embedding model not loaded")
            
            # Generate embeddings
            embedding1 = self.embedding_model.encode(text1)
            embedding2 = self.embedding_model.encode(text2)
            
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    def _create_resume_analysis_prompt(self, resume: ParsedResume) -> str:
        """Create prompt for resume analysis."""
        prompt = f"""
        Analyze the following resume and provide a comprehensive assessment:
        
        Name: {resume.contact_info.name or 'Not provided'}
        Email: {resume.contact_info.email or 'Not provided'}
        Phone: {resume.contact_info.phone or 'Not provided'}
        Location: {resume.contact_info.location or 'Not provided'}
        
        Summary: {resume.summary or 'Not provided'}
        
        Work Experience:
        {self._format_work_experience(resume.work_experience)}
        
        Education:
        {self._format_education(resume.education)}
        
        Skills:
        {self._format_skills(resume.skills)}
        
        Projects:
        {self._format_projects(resume.projects)}
        
        Please provide:
        1. Overall score (0-100)
        2. Confidence level (0-1)
        3. Key strengths
        4. Areas for improvement
        5. Specific issues found
        6. Actionable recommendations
        7. Metrics and statistics
        
        Format your response as JSON with the following structure:
        {{
            "overall_score": 85,
            "confidence": 0.9,
            "strengths": ["Strong technical skills", "Relevant experience"],
            "weaknesses": ["Missing quantifiable achievements", "Weak summary"],
            "issues": ["No phone number", "Inconsistent formatting"],
            "recommendations": ["Add metrics to achievements", "Improve summary"],
            "metrics": {{
                "word_count": 500,
                "skills_count": 15,
                "experience_years": 5
            }}
        }}
        """
        return prompt
    
    def _create_job_matching_prompt(self, resume: ParsedResume, job: JobDescription) -> str:
        """Create prompt for job matching analysis."""
        prompt = f"""
        Analyze how well this resume matches the job requirements:
        
        RESUME SUMMARY:
        {resume.summary or 'No summary provided'}
        
        KEY SKILLS: {', '.join([skill.name for skill in resume.skills]) if resume.skills else 'None listed'}
        
        EXPERIENCE: {self._format_work_experience(resume.work_experience)}
        
        JOB REQUIREMENTS:
        Title: {job.title or 'Not specified'}
        Company: {job.company or 'Not specified'}
        Description: {job.description or 'Not provided'}
        Required Skills: {', '.join(job.required_skills) if job.required_skills else 'None listed'}
        Requirements: {job.requirements or 'Not provided'}
        
        Please provide:
        1. Overall match score (0-100)
        2. Skill match percentage
        3. Experience match percentage
        4. Missing skills
        5. Extra skills
        6. Recommendations for improvement
        
        Format as JSON with detailed analysis.
        """
        return prompt
    
    def _create_ats_check_prompt(self, resume: ParsedResume) -> str:
        """Create prompt for ATS compatibility check."""
        prompt = f"""
        Check this resume for ATS (Applicant Tracking System) compatibility:
        
        {resume.raw_text or 'Resume text not available'}
        
        Please evaluate:
        1. ATS compatibility score (0-100)
        2. Format issues
        3. Keyword optimization
        4. Structure problems
        5. Content quality
        6. Missing elements
        7. Specific recommendations
        
        Format as JSON with detailed analysis.
        """
        return prompt
    
    def _create_enhancement_prompt(self, resume: ParsedResume, focus_area: str) -> str:
        """Create prompt for enhancement suggestions."""
        prompt = f"""
        Provide enhancement suggestions for this resume focusing on: {focus_area}
        
        {resume.raw_text or 'Resume text not available'}
        
        Please provide specific, actionable suggestions with:
        1. Current text (if applicable)
        2. Suggested improvement
        3. Impact score (0-10)
        4. Effort level (low/medium/high)
        5. Reasoning
        6. Examples
        
        Format as JSON array of suggestions.
        """
        return prompt
    
    def _create_career_insights_prompt(self, resume: ParsedResume, industry: str) -> str:
        """Create prompt for career insights."""
        prompt = f"""
        Generate career insights for this resume in the {industry or 'general'} industry:
        
        {resume.raw_text or 'Resume text not available'}
        
        Please provide insights on:
        1. Market trends
        2. Salary expectations
        3. Skill demand
        4. Career progression
        5. Industry recommendations
        6. Growth opportunities
        
        Format as JSON array of insights with data points and recommendations.
        """
        return prompt
    
    def _format_work_experience(self, experiences) -> str:
        """Format work experience for prompts."""
        if not experiences:
            return "No work experience listed"
        
        formatted = []
        for exp in experiences:
            exp_text = f"- {exp.title} at {exp.company}"
            if exp.start_date and exp.end_date:
                exp_text += f" ({exp.start_date} - {exp.end_date})"
            if exp.description:
                exp_text += f": {exp.description}"
            formatted.append(exp_text)
        
        return "\n".join(formatted)
    
    def _format_education(self, education) -> str:
        """Format education for prompts."""
        if not education:
            return "No education listed"
        
        formatted = []
        for edu in education:
            edu_text = f"- {edu.degree} from {edu.institution}"
            if edu.graduation_date:
                edu_text += f" ({edu.graduation_date})"
            formatted.append(edu_text)
        
        return "\n".join(formatted)
    
    def _format_skills(self, skills) -> str:
        """Format skills for prompts."""
        if not skills:
            return "No skills listed"
        
        return ", ".join([skill.name for skill in skills])
    
    def _format_projects(self, projects) -> str:
        """Format projects for prompts."""
        if not projects:
            return "No projects listed"
        
        formatted = []
        for project in projects:
            proj_text = f"- {project.name}"
            if project.description:
                proj_text += f": {project.description}"
            formatted.append(proj_text)
        
        return "\n".join(formatted)
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse AI analysis response."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {
                    'overall_score': 75,
                    'confidence': 0.8,
                    'strengths': ['Resume analysis completed'],
                    'weaknesses': ['Unable to parse detailed analysis'],
                    'issues': ['AI response parsing failed'],
                    'recommendations': ['Please try again or contact support']
                }
        except Exception as e:
            logger.error(f"Failed to parse analysis response: {e}")
            return {
                'overall_score': 0,
                'confidence': 0.0,
                'issues': ['Analysis parsing failed']
            }
    
    def _parse_job_matching_response(self, response: str) -> Dict:
        """Parse job matching response."""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    'match_score': 0,
                    'issues': ['Job matching analysis failed']
                }
        except Exception as e:
            logger.error(f"Failed to parse job matching response: {e}")
            return {'match_score': 0, 'issues': ['Parsing failed']}
    
    def _parse_ats_response(self, response: str) -> Dict:
        """Parse ATS check response."""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    'ats_score': 0,
                    'compatibility_issues': ['ATS analysis failed']
                }
        except Exception as e:
            logger.error(f"Failed to parse ATS response: {e}")
            return {'ats_score': 0, 'compatibility_issues': ['Parsing failed']}
    
    def _parse_enhancement_response(self, response: str) -> List[Dict]:
        """Parse enhancement suggestions response."""
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return [{
                    'category': 'general',
                    'title': 'Enhancement Suggestion',
                    'description': 'Unable to parse enhancement suggestions',
                    'impact_score': 0.0
                }]
        except Exception as e:
            logger.error(f"Failed to parse enhancement response: {e}")
            return []
    
    def _parse_career_insights_response(self, response: str) -> List[Dict]:
        """Parse career insights response."""
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return [{
                    'category': 'general',
                    'title': 'Career Insight',
                    'description': 'Unable to parse career insights',
                    'confidence': 0.0
                }]
        except Exception as e:
            logger.error(f"Failed to parse career insights response: {e}")
            return []