"""
Database adapter interface for dual-mode support (SQLite/DynamoDB)
Provides abstraction layer to switch between local and AWS databases
"""

from abc import ABC, abstractmethod
import sqlite3
import uuid
from config import Config

class DatabaseAdapter(ABC):
    """Abstract base class for database operations"""
    
    @abstractmethod
    def get_user(self, user_id):
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email):
        """Get user by email"""
        pass
    
    @abstractmethod
    def create_user(self, user_data):
        """Create new user"""
        pass
    
    @abstractmethod
    def get_all_users(self):
        """Get all users"""
        pass
    
    @abstractmethod
    def get_account(self, account_id):
        """Get account by ID"""
        pass
    
    @abstractmethod
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user"""
        pass
    
    @abstractmethod
    def create_account(self, account_data):
        """Create new account"""
        pass
    
    @abstractmethod
    def update_account_balance(self, account_id, new_balance):
        """Update account balance"""
        pass
    
    @abstractmethod
    def get_transaction(self, transaction_id):
        """Get transaction by ID"""
        pass
    
    @abstractmethod
    def get_transactions_by_account(self, account_id, limit):
        """Get transactions for an account"""
        pass
    
    @abstractmethod
    def create_transaction(self, transaction_data):
        """Create new transaction"""
        pass
    
    @abstractmethod
    def update_transaction(self, transaction_id, updates):
        """Update transaction data"""
        pass


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter (local mode)"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_user(self, user_id):
        """Get user by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, name, email, role, password_hash
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'role': row[3],
                'password_hash': row[4]
            }
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, name, email, role, password_hash
            FROM users
            WHERE email = ?
        ''', (email,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'role': row[3],
                'password_hash': row[4]
            }
        return None
    
    def create_user(self, user_data):
        """Create new user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, name, email, password_hash, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_data['user_id'], user_data['name'], user_data['email'],
                  user_data['password_hash'], user_data['role']))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_users(self):
        """Get all users"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, name, email, role, password_hash
            FROM users
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'user_id': row[0],
            'name': row[1],
            'email': row[2],
            'role': row[3],
            'password_hash': row[4]
        } for row in rows]
    
    def get_account(self, account_id):
        """Get account by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_id, user_id, balance, status
            FROM accounts
            WHERE account_id = ?
        ''', (account_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'account_id': row[0],
                'user_id': row[1],
                'balance': row[2],
                'status': row[3]
            }
        return None
    
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_id, user_id, balance, status
            FROM accounts
            WHERE user_id = ?
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'account_id': row[0],
            'user_id': row[1],
            'balance': row[2],
            'status': row[3]
        } for row in rows]
    
    def create_account(self, account_data):
        """Create new account"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO accounts (account_id, user_id, balance, status)
            VALUES (?, ?, ?, ?)
        ''', (account_data['account_id'], account_data['user_id'],
              account_data['balance'], account_data['status']))
        
        conn.commit()
        conn.close()
        return True
    
    def update_account_balance(self, account_id, new_balance):
        """Update account balance"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
        ''', (new_balance, account_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_transaction(self, transaction_id):
        """Get transaction by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_id, account_id, transaction_type, amount, target_account_id,
                   timestamp, status, fraud_flag, description
            FROM transactions
            WHERE transaction_id = ?
        ''', (transaction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'transaction_id': row[0],
                'account_id': row[1],
                'transaction_type': row[2],
                'amount': row[3],
                'target_account_id': row[4],
                'timestamp': row[5],
                'status': row[6],
                'fraud_flag': bool(row[7]),
                'description': row[8]
            }
        return None
    
    def get_transactions_by_account(self, account_id, limit=100):
        """Get transactions for an account"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_id, account_id, transaction_type, amount, target_account_id,
                   timestamp, status, fraud_flag, description
            FROM transactions
            WHERE account_id = ? OR target_account_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (account_id, account_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'transaction_id': row[0],
            'account_id': row[1],
            'transaction_type': row[2],
            'amount': row[3],
            'target_account_id': row[4],
            'timestamp': row[5],
            'status': row[6],
            'fraud_flag': bool(row[7]),
            'description': row[8]
        } for row in rows]
    
    def create_transaction(self, transaction_data):
        """Create new transaction"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions 
            (transaction_id, account_id, transaction_type, amount, target_account_id, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (transaction_data['transaction_id'], transaction_data['account_id'],
              transaction_data['transaction_type'], transaction_data['amount'],
              transaction_data.get('target_account_id'), transaction_data.get('description'),
              transaction_data.get('status', 'completed')))
        
        conn.commit()
        conn.close()
        return True
    
    def update_transaction(self, transaction_id, updates):
        """Update transaction data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build dynamic UPDATE query based on provided updates
        set_clauses = []
        values = []
        for key, value in updates.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        values.append(transaction_id)
        
        cursor.execute(f'''
            UPDATE transactions
            SET {", ".join(set_clauses)}
            WHERE transaction_id = ?
        ''', values)
        
        conn.commit()
        conn.close()
        return True


class DynamoDBAdapter(DatabaseAdapter):
    """DynamoDB adapter (AWS mode) - To be implemented in Phase 3"""
    
    def __init__(self):
        # Will initialize boto3 DynamoDB resource here
        raise NotImplementedError("DynamoDB adapter will be implemented in Phase 3")
    
    def get_user(self, user_id):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_user_by_email(self, email):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def create_user(self, user_data):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_all_users(self):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_account(self, account_id):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_accounts_by_user(self, user_id):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def create_account(self, account_data):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def update_account_balance(self, account_id, new_balance):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_transaction(self, transaction_id):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def get_transactions_by_account(self, account_id, limit):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def create_transaction(self, transaction_data):
        raise NotImplementedError("DynamoDB adapter not yet implemented")
    
    def update_transaction(self, transaction_id, updates):
        raise NotImplementedError("DynamoDB adapter not yet implemented")


def get_database_adapter():
    """
    Factory function to get the appropriate database adapter
    
    Returns:
        DatabaseAdapter: SQLiteAdapter or DynamoDBAdapter based on config
    """
    if Config.USE_AWS:
        return DynamoDBAdapter()
    else:
        return SQLiteAdapter()
