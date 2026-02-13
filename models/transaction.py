"""
Transaction model for managing financial transactions
Handles deposits, withdrawals, transfers, and transaction history
"""

import uuid
from datetime import datetime
from config import Config
from models.account import Account
from services.database_adapter import get_database_adapter

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
        
        db = get_database_adapter()
        transaction_id = str(uuid.uuid4())
        
        # Create transaction
        transaction_data = {
            'transaction_id': transaction_id,
            'account_id': account_id,
            'transaction_type': 'deposit',
            'amount': amount,
            'description': description,
            'status': 'completed'
        }
        db.create_transaction(transaction_data)
        
        # Update account balance
        new_balance = account.balance + amount
        db.update_account_balance(account_id, new_balance)
        
        return Transaction(transaction_id, account_id, 'deposit', amount, 
                         description=description, status='completed')
    
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
        
        db = get_database_adapter()
        transaction_id = str(uuid.uuid4())
        
        # Create transaction
        transaction_data = {
            'transaction_id': transaction_id,
            'account_id': account_id,
            'transaction_type': 'withdrawal',
            'amount': amount,
            'description': description,
            'status': 'completed'
        }
        db.create_transaction(transaction_data)
        
        # Update account balance
        new_balance = account.balance - amount
        db.update_account_balance(account_id, new_balance)
        
        return Transaction(transaction_id, account_id, 'withdrawal', amount, 
                         description=description, status='completed')
    
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
        
        db = get_database_adapter()
        transaction_id = str(uuid.uuid4())
        
        # Create transfer transaction
        transaction_data = {
            'transaction_id': transaction_id,
            'account_id': from_account_id,
            'transaction_type': 'transfer',
            'amount': amount,
            'target_account_id': to_account_id,
            'description': description,
            'status': 'completed'
        }
        db.create_transaction(transaction_data)
        
        # Update balances
        from_new_balance = from_account.balance - amount
        to_new_balance = to_account.balance + amount
        db.update_account_balance(from_account_id, from_new_balance)
        db.update_account_balance(to_account_id, to_new_balance)
        
        return Transaction(transaction_id, from_account_id, 'transfer', amount, 
                         target_account_id=to_account_id, description=description, 
                         status='completed')
    
    @staticmethod
    def get_by_id(transaction_id):
        """Get transaction by ID"""
        db = get_database_adapter()
        transaction_data = db.get_transaction(transaction_id)
        
        if transaction_data:
            return Transaction(
                transaction_data['transaction_id'],
                transaction_data['account_id'],
                transaction_data['transaction_type'],
                transaction_data['amount'],
                transaction_data.get('target_account_id'),
                transaction_data.get('timestamp'),
                transaction_data.get('status', 'completed'),
                transaction_data.get('fraud_flag', False),
                transaction_data.get('description')
            )
        return None
    
    @staticmethod
    def get_by_account(account_id, limit=100):
        """Get transactions for an account"""
        db = get_database_adapter()
        transactions_data = db.get_transactions_by_account(account_id, limit)
        
        return [Transaction(
            txn_data['transaction_id'],
            txn_data['account_id'],
            txn_data['transaction_type'],
            txn_data['amount'],
            txn_data.get('target_account_id'),
            txn_data.get('timestamp'),
            txn_data.get('status', 'completed'),
            txn_data.get('fraud_flag', False),
            txn_data.get('description')
        ) for txn_data in transactions_data]
    
    @staticmethod
    def get_all(limit=1000, offset=0):
        """Get all transactions with pagination"""
        db = get_database_adapter()
        transactions_data = db.get_all_transactions(limit)
        
        # Note: DynamoDB doesn't support offset-based pagination in the same way
        # For simplicity, we'll use limit only. Proper implementation would use LastEvaluatedKey
        transactions = [Transaction(
            txn_data['transaction_id'],
            txn_data['account_id'],
            txn_data['transaction_type'],
            txn_data['amount'],
            txn_data.get('target_account_id'),
            txn_data.get('timestamp'),
            txn_data.get('status', 'completed'),
            txn_data.get('fraud_flag', False),
            txn_data.get('description')
        ) for txn_data in transactions_data]
        
        # Apply offset if needed (client-side)
        return transactions[offset:offset+limit] if offset > 0 else transactions[:limit]
    
    @staticmethod
    def get_suspicious(limit=50):
        """Get flagged/suspicious transactions"""
        db = get_database_adapter()
        all_transactions = db.get_all_transactions(limit=500)  # Get more to filter
        
        # Filter for suspicious transactions
        suspicious = [
            Transaction(
                txn_data['transaction_id'],
                txn_data['account_id'],
                txn_data['transaction_type'],
                txn_data['amount'],
                txn_data.get('target_account_id'),
                txn_data.get('timestamp'),
                txn_data.get('status', 'completed'),
                txn_data.get('fraud_flag', False),
                txn_data.get('description')
            )
            for txn_data in all_transactions
            if txn_data.get('fraud_flag') or txn_data.get('status') == 'flagged'
        ]
        
        return suspicious[:limit]
    
    def flag_fraud(self):
        """Flag transaction as fraudulent"""
        db = get_database_adapter()
        updates = {
            'fraud_flag': 1,
            'status': 'flagged'
        }
        db.update_transaction(self.transaction_id, updates)
        
        self.fraud_flag = True
        self.status = 'flagged'
    
    def unflag_fraud(self):
        """Remove fraud flag from transaction"""
        db = get_database_adapter()
        updates = {
            'fraud_flag': 0,
            'status': 'completed'
        }
        db.update_transaction(self.transaction_id, updates)
        
        self.fraud_flag = False
        self.status = 'completed'
    
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
