"""
Services Module for Resume/CV AI Application
Handles business services and external integrations.

This module provides:
- Business service layer
- External API integrations
- Service orchestration
- Service monitoring
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("services")

class ServiceManager:
    """
    Service manager class with comprehensive logging.
    
    This class provides service management including service registration,
    orchestration, monitoring, and lifecycle management for the Resume/CV
    AI application.
    
    Key Features:
    - Business service layer
    - External API integrations
    - Service orchestration
    - Service monitoring
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _services (Dict[str, Any]): Registered services
        _service_status (Dict[str, bool]): Service status tracking
    """
    
    def __init__(self):
        """Initialize service manager with comprehensive logging."""
        logger.info("Initializing Service Manager")
        self._initialization_time = datetime.now()
        
        # Initialize services
        self._services = {}
        self._service_status = {}
        
        try:
            # Register core services
            self._register_core_services()
            
            logger.info("Service Manager initialized successfully")
            logger.info(f"Registered {len(self._services)} services")
            
        except Exception as e:
            logger.error(f"Service Manager initialization failed: {e}")
            raise
    
    def _register_core_services(self):
        """Register core services."""
        try:
            # Import and register services
            from .ai_service import AIService
            from .document_service import DocumentService
            from .analysis_service import AnalysisService
            from .export_service import ExportService
            from .notification_service import NotificationService
            
            # Register services
            self._services = {
                'ai_service': AIService(),
                'document_service': DocumentService(),
                'analysis_service': AnalysisService(),
                'export_service': ExportService(),
                'notification_service': NotificationService()
            }
            
            # Initialize service status
            for service_name in self._services:
                self._service_status[service_name] = True
            
            logger.debug(f"Registered {len(self._services)} core services")
            
        except Exception as e:
            logger.warning(f"Failed to register core services: {e}")
            self._services = {}
    
    def get_service(self, service_name: str) -> Any:
        """
        Get service by name.
        
        Args:
            service_name (str): Name of the service
            
        Returns:
            Any: Service instance or None if not found
        """
        try:
            return self._services.get(service_name)
        except Exception as e:
            logger.error(f"Failed to get service '{service_name}': {e}")
            return None
    
    def register_service(self, service_name: str, service_instance: Any):
        """
        Register a new service.
        
        Args:
            service_name (str): Name of the service
            service_instance (Any): Service instance
        """
        try:
            self._services[service_name] = service_instance
            self._service_status[service_name] = True
            logger.info(f"Service '{service_name}' registered successfully")
        except Exception as e:
            logger.error(f"Failed to register service '{service_name}': {e}")
    
    def unregister_service(self, service_name: str):
        """
        Unregister a service.
        
        Args:
            service_name (str): Name of the service to unregister
        """
        try:
            if service_name in self._services:
                del self._services[service_name]
                del self._service_status[service_name]
                logger.info(f"Service '{service_name}' unregistered successfully")
            else:
                logger.warning(f"Service '{service_name}' not found for unregistration")
        except Exception as e:
            logger.error(f"Failed to unregister service '{service_name}': {e}")
    
    def get_service_status(self, service_name: str) -> bool:
        """
        Get service status.
        
        Args:
            service_name (str): Name of the service
            
        Returns:
            bool: True if service is active, False otherwise
        """
        try:
            return self._service_status.get(service_name, False)
        except Exception as e:
            logger.error(f"Failed to get service status for '{service_name}': {e}")
            return False
    
    def set_service_status(self, service_name: str, status: bool):
        """
        Set service status.
        
        Args:
            service_name (str): Name of the service
            status (bool): Service status
        """
        try:
            if service_name in self._services:
                self._service_status[service_name] = status
                logger.info(f"Service '{service_name}' status set to {status}")
            else:
                logger.warning(f"Service '{service_name}' not found for status update")
        except Exception as e:
            logger.error(f"Failed to set service status for '{service_name}': {e}")
    
    def get_all_services(self) -> Dict[str, Any]:
        """
        Get all registered services.
        
        Returns:
            Dict[str, Any]: Dictionary of all services
        """
        return self._services.copy()
    
    def get_service_statuses(self) -> Dict[str, bool]:
        """
        Get all service statuses.
        
        Returns:
            Dict[str, bool]: Dictionary of service statuses
        """
        return self._service_status.copy()
    
    def get_service_manager_info(self) -> Dict[str, Any]:
        """
        Get service manager information and statistics.
        
        Returns:
            Dict[str, Any]: Service manager information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "services_count": len(self._services),
                "active_services": sum(1 for status in self._service_status.values() if status),
                "service_names": list(self._services.keys()),
                "service_statuses": self._service_status,
                "service_manager_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get service manager info: {e}")
            return {
                "error": str(e),
                "service_manager_timestamp": datetime.now().isoformat()
            }

# Create global service manager instance
service_manager = ServiceManager()

# Export service manager functions
get_service = service_manager.get_service
register_service = service_manager.register_service
unregister_service = service_manager.unregister_service
get_service_status = service_manager.get_service_status
set_service_status = service_manager.set_service_status
get_all_services = service_manager.get_all_services
get_service_statuses = service_manager.get_service_statuses
