import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application Configuration - Local SQLite"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database (SQLite)
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
    
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
