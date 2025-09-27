"""
Cache Manager Utilities for Resume/CV AI Application
Provides caching functionality for improved performance.

This module provides:
- In-memory caching system
- Cache expiration and cleanup
- Cache statistics and monitoring
- Cache configuration management
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import time
import json
import logging
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from threading import Lock

from .logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("cache_manager")

class CacheManager:
    """
    Cache manager utilities class with comprehensive logging.
    
    This class provides caching functionality including in-memory caching,
    expiration management, cleanup, and monitoring for the Resume/CV AI
    application.
    
    Key Features:
    - In-memory caching system
    - Cache expiration and cleanup
    - Cache statistics and monitoring
    - Cache configuration management
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _cache (Dict[str, Dict]): Cache storage
        _lock (Lock): Thread lock for cache operations
        _default_ttl (int): Default time-to-live in seconds
        _max_size (int): Maximum cache size
        _cleanup_interval (int): Cache cleanup interval in seconds
    """
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000, 
                 cleanup_interval: int = 300):
        """
        Initialize cache manager with comprehensive logging.
        
        Args:
            default_ttl (int): Default time-to-live in seconds
            max_size (int): Maximum cache size
            cleanup_interval (int): Cache cleanup interval in seconds
        """
        logger.info("Initializing Cache Manager")
        self._initialization_time = datetime.now()
        
        # Set cache configuration
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._cleanup_interval = cleanup_interval
        
        # Initialize cache storage
        self._cache = {}
        self._lock = Lock()
        
        # Initialize statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'cleanups': 0,
            'evictions': 0
        }
        
        try:
            logger.info("Cache Manager initialized successfully")
            logger.info(f"Default TTL: {default_ttl} seconds")
            logger.info(f"Max size: {max_size}")
            logger.info(f"Cleanup interval: {cleanup_interval} seconds")
            
        except Exception as e:
            logger.error(f"Cache Manager initialization failed: {e}")
            raise
    
    def get(self, key: str) -> Any:
        """
        Get value from cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            Any: Cached value or None if not found/expired
        """
        try:
            with self._lock:
                if key not in self._cache:
                    self._stats['misses'] += 1
                    logger.debug(f"Cache miss for key: {key}")
                    return None
                
                cache_entry = self._cache[key]
                
                # Check if expired
                if self._is_expired(cache_entry):
                    del self._cache[key]
                    self._stats['misses'] += 1
                    logger.debug(f"Cache miss for expired key: {key}")
                    return None
                
                # Update access time
                cache_entry['last_accessed'] = time.time()
                self._stats['hits'] += 1
                logger.debug(f"Cache hit for key: {key}")
                
                return cache_entry['value']
                
        except Exception as e:
            logger.error(f"Failed to get cache key '{key}': {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Set value in cache.
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            ttl (int): Time-to-live in seconds (optional)
            
        Returns:
            bool: True if set successfully, False otherwise
        """
        try:
            with self._lock:
                # Use default TTL if not specified
                if ttl is None:
                    ttl = self._default_ttl
                
                # Check cache size limit
                if len(self._cache) >= self._max_size and key not in self._cache:
                    self._evict_oldest()
                
                # Create cache entry
                cache_entry = {
                    'value': value,
                    'created_at': time.time(),
                    'last_accessed': time.time(),
                    'ttl': ttl
                }
                
                self._cache[key] = cache_entry
                self._stats['sets'] += 1
                
                logger.debug(f"Cache set for key: {key} (TTL: {ttl}s)")
                return True
                
        except Exception as e:
            logger.error(f"Failed to set cache key '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key (str): Cache key to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            with self._lock:
                if key in self._cache:
                    del self._cache[key]
                    self._stats['deletes'] += 1
                    logger.debug(f"Cache delete for key: {key}")
                    return True
                else:
                    logger.debug(f"Cache key not found for deletion: {key}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to delete cache key '{key}': {e}")
            return False
    
    def clear(self) -> bool:
        """
        Clear all cache entries.
        
        Returns:
            bool: True if cleared successfully, False otherwise
        """
        try:
            with self._lock:
                self._cache.clear()
                logger.info("Cache cleared successfully")
                return True
                
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache and is not expired.
        
        Args:
            key (str): Cache key to check
            
        Returns:
            bool: True if key exists and is not expired, False otherwise
        """
        try:
            with self._lock:
                if key not in self._cache:
                    return False
                
                cache_entry = self._cache[key]
                return not self._is_expired(cache_entry)
                
        except Exception as e:
            logger.error(f"Failed to check cache key existence '{key}': {e}")
            return False
    
    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: int = None) -> Any:
        """
        Get value from cache or set it using factory function.
        
        Args:
            key (str): Cache key
            factory (Callable[[], Any]): Function to generate value if not cached
            ttl (int): Time-to-live in seconds (optional)
            
        Returns:
            Any: Cached or generated value
        """
        try:
            # Try to get from cache first
            value = self.get(key)
            if value is not None:
                return value
            
            # Generate value using factory
            value = factory()
            
            # Set in cache
            self.set(key, value, ttl)
            
            return value
            
        except Exception as e:
            logger.error(f"Failed to get or set cache key '{key}': {e}")
            return None
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """
        Check if cache entry is expired.
        
        Args:
            cache_entry (Dict[str, Any]): Cache entry to check
            
        Returns:
            bool: True if expired, False otherwise
        """
        try:
            current_time = time.time()
            created_at = cache_entry['created_at']
            ttl = cache_entry['ttl']
            
            return (current_time - created_at) > ttl
            
        except Exception as e:
            logger.error(f"Failed to check cache entry expiration: {e}")
            return True
    
    def _evict_oldest(self):
        """Evict oldest cache entry."""
        try:
            if not self._cache:
                return
            
            # Find oldest entry
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k]['last_accessed'])
            
            del self._cache[oldest_key]
            self._stats['evictions'] += 1
            
            logger.debug(f"Evicted oldest cache entry: {oldest_key}")
            
        except Exception as e:
            logger.error(f"Failed to evict oldest cache entry: {e}")
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired cache entries.
        
        Returns:
            int: Number of entries cleaned up
        """
        try:
            with self._lock:
                expired_keys = []
                
                for key, cache_entry in self._cache.items():
                    if self._is_expired(cache_entry):
                        expired_keys.append(key)
                
                for key in expired_keys:
                    del self._cache[key]
                
                self._stats['cleanups'] += 1
                
                if expired_keys:
                    logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
                
                return len(expired_keys)
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired cache entries: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        try:
            with self._lock:
                total_requests = self._stats['hits'] + self._stats['misses']
                hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0
                
                return {
                    'hits': self._stats['hits'],
                    'misses': self._stats['misses'],
                    'sets': self._stats['sets'],
                    'deletes': self._stats['deletes'],
                    'cleanups': self._stats['cleanups'],
                    'evictions': self._stats['evictions'],
                    'hit_rate': round(hit_rate, 2),
                    'size': len(self._cache),
                    'max_size': self._max_size,
                    'default_ttl': self._default_ttl
                }
                
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache information and statistics.
        
        Returns:
            Dict[str, Any]: Cache information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "cache_size": len(self._cache),
                "max_size": self._max_size,
                "default_ttl": self._default_ttl,
                "cleanup_interval": self._cleanup_interval,
                "stats": self.get_stats(),
                "cache_manager_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get cache info: {e}")
            return {
                "error": str(e),
                "cache_manager_timestamp": datetime.now().isoformat()
            }

# Create global cache manager instance
cache_manager = CacheManager()

# Export commonly used functions
get = cache_manager.get
set = cache_manager.set
delete = cache_manager.delete
clear = cache_manager.clear
exists = cache_manager.exists
get_or_set = cache_manager.get_or_set
cleanup_expired = cache_manager.cleanup_expired
get_stats = cache_manager.get_stats