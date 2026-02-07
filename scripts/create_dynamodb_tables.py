"""
Script to create DynamoDB tables for Cloud Banking Analytics
Creates all tables with appropriate partition keys and Global Secondary Indexes (GSIs)
"""

import boto3
import sys
from botocore.exceptions import ClientError

def create_dynamodb_tables(region='us-east-1'):
    """
    Create all DynamoDB tables for the application
    
    Tables created:
    1. cloudbank-users (Partition: user_id, GSI: email)
    2. cloudbank-accounts (Partition: account_id, GSI: user_id)
    3. cloudbank-transactions (Partition: transaction_id, GSI: account_id + timestamp, fraud_flag + timestamp)
    4. cloudbank-notifications (Partition: notification_id, GSI: user_id + created_at)
    5. cloudbank-audit-log (Partition: log_id, GSI: user_id + timestamp)
    """
    
    print("=" * 70)
    print("DynamoDB Table Creation Script")
    print("=" * 70)
    print(f"Region: {region}")
    print()
    
    try:
        dynamodb = boto3.client('dynamodb', region_name=region)
        
        # 1. Users Table
        print("Creating cloudbank-users table...")
        try:
            dynamodb.create_table(
                TableName='cloudbank-users',
                KeySchema=[
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'}  # Partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'user_id', 'AttributeType': 'S'},
                    {'AttributeName': 'email', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'email-index',
                        'KeySchema': [
                            {'AttributeName': 'email', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
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
            print("✅ cloudbank-users table created")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("⚠️  cloudbank-users table already exists")
            else:
                raise
        
        # 2. Accounts Table
        print("\nCreating cloudbank-accounts table...")
        try:
            dynamodb.create_table(
                TableName='cloudbank-accounts',
                KeySchema=[
                    {'AttributeName': 'account_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'account_id', 'AttributeType': 'S'},
                    {'AttributeName': 'user_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'user-accounts-index',
                        'KeySchema': [
                            {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
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
            print("✅ cloudbank-accounts table created")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("⚠️  cloudbank-accounts table already exists")
            else:
                raise
        
        # 3. Transactions Table
        print("\nCreating cloudbank-transactions table...")
        try:
            dynamodb.create_table(
                TableName='cloudbank-transactions',
                KeySchema=[
                    {'AttributeName': 'transaction_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'transaction_id', 'AttributeType': 'S'},
                    {'AttributeName': 'account_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'N'},
                    {'AttributeName': 'fraud_flag', 'AttributeType': 'N'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'account-transactions-index',
                        'KeySchema': [
                            {'AttributeName': 'account_id', 'KeyType': 'HASH'},
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                    },
                    {
                        'IndexName': 'fraud-transactions-index',
                        'KeySchema': [
                            {'AttributeName': 'fraud_flag', 'KeyType': 'HASH'},
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print("✅ cloudbank-transactions table created")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("⚠️  cloudbank-transactions table already exists")
            else:
                raise
        
        # 4. Notifications Table
        print("\nCreating cloudbank-notifications table...")
        try:
            dynamodb.create_table(
                TableName='cloudbank-notifications',
                KeySchema=[
                    {'AttributeName': 'notification_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'notification_id', 'AttributeType': 'S'},
                    {'AttributeName': 'user_id', 'AttributeType': 'S'},
                    {'AttributeName': 'created_at', 'AttributeType': 'N'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'user-notifications-index',
                        'KeySchema': [
                            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                            {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
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
            print("✅ cloudbank-notifications table created")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("⚠️  cloudbank-notifications table already exists")
            else:
                raise
        
        # 5. Audit Log Table
        print("\nCreating cloudbank-audit-log table...")
        try:
            dynamodb.create_table(
                TableName='cloudbank-audit-log',
                KeySchema=[
                    {'AttributeName': 'log_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'log_id', 'AttributeType': 'S'},
                    {'AttributeName': 'user_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'N'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'user-audit-index',
                        'KeySchema': [
                            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
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
            print("✅ cloudbank-audit-log table created")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("⚠️  cloudbank-audit-log table already exists")
            else:
                raise
        
        print("\n" + "=" * 70)
        print("✅ Table creation complete!")
        print("=" * 70)
        print("\nWaiting for tables to become ACTIVE...")
        print("This may take 30-60 seconds...")
        
        # Wait for all tables to become active
        waiter = dynamodb.get_waiter('table_exists')
        tables = [
            'cloudbank-users',
            'cloudbank-accounts',
            'cloudbank-transactions',
            'cloudbank-notifications',
            'cloudbank-audit-log'
        ]
        
        for table_name in tables:
            print(f"Waiting for {table_name}...", end='', flush=True)
            waiter.wait(TableName=table_name)
            print(" ✅")
        
        print("\n" + "=" * 70)
        print("🎉 All tables are ACTIVE and ready to use!")
        print("=" * 70)
        
        # Display table information
        print("\nTable Summary:")
        for table_name in tables:
            response = dynamodb.describe_table(TableName=table_name)
            table = response['Table']
            print(f"\n📊 {table_name}")
            print(f"   Status: {table['TableStatus']}")
            print(f"   Items: {table['ItemCount']}")
            print(f"   Size: {table['TableSizeBytes']} bytes")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import os
    
    # Get region from environment or use default
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print("\n⚠️  WARNING: This script will create DynamoDB tables in your AWS account.")
    print("   Make sure your AWS credentials are configured correctly.")
    print(f"   Region: {region}")
    print()
    
    response = input("Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        sys.exit(0)
    
    success = create_dynamodb_tables(region)
    sys.exit(0 if success else 1)
