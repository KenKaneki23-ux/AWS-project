"""
SQLite Database Initialization
Creates all required tables with proper schemas
"""

import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


def init_db():
    """Initialize all SQLite tables"""
    db_path = Config.DATABASE_PATH
    
    print("=" * 60)
    print("INITIALIZING SQLITE DATABASE")
    print("=" * 60)
    print(f"Database path: {os.path.abspath(db_path)}")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    
    # Create Users Table
    print("\n📦 Creating table: users")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    print("✅ Table users created successfully!")
    
    # Create Accounts Table
    print("\n📦 Creating table: accounts")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    print("✅ Table accounts created successfully!")
    
    # Create Transactions Table
    print("\n📦 Creating table: transactions")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            target_account_id TEXT,
            timestamp INTEGER,
            status TEXT DEFAULT 'completed',
            fraud_flag INTEGER DEFAULT 0,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        )
    """)
    print("✅ Table transactions created successfully!")
    
    # Create Notifications Table
    print("\n📦 Creating table: notifications")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            message TEXT,
            category TEXT DEFAULT 'system_info',
            priority TEXT DEFAULT 'normal',
            is_read INTEGER DEFAULT 0,
            timestamp INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    print("✅ Table notifications created successfully!")
    
    # Create indexes for common queries
    print("\n📇 Creating indexes...")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_accounts_user ON accounts(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)")
    print("✅ Indexes created successfully!")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ ALL TABLES INITIALIZED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📁 Database file: {os.path.abspath(db_path)}")
    print(f"✨ Next step: Run 'python scripts/seed_data.py' to add test data")


if __name__ == '__main__':
    """Run table initialization"""
    init_db()
