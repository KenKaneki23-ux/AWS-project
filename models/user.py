"""
User model for authentication and user management
Handles user creation, authentication, and Flask-Login integration
"""

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config
from services.database_adapter import get_database_adapter

class User(UserMixin):
    """User model with Flask-Login integration"""
    
    def __init__(self, user_id, name, email, role, password_hash=None):
        self.id = user_id  # Required by Flask-Login
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.password_hash = password_hash
    
    @staticmethod
    def create(name, email, password, role):
        """
        Create a new user
        
        Args:
            name: User's full name
            email: User's email (must be unique)
            password: Plain text password (will be hashed)
            role: User role (FRAUD_ANALYST, FINANCIAL_MANAGER, COMPLIANCE_OFFICER)
        
        Returns:
            User object or None if email already exists
        """
        if role not in Config.ROLES:
            raise ValueError(f"Invalid role. Must be one of: {list(Config.ROLES.keys())}")
        
        db = get_database_adapter()
        
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(password)
        
        user_data = {
            'user_id': user_id,
            'name': name,
            'email': email,
            'password_hash': password_hash,
            'role': role
        }
        
        success = db.create_user(user_data)
        
        if success:
            return User(user_id, name, email, role, password_hash)
        else:
            # Email already exists
            return None
    
    @staticmethod
    def get_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id: User's UUID
        
        Returns:
            User object or None if not found
        """
        db = get_database_adapter()
        user_data = db.get_user(user_id)
        
        if user_data:
            return User(
                user_data['user_id'],
                user_data['name'],
                user_data['email'],
                user_data['role'],
                user_data['password_hash']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """
        Get user by email
        
        Args:
            email: User's email
        
        Returns:
            User object or None if not found
        """
        db = get_database_adapter()
        user_data = db.get_user_by_email(email)
        
        if user_data:
            return User(
                user_data['user_id'],
                user_data['name'],
                user_data['email'],
                user_data['role'],
                user_data['password_hash']
            )
        return None
    
    def check_password(self, password):
        """
        Verify password
        
        Args:
            password: Plain text password to check
        
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_all():
        """
        Get all users
        
        Returns:
            List of User objects
        """
        db = get_database_adapter()
        users_data = db.get_all_users()
        
        return [User(
            user_data['user_id'],
            user_data['name'],
            user_data['email'],
            user_data['role'],
            user_data['password_hash']
        ) for user_data in users_data]
    
    def get_role_display(self):
        """Get display name for user role"""
        return Config.ROLES.get(self.role, self.role)
    
    def to_dict(self):
        """Convert user to dictionary (excluding password hash)"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'role_display': self.get_role_display()
        }
