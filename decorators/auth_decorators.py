"""
Authentication decorators for route protection
Provides login_required and role_required decorators
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def login_required(f):
    """
    Decorator to require authentication for a route
    Redirects to login page if not authenticated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    Decorator to require a specific role for a route
    
    Args:
        required_role: Required user role (FRAUD_ANALYST, FINANCIAL_MANAGER, COMPLIANCE_OFFICER)
    
    Returns:
        Decorated function that checks user role
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to  access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role != required_role:
                flash('You do not have permission to access this page.', 'danger')
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
