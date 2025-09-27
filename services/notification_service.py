"""
Notification Service for Resume/CV AI Application
Handles notifications and alerts.

This module provides:
- Notification management
- Alert system
- User notifications
- System notifications
- Comprehensive logging

Author: Resume AI Team
Created: 2024
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum

from utils.logger import setup_logger

# Initialize logger with module-specific name
logger = setup_logger("notification_service")

class NotificationType(Enum):
    """Notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SYSTEM = "system"

class NotificationPriority(Enum):
    """Notification priorities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationService:
    """
    Notification service class with comprehensive logging.
    
    This class provides notification management including alerts,
    user notifications, and system notifications for the Resume/CV
    AI application.
    
    Key Features:
    - Notification management
    - Alert system
    - User notifications
    - System notifications
    - Comprehensive logging
    
    Attributes:
        _initialization_time (datetime): Timestamp of initialization start
        _notifications (List[Dict]): Notification storage
        _notification_settings (Dict[str, Any]): Notification settings
        _max_notifications (int): Maximum number of notifications to store
    """
    
    def __init__(self, max_notifications: int = 1000):
        """
        Initialize notification service with comprehensive logging.
        
        Args:
            max_notifications (int): Maximum number of notifications to store
        """
        logger.info("Initializing Notification Service")
        self._initialization_time = datetime.now()
        
        # Initialize notification components
        self._notifications = []
        self._max_notifications = max_notifications
        self._notification_settings = {
            'enable_notifications': True,
            'enable_system_notifications': True,
            'enable_user_notifications': True,
            'notification_retention_days': 30,
            'max_notifications_per_user': 100
        }
        
        try:
            logger.info("Notification Service initialized successfully")
            logger.info(f"Max notifications: {max_notifications}")
            
        except Exception as e:
            logger.error(f"Notification Service initialization failed: {e}")
            raise
    
    def create_notification(self, title: str, message: str, 
                          notification_type: NotificationType = NotificationType.INFO,
                          priority: NotificationPriority = NotificationPriority.MEDIUM,
                          user_id: str = None, category: str = None,
                          expires_at: datetime = None) -> Dict[str, Any]:
        """
        Create a new notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            notification_type (NotificationType): Type of notification
            priority (NotificationPriority): Priority level
            user_id (str): User ID (optional)
            category (str): Notification category (optional)
            expires_at (datetime): Expiration time (optional)
            
        Returns:
            Dict[str, Any]: Notification creation result
        """
        try:
            logger.info(f"Creating notification: {title}")
            
            # Generate notification ID
            notification_id = f"notif_{len(self._notifications) + 1}_{int(time.time())}"
            
            # Set default expiration time
            if expires_at is None:
                expires_at = datetime.now() + timedelta(days=7)
            
            # Create notification
            notification = {
                'id': notification_id,
                'title': title,
                'message': message,
                'type': notification_type.value,
                'priority': priority.value,
                'user_id': user_id,
                'category': category,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat(),
                'read': False,
                'dismissed': False
            }
            
            # Add to notifications list
            self._notifications.append(notification)
            
            # Clean up old notifications if needed
            self._cleanup_old_notifications()
            
            logger.info(f"Notification created successfully: {notification_id}")
            return {
                'success': True,
                'notification_id': notification_id,
                'notification': notification
            }
            
        except Exception as e:
            logger.error(f"Failed to create notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_notifications(self, user_id: str = None, category: str = None,
                         unread_only: bool = False, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get notifications based on filters.
        
        Args:
            user_id (str): User ID filter (optional)
            category (str): Category filter (optional)
            unread_only (bool): Only return unread notifications
            limit (int): Maximum number of notifications to return
            
        Returns:
            List[Dict[str, Any]]: List of notifications
        """
        try:
            logger.debug(f"Getting notifications for user: {user_id}")
            
            # Filter notifications
            filtered_notifications = self._notifications.copy()
            
            # Apply filters
            if user_id:
                filtered_notifications = [n for n in filtered_notifications if n.get('user_id') == user_id]
            
            if category:
                filtered_notifications = [n for n in filtered_notifications if n.get('category') == category]
            
            if unread_only:
                filtered_notifications = [n for n in filtered_notifications if not n.get('read', False)]
            
            # Sort by creation time (newest first)
            filtered_notifications.sort(key=lambda x: x['created_at'], reverse=True)
            
            # Apply limit
            if limit > 0:
                filtered_notifications = filtered_notifications[:limit]
            
            logger.debug(f"Found {len(filtered_notifications)} notifications")
            return filtered_notifications
            
        except Exception as e:
            logger.error(f"Failed to get notifications: {e}")
            return []
    
    def mark_as_read(self, notification_id: str) -> bool:
        """
        Mark notification as read.
        
        Args:
            notification_id (str): ID of the notification
            
        Returns:
            bool: True if marked as read successfully, False otherwise
        """
        try:
            for notification in self._notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    logger.debug(f"Notification marked as read: {notification_id}")
                    return True
            
            logger.warning(f"Notification not found: {notification_id}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {e}")
            return False
    
    def mark_as_unread(self, notification_id: str) -> bool:
        """
        Mark notification as unread.
        
        Args:
            notification_id (str): ID of the notification
            
        Returns:
            bool: True if marked as unread successfully, False otherwise
        """
        try:
            for notification in self._notifications:
                if notification['id'] == notification_id:
                    notification['read'] = False
                    logger.debug(f"Notification marked as unread: {notification_id}")
                    return True
            
            logger.warning(f"Notification not found: {notification_id}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to mark notification as unread: {e}")
            return False
    
    def dismiss_notification(self, notification_id: str) -> bool:
        """
        Dismiss notification.
        
        Args:
            notification_id (str): ID of the notification
            
        Returns:
            bool: True if dismissed successfully, False otherwise
        """
        try:
            for notification in self._notifications:
                if notification['id'] == notification_id:
                    notification['dismissed'] = True
                    logger.debug(f"Notification dismissed: {notification_id}")
                    return True
            
            logger.warning(f"Notification not found: {notification_id}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to dismiss notification: {e}")
            return False
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        Delete notification.
        
        Args:
            notification_id (str): ID of the notification
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            for i, notification in enumerate(self._notifications):
                if notification['id'] == notification_id:
                    del self._notifications[i]
                    logger.debug(f"Notification deleted: {notification_id}")
                    return True
            
            logger.warning(f"Notification not found: {notification_id}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete notification: {e}")
            return False
    
    def get_notification_count(self, user_id: str = None, unread_only: bool = False) -> int:
        """
        Get notification count.
        
        Args:
            user_id (str): User ID filter (optional)
            unread_only (bool): Only count unread notifications
            
        Returns:
            int: Number of notifications
        """
        try:
            notifications = self.get_notifications(user_id=user_id, unread_only=unread_only)
            return len(notifications)
            
        except Exception as e:
            logger.error(f"Failed to get notification count: {e}")
            return 0
    
    def _cleanup_old_notifications(self):
        """Clean up old notifications."""
        try:
            current_time = datetime.now()
            retention_days = self._notification_settings.get('notification_retention_days', 30)
            cutoff_time = current_time - timedelta(days=retention_days)
            
            # Remove expired notifications
            original_count = len(self._notifications)
            self._notifications = [
                n for n in self._notifications
                if datetime.fromisoformat(n['expires_at']) > cutoff_time
            ]
            
            removed_count = original_count - len(self._notifications)
            if removed_count > 0:
                logger.debug(f"Cleaned up {removed_count} old notifications")
            
            # Limit total notifications
            if len(self._notifications) > self._max_notifications:
                # Remove oldest notifications
                self._notifications.sort(key=lambda x: x['created_at'])
                self._notifications = self._notifications[-self._max_notifications:]
                logger.debug(f"Limited notifications to {self._max_notifications}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old notifications: {e}")
    
    def send_system_notification(self, title: str, message: str, 
                               priority: NotificationPriority = NotificationPriority.MEDIUM) -> Dict[str, Any]:
        """
        Send system notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            priority (NotificationPriority): Priority level
            
        Returns:
            Dict[str, Any]: Notification result
        """
        try:
            if not self._notification_settings.get('enable_system_notifications', True):
                return {'success': False, 'error': 'System notifications are disabled'}
            
            return self.create_notification(
                title=title,
                message=message,
                notification_type=NotificationType.SYSTEM,
                priority=priority,
                category='system'
            )
            
        except Exception as e:
            logger.error(f"Failed to send system notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_user_notification(self, user_id: str, title: str, message: str,
                             notification_type: NotificationType = NotificationType.INFO,
                             priority: NotificationPriority = NotificationPriority.MEDIUM,
                             category: str = None) -> Dict[str, Any]:
        """
        Send user notification.
        
        Args:
            user_id (str): User ID
            title (str): Notification title
            message (str): Notification message
            notification_type (NotificationType): Type of notification
            priority (NotificationPriority): Priority level
            category (str): Notification category
            
        Returns:
            Dict[str, Any]: Notification result
        """
        try:
            if not self._notification_settings.get('enable_user_notifications', True):
                return {'success': False, 'error': 'User notifications are disabled'}
            
            return self.create_notification(
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                user_id=user_id,
                category=category
            )
            
        except Exception as e:
            logger.error(f"Failed to send user notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_notification_statistics(self) -> Dict[str, Any]:
        """
        Get notification statistics.
        
        Returns:
            Dict[str, Any]: Notification statistics
        """
        try:
            total_notifications = len(self._notifications)
            unread_count = sum(1 for n in self._notifications if not n.get('read', False))
            dismissed_count = sum(1 for n in self._notifications if n.get('dismissed', False))
            
            # Count by type
            type_counts = {}
            for notification in self._notifications:
                notif_type = notification.get('type', 'unknown')
                type_counts[notif_type] = type_counts.get(notif_type, 0) + 1
            
            # Count by priority
            priority_counts = {}
            for notification in self._notifications:
                priority = notification.get('priority', 'unknown')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            return {
                'total_notifications': total_notifications,
                'unread_count': unread_count,
                'dismissed_count': dismissed_count,
                'read_count': total_notifications - unread_count,
                'type_counts': type_counts,
                'priority_counts': priority_counts
            }
            
        except Exception as e:
            logger.error(f"Failed to get notification statistics: {e}")
            return {'error': str(e)}
    
    def update_notification_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Update notification settings.
        
        Args:
            settings (Dict[str, Any]): Settings to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            self._notification_settings.update(settings)
            logger.info("Notification settings updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update notification settings: {e}")
            return False
    
    def get_notification_settings(self) -> Dict[str, Any]:
        """
        Get notification settings.
        
        Returns:
            Dict[str, Any]: Notification settings
        """
        return self._notification_settings.copy()
    
    def get_notification_service_info(self) -> Dict[str, Any]:
        """
        Get notification service information and statistics.
        
        Returns:
            Dict[str, Any]: Notification service information
        """
        try:
            return {
                "initialization_time": self._initialization_time.isoformat(),
                "total_notifications": len(self._notifications),
                "max_notifications": self._max_notifications,
                "notification_settings": self._notification_settings,
                "statistics": self.get_notification_statistics(),
                "notification_service_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get notification service info: {e}")
            return {
                "error": str(e),
                "notification_service_timestamp": datetime.now().isoformat()
            }
