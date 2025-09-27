"""
Database Models for Resume/CV AI Application
Defines data models and schemas.

This module provides:
- Data models and schemas
- Model validation
- Model relationships
- Model operations
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("database_models")

class UserRole(Enum):
    """User roles."""
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"

class ResumeStatus(Enum):
    """Resume status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class AnalysisStatus(Enum):
    """Analysis status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class User:
    """User model."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    preferences: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'preferences': self.preferences
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=UserRole(data.get('role', 'user')),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            is_active=data.get('is_active', True),
            preferences=data.get('preferences', {})
        )

@dataclass
class Resume:
    """Resume model."""
    id: str
    user_id: str
    title: str
    status: ResumeStatus = ResumeStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_analyzed: Optional[datetime] = None
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_analyzed': self.last_analyzed.isoformat() if self.last_analyzed else None,
            'content': self.content,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resume':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            title=data['title'],
            status=ResumeStatus(data.get('status', 'draft')),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            last_analyzed=datetime.fromisoformat(data['last_analyzed']) if data.get('last_analyzed') else None,
            content=data.get('content', {}),
            metadata=data.get('metadata', {})
        )

@dataclass
class JobDescription:
    """Job description model."""
    id: str
    user_id: str
    title: str
    company: str
    description: str
    requirements: List[str] = field(default_factory=list)
    location: Optional[str] = None
    salary_range: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'requirements': self.requirements,
            'location': self.location,
            'salary_range': self.salary_range,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobDescription':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            title=data['title'],
            company=data['company'],
            description=data['description'],
            requirements=data.get('requirements', []),
            location=data.get('location'),
            salary_range=data.get('salary_range'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            metadata=data.get('metadata', {})
        )

@dataclass
class Analysis:
    """Analysis model."""
    id: str
    user_id: str
    resume_id: Optional[str] = None
    job_id: Optional[str] = None
    analysis_type: str = "resume"
    status: AnalysisStatus = AnalysisStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'analysis_type': self.analysis_type,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'results': self.results,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Analysis':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            resume_id=data.get('resume_id'),
            job_id=data.get('job_id'),
            analysis_type=data.get('analysis_type', 'resume'),
            status=AnalysisStatus(data.get('status', 'pending')),
            created_at=datetime.fromisoformat(data['created_at']),
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            results=data.get('results', {}),
            metadata=data.get('metadata', {})
        )

@dataclass
class Export:
    """Export model."""
    id: str
    user_id: str
    resume_id: Optional[str] = None
    export_type: str = "resume"
    format: str = "pdf"
    filename: str = ""
    file_path: str = ""
    file_size: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_id': self.resume_id,
            'export_type': self.export_type,
            'format': self.format,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Export':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            resume_id=data.get('resume_id'),
            export_type=data.get('export_type', 'resume'),
            format=data.get('format', 'pdf'),
            filename=data.get('filename', ''),
            file_path=data.get('file_path', ''),
            file_size=data.get('file_size', 0),
            created_at=datetime.fromisoformat(data['created_at']),
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None,
            metadata=data.get('metadata', {})
        )

@dataclass
class Notification:
    """Notification model."""
    id: str
    user_id: Optional[str] = None
    title: str = ""
    message: str = ""
    notification_type: str = "info"
    priority: str = "medium"
    category: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    read: bool = False
    dismissed: bool = False
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'priority': self.priority,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'read': self.read,
            'dismissed': self.dismissed,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            user_id=data.get('user_id'),
            title=data.get('title', ''),
            message=data.get('message', ''),
            notification_type=data.get('notification_type', 'info'),
            priority=data.get('priority', 'medium'),
            category=data.get('category'),
            created_at=datetime.fromisoformat(data['created_at']),
            read=data.get('read', False),
            dismissed=data.get('dismissed', False),
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None,
            metadata=data.get('metadata', {})
        )

