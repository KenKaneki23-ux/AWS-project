"""
Notification service for alerts and messages
Console-based for Phase 1, will integrate with AWS SNS in Phase 3
"""

import sqlite3
import uuid
from datetime import datetime
from config import Config

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
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        notification_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO notifications 
            (notification_id, user_id, title, message, category, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (notification_id, user_id, title, message, category, priority))
        
        conn.commit()
        conn.close()
        
        # Also print to console (Phase 1)
        print(f"\n📢 NOTIFICATION [{priority.upper()}]: {title}")
        print(f"   {message}")
        if user_id:
            print(f"   Target: User {user_id[:8]}...")
        
        return notification_id
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False, limit=20):
        """Get notifications for a user"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        if unread_only:
            cursor.execute('''
                SELECT notification_id, title, message, category, priority, is_read, created_at
                FROM notifications
                WHERE user_id = ? AND is_read = 0
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT notification_id, title, message, category, priority, is_read, created_at
                FROM notifications
                WHERE user_id = ? OR user_id IS NULL
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'notification_id': row[0],
            'title': row[1],
            'message': row[2],
            'category': row[3],
            'priority': row[4],
            'is_read': bool(row[5]),
            'created_at': row[6]
        } for row in rows]
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications
            SET is_read = 1
            WHERE notification_id = ?
        ''', (notification_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM notifications
            WHERE (user_id = ? OR user_id IS NULL) AND is_read = 0
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
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
