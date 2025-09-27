"""
Vector Database Module for Resume/CV AI Application
Handles semantic search, similarity matching, and vector storage for resumes and job descriptions.

This module provides:
- ChromaDB integration for vector storage
- SentenceTransformer embeddings for semantic search
- Resume and job description storage and retrieval
- Similarity matching and search capabilities
- Collection management and statistics

Author: Resume AI Team
Created: 2024
"""

import os
import json
import uuid
import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

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

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd

from models.resume_model import ParsedResume, ResumeMetadata
from models.job_model import JobDescription, JobMetadata
from utils.helpers import generate_unique_id, clean_text
from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("vector_db")

class VectorDatabase:
    """
    Vector database handler for semantic search and similarity matching.
    
    This class provides a high-level interface for:
    - Storing and retrieving resume and job description embeddings
    - Performing semantic similarity searches
    - Managing vector collections (resumes, jobs, skills, keywords)
    - Calculating similarity scores between documents
    
    The database uses ChromaDB for vector storage and SentenceTransformers
    for generating embeddings from text content.
    
    Attributes:
        persist_directory (str): Directory path for persistent storage
        client (chromadb.Client): ChromaDB client instance
        embedding_model (SentenceTransformer): Model for generating embeddings
        collections (dict): Dictionary of collection objects
    """
    
    def __init__(self, persist_directory: str = "./data/vectordb"):
        """
        Initialize the vector database with persistent storage.
        
        Args:
            persist_directory: Directory to persist the vector database
                              Defaults to "./data/vectordb"
        
        Raises:
            Exception: If database initialization fails
        """
        logger.info(f"Initializing VectorDatabase with persist directory: {persist_directory}")
        
        self.persist_directory = persist_directory
        self.client = None
        self.embedding_model = None
        self.collections = {}
        self._initialization_time = time.time()
        
        try:
            # Initialize the database components
            logger.info("Starting database initialization sequence")
            self._initialize_database()
            logger.info("Database client initialized successfully")
            
            # Try to load embedding model with fallback
            try:
                self._load_embedding_model()
                logger.info("Embedding model loaded successfully")
            except Exception as model_error:
                logger.error(f"Failed to load embedding model: {model_error}")
                logger.warning("Continuing without embedding model - some features may be limited")
                self.embedding_model = None
            
            # Create collections (this should work even without embedding model)
            try:
                self._create_collections()
                logger.info("Collections created successfully")
            except Exception as collection_error:
                logger.error(f"Failed to create collections: {collection_error}")
                logger.warning("Continuing with limited collection functionality")
                self.collections = {}
            
            initialization_duration = time.time() - self._initialization_time
            logger.info(f"VectorDatabase initialization completed in {initialization_duration:.2f}s")
            
            # Check if we have critical components
            if self.embedding_model is None:
                logger.warning("VectorDatabase initialized but embedding model is not available")
                logger.warning("Semantic search and similarity features will be disabled")
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorDatabase: {e}")
            logger.error("VectorDatabase will not be available - some features will be disabled")
            # Don't raise the exception, just log it and continue
            self.embedding_model = None
            self.collections = {}
    
    def is_initialized(self) -> bool:
        """
        Check if the VectorDatabase is properly initialized.
        
        Returns:
            bool: True if properly initialized, False otherwise
        """
        try:
            return (
                self.client is not None and 
                hasattr(self.client, 'heartbeat') and
                len(self.collections) > 0
            )
        except Exception:
            return False
    
    def is_embedding_available(self) -> bool:
        """
        Check if embedding model is available.
        
        Returns:
            bool: True if embedding model is available, False otherwise
        """
        try:
            return self.embedding_model is not None
        except Exception:
            return False
    
    def _initialize_database(self):
        """
        Initialize ChromaDB client with persistent storage configuration.
        
        Creates the persistent directory if it doesn't exist and configures
        ChromaDB with appropriate settings for production use.
        
        Raises:
            Exception: If ChromaDB client initialization fails
        """
        try:
            logger.debug(f"Creating persist directory: {self.persist_directory}")
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Configure ChromaDB settings for optimal performance
            logger.debug("Configuring ChromaDB client settings")
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,  # Disable telemetry for privacy
                    allow_reset=True,           # Allow collection resets
                    is_persistent=True          # Ensure persistence is enabled
                )
            )
            
            logger.info(f"ChromaDB client initialized successfully at {self.persist_directory}")
            
            # Verify client connectivity
            try:
                self.client.heartbeat()
                logger.debug("ChromaDB client heartbeat successful")
            except Exception as heartbeat_error:
                logger.warning(f"ChromaDB heartbeat failed: {heartbeat_error}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            logger.error(f"Persist directory: {self.persist_directory}")
            raise
    
    def _load_embedding_model(self):
        """
        Load the SentenceTransformer model for generating text embeddings.
        
        Uses the 'all-MiniLM-L6-v2' model which provides a good balance between
        performance and computational efficiency for semantic similarity tasks.
        
        Raises:
            Exception: If model loading fails
        """
        try:
            logger.debug("Loading SentenceTransformer embedding model")
            model_name = 'all-MiniLM-L6-v2'
            
            # Load the embedding model with proper device handling
            start_time = time.time()
            
            # Try to load with device specification to avoid meta tensor issues
            try:
                import torch
                device = 'cpu'  # Force CPU to avoid GPU/meta tensor issues
                logger.debug(f"Loading model on device: {device}")
                
                # Load with explicit device configuration
                self.embedding_model = SentenceTransformer(
                    model_name,
                    device=device,
                    cache_folder='./models'  # Use local cache
                )
                
            except Exception as device_error:
                logger.warning(f"Device-specific loading failed: {device_error}")
                logger.debug("Trying fallback loading method")
                
                # Fallback: Load without device specification
                self.embedding_model = SentenceTransformer(
                    model_name,
                    cache_folder='./models'
                )
            
            load_time = time.time() - start_time
            logger.info(f"Embedding model '{model_name}' loaded successfully in {load_time:.2f}s")
            
            # Get model information safely
            try:
                logger.debug(f"Model device: {getattr(self.embedding_model, 'device', 'unknown')}")
                logger.debug(f"Model max sequence length: {getattr(self.embedding_model, 'max_seq_length', 'unknown')}")
            except Exception as info_error:
                logger.warning(f"Could not get model info: {info_error}")
            
            # Test the model with a sample embedding
            try:
                test_text = "This is a test sentence for embedding generation."
                test_embedding = self.embedding_model.encode([test_text])
                logger.debug(f"Test embedding generated successfully, shape: {test_embedding.shape}")
            except Exception as test_error:
                logger.warning(f"Model test embedding failed: {test_error}")
                # Don't raise here, just log the warning
                logger.warning("Model loaded but test embedding failed - this may indicate issues")
            
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model '{model_name}': {e}")
            logger.error("This could be due to network issues, model download problems, or PyTorch version conflicts")
            
            # Try alternative model as fallback
            try:
                logger.info("Attempting to load alternative embedding model...")
                alternative_model = 'paraphrase-MiniLM-L6-v2'
                self.embedding_model = SentenceTransformer(alternative_model, cache_folder='./models')
                logger.info(f"Alternative model '{alternative_model}' loaded successfully")
            except Exception as fallback_error:
                logger.error(f"Fallback model loading also failed: {fallback_error}")
                raise Exception(f"Both primary and fallback model loading failed. Primary error: {e}, Fallback error: {fallback_error}")
    
    def _create_collections(self):
        """
        Create or retrieve ChromaDB collections for different data types.
        
        Sets up four main collections:
        - resumes: For storing resume document embeddings and metadata
        - jobs: For storing job description embeddings and metadata  
        - skills: For skill-based matching and competency analysis
        - keywords: For industry-specific keyword and phrase storage
        
        Raises:
            Exception: If collection creation fails
        """
        try:
            logger.debug("Creating ChromaDB collections for different data types")
            
            # Define collection configurations
            collection_configs = {
                'resumes': {
                    'name': "resumes",
                    'metadata': {
                        "description": "Resume documents and their embeddings",
                        "created_at": datetime.now().isoformat(),
                        "version": "1.0"
                    }
                },
                'jobs': {
                    'name': "jobs", 
                    'metadata': {
                        "description": "Job descriptions and their embeddings",
                        "created_at": datetime.now().isoformat(),
                        "version": "1.0"
                    }
                },
                'skills': {
                    'name': "skills",
                    'metadata': {
                        "description": "Skills and competencies database",
                        "created_at": datetime.now().isoformat(),
                        "version": "1.0"
                    }
                },
                'keywords': {
                    'name': "keywords",
                    'metadata': {
                        "description": "Industry-specific keywords and phrases",
                        "created_at": datetime.now().isoformat(),
                        "version": "1.0"
                    }
                }
            }
            
            # Create or get collections
            for collection_key, config in collection_configs.items():
                try:
                    logger.debug(f"Creating/getting collection: {config['name']}")
                    self.collections[collection_key] = self.client.get_or_create_collection(
                        name=config['name'],
                        metadata=config['metadata']
                    )
                    logger.debug(f"Collection '{config['name']}' ready")
                except Exception as collection_error:
                    logger.error(f"Failed to create collection '{config['name']}': {collection_error}")
                    raise
            
            logger.info(f"Successfully created/retrieved {len(self.collections)} collections")
            
            # Log collection statistics
            for name, collection in self.collections.items():
                try:
                    count = collection.count()
                    logger.debug(f"Collection '{name}' contains {count} documents")
                except Exception as count_error:
                    logger.warning(f"Could not get count for collection '{name}': {count_error}")
            
        except Exception as e:
            logger.error(f"Failed to create collections: {e}")
            logger.error("This could be due to ChromaDB connectivity issues or permission problems")
            raise
    
    def add_resume(self, resume: ParsedResume, metadata: ResumeMetadata) -> str:
        """
        Add a resume to the vector database with comprehensive logging.
        
        Processes the resume by:
        1. Generating a unique document ID
        2. Creating a text representation for embedding generation
        3. Generating embeddings using the SentenceTransformer model
        4. Preparing metadata for storage
        5. Adding the document to the resumes collection
        
        Args:
            resume (ParsedResume): Parsed resume object containing all resume data
            metadata (ResumeMetadata): Metadata about the resume file and analysis
            
        Returns:
            str: Unique document ID assigned to the resume in the database
            
        Raises:
            Exception: If any step in the resume addition process fails
            
        Example:
            >>> resume = ParsedResume(...)
            >>> metadata = ResumeMetadata(...)
            >>> doc_id = vector_db.add_resume(resume, metadata)
            >>> print(f"Resume stored with ID: {doc_id}")
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting resume addition process for: {resume.contact_info.name or 'Unknown'}")
            
            # Generate unique ID
            doc_id = generate_unique_id()
            logger.debug(f"Generated document ID: {doc_id}")
            
            # Create text representation for embedding
            logger.debug("Creating text representation for embedding generation")
            resume_text = self._create_resume_text(resume)
            
            # Validate text content
            if not resume_text or len(resume_text.strip()) < 10:
                logger.warning("Resume text is very short or empty, may affect embedding quality")
            
            logger.debug(f"Resume text length: {len(resume_text)} characters")
            
            # Generate embedding
            logger.debug("Generating embeddings using SentenceTransformer model")
            embedding_start = time.time()
            
            try:
                embedding = self.embedding_model.encode(resume_text).tolist()
                embedding_time = time.time() - embedding_start
                logger.debug(f"Embedding generated in {embedding_time:.3f}s, dimension: {len(embedding)}")
            except Exception as embedding_error:
                logger.error(f"Failed to generate embedding: {embedding_error}")
                raise
            
            # Prepare comprehensive metadata
            logger.debug("Preparing metadata for database storage")
            doc_metadata = {
                "name": resume.contact_info.name or "Unknown",
                "email": resume.contact_info.email or "",
                "phone": resume.contact_info.phone or "",
                "location": resume.contact_info.location or "",
                "experience_years": metadata.experience_years,
                "education_level": metadata.education_level,
                "industry": metadata.industry or "General",
                "skills": json.dumps([skill.name for skill in resume.skills]) if resume.skills else "[]",
                "skills_count": len(resume.skills) if resume.skills else 0,
                "experience_count": len(resume.work_experience) if resume.work_experience else 0,
                "education_count": len(resume.education) if resume.education else 0,
                "created_at": datetime.now().isoformat(),
                "file_type": metadata.file_type,
                "file_size": metadata.file_size,
                "parse_confidence": resume.parse_confidence,
                "text_length": len(resume_text),
                "embedding_dimension": len(embedding)
            }
            
            logger.debug(f"Metadata prepared with {len(doc_metadata)} fields")
            
            # Add to collection
            logger.debug("Adding resume to ChromaDB collection")
            add_start = time.time()
            
            self.collections['resumes'].add(
                documents=[resume_text],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            add_time = time.time() - add_start
            total_time = time.time() - start_time
            
            logger.info(f"Resume successfully added to vector database")
            logger.info(f"  - Document ID: {doc_id}")
            logger.info(f"  - Name: {resume.contact_info.name or 'Unknown'}")
            logger.info(f"  - Skills: {len(resume.skills) if resume.skills else 0}")
            logger.info(f"  - Experience entries: {len(resume.work_experience) if resume.work_experience else 0}")
            logger.info(f"  - Parse confidence: {resume.parse_confidence:.1f}%")
            logger.info(f"  - Total processing time: {total_time:.3f}s")
            logger.info(f"  - Database write time: {add_time:.3f}s")
            
            return doc_id
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Failed to add resume to vector database after {processing_time:.3f}s: {e}")
            logger.error(f"Resume name: {resume.contact_info.name or 'Unknown'}")
            logger.error(f"Document ID: {doc_id if 'doc_id' in locals() else 'Not generated'}")
            raise
    
    def add_job_description(self, job: JobDescription, metadata: JobMetadata) -> str:
        """
        Add a job description to the vector database.
        
        Args:
            job: Job description object
            metadata: Job metadata
            
        Returns:
            Document ID in the database
        """
        try:
            # Generate unique ID
            doc_id = generate_unique_id()
            
            # Create text representation for embedding
            job_text = self._create_job_text(job)
            
            # Generate embedding
            embedding = self.embedding_model.encode(job_text).tolist()
            
            # Prepare metadata
            doc_metadata = {
                "title": job.title or "Unknown Position",
                "company": job.company or "Unknown Company",
                "location": job.location or "",
                "industry": metadata.industry or "General",
                "experience_required": metadata.experience_required,
                "education_required": metadata.education_required,
                "employment_type": metadata.employment_type or "Full-time",
                "salary_range": metadata.salary_range or "",
                "skills_required": json.dumps(job.required_skills) if job.required_skills else "[]",
                "created_at": datetime.now().isoformat(),
                "source": metadata.source or "Unknown"
            }
            
            # Add to collection
            self.collections['jobs'].add(
                documents=[job_text],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Job description added to vector database with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to add job description to vector database: {e}")
            raise
    
    def search_similar_resumes(self, query: str, n_results: int = 10, 
                             filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar resumes using semantic similarity matching.
        
        This method performs a vector-based semantic search to find resumes
        that are most similar to the provided query. The search uses cosine
        similarity between the query embedding and stored resume embeddings.
        
        Args:
            query (str): Search query text describing desired resume characteristics
            n_results (int): Maximum number of similar resumes to return (default: 10)
            filters (Optional[Dict]): Optional metadata filters for narrowing search
                                    Example: {"industry": "Technology", "experience_years": {"$gte": 5}}
            
        Returns:
            List[Dict]: List of similar resumes with the following structure:
                - id: Document ID in the database
                - document: Full resume text content
                - metadata: Resume metadata including contact info, skills, etc.
                - distance: Cosine distance (lower = more similar)
                - similarity: Calculated similarity score (1 - distance)
                
        Raises:
            Exception: If search fails due to database or model errors
            
        Example:
            >>> results = vector_db.search_similar_resumes("Python developer with Django experience", 5)
            >>> for result in results:
            ...     print(f"Similarity: {1-result['distance']:.3f}, Name: {result['metadata']['name']}")
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting resume similarity search")
            logger.debug(f"Query: '{query[:100]}{'...' if len(query) > 100 else ''}'")
            logger.debug(f"Requested results: {n_results}")
            logger.debug(f"Filters applied: {filters}")
            
            # Validate input
            if not query or len(query.strip()) < 3:
                logger.warning("Search query is too short, may return poor results")
            
            # Generate query embedding
            logger.debug("Generating embedding for search query")
            embedding_start = time.time()
            
            try:
                query_embedding = self.embedding_model.encode(query).tolist()
                embedding_time = time.time() - embedding_start
                logger.debug(f"Query embedding generated in {embedding_time:.3f}s, dimension: {len(query_embedding)}")
            except Exception as embedding_error:
                logger.error(f"Failed to generate query embedding: {embedding_error}")
                return []
            
            # Search in resumes collection
            logger.debug("Performing vector similarity search in resumes collection")
            search_start = time.time()
            
            try:
                results = self.collections['resumes'].query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    where=filters
                )
                search_time = time.time() - search_start
                logger.debug(f"Vector search completed in {search_time:.3f}s")
            except Exception as search_error:
                logger.error(f"Vector search failed: {search_error}")
                return []
            
            # Validate search results
            if not results or not results.get('ids') or not results['ids'][0]:
                logger.info("No similar resumes found matching the query")
                return []
            
            found_count = len(results['ids'][0])
            logger.info(f"Found {found_count} similar resumes")
            
            # Format results with enhanced metadata
            logger.debug("Formatting search results")
            similar_resumes = []
            
            for i, doc_id in enumerate(results['ids'][0]):
                try:
                    # Calculate similarity score from distance
                    distance = results['distances'][0][i]
                    similarity = 1 - distance
                    
                    # Extract metadata
                    metadata = results['metadatas'][0][i]
                    document = results['documents'][0][i]
                    
                    # Create enhanced result entry
                    result_entry = {
                        'id': doc_id,
                        'document': document,
                        'metadata': metadata,
                        'distance': distance,
                        'similarity': similarity,
                        'query': query,  # Include original query for reference
                        'search_timestamp': datetime.now().isoformat()
                    }
                    
                    similar_resumes.append(result_entry)
                    
                    # Log top results
                    if i < 3:  # Log details for top 3 results
                        logger.debug(f"Result {i+1}: {metadata.get('name', 'Unknown')} "
                                   f"(similarity: {similarity:.3f})")
                
                except Exception as result_error:
                    logger.warning(f"Error formatting result {i}: {result_error}")
                    continue
            
            total_time = time.time() - start_time
            
            # Log search summary
            logger.info(f"Resume similarity search completed successfully")
            logger.info(f"  - Query length: {len(query)} characters")
            logger.info(f"  - Results found: {len(similar_resumes)}")
            logger.info(f"  - Total search time: {total_time:.3f}s")
            
            if similar_resumes:
                best_match = similar_resumes[0]
                logger.info(f"  - Best match: {best_match['metadata'].get('name', 'Unknown')} "
                          f"(similarity: {best_match['similarity']:.3f})")
            
            return similar_resumes
            
        except Exception as e:
            search_time = time.time() - start_time
            logger.error(f"Resume similarity search failed after {search_time:.3f}s: {e}")
            logger.error(f"Query: '{query[:100]}{'...' if len(query) > 100 else ''}'")
            logger.error(f"Requested results: {n_results}")
            return []
    
    def search_similar_jobs(self, query: str, n_results: int = 10,
                           filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar job descriptions based on a query.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of similar job descriptions with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in jobs collection
            results = self.collections['jobs'].query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filters
            )
            
            # Format results
            similar_jobs = []
            for i, doc_id in enumerate(results['ids'][0]):
                similar_jobs.append({
                    'id': doc_id,
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return similar_jobs
            
        except Exception as e:
            logger.error(f"Failed to search similar jobs: {e}")
            return []
    
    def find_matching_jobs_for_resume(self, resume_id: str, n_results: int = 10) -> List[Dict]:
        """
        Find job descriptions that match a specific resume.
        
        Args:
            resume_id: ID of the resume in the database
            n_results: Number of matching jobs to return
            
        Returns:
            List of matching job descriptions
        """
        try:
            # Get the resume document
            resume_data = self.collections['resumes'].get(ids=[resume_id])
            
            if not resume_data['documents']:
                logger.warning(f"Resume with ID {resume_id} not found")
                return []
            
            # Use resume text as query
            resume_text = resume_data['documents'][0]
            
            # Search for similar jobs
            return self.search_similar_jobs(resume_text, n_results)
            
        except Exception as e:
            logger.error(f"Failed to find matching jobs for resume: {e}")
            return []
    
    def find_matching_resumes_for_job(self, job_id: str, n_results: int = 10) -> List[Dict]:
        """
        Find resumes that match a specific job description.
        
        Args:
            job_id: ID of the job in the database
            n_results: Number of matching resumes to return
            
        Returns:
            List of matching resumes
        """
        try:
            # Get the job document
            job_data = self.collections['jobs'].get(ids=[job_id])
            
            if not job_data['documents']:
                logger.warning(f"Job with ID {job_id} not found")
                return []
            
            # Use job text as query
            job_text = job_data['documents'][0]
            
            # Search for similar resumes
            return self.search_similar_resumes(job_text, n_results)
            
        except Exception as e:
            logger.error(f"Failed to find matching resumes for job: {e}")
            return []
    
    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Generate embeddings
            embedding1 = self.embedding_model.encode(text1)
            embedding2 = self.embedding_model.encode(text2)
            
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity score: {e}")
            return 0.0
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector database collections.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            stats = {}
            
            for collection_name, collection in self.collections.items():
                count = collection.count()
                stats[collection_name] = {
                    'count': count,
                    'status': 'active' if count > 0 else 'empty'
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def delete_document(self, collection_name: str, doc_id: str) -> bool:
        """
        Delete a document from the specified collection.
        
        Args:
            collection_name: Name of the collection
            doc_id: ID of the document to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if collection_name not in self.collections:
                logger.error(f"Collection {collection_name} not found")
                return False
            
            self.collections[collection_name].delete(ids=[doc_id])
            logger.info(f"Document {doc_id} deleted from {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False
    
    def clear_collection(self, collection_name: str) -> bool:
        """
        Clear all documents from a collection.
        
        Args:
            collection_name: Name of the collection to clear
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if collection_name not in self.collections:
                logger.error(f"Collection {collection_name} not found")
                return False
            
            # Get all document IDs
            all_docs = self.collections[collection_name].get()
            if all_docs['ids']:
                self.collections[collection_name].delete(ids=all_docs['ids'])
            
            logger.info(f"Collection {collection_name} cleared")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            return False
    
    def _create_resume_text(self, resume: ParsedResume) -> str:
        """Create a text representation of the resume for embedding."""
        text_parts = []
        
        # Add contact info
        if resume.contact_info.name:
            text_parts.append(f"Name: {resume.contact_info.name}")
        if resume.contact_info.email:
            text_parts.append(f"Email: {resume.contact_info.email}")
        if resume.contact_info.location:
            text_parts.append(f"Location: {resume.contact_info.location}")
        
        # Add summary
        if resume.summary:
            text_parts.append(f"Summary: {resume.summary}")
        
        # Add work experience
        if resume.work_experience:
            text_parts.append("Work Experience:")
            for exp in resume.work_experience:
                exp_text = f"{exp.title} at {exp.company}"
                if exp.description:
                    exp_text += f" - {exp.description}"
                text_parts.append(exp_text)
        
        # Add education
        if resume.education:
            text_parts.append("Education:")
            for edu in resume.education:
                edu_text = f"{edu.degree} from {edu.institution}"
                text_parts.append(edu_text)
        
        # Add skills
        if resume.skills:
            skills_text = ", ".join([skill.name for skill in resume.skills])
            text_parts.append(f"Skills: {skills_text}")
        
        # Add projects
        if resume.projects:
            text_parts.append("Projects:")
            for project in resume.projects:
                proj_text = f"{project.name}"
                if project.description:
                    proj_text += f" - {project.description}"
                text_parts.append(proj_text)
        
        return " ".join(text_parts)
    
    def _create_job_text(self, job: JobDescription) -> str:
        """Create a text representation of the job description for embedding."""
        text_parts = []
        
        # Add basic info
        if job.title:
            text_parts.append(f"Position: {job.title}")
        if job.company:
            text_parts.append(f"Company: {job.company}")
        if job.location:
            text_parts.append(f"Location: {job.location}")
        
        # Add description
        if job.description:
            text_parts.append(f"Description: {job.description}")
        
        # Add requirements
        if job.requirements:
            text_parts.append(f"Requirements: {job.requirements}")
        
        # Add required skills
        if job.required_skills:
            skills_text = ", ".join(job.required_skills)
            text_parts.append(f"Required Skills: {skills_text}")
        
        # Add responsibilities
        if job.responsibilities:
            text_parts.append(f"Responsibilities: {job.responsibilities}")
        
        return " ".join(text_parts)
    
    def close(self):
        """Close the vector database connection."""
        try:
            if self.client:
                # ChromaDB handles cleanup automatically
                logger.info("Vector database connection closed")
        except Exception as e:
            logger.error(f"Error closing vector database: {e}")
