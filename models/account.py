"""
Account model for managing user bank accounts
Handles account creation, balance updates, and status management
"""

import uuid
from config import Config
from services.database_adapter import get_database_adapter

class Account:
    """Bank account model"""
    
    def __init__(self, account_id, user_id, balance, status, created_at=None):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance
        self.status = status
        self.created_at = created_at
    
    @staticmethod
    def create(user_id, initial_balance=0.0):
        """
        Create a new account for a user
        
        Args:
            user_id: Owner's user ID
            initial_balance: Starting balance (default 0.0)
        
        Returns:
            Account object
        """
        db = get_database_adapter()
        
        account_id = str(uuid.uuid4())
        
        account_data = {
            'account_id': account_id,
            'user_id': user_id,
            'balance': initial_balance,
            'status': 'active'
        }
        
        db.create_account(account_data)
        
        return Account(account_id, user_id, initial_balance, 'active')
    
    @staticmethod
    def get_by_id(account_id):
        """
        Get account by ID
        
        Args:
            account_id: Account UUID
        
        Returns:
            Account object or None if not found
        """
        db = get_database_adapter()
        account_data = db.get_account(account_id)
        
        if account_data:
            return Account(
                account_data['account_id'],
                account_data['user_id'],
                account_data['balance'],
                account_data['status'],
                account_data.get('created_at')
            )
        return None
    
    @staticmethod
    def get_by_user(user_id):
        """
        Get all accounts for a user
        
        Args:
            user_id: User's UUID
        
        Returns:
            List of Account objects
        """
        db = get_database_adapter()
        accounts_data = db.get_accounts_by_user(user_id)
        
        return [Account(
            account_data['account_id'],
            account_data['user_id'],
            account_data['balance'],
            account_data['status'],
            account_data.get('created_at')
        ) for account_data in accounts_data]
    
    @staticmethod
    def get_all():
        """
        Get all accounts
        
        Returns:
            List of Account objects
        """
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_id, user_id, balance, status, created_at
            FROM accounts
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Account(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    
    def update_balance(self, amount):
        """
        Update account balance
        
        Args:
            amount: Amount to add (positive) or subtract (negative)
        
        Returns:
            New balance
        """
        db = get_database_adapter()
        new_balance = self.balance + amount
        db.update_account_balance(self.account_id, new_balance)
        self.balance = new_balance
        return new_balance
    
    def freeze(self):
        """Freeze account (fraud prevention)"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts
            SET status = 'frozen'
            WHERE account_id = ?
        ''', (self.account_id,))
        
        conn.commit()
        conn.close()
        
        self.status = 'frozen'
    
    def activate(self):
        """Activate frozen account"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts
            SET status = 'active'
            WHERE account_id = ?
        ''', (self.account_id,))
        
        conn.commit()
        conn.close()
        
        self.status = 'active'
    
    def is_active(self):
        """Check if account is active"""
        return self.status == 'active'
    
    def to_dict(self):
        """Convert account to dictionary"""
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'balance': round(self.balance, 2),
            'status': self.status,
            'created_at': self.created_at
        }