class ModelManager:
    """
    Model manager class with comprehensive logging.
    
    This class provides model management including validation,
    serialization, and operations for the Resume/CV AI application.
    
    Key Features:
    - Model validation
    - Model serialization
    - Model operations
    - Model relationships
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _models (Dict[str, type]): Registered models
    """
    
    def __init__(self):
        """Initialize model manager with comprehensive logging."""
        logger.info("Initializing Model Manager")
        self._initialization_time = datetime.now()
        
        # Initialize models
        self._models = {
            'User': User,
            'Resume': Resume,
            'JobDescription': JobDescription,
            'Analysis': Analysis,
            'Export': Export,
            'Notification': Notification
        }
        
        try:
            logger.info("Model Manager initialized successfully")
            logger.info(f"Registered {len(self._models)} models")
            
        except Exception as e:
            logger.error(f"Model Manager initialization failed: {e}")
            raise
    
    def get_model(self, model_name: str) -> type:
        """
        Get model class by name.
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            type: Model class
        """
        try:
            return self._models.get(model_name)
        except Exception as e:
            logger.error(f"Failed to get model '{model_name}': {e}")
            return None
    
    def register_model(self, model_name: str, model_class: type):
        """
        Register a new model.
        
        Args:
            model_name (str): Name of the model
            model_class (type): Model class
        """
        try:
            self._models[model_name] = model_class
            logger.info(f"Model '{model_name}' registered successfully")
        except Exception as e:
            logger.error(f"Failed to register model '{model_name}': {e}")
    
    def validate_model_data(self, model_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate model data.
        
        Args:
            model_name (str): Name of the model
            data (Dict[str, Any]): Data to validate
            
        Returns:
            Dict[str, Any]: Validation result
        """
        try:
            model_class = self.get_model(model_name)
            if not model_class:
                return {'valid': False, 'error': f'Unknown model: {model_name}'}
            
            # Basic validation
            required_fields = self._get_required_fields(model_class)
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {
                    'valid': False,
                    'error': f'Missing required fields: {missing_fields}',
                    'missing_fields': missing_fields
                }
            
            return {'valid': True}
            
        except Exception as e:
            logger.error(f"Failed to validate model data for '{model_name}': {e}")
            return {'valid': False, 'error': str(e)}
    
    def _get_required_fields(self, model_class: type) -> List[str]:
        """Get required fields for a model class."""
        try:
            # This is a simplified implementation
            # In a real implementation, you would use more sophisticated validation
            if model_class == User:
                return ['id', 'email', 'first_name', 'last_name']
            elif model_class == Resume:
                return ['id', 'user_id', 'title']
            elif model_class == JobDescription:
                return ['id', 'user_id', 'title', 'company', 'description']
            elif model_class == Analysis:
                return ['id', 'user_id']
            elif model_class == Export:
                return ['id', 'user_id']
            elif model_class == Notification:
                return ['id', 'title', 'message']
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to get required fields for model: {e}")
            return []
    
    def serialize_model(self, model_instance: Any) -> Dict[str, Any]:
        """
        Serialize model instance to dictionary.
        
        Args:
            model_instance (Any): Model instance to serialize
            
        Returns:
            Dict[str, Any]: Serialized data
        """
        try:
            if hasattr(model_instance, 'to_dict'):
                return model_instance.to_dict()
            else:
                return {'error': 'Model instance does not have to_dict method'}
                
        except Exception as e:
            logger.error(f"Failed to serialize model instance: {e}")
            return {'error': str(e)}
    
    def deserialize_model(self, model_name: str, data: Dict[str, Any]) -> Any:
        """
        Deserialize dictionary to model instance.
        
        Args:
            model_name (str): Name of the model
            data (Dict[str, Any]): Data to deserialize
            
        Returns:
            Any: Model instance
        """
        try:
            model_class = self.get_model(model_name)
            if not model_class:
                return None
            
            if hasattr(model_class, 'from_dict'):
                return model_class.from_dict(data)
            else:
                return {'error': 'Model class does not have from_dict method'}
                
        except Exception as e:
            logger.error(f"Failed to deserialize model '{model_name}': {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model manager information and statistics.
        
        Returns:
            Dict[str, Any]: Model manager information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "models_count": len(self._models),
                "registered_models": list(self._models.keys()),
                "model_manager_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get model manager info: {e}")
            return {
                "error": str(e),
                "model_manager_timestamp": datetime.now().isoformat()
            }

# Create global model manager instance
model_manager = ModelManager()

# Export model manager functions
get_model = model_manager.get_model
register_model = model_manager.register_model
validate_model_data = model_manager.validate_model_data
serialize_model = model_manager.serialize_model
deserialize_model = model_manager.deserialize_model
