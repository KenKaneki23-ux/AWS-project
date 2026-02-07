"""
Notification adapter for DynamoDB
"""

import boto3
import uuid
from decimal import Decimal
from datetime import datetime
from config import Config


class NotificationAdapter:
    """DynamoDB notification adapter"""
    
    def __init__(self):
        """Initialize DynamoDB resource"""
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        self.notifications_table = self.dynamodb.Table(Config.DYNAMODB_NOTIFICATIONS_TABLE)
    
    def create_notification(self, notification_data):
        """Create notification in DynamoDB"""
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
                if 'created_at' in item and isinstance(item['created_at'], Decimal):
                    item['created_at'] = float(item['created_at'])
            
            return items
        except Exception as e:
            print(f"Error getting notifications: {e}")
            return []


def get_notification_adapter():
    """Get the notification adapter instance"""
    return NotificationAdapter()
