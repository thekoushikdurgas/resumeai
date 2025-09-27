"""
AI Provider Handler Module for Resume/CV AI Application
Handles multiple AI provider integrations (Hugging Face and Groq) with unified interface.

This module provides:
- Multi-provider AI model integration (Hugging Face and Groq)
- Unified interface for AI operations across providers
- Provider selection and fallback mechanisms
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
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import requests
import torch

# Hugging Face imports
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    AutoModelForSequenceClassification,
    AutoModelForQuestionAnswering,
    AutoModelForSeq2SeqLM,
    pipeline
)

# Groq imports
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: Groq library not available. Install with: pip install groq")

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
logger = setup_logger("ai_provider_handler")

class AIProviderHandler:
    """
    Multi-provider AI handler supporting Hugging Face and Groq AI.
    
    This class provides a unified interface for interacting with multiple AI providers
    for text generation, classification, summarization, and other AI tasks.
    
    Key Features:
    - Multi-provider support (Hugging Face and Groq)
    - Provider selection and fallback mechanisms
    - Local and API-based inference options
    - Embedding generation using SentenceTransformers
    - Semantic similarity calculations
    - AI-powered resume analysis and enhancement
    - Comprehensive error handling and logging
    
    Attributes:
        config (Dict): Configuration settings for AI services
        providers (Dict): Available AI providers
        embedding_model (SentenceTransformer): Model for generating embeddings
        _initialization_time (float): Timestamp of initialization start
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize AI provider handler with multi-provider support.
        
        Args:
            config (Optional[Dict]): Configuration dictionary containing API keys
                                   and service settings. If None, uses environment
                                   variables for configuration.
        
        Raises:
            Exception: If critical AI services fail to initialize
        """
        logger.info("Initializing AIProviderHandler with multi-provider support")
        
        self.config = config or {}
        self.providers = {}
        self.embedding_model = None
        self._initialization_time = time.time()
        
        # Load configuration
        self._load_config()
        
        try:
            # Initialize AI providers
            logger.info("Setting up AI provider connections")
            self._setup_providers()
            logger.info("AI provider setup completed")
            
            # Load embedding model
            logger.info("Loading embedding model for semantic operations")
            self._load_embedding_model()
            logger.info("Embedding model loaded successfully")
            
            # Log initialization summary
            initialization_time = time.time() - self._initialization_time
            available_providers = list(self.providers.keys())
            
            logger.info(f"AIProviderHandler initialization completed in {initialization_time:.2f}s")
            logger.info(f"Available providers: {available_providers}")
            logger.info(f"Total available providers: {len(self.providers)}")
            logger.info(f"Using device: {self.device}")
            
            if not available_providers:
                logger.warning("No AI providers are available - configuration may be incorrect")
            else:
                logger.info("AI services are ready for use")
                
        except Exception as e:
            initialization_time = time.time() - self._initialization_time
            logger.error(f"AIProviderHandler initialization failed after {initialization_time:.2f}s: {e}")
            raise
    
    def _load_config(self):
        """Load configuration from file or environment variables."""
        try:
            # Load from config file if available
            config_file = "config/api_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
            
            # Hugging Face configuration
            self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY') or self.config.get('huggingface', {}).get('api_keys')
            self.use_local_models = self.config.get('huggingface', {}).get('local_files_only', True)
            
            # Groq configuration
            self.groq_api_key = os.getenv('GROQ_API_KEY') or self.config.get('groq', {}).get('api_keys')
            
            # Device configuration
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            logger.debug("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _setup_providers(self):
        """Setup AI provider connections."""
        logger.debug("Starting AI provider setup process")
        setup_start_time = time.time()
        
        providers_configured = 0
        providers_failed = 0
        
        try:
            # Setup Hugging Face provider
            if self._setup_huggingface_provider():
                providers_configured += 1
            else:
                providers_failed += 1
            
            # Setup Groq provider
            if self._setup_groq_provider():
                providers_configured += 1
            else:
                providers_failed += 1
            
            # Summary logging
            setup_time = time.time() - setup_start_time
            logger.info(f"AI provider setup completed in {setup_time:.2f}s")
            logger.info(f"Providers configured: {providers_configured}")
            logger.info(f"Providers failed: {providers_failed}")
            
            if not self.providers:
                logger.error("No AI providers could be configured")
                raise Exception("No AI providers available")
            else:
                available_providers = list(self.providers.keys())
                logger.info(f"Available AI providers: {available_providers}")
                
        except Exception as e:
            setup_time = time.time() - setup_start_time
            logger.error(f"AI provider setup failed after {setup_time:.2f}s: {e}")
            raise
    
    def _setup_huggingface_provider(self) -> bool:
        """Setup Hugging Face provider."""
        try:
            logger.debug("Setting up Hugging Face provider")
            
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
                    'max_length': 1024,
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
                    'local': self.use_local_models
                },
                'named_entity_recognition': {
                    'model_name': 'dbmdz/bert-large-cased-finetuned-conll03-english',
                    'task': 'ner',
                    'local': self.use_local_models
                }
            }
            
            # Initialize models
            hf_models = {}
            for model_name, config in model_configs.items():
                try:
                    logger.debug(f"Initializing {model_name} model: {config['model_name']}")
                    
                    if config['local']:
                        # Load model locally
                        pipeline_obj = pipeline(
                            config['task'],
                            model=config['model_name'],
                            device=0 if self.device == "cuda" else -1
                        )
                        hf_models[model_name] = pipeline_obj
                        logger.info(f"{model_name} model loaded locally successfully")
                    else:
                        # Use API inference
                        hf_models[model_name] = {
                            'model_name': config['model_name'],
                            'task': config['task'],
                            'api_key': self.hf_api_key
                        }
                        logger.info(f"{model_name} model configured for API inference")
                    
                except Exception as model_error:
                    logger.error(f"Failed to initialize {model_name}: {model_error}")
            
            if hf_models:
                self.providers['huggingface'] = {
                    'name': 'Hugging Face',
                    'models': hf_models,
                    'api_key': self.hf_api_key,
                    'enabled': True
                }
                logger.info("Hugging Face provider configured successfully")
                return True
            else:
                logger.warning("No Hugging Face models could be configured")
                return False
                
        except Exception as e:
            logger.error(f"Failed to setup Hugging Face provider: {e}")
            return False
    
    def _setup_groq_provider(self) -> bool:
        """Setup Groq provider."""
        try:
            if not GROQ_AVAILABLE:
                logger.warning("Groq library not available, skipping Groq provider setup")
                return False
            
            if not self.groq_api_key:
                logger.warning("Groq API key not configured, skipping Groq provider setup")
                return False
            
            logger.debug("Setting up Groq provider")
            
            # Initialize Groq client
            groq_client = Groq(api_key=self.groq_api_key)
            
            # Test the connection
            try:
                # Simple test to verify API key works
                test_response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": "Hello"}],
                    model="llama3-8b-8192",
                    max_tokens=10
                )
                logger.debug("Groq API connection test successful")
            except Exception as test_error:
                logger.error(f"Groq API connection test failed: {test_error}")
                return False
            
            # Model configurations
            groq_models = {
                'text_generation': 'llama3-8b-8192',
                'text_generation_long': 'llama3-70b-8192',
                'chat_completion': 'llama3-8b-8192',
                'chat_completion_long': 'llama3-70b-8192',
                'resume_analysis': 'llama3-8b-8192',
                'job_matching': 'llama3-8b-8192',
                'ats_checking': 'llama3-8b-8192',
                'text_enhancement': 'llama3-8b-8192',
                'career_advice': 'llama3-70b-8192'
            }
            
            self.providers['groq'] = {
                'name': 'Groq',
                'client': groq_client,
                'models': groq_models,
                'api_key': self.groq_api_key,
                'enabled': True
            }
            
            logger.info("Groq provider configured successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Groq provider: {e}")
            return False
    
    def _load_embedding_model(self):
        """Load sentence transformer model for embeddings."""
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
    
    def is_connected(self) -> bool:
        """Check if any AI provider is available and functional."""
        is_available = len(self.providers) > 0
        logger.debug(f"AI provider availability check: {is_available}")
        
        if is_available:
            available_providers = list(self.providers.keys())
            logger.debug(f"Available providers: {available_providers}")
        else:
            logger.warning("No AI providers are currently available")
            
        return is_available
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers."""
        available_providers = list(self.providers.keys())
        logger.debug(f"Retrieved available providers: {available_providers}")
        return available_providers
    
    async def generate_response(
        self, 
        prompt: str, 
        context: str = "", 
        provider: str = "auto",
        model: str = "text_generation",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI response using the specified provider and model.
        
        Args:
            prompt (str): Input prompt for the AI model
            context (str): Additional context to prepend to the prompt
            provider (str): Provider to use ("auto", "huggingface", "groq")
            model (str): Model to use within the provider
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Temperature for generation randomness
            
        Returns:
            str: Generated AI response or error message if generation fails
        """
        start_time = time.time()
        
        try:
            logger.info("Starting AI response generation")
            logger.debug(f"Original prompt length: {len(prompt)} characters")
            logger.debug(f"Context length: {len(context)} characters")
            logger.debug(f"Requested provider: {provider}, model: {model}")
            logger.debug(f"Max tokens: {max_tokens}, Temperature: {temperature}")
            
            # Validate inputs
            if not prompt or len(prompt.strip()) < 3:
                logger.warning("Prompt is very short or empty, may result in poor response quality")
            
            # Prepare full prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            logger.debug(f"Full prompt length: {len(full_prompt)} characters")
            
            # Select provider
            if provider == "auto":
                provider = self._select_best_provider(model)
            
            if provider not in self.providers:
                available_providers = list(self.providers.keys())
                logger.error(f"Requested provider '{provider}' not available")
                logger.error(f"Available providers: {available_providers}")
                raise ValueError(f"Provider {provider} not available. Available: {available_providers}")
            
            logger.debug(f"Using provider: {provider}")
            
            # Generate response based on provider
            try:
                if provider == "huggingface":
                    response = await self._generate_huggingface_response(full_prompt, model, max_tokens, temperature)
                elif provider == "groq":
                    response = await self._generate_groq_response(full_prompt, model, max_tokens, temperature)
                else:
                    raise ValueError(f"Unknown provider: {provider}")
            except Exception as provider_error:
                logger.warning(f"Primary provider {provider} failed: {provider_error}")
                # Try fallback provider
                fallback_provider = self._get_fallback_provider(provider)
                if fallback_provider:
                    logger.info(f"Attempting fallback to {fallback_provider} provider")
                    try:
                        if fallback_provider == "huggingface":
                            response = await self._generate_huggingface_response(full_prompt, model, max_tokens, temperature)
                        elif fallback_provider == "groq":
                            response = await self._generate_groq_response(full_prompt, model, max_tokens, temperature)
                    except Exception as fallback_error:
                        logger.error(f"Fallback provider also failed: {fallback_error}")
                        raise provider_error
                else:
                    raise provider_error
            
            # Log response details
            generation_time = time.time() - start_time
            logger.info(f"AI response generated successfully in {generation_time:.2f}s")
            logger.info(f"Provider used: {provider}")
            logger.info(f"Model used: {model}")
            logger.info(f"Response length: {len(response)} characters")
            logger.debug(f"Response preview: {response[:100]}{'...' if len(response) > 100 else ''}")
            
            return response
                
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"AI response generation failed after {generation_time:.2f}s: {e}")
            logger.error(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
            logger.error(f"Requested provider: {provider}, model: {model}")
            
            # Return user-friendly error message
            error_message = "I apologize, but I'm unable to generate a response at the moment. Please try again later."
            logger.info(f"Returning error message to user: {error_message}")
            return error_message
    
    def _select_best_provider(self, model: str) -> str:
        """Select the best provider for the given model."""
        # Simple selection logic - can be enhanced based on performance metrics
        if "groq" in self.providers and model in ["text_generation", "chat_completion", "resume_analysis"]:
            return "groq"
        elif "huggingface" in self.providers:
            return "huggingface"
        else:
            # Return first available provider
            return list(self.providers.keys())[0] if self.providers else "huggingface"
    
    def _get_fallback_provider(self, current_provider: str) -> Optional[str]:
        """Get fallback provider if current one fails."""
        available_providers = list(self.providers.keys())
        if len(available_providers) > 1:
            # Return first provider that's not the current one
            for provider in available_providers:
                if provider != current_provider:
                    return provider
        return None
    
    async def _generate_huggingface_response(self, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Generate response using Hugging Face models."""
        start_time = time.time()
        
        try:
            logger.debug(f"Generating response using Hugging Face {model}")
            
            hf_provider = self.providers['huggingface']
            model_config = hf_provider['models'].get(model)
            
            if not model_config:
                raise ValueError(f"Model {model} not available in Hugging Face provider")
            
            if isinstance(model_config, dict) and 'api_key' in model_config:
                # Use API inference
                response = await self._call_huggingface_api(prompt, model_config, max_tokens, temperature)
            else:
                # Use local model
                response = await self._call_huggingface_local(prompt, model_config, max_tokens, temperature)
            
            generation_time = time.time() - start_time
            logger.info(f"Hugging Face response generated in {generation_time:.2f}s")
            
            return response
            
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Hugging Face generation error after {generation_time:.2f}s: {e}")
            raise
    
    async def _generate_groq_response(self, prompt: str, model: str, max_tokens: int, temperature: float) -> str:
        """Generate response using Groq models."""
        start_time = time.time()
        
        try:
            logger.debug(f"Generating response using Groq {model}")
            
            groq_provider = self.providers['groq']
            groq_client = groq_provider['client']
            model_name = groq_provider['models'].get(model, 'llama3-8b-8192')
            
            # Prepare messages for chat completion
            messages = [{"role": "user", "content": prompt}]
            
            # Generate response
            response = groq_client.chat.completions.create(
                messages=messages,
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stream=False
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            generation_time = time.time() - start_time
            logger.info(f"Groq response generated in {generation_time:.2f}s")
            
            return response_text
            
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Groq generation error after {generation_time:.2f}s: {e}")
            raise
    
    async def _call_huggingface_api(self, prompt: str, model_config: Dict, max_tokens: int, temperature: float) -> str:
        """Call Hugging Face API for inference."""
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
    
    async def _call_huggingface_local(self, prompt: str, pipeline_obj, max_tokens: int, temperature: float) -> str:
        """Call local Hugging Face model for inference."""
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
                truncated_tokens = input_tokens[:max_model_length]
                prompt = tokenizer.decode(truncated_tokens, skip_special_tokens=True)
            
            # Calculate available tokens for generation
            available_tokens = max_model_length - input_length
            generation_tokens = min(max_tokens, max(50, available_tokens - 10))
            
            # Configure generation parameters
            generation_kwargs = {
                "max_new_tokens": generation_tokens,
                "temperature": temperature,
                "do_sample": True,
                "pad_token_id": tokenizer.eos_token_id,
                "truncation": True,
                "return_full_text": False
            }
            
            # Generate response
            result = pipeline_obj(prompt, **generation_kwargs)
            
            if isinstance(result, list) and len(result) > 0:
                response = result[0].get('generated_text', '')
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
            logger.error(f"Local Hugging Face model call failed: {e}")
            raise
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using sentence transformer."""
        try:
            if not self.embedding_model:
                raise ValueError("Embedding model not loaded")
            
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
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
    
    # Resume analysis methods (same as original AIHandler)
    async def analyze_resume_content(self, resume: ParsedResume) -> AnalysisResult:
        """Analyze resume content using AI."""
        try:
            # Create analysis prompt
            prompt = self._create_resume_analysis_prompt(resume)
            
            # Generate AI analysis using best provider for this task
            ai_response = await self.generate_response(prompt, model="resume_analysis")
            
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
