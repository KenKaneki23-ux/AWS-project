import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database Mode
    DB_MODE = os.getenv('DB_MODE', 'local')  # 'local' or 'aws'
    
    # SQLite Configuration (for local mode)
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
    
    # Dual-Mode Configuration
    USE_AWS = os.getenv('USE_AWS', 'false').lower() == 'true'
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # DynamoDB Table Names
    DYNAMODB_USERS_TABLE = os.getenv('DYNAMODB_USERS_TABLE', 'cloudbank-users')
    DYNAMODB_ACCOUNTS_TABLE = os.getenv('DYNAMODB_ACCOUNTS_TABLE', 'cloudbank-accounts')
    DYNAMODB_TRANSACTIONS_TABLE = os.getenv('DYNAMODB_TRANSACTIONS_TABLE', 'cloudbank-transactions')
    DYNAMODB_NOTIFICATIONS_TABLE = os.getenv('DYNAMODB_NOTIFICATIONS_TABLE', 'cloudbank-notifications')
    DYNAMODB_AUDIT_LOG_TABLE = os.getenv('DYNAMODB_AUDIT_LOG_TABLE', 'cloudbank-audit-log')
    


    
    # Session Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # User Roles
    ROLES = {
        'FRAUD_ANALYST': 'Fraud Analyst',
        'FINANCIAL_MANAGER': 'Financial Manager',
        'COMPLIANCE_OFFICER': 'Compliance Officer'
    }
    
    # Transaction Types
    TRANSACTION_TYPES = ['deposit', 'withdrawal', 'transfer']
    
    # Pagination
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
