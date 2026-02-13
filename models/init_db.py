"""
DynamoDB Table Initialization
Creates all required tables with proper schemas and indexes
"""

import boto3
from config import Config

def get_dynamodb_resource():
    """
    Get DynamoDB resource with credentials from config
    Supports both:
    - Explicit credentials (local development)
    - IAM roles (EC2 instance with attached role)
    """
    # If credentials are provided, use them (local development)
    if Config.AWS_ACCESS_KEY_ID and Config.AWS_SECRET_ACCESS_KEY:
        return boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
    
    # Otherwise, use IAM role (EC2 instance)
    return boto3.resource('dynamodb', region_name=Config.AWS_REGION)

def init_db():
    """Initialize all DynamoDB tables"""
    dynamodb = get_dynamodb_resource()
    existing_tables = [table.name for table in dynamodb.tables.all()]
    
    print("=" * 60)
    print("INITIALIZING DYNAMODB TABLES")
    print("=" * 60)
    print(f"Region: {Config.AWS_REGION}")
    print(f"Existing tables: {existing_tables}")
    print("=" * 60)
    
    # Create Users Table
    if Config.DYNAMODB_USERS_TABLE not in existing_tables:
        print(f"\n📦 Creating table: {Config.DYNAMODB_USERS_TABLE}")
        users_table = dynamodb.create_table(
            TableName=Config.DYNAMODB_USERS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        print(f"⏳ Waiting for {Config.DYNAMODB_USERS_TABLE} to be created...")
        users_table.meta.client.get_waiter('table_exists').wait(TableName=Config.DYNAMODB_USERS_TABLE)
        print(f"✅ Table {Config.DYNAMODB_USERS_TABLE} created successfully!")
    else:
        print(f"✓ Table {Config.DYNAMODB_USERS_TABLE} already exists")
    
    # Create Accounts Table
    if Config.DYNAMODB_ACCOUNTS_TABLE not in existing_tables:
        print(f"\n📦 Creating table: {Config.DYNAMODB_ACCOUNTS_TABLE}")
        accounts_table = dynamodb.create_table(
            TableName=Config.DYNAMODB_ACCOUNTS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'account_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'account_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-accounts-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        print(f"⏳ Waiting for {Config.DYNAMODB_ACCOUNTS_TABLE} to be created...")
        accounts_table.meta.client.get_waiter('table_exists').wait(TableName=Config.DYNAMODB_ACCOUNTS_TABLE)
        print(f"✅ Table {Config.DYNAMODB_ACCOUNTS_TABLE} created successfully!")
    else:
        print(f"✓ Table {Config.DYNAMODB_ACCOUNTS_TABLE} already exists")
    
    # Create Transactions Table
    if Config.DYNAMODB_TRANSACTIONS_TABLE not in existing_tables:
        print(f"\n📦 Creating table: {Config.DYNAMODB_TRANSACTIONS_TABLE}")
        transactions_table = dynamodb.create_table(
            TableName=Config.DYNAMODB_TRANSACTIONS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'transaction_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'transaction_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'account_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'account-transactions-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'account_id',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'timestamp',
                            'KeyType': 'RANGE'  # Sort key for chronological ordering
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        print(f"⏳ Waiting for {Config.DYNAMODB_TRANSACTIONS_TABLE} to be created...")
        transactions_table.meta.client.get_waiter('table_exists').wait(TableName=Config.DYNAMODB_TRANSACTIONS_TABLE)
        print(f"✅ Table {Config.DYNAMODB_TRANSACTIONS_TABLE} created successfully!")
    else:
        print(f"✓ Table {Config.DYNAMODB_TRANSACTIONS_TABLE} already exists")
    
    # Create Notifications Table (optional)
    if Config.DYNAMODB_NOTIFICATIONS_TABLE not in existing_tables:
        print(f"\n📦 Creating table: {Config.DYNAMODB_NOTIFICATIONS_TABLE}")
        notifications_table = dynamodb.create_table(
            TableName=Config.DYNAMODB_NOTIFICATIONS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'notification_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'notification_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-notifications-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        print(f"⏳ Waiting for {Config.DYNAMODB_NOTIFICATIONS_TABLE} to be created...")
        notifications_table.meta.client.get_waiter('table_exists').wait(TableName=Config.DYNAMODB_NOTIFICATIONS_TABLE)
        print(f"✅ Table {Config.DYNAMODB_NOTIFICATIONS_TABLE} created successfully!")
    else:
        print(f"✓ Table {Config.DYNAMODB_NOTIFICATIONS_TABLE} already exists")
    
    print("\n" + "=" * 60)
    print("✅ ALL TABLES INITIALIZED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    """Run table initialization"""
    init_db()
