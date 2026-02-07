"""
DynamoDB Adapter Implementation
Complete implementation of DatabaseAdapter for AWS DynamoDB
"""

import boto3
from decimal import Decimal
from datetime import datetime
from config import Config


class DynamoDBAdapter:
    """DynamoDB adapter (AWS mode)"""
    
    def __init__(self):
        """Initialize DynamoDB resource"""
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # Table references
        self.users_table = self.dynamodb.Table(Config.DYNAMODB_USERS_TABLE)
        self.accounts_table = self.dynamodb.Table(Config.DYNAMODB_ACCOUNTS_TABLE)
        self.transactions_table = self.dynamodb.Table(Config.DYNAMODB_TRANSACTIONS_TABLE)
    
    def _convert_decimals(self, obj):
        """Convert DynamoDB Decimal objects to float"""
        if isinstance(obj, list):
            return [self._convert_decimals(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            response = self.users_table.get_item(Key={'user_id': user_id})
            if 'Item' in response:
                return self._convert_decimals(response['Item'])
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email using GSI"""
        try:
            response = self.users_table.query(
                IndexName='email-index',
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            if response['Items']:
                return self._convert_decimals(response['Items'][0])
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def create_user(self, user_data):
        """Create new user"""
        try:
            # DynamoDB requires Decimal for numbers
            item = {k: Decimal(str(v)) if isinstance(v, float) else v 
                   for k, v in user_data.items()}
            
            self.users_table.put_item(
                Item=item,
                ConditionExpression='attribute_not_exists(user_id)'
            )
            return True
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return False  # User already exists
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_all_users(self):
        """Get all users"""
        try:
            response = self.users_table.scan()
            return self._convert_decimals(response.get('Items', []))
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    def get_account(self, account_id):
        """Get account by ID"""
        try:
            response = self.accounts_table.get_item(Key={'account_id': account_id})
            if 'Item' in response:
                return self._convert_decimals(response['Item'])
            return None
        except Exception as e:
            print(f"Error getting account: {e}")
            return None
    
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user using GSI"""
        try:
            response = self.accounts_table.query(
                IndexName='user-accounts-index',
                KeyConditionExpression='user_id = :user_id',
                ExpressionAttributeValues={':user_id': user_id}
            )
            return self._convert_decimals(response.get('Items', []))
        except Exception as e:
            print(f"Error getting accounts by user: {e}")
            return []
    
    def create_account(self, account_data):
        """Create new account"""
        try:
            item = {k: Decimal(str(v)) if isinstance(v, float) else v 
                   for k, v in account_data.items()}
            
            self.accounts_table.put_item(Item=item)
            return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
    
    def update_account_balance(self, account_id, new_balance):
        """Update account balance"""
        try:
            self.accounts_table.update_item(
                Key={'account_id': account_id},
                UpdateExpression='SET balance = :balance',
                ExpressionAttributeValues={':balance': Decimal(str(new_balance))}
            )
            return True
        except Exception as e:
            print(f"Error updating account balance: {e}")
            return False
    
    def get_transaction(self, transaction_id):
        """Get transaction by ID"""
        try:
            response = self.transactions_table.get_item(Key={'transaction_id': transaction_id})
            if 'Item' in response:
                item = self._convert_decimals(response['Item'])
                # Convert fraud_flag from number to boolean
                if 'fraud_flag' in item:
                    item['fraud_flag'] = bool(item['fraud_flag'])
                return item
            return None
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    def get_transactions_by_account(self, account_id, limit=100):
        """Get transactions for an account using GSI"""
        try:
            response = self.transactions_table.query(
                IndexName='account-transactions-index',
                KeyConditionExpression='account_id = :account_id',
                ExpressionAttributeValues={':account_id': account_id},
                Limit=limit,
                ScanIndexForward=False  # Sort by timestamp descending
            )
            items = self._convert_decimals(response.get('Items', []))
            # Convert fraud_flag to boolean
            for item in items:
                if 'fraud_flag' in item:
                    item['fraud_flag'] = bool(item['fraud_flag'])
            return items
        except Exception as e:
            print(f"Error getting transactions by account: {e}")
            return []
    
    def create_transaction(self, transaction_data):
        """Create new transaction"""
        try:
            # Add timestamp if not present
            if 'timestamp' not in transaction_data:
                transaction_data['timestamp'] = int(datetime.now().timestamp())
            
            # Convert to DynamoDB format
            item = {}
            for k, v in transaction_data.items():
                if isinstance(v, float):
                    item[k] = Decimal(str(v))
                elif k == 'fraud_flag':
                    item[k] = 1 if v else 0
                else:
                    item[k] = v
            
            # Ensure  timestamp is a number
            if 'timestamp' in item and not isinstance(item['timestamp'], (int, float, Decimal)):
                item['timestamp'] = int(datetime.now().timestamp())
            
            self.transactions_table.put_item(Item=item)
            return True
        except Exception as e:
            print(f"Error creating transaction: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_transaction(self, transaction_id, updates):
        """Update transaction data"""
        try:
            # Build update expression
            update_expr = "SET "
            expr_values = {}
            
            for i, (key, value) in enumerate(updates.items()):
                update_expr += f"{key} = :val{i}, "
                if isinstance(value, float):
                    expr_values[f':val{i}'] = Decimal(str(value))
                elif key == 'fraud_flag':
                    expr_values[f':val{i}'] = 1 if value else 0
                else:
                    expr_values[f':val{i}'] = value
            
            update_expr = update_expr.rstrip(', ')
            
            self.transactions_table.update_item(
                Key={'transaction_id': transaction_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values
            )
            return True
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
