"""
Reporting service for financial analytics
Generates KPIs, reports, and trend analysis
"""

import sqlite3
from datetime import datetime, timedelta
from config import Config

class ReportingService:
    """Service for financial reporting and analytics"""
    
    @staticmethod
    def get_kpi_summary():
        """
        Get key performance indicators summary
        
        Returns:
            dict with KPIs
        """
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total transactions
        cursor.execute('SELECT COUNT(*) FROM transactions')
        total_transactions = cursor.fetchone()[0]
        
        # Total transaction volume
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE status = "completed"')
        total_volume = cursor.fetchone()[0]
        
        # Total deposits
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = "deposit"')
        total_deposits = cursor.fetchone()[0]
        
        # Total withdrawals
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = "withdrawal"')
        total_withdrawals = cursor.fetchone()[0]
        
        # Total transfers
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = "transfer"')
        total_transfers = cursor.fetchone()[0]
        
        # Active accounts
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = "active"')
        active_accounts = cursor.fetchone()[0]
        
        # Total accounts
        cursor.execute('SELECT COUNT(*) FROM accounts')
        total_accounts = cursor.fetchone()[0]
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Average account balance
        cursor.execute('SELECT COALESCE(AVG(balance), 0) FROM accounts WHERE status = "active"')
        avg_balance = cursor.fetchone()[0]
        
        conn.close()
        
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
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(timestamp) as date, 
                   COUNT(*) as count,
                   SUM(amount) as volume,
                   transaction_type
            FROM transactions
            WHERE datetime(timestamp) > datetime('now', ? || ' days')
            GROUP BY DATE(timestamp), transaction_type
            ORDER BY date DESC
        ''', (f'-{days}',))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Organize data by date
        trends = {}
        for row in rows:
            date = row[0]
            if date not in trends:
                trends[date] = {'date': date, 'deposits': 0, 'withdrawals': 0, 'transfers': 0, 'total_volume': 0}
            
            txn_type = row[3]
            trends[date][f'{txn_type}s'] = row[1]  # count
            trends[date]['total_volume'] += row[2] if row[2] else 0
        
        return list(trends.values())
    
    @staticmethod
    def get_top_transactions(limit=10, transaction_type=None):
        """Get top transactions by amount"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        if transaction_type:
            cursor.execute('''
                SELECT transaction_id, account_id, transaction_type, amount, timestamp, description
                FROM transactions
                WHERE transaction_type = ?
                ORDER BY amount DESC
                LIMIT ?
            ''', (transaction_type, limit))
        else:
            cursor.execute('''
                SELECT transaction_id, account_id, transaction_type, amount, timestamp, description
                FROM transactions
                ORDER BY amount DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'transaction_id': row[0],
            'account_id': row[1],
            'transaction_type': row[2],
            'amount': round(row[3], 2),
            'timestamp': row[4],
            'description': row[5]
        } for row in rows]
    
    @staticmethod
    def generate_custom_report(filters=None):
        """
        Generate custom report based on filters
        
        Args:
            filters: dict with optional keys: start_date, end_date, transaction_type, min_amount, max_amount
        
        Returns:
            dict with report data
        """
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM transactions WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('start_date'):
                query += ' AND DATE(timestamp) >= ?'
                params.append(filters['start_date'])
            
            if filters.get('end_date'):
                query += ' AND DATE(timestamp) <= ?'
                params.append(filters['end_date'])
            
            if filters.get('transaction_type'):
                query += ' AND transaction_type = ?'
                params.append(filters['transaction_type'])
            
            if filters.get('min_amount'):
                query += ' AND amount >= ?'
                params.append(filters['min_amount'])
            
            if filters.get('max_amount'):
                query += ' AND amount <= ?'
                params.append(filters['max_amount'])
        
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Calculate summary
        total_count = len(rows)
        total_amount = sum(row[3] for row in rows) if rows else 0
        
        conn.close()
        
        return {
            'transaction_count': total_count,
            'total_amount': round(total_amount, 2),
            'filters_applied': filters or {},
            'transactions': [{
                'transaction_id': row[0],
                'account_id': row[1],
                'type': row[2],
                'amount': round(row[3], 2),
                'timestamp': row[5]
            } for row in rows[:100]]  # Limit to 100 for display
        }
