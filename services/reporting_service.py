"""
Reporting service for financial analytics
Generates KPIs, reports, and trend analysis
"""

from datetime import datetime, timedelta
from services.database_adapter import get_database_adapter

class ReportingService:
    """Service for financial reporting and analytics"""
    
    @staticmethod
    def get_kpi_summary():
        """
        Get key performance indicators summary
        
        Returns:
            dict with KPIs
        """
        db = get_database_adapter()
        
        # Get all data
        all_transactions = db.get_all_transactions(limit=2000)
        all_accounts = db.get_all_accounts()
        all_users = db.get_all_users()
        
        # Total transactions
        total_transactions = len(all_transactions)
        
        # Total transaction volume (completed only)
        total_volume = sum(txn.get('amount', 0) for txn in all_transactions 
                          if txn.get('status') == 'completed')
        
        # Total deposits
        total_deposits = sum(txn.get('amount', 0) for txn in all_transactions 
                            if txn.get('transaction_type') == 'deposit')
        
        # Total withdrawals
        total_withdrawals = sum(txn.get('amount', 0) for txn in all_transactions 
                               if txn.get('transaction_type') == 'withdrawal')
        
        # Total transfers
        total_transfers = sum(txn.get('amount', 0) for txn in all_transactions 
                             if txn.get('transaction_type') == 'transfer')
        
        # Active accounts
        active_accounts = sum(1 for acc in all_accounts if acc.get('status') == 'active')
        
        # Total accounts
        total_accounts = len(all_accounts)
        
        # Total users
        total_users = len(all_users)
        
        # Average account balance (active only)
        active_balances = [acc.get('balance', 0) for acc in all_accounts 
                          if acc.get('status') == 'active']
        avg_balance = sum(active_balances) / len(active_balances) if active_balances else 0
        
        return {
            'total_transactions': total_transactions,
            'total_volume': round(total_volume, 2),
            'total_deposits': round(total_deposits, 2),
            'total_withdrawals': round(total_withdrawals, 2),
            'total_transfers': round(total_transfers, 2),
            'active_accounts': active_accounts,
            'total_accounts': total_accounts,
            'total_users': total_users,
            'avg_balance': round(avg_balance, 2),
            'net_flow': round(total_deposits - total_withdrawals, 2)
        }
    
    @staticmethod
    def get_transaction_trends(days=30):
        """
        Get transaction trends over specified days
        
        Returns:
            dict with daily transaction counts and volumes
        """
        db = get_database_adapter()
        all_transactions = db.get_all_transactions(limit=2000)
        
        # Organize data by date (simplified - would need proper date filtering in production)
        trends = {}
        for txn in all_transactions:
            # For now, we'll create a simple aggregation
            # In production, you'd want to filter by actual timestamp
            pass
        
        # Return empty trends for now (would need timestamp-based filtering)
        return []
    
    @staticmethod
    def get_top_transactions(limit=10, transaction_type=None):
        """Get top transactions by amount"""
        db = get_database_adapter()
        all_transactions = db.get_all_transactions(limit=500)
        
        # Filter by type if specified
        if transaction_type:
            filtered = [txn for txn in all_transactions 
                       if txn.get('transaction_type') == transaction_type]
        else:
            filtered = all_transactions
        
        # Sort by amount (descending)
        sorted_txns = sorted(filtered, key=lambda x: x.get('amount', 0), reverse=True)
        
        return [{
            'transaction_id': txn.get('transaction_id'),
            'account_id': txn.get('account_id'),
            'transaction_type': txn.get('transaction_type'),
            'amount': round(txn.get('amount', 0), 2),
            'timestamp': txn.get('timestamp'),
            'description': txn.get('description')
        } for txn in sorted_txns[:limit]]
    
    @staticmethod
    def generate_custom_report(filters=None):
        """
        Generate custom report based on filters
        
        Args:
            filters: dict with optional keys: start_date, end_date, transaction_type, min_amount, max_amount
        
        Returns:
            dict with report data
        """
        db = get_database_adapter()
        all_transactions = db.get_all_transactions(limit=2000)
        
        # Apply filters
        filtered_txns = all_transactions
        
        if filters:
            if filters.get('transaction_type'):
                filtered_txns = [t for t in filtered_txns 
                                if t.get('transaction_type') == filters['transaction_type']]
            
            if filters.get('min_amount'):
                filtered_txns = [t for t in filtered_txns 
                                if t.get('amount', 0) >= filters['min_amount']]
            
            if filters.get('max_amount'):
                filtered_txns = [t for t in filtered_txns 
                                if t.get('amount', 0) <= filters['max_amount']]
        
        # Calculate summary
        total_count = len(filtered_txns)
        total_amount = sum(t.get('amount', 0) for t in filtered_txns)
        
        return {
            'transaction_count': total_count,
            'total_amount': round(total_amount, 2),
            'filters_applied': filters or {},
            'transactions': [{
                'transaction_id': t.get('transaction_id'),
                'account_id': t.get('account_id'),
                'type': t.get('transaction_type'),
                'amount': round(t.get('amount', 0), 2),
                'timestamp': t.get('timestamp')
            } for t in filtered_txns[:100]]  # Limit to 100 for display
        }
