"""
Transaction model for managing financial transactions
Handles deposits, withdrawals, transfers, and transaction history
"""

import sqlite3
import uuid
from datetime import datetime
from config import Config
from models.account import Account

class Transaction:
    """Financial transaction model"""
    
    def __init__(self, transaction_id, account_id, transaction_type, amount, 
                 target_account_id=None, timestamp=None, status='completed', 
                 fraud_flag=False, description=None):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.target_account_id = target_account_id
        self.timestamp = timestamp
        self.status = status
        self.fraud_flag = fraud_flag
        self.description = description
    
    @staticmethod
    def create_deposit(account_id, amount, description=None):
        """
        Create a deposit transaction
        
        Args:
            account_id: Account to deposit into
            amount: Deposit amount
            description: Optional description
        
        Returns:
            Transaction object or None if failed
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        account = Account.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        if not account.is_active():
            raise ValueError("Account is not active")
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            transaction_id = str(uuid.uuid4())
            
            # Create transaction
            cursor.execute('''
                INSERT INTO transactions 
                (transaction_id, account_id, transaction_type, amount, description, status)
                VALUES (?, ?, 'deposit', ?, ?, 'completed')
            ''', (transaction_id, account_id, amount, description))
            
            # Update account balance
            cursor.execute('''
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_id = ?
            ''', (amount, account_id))
            
            conn.commit()
            
            return Transaction(transaction_id, account_id, 'deposit', amount, 
                             description=description, status='completed')
        
        finally:
            conn.close()
    
    @staticmethod
    def create_withdrawal(account_id, amount, description=None):
        """
        Create a withdrawal transaction
        
        Args:
            account_id: Account to withdraw from
            amount: Withdrawal amount
            description: Optional description
        
        Returns:
            Transaction object or None if failed
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        account = Account.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        if not account.is_active():
            raise ValueError("Account is not active")
        
        if account.balance < amount:
            raise ValueError("Insufficient balance")
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            transaction_id = str(uuid.uuid4())
            
            # Create transaction
            cursor.execute('''
                INSERT INTO transactions 
                (transaction_id, account_id, transaction_type, amount, description, status)
                VALUES (?, ?, 'withdrawal', ?, ?, 'completed')
            ''', (transaction_id, account_id, amount, description))
            
            # Update account balance
            cursor.execute('''
                UPDATE accounts
                SET balance = balance - ?
                WHERE account_id = ?
            ''', (amount, account_id))
            
            conn.commit()
            
            return Transaction(transaction_id, account_id, 'withdrawal', amount, 
                             description=description, status='completed')
        
        finally:
            conn.close()
    
    @staticmethod
    def create_transfer(from_account_id, to_account_id, amount, description=None):
        """
        Create a transfer transaction
        
        Args:
            from_account_id: Source account
            to_account_id: Destination account
            amount: Transfer amount
            description: Optional description
        
        Returns:
            Tuple of (withdrawal_transaction, deposit_transaction) or None if failed
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account")
        
        from_account = Account.get_by_id(from_account_id)
        to_account = Account.get_by_id(to_account_id)
        
        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")
        
        if not from_account.is_active() or not to_account.is_active():
            raise ValueError("One or both accounts are not active")
        
        if from_account.balance < amount:
            raise ValueError("Insufficient balance in source account")
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            transaction_id = str(uuid.uuid4())
            
            # Create transfer transaction (from sender's perspective)
            cursor.execute('''
                INSERT INTO transactions 
                (transaction_id, account_id, transaction_type, amount, target_account_id, description, status)
                VALUES (?, ?, 'transfer', ?, ?, ?, 'completed')
            ''', (transaction_id, from_account_id, amount, to_account_id, description))
            
            # Update balances
            cursor.execute('''
                UPDATE accounts
                SET balance = balance - ?
                WHERE account_id = ?
            ''', (amount, from_account_id))
            
            cursor.execute('''
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_id = ?
            ''', (amount, to_account_id))
            
            conn.commit()
            
            return Transaction(transaction_id, from_account_id, 'transfer', amount, 
                             target_account_id=to_account_id, description=description, 
                             status='completed')
        
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(transaction_id):
        """Get transaction by ID"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
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
            return Transaction(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                             bool(row[7]), row[8])
        return None
    
    @staticmethod
    def get_by_account(account_id, limit=100):
        """Get transactions for an account"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
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
        
        return [Transaction(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                          bool(row[7]), row[8]) for row in rows]
    
    @staticmethod
    def get_all(limit=100, offset=0):
        """Get all transactions with pagination"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_id, account_id, transaction_type, amount, target_account_id,
                   timestamp, status, fraud_flag, description
            FROM transactions
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Transaction(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                          bool(row[7]), row[8]) for row in rows]
    
    @staticmethod
    def get_suspicious(limit=50):
        """Get flagged/suspicious transactions"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT transaction_id, account_id, transaction_type, amount, target_account_id,
                   timestamp, status, fraud_flag, description
            FROM transactions
            WHERE fraud_flag = 1 OR status = 'flagged'
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Transaction(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                          bool(row[7]), row[8]) for row in rows]
    
    def flag_fraud(self):
        """Flag transaction as fraudulent"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE transactions
            SET fraud_flag = 1, status = 'flagged'
            WHERE transaction_id = ?
        ''', (self.transaction_id,))
        
        conn.commit()
        conn.close()
        
        self.fraud_flag = True
        self.status = 'flagged'
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': round(self.amount, 2),
            'target_account_id': self.target_account_id,
            'timestamp': self.timestamp,
            'status': self.status,
            'fraud_flag': self.fraud_flag,
            'description': self.description
        }
