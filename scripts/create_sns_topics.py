"""
Script to create SNS topics for Cloud Banking Analytics
Creates topics for fraud alerts, compliance warnings, and system notifications
"""

import boto3
import sys
from botocore.exceptions import ClientError


def create_sns_topics(region='us-east-1'):
    """
    Create SNS topics for the application
    
    Topics created:
    1. cloudbank-fraud-alerts - High priority fraud notifications
    2. cloudbank-compliance-warnings - Compliance threshold violations
    3. cloudbank-system-alerts - System errors and notifications
    """
    
    print("=" * 70)
    print("SNS Topic Creation Script")
    print("=" * 70)
    print(f"Region: {region}")
    print()
    
    try:
        sns = boto3.client('sns', region_name=region)
        topic_arns = {}
        
        # 1. Fraud Alerts Topic
        print("Creating cloudbank-fraud-alerts topic...")
        try:
            response = sns.create_topic(
                Name='cloudbank-fraud-alerts',
                Attributes={
                    'DisplayName': 'CloudBank Fraud Alerts',
                    'FifoTopic': 'false'
                }
            )
            topic_arns['fraud'] = response['TopicArn']
            print(f"✅ Created: {response['TopicArn']}")
        except ClientError as e:
            print(f"⚠️  Error: {e}")
        
        # 2. Compliance Warnings Topic
        print("\nCreating cloudbank-compliance-warnings topic...")
        try:
            response = sns.create_topic(
                Name='cloudbank-compliance-warnings',
                Attributes={
                    'DisplayName': 'CloudBank Compliance Warnings',
                    'FifoTopic': 'false'
                }
            )
            topic_arns['compliance'] = response['TopicArn']
            print(f"✅ Created: {response['TopicArn']}")
        except ClientError as e:
            print(f"⚠️  Error: {e}")
        
        # 3. System Alerts Topic
        print("\nCreating cloudbank-system-alerts topic...")
        try:
            response = sns.create_topic(
                Name='cloudbank-system-alerts',
                Attributes={
                    'DisplayName': 'CloudBank System Alerts',
                    'FifoTopic': 'false'
                }
            )
            topic_arns['system'] = response['TopicArn']
            print(f"✅ Created: {response['TopicArn']}")
        except ClientError as e:
            print(f"⚠️  Error: {e}")
        
        print("\n" + "=" * 70)
        print("✅ Topic creation complete!")
        print("=" * 70)
        
        # Display topic ARNs for .env.aws file
        print("\n📋 Add these ARNs to your .env.aws file:")
        print("-" * 70)
        if 'fraud' in topic_arns:
            print(f"SNS_FRAUD_TOPIC_ARN={topic_arns['fraud']}")
        if 'compliance' in topic_arns:
            print(f"SNS_COMPLIANCE_TOPIC_ARN={topic_arns['compliance']}")
        if 'system' in topic_arns:
            print(f"SNS_SYSTEM_TOPIC_ARN={topic_arns['system']}")
        print("-" * 70)
        
        # Ask about email subscription
        print("\n📧 Would you like to subscribe an email to these topics?")
        email = input("Enter email address (or press Enter to skip): ").strip()
        
        if email:
            print(f"\nSubscribing {email} to all topics...")
            for topic_type, arn in topic_arns.items():
                try:
                    response = sns.subscribe(
                        TopicArn=arn,
                        Protocol='email',
                        Endpoint=email
                    )
                    print(f"✅ Subscribed to {topic_type} topic")
                    print(f"   Check {email} for confirmation email!")
                except ClientError as e:
                    print(f"⚠️  Error subscribing to {topic_type}: {e}")
            
            print("\n⚠️  IMPORTANT: Check your email and confirm the subscriptions!")
        
        return topic_arns
        
    except Exception as e:
        print(f"\n❌ Error creating topics: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    import os
    
    # Get region from environment or use default
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print("\n⚠️  WARNING: This script will create SNS topics in your AWS account.")
    print("   Make sure your AWS credentials are configured correctly.")
    print(f"   Region: {region}")
    print()
    
    response = input("Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        sys.exit(0)
    
    topic_arns = create_sns_topics(region)
    sys.exit(0 if topic_arns else 1)
