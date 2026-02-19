"""
Cloud-hosted Banking Data Analytics and Reporting System
Main Flask Application - Local Development (SQLite)
"""

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import get_config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_by_id(user_id)

# Register blueprints
from routes.auth import auth_bp
from routes.transactions import transactions_bp
from routes.fraud_dashboard import fraud_bp
from routes.financial_dashboard import financial_bp
from routes.compliance_dashboard import compliance_bp

app.register_blueprint(auth_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(fraud_bp)
app.register_blueprint(financial_bp)
app.register_blueprint(compliance_bp)

# Home route
@app.route('/')
def index():
    """Homepage - redirects to dashboard or login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

# Dashboard route (generic, redirects based on role)
@app.route('/dashboard')
def dashboard():
    """Generic dashboard - redirects to role-specific dashboard"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Redirect based on user role
    if current_user.role == 'FRAUD_ANALYST':
        return redirect(url_for('fraud.dashboard'))
    elif current_user.role == 'FINANCIAL_MANAGER':
        return redirect(url_for('financial.dashboard'))
    elif current_user.role == 'COMPLIANCE_OFFICER':
        return redirect(url_for('compliance.dashboard'))
    else:
        # Fallback dashboard
        from models.account import Account
        from services.notification_service import NotificationService
        
        accounts = Account.get_by_user(current_user.user_id)
        notifications = NotificationService.get_user_notifications(current_user.user_id, limit=5)
        
        return render_template('dashboard.html', 
                               accounts=accounts,
                               notifications=notifications)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    """403 error handler"""
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('errors/500.html'), 500

# Context processor for global template variables
@app.context_processor
def inject_globals():
    """Inject global variables into templates"""
    from datetime import datetime
    
    unread_count = 0
    if current_user.is_authenticated:
        from services.notification_service import NotificationService
        unread_count = NotificationService.get_unread_count(current_user.user_id)
    
    return {
        'app_name': 'Cloud Bank Analytics',
        'unread_notifications': unread_count,
        'now': datetime.now()
    }

# Development server
if __name__ == '__main__':
    print("=" * 60)
    print("🏦 Cloud-hosted Banking Data Analytics System")
    print("=" * 60)
    print("📍 Mode: Local Development (SQLite)")
    print("🌐 Running on: http://localhost:5000")
    print("=" * 60)
    print("\n✨ Application started successfully!")
    print("\n🔑 Test Credentials:")
    print("   • Fraud Analyst:      fraud@test.com / test123")
    print("   • Financial Manager:  finance@test.com / test123")
    print("   • Compliance Officer: compliance@test.com / test123")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
