"""
SQLite Database Adapter
Local development database implementation using SQLite
"""

import sqlite3
import os
from datetime import datetime
from config import Config


class SQLiteAdapter:
    """SQLite database adapter - same interface as the old DynamoDB adapter"""
    
    def __init__(self):
        """Initialize SQLite connection"""
        self.db_path = Config.DATABASE_PATH
        self._ensure_tables()
    
    def _get_connection(self):
        """Get a new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _ensure_tables(self):
        """Create tables if they don't exist"""
        conn = self._get_connection()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    balance REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    created_at TEXT
                );
                
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    target_account_id TEXT,
                    timestamp INTEGER,
                    status TEXT DEFAULT 'completed',
                    fraud_flag INTEGER DEFAULT 0,
                    description TEXT
                );
                
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    title TEXT,
                    message TEXT,
                    category TEXT DEFAULT 'system_info',
                    priority TEXT DEFAULT 'normal',
                    is_read INTEGER DEFAULT 0,
                    timestamp INTEGER
                );
            """)
            conn.commit()
        finally:
            conn.close()
    
    def _row_to_dict(self, row):
        """Convert sqlite3.Row to dict"""
        if row is None:
            return None
        return dict(row)
    
    # ========================
    # USER OPERATIONS
    # ========================
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            return self._row_to_dict(row)
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            conn.close()
            return self._row_to_dict(row)
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def create_user(self, user_data):
        """Create new user"""
        try:
            conn = self._get_connection()
            
            # Check if email already exists
            cursor = conn.execute("SELECT user_id FROM users WHERE email = ?", 
                                  (user_data['email'],))
            if cursor.fetchone():
                conn.close()
                print(f"✗ User already exists: {user_data.get('email')}")
                return False
            
            conn.execute(
                "INSERT INTO users (user_id, name, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
                (user_data['user_id'], user_data['name'], user_data['email'],
                 user_data['password_hash'], user_data['role'])
            )
            conn.commit()
            conn.close()
            print(f"✓ User created successfully: {user_data.get('email')}")
            return True
        except Exception as e:
            print(f"✗ Error creating user: {type(e).__name__}: {str(e)}")
            return False
    
    def get_all_users(self):
        """Get all users"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            conn.close()
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    # ========================
    # ACCOUNT OPERATIONS
    # ========================
    
    def get_account(self, account_id):
        """Get account by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
            row = cursor.fetchone()
            conn.close()
            return self._row_to_dict(row)
        except Exception as e:
            print(f"Error getting account: {e}")
            return None
    
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            conn.close()
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting accounts by user: {e}")
            return []
    
    def create_account(self, account_data):
        """Create new account"""
        try:
            conn = self._get_connection()
            conn.execute(
                "INSERT INTO accounts (account_id, user_id, balance, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (account_data['account_id'], account_data['user_id'],
                 account_data.get('balance', 0.0), account_data.get('status', 'active'),
                 account_data.get('created_at', datetime.now().isoformat()))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
    
    def update_account_balance(self, account_id, new_balance):
        """Update account balance"""
        try:
            conn = self._get_connection()
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_id = ?",
                (new_balance, account_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating account balance: {e}")
            return False
    
    def get_all_accounts(self):
        """Get all accounts"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM accounts")
            rows = cursor.fetchall()
            conn.close()
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting all accounts: {e}")
            return []
    
    def freeze_account(self, account_id):
        """Freeze account"""
        try:
            conn = self._get_connection()
            conn.execute(
                "UPDATE accounts SET status = 'frozen' WHERE account_id = ?",
                (account_id,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error freezing account: {e}")
            return False
    
    def activate_account(self, account_id):
        """Activate account"""
        try:
            conn = self._get_connection()
            conn.execute(
                "UPDATE accounts SET status = 'active' WHERE account_id = ?",
                (account_id,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error activating account: {e}")
            return False
    
    # ========================
    # TRANSACTION OPERATIONS
    # ========================
    
    def get_transaction(self, transaction_id):
        """Get transaction by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT * FROM transactions WHERE transaction_id = ?", 
                                  (transaction_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                item = self._row_to_dict(row)
                item['fraud_flag'] = bool(item.get('fraud_flag', 0))
                return item
            return None
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    def get_transactions_by_account(self, account_id, limit=100):
        """Get transactions for an account, sorted by timestamp descending"""
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT ?",
                (account_id, limit)
            )
            rows = cursor.fetchall()
            conn.close()
            items = [self._row_to_dict(row) for row in rows]
            for item in items:
                item['fraud_flag'] = bool(item.get('fraud_flag', 0))
            return items
        except Exception as e:
            print(f"Error getting transactions by account: {e}")
            return []
    
    def create_transaction(self, transaction_data):
        """Create new transaction"""
        try:
            if 'timestamp' not in transaction_data or transaction_data['timestamp'] is None:
                transaction_data['timestamp'] = int(datetime.now().timestamp())
            
            fraud_flag = 1 if transaction_data.get('fraud_flag') else 0
            
            conn = self._get_connection()
            conn.execute(
                """INSERT INTO transactions 
                   (transaction_id, account_id, transaction_type, amount, 
                    target_account_id, timestamp, status, fraud_flag, description) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (transaction_data['transaction_id'], transaction_data['account_id'],
                 transaction_data['transaction_type'], transaction_data['amount'],
                 transaction_data.get('target_account_id'),
                 transaction_data['timestamp'],
                 transaction_data.get('status', 'completed'),
                 fraud_flag,
                 transaction_data.get('description'))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return False
    
    def update_transaction(self, transaction_id, updates):
        """Update transaction data"""
        try:
            conn = self._get_connection()
            
            set_clauses = []
            values = []
            for key, value in updates.items():
                set_clauses.append(f"{key} = ?")
                if key == 'fraud_flag':
                    values.append(1 if value else 0)
                else:
                    values.append(value)
            
            values.append(transaction_id)
            
            conn.execute(
                f"UPDATE transactions SET {', '.join(set_clauses)} WHERE transaction_id = ?",
                values
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    def get_all_transactions(self, limit=1000):
        """Get all transactions"""
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            items = [self._row_to_dict(row) for row in rows]
            for item in items:
                item['fraud_flag'] = bool(item.get('fraud_flag', 0))
            return items
        except Exception as e:
            print(f"Error getting all transactions: {e}")
            return []


def get_database_adapter():
    """
    Get the database adapter instance
    
    Returns:
        SQLiteAdapter: Local SQLite database adapter
    """
    return SQLiteAdapter()
