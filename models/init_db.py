"""
Database initialization script for Cloud Banking Analytics
Creates SQLite database with tables for users, accounts, and transactions
"""

import sqlite3
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def init_database():
    """Initialize SQLite database with required tables"""
    
    db_path = Config.DATABASE_PATH
    
    # Remove existing database if present
    if os.path.exists(db_path):
        print(f"⚠️  Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Creating database schema...")
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('FRAUD_ANALYST', 'FINANCIAL_MANAGER', 'COMPLIANCE_OFFICER')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Created 'users' table")
    
    # Create Accounts table
    cursor.execute('''
        CREATE TABLE accounts (
            account_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'frozen', 'closed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('CREATE INDEX idx_accounts_user_id ON accounts(user_id)')
    print("✅ Created 'accounts' table with user_id index")
    
    # Create Transactions table
    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('deposit', 'withdrawal', 'transfer')),
            amount REAL NOT NULL,
            target_account_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed' CHECK(status IN ('pending', 'completed', 'failed', 'flagged')),
            fraud_flag INTEGER DEFAULT 0,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id),
            FOREIGN KEY (target_account_id) REFERENCES accounts(account_id)
        )
    ''')
    cursor.execute('CREATE INDEX idx_transactions_account_id ON transactions(account_id)')
    cursor.execute('CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC)')
    cursor.execute('CREATE INDEX idx_transactions_fraud_flag ON transactions(fraud_flag)')
    print("✅ Created 'transactions' table with indexes")
    
    # Create Notifications table (for fraud alerts, compliance warnings)
    cursor.execute('''
        CREATE TABLE notifications (
            notification_id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('fraud_alert', 'compliance_warning', 'system_info')),
            priority TEXT DEFAULT 'normal' CHECK(priority IN ('low', 'normal', 'high', 'critical')),
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('CREATE INDEX idx_notifications_user_id ON notifications(user_id)')
    cursor.execute('CREATE INDEX idx_notifications_is_read ON notifications(is_read)')
    print("✅ Created 'notifications' table with indexes")
    
    # Create Audit Log table (for compliance tracking)
    cursor.execute('''
        CREATE TABLE audit_log (
            log_id TEXT PRIMARY KEY,
            user_id TEXT,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT,
            details TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute('CREATE INDEX idx_audit_log_user_id ON audit_log(user_id)')
    cursor.execute('CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp DESC)')
    print("✅ Created 'audit_log' table with indexes")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Database initialized successfully: {db_path}")
    print("📝 Next step: Run 'python scripts/seed_data.py' to add test data")

if __name__ == '__main__':
    init_database()
