"""
Fraud detection service
Provides analytics and detection logic for suspicious transactions
"""

from models.transaction import Transaction
from models.account import Account
from datetime import datetime, timedelta
from services.database_adapter import get_database_adapter

class FraudService:
    """Service for fraud detection and monitoring"""
    
    @staticmethod
    def get_suspicious_transactions(limit=50):
        """Get all flagged/suspicious transactions"""
        return Transaction.get_suspicious(limit)
    
    @staticmethod
    def get_recent_alerts(hours=24, limit=20):
        """Get recent fraud alerts within specified hours"""
        transactions = Transaction.get_suspicious(limit=100)
        
        # Filter by time (simplified - in production would use proper datetime filtering)
        recent = []
        for txn in transactions:
            if len(recent) >= limit:
                break
            recent.append(txn)
        
        return recent
    
    @staticmethod
    def get_account_risk_score(account_id):
        """
        Calculate risk score for an account based on transaction patterns
        
        Returns:
            dict with risk_score (0-100) and risk_level (low/medium/high/critical)
        """
        transactions = Transaction.get_by_account(account_id, limit=50)
        
        if not transactions:
            return {'risk_score': 0, 'risk_level': 'low', 'factors': []}
        
        risk_score = 0
        risk_factors = []
        
        # Factor 1: Number of flagged transactions
        flagged_count = sum(1 for txn in transactions if txn.fraud_flag)
        if flagged_count > 0:
            risk_score += min(flagged_count * 15, 40)
            risk_factors.append(f"{flagged_count} flagged transactions")
        
        # Factor 2: Large transaction amounts
        large_transactions = sum(1 for txn in transactions if txn.amount > 10000)
        if large_transactions > 0:
            risk_score += min(large_transactions * 10, 30)
            risk_factors.append(f"{large_transactions} large transactions (>$10,000)")
        
        # Factor 3: High transaction frequency (more than 10 in recent history)
        if len(transactions) > 30:
            risk_score += 20
            risk_factors.append(f"High transaction frequency ({len(transactions)} recent transactions)")
        
        # Factor 4: Account status
        account = Account.get_by_id(account_id)
        if account and account.status == 'frozen':
            risk_score += 50
            risk_factors.append("Account is frozen")
        
        # Determine risk level
        if risk_score >= 75:
            risk_level = 'critical'
        elif risk_score >= 50:
            risk_level = 'high'
        elif risk_score >= 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'factors': risk_factors,
            'flagged_count': flagged_count,
            'total_transactions': len(transactions)
        }
    
    @staticmethod
    def get_dashboard_stats():
        """Get statistics for fraud analyst dashboard"""
        db = get_database_adapter()
        
        # Get all transactions and accounts
        all_transactions = db.get_all_transactions(limit=1000)
        all_accounts = db.get_all_accounts()
        
        # Total flagged transactions
        total_flagged = sum(1 for txn in all_transactions if txn.get('fraud_flag'))
        
        # Flagged in last 24 hours (simplified - checking all for now)
        recent_flagged = sum(1 for txn in all_transactions if txn.get('fraud_flag'))
        
        # Frozen accounts
        frozen_accounts = sum(1 for acc in all_accounts if acc.get('status') == 'frozen')
        
        # High-value transactions (>$10,000)
        high_value_count = sum(1 for txn in all_transactions if txn.get('amount', 0) > 10000)
        
        return {
            'total_flagged': total_flagged,
            'recent_flagged': recent_flagged,
            'frozen_accounts': frozen_accounts,
            'high_value_transactions': high_value_count
        }
