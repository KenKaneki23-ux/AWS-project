"""
Notification service for alerts and messages
DynamoDB-based for Phase 2+, will integrate with AWS SNS in Phase 3
"""

import uuid
from datetime import datetime
from services.database_adapter import get_database_adapter

class NotificationService:
    """Service for managing notifications and alerts"""
    
    @staticmethod
    def create_notification(user_id, title, message, category='system_info', priority='normal'):
        """
        Create a new notification
        
        Args:
            user_id: Target user ID (None for system-wide)
            title: Notification title
            message: Notification message
            category: fraud_alert, compliance_warning, or system_info
            priority: low, normal, high, or critical
        
        Returns:
            Notification ID
        """
        db = get_database_adapter()
        
        notification_id = str(uuid.uuid4())
        
        notification_data = {
            'notification_id': notification_id,
            'user_id': user_id,
            'title': title,
            'message': message,
            'category': category,
            'priority': priority,
            'is_read': 0,
            'timestamp': int(datetime.now().timestamp())
        }
        
        # Would need to implement create_notification in database_adapter
        # For now, just print to console
        
        # Also print to console (Phase 1 compatibility)
        print(f"\n📢 NOTIFICATION [{priority.upper()}]: {title}")
        print(f"   {message}")
        if user_id:
            print(f"   Target: User {user_id[:8]}...")
        
        return notification_id
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False, limit=20):
        """Get notifications for a user"""
        # Placeholder - would need notifications table in DynamoDB
        # For now, return empty list
        return []
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        # Placeholder - would need notifications table in DynamoDB
        pass
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        # Placeholder - would need notifications table in DynamoDB
        return 0
    
    @staticmethod
    def send_fraud_alert(user_id, transaction_id, reason):
        """Send fraud alert notification"""
        return NotificationService.create_notification(
            user_id,
            '🚨 Fraud Alert',
            f'Suspicious transaction detected: {transaction_id[:8]}... - {reason}',
            category='fraud_alert',
            priority='high'
        )
    
    @staticmethod
    def send_compliance_warning(user_id, metric, value, threshold):
        """Send compliance warning notification"""
        return NotificationService.create_notification(
            user_id,
            '⚠️ Compliance Warning',
            f'{metric} ({value}) has exceeded threshold ({threshold})',
            category='compliance_warning',
            priority='high'
        )
