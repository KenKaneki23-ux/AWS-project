"""
Notification adapter interface for dual-mode support
Provides abstraction layer for notifications (database storage only)
"""

from abc import ABC, abstractmethod
import sqlite3
import uuid
from datetime import datetime
from config import Config


class NotificationAdapter(ABC):
    """Abstract base class for notification operations"""
    
    @abstractmethod
    def create_notification(self, notification_data):
        """Create notification"""
        pass
    
    @abstractmethod
    def get_notifications_by_user(self, user_id, limit=50):
        """Get notifications for a user"""
        pass


class LocalNotificationAdapter(NotificationAdapter):
    """Local notification adapter (database only)"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_notification(self, notification_data):
        """Create notification in database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        notification_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO notifications 
            (notification_id, user_id, title, message, category, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            notification_id,
            notification_data.get('user_id'),
            notification_data.get('title'),
            notification_data.get('message'),
            notification_data.get('category', 'info'),
            notification_data.get('priority', 'normal'),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return notification_id
    
    def get_notifications_by_user(self, user_id, limit=50):
        """Get notifications for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT notification_id, user_id, title, message, category, priority, created_at, read_status
            FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'notification_id': row[0],
            'user_id': row[1],
            'title': row[2],
            'message': row[3],
            'category': row[4],
            'priority': row[5],
            'created_at': row[6],
            'read_status': row[7]
        } for row in rows]


class AWSNotificationAdapter(NotificationAdapter):
    """AWS notification adapter (DynamoDB storage only)"""
    
    def __init__(self):
        import boto3
        from decimal import Decimal
        
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        self.notifications_table = self.dynamodb.Table(Config.DYNAMODB_NOTIFICATIONS_TABLE)
    
    def create_notification(self, notification_data):
        """Create notification in DynamoDB"""
        from decimal import Decimal
        
        notification_id = str(uuid.uuid4())
        
        item = {
            'notification_id': notification_id,
            'user_id': notification_data.get('user_id'),
            'title': notification_data.get('title'),
            'message': notification_data.get('message'),
            'category': notification_data.get('category', 'info'),
            'priority': notification_data.get('priority', 'normal'),
            'created_at': Decimal(str(datetime.now().timestamp())),
            'read_status': False
        }
        
        try:
            self.notifications_table.put_item(Item=item)
            return notification_id
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
    
    def get_notifications_by_user(self, user_id, limit=50):
        """Get notifications for a user using GSI"""
        try:
            response = self.notifications_table.query(
                IndexName='user-notifications-index',
                KeyConditionExpression='user_id = :user_id',
                ExpressionAttributeValues={':user_id': user_id},
                Limit=limit,
                ScanIndexForward=False
            )
            
            items = response.get('Items', [])
            
            for item in items:
                if 'created_at' in item:
                    from decimal import Decimal
                    if isinstance(item['created_at'], Decimal):
                        item['created_at'] = float(item['created_at'])
            
            return items
        except Exception as e:
            print(f"Error getting notifications: {e}")
            return []


def get_notification_adapter():
    """
    Factory function to get the appropriate notification adapter
    
    Returns:
        NotificationAdapter: LocalNotificationAdapter or AWSNotificationAdapter
    """
    if Config.USE_AWS:
        return AWSNotificationAdapter()
    else:
        return LocalNotificationAdapter()
