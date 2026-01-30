"""
Authentication routes
Handles login, signup, and logout functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models.user import User
from models.account import Account

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Validate input
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('auth/login.html')
        
        # Get user
        user = User.get_by_email(email)
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.name}!', 'success')
            
           # Redirect based on role
            if user.role == 'FRAUD_ANALYST':
                return redirect(url_for('fraud.dashboard'))
            elif user.role == 'FINANCIAL_MANAGER':
                return redirect(url_for('financial.dashboard'))
            elif user.role == 'COMPLIANCE_OFFICER':
                return redirect(url_for('compliance.dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and handler"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        # Validate input
        if not all([name, email, password, confirm_password, role]):
            flash('Please fill in all fields.', 'danger')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/signup.html')
        
        # Create user
        user = User.create(name, email, password, role)
        
        if user:
            # Create initial account with $1000 balance
            Account.create(user.user_id, initial_balance=1000.0)
            
            flash(f'Account created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already exists. Please use a different email.', 'danger')
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
