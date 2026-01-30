"""
Compliance monitoring service
Tracks regulatory metrics and audit logs
"""

import sqlite3
from datetime import datetime, timedelta
from config import Config

class ComplianceService:
    """Service for compliance monitoring and regulatory tracking"""
    
    @staticmethod
    def get_regulatory_metrics():
        """
        Get key regulatory compliance metrics
        
        Returns:
            dict with compliance metrics
        """
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Large transaction reporting (>$10,000)
        cursor.execute('''
            SELECT COUNT(*) FROM transactions 
            WHERE amount > 10000 AND status = "completed"
        ''')
        large_transactions = cursor.fetchone()[0]
        
        # Suspicious activity reports (flagged transactions)
        cursor.execute('SELECT COUNT(*) FROM transactions WHERE fraud_flag = 1')
        suspicious_activities = cursor.fetchone()[0]
        
        # Account verification rate (active vs total)
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = "active"')
        verified_accounts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM accounts')
        total_accounts = cursor.fetchone()[0]
        
        verification_rate = (verified_accounts / total_accounts * 100) if total_accounts > 0 else 0
        
        # Recent audit log entries
        cursor.execute('SELECT COUNT(*) FROM audit_log WHERE datetime(timestamp) > datetime("now", "-7 days")')
        recent_audits = cursor.fetchone()[0]
        
        # Frozen accounts (risk mitigation)
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = "frozen"')
        frozen_accounts = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'large_transactions': large_transactions,
            'suspicious_activities': suspicious_activities,
            'verification_rate': round(verification_rate, 2),
            'verified_accounts': verified_accounts,
            'total_accounts': total_accounts,
            'recent_audits': recent_audits,
            'frozen_accounts': frozen_accounts
        }
    
    @staticmethod
    def get_threshold_alerts():
        """
        Get compliance threshold alerts
        
        Returns:
            list of alerts for metrics approaching regulatory thresholds
        """
        alerts = []
        metrics = ComplianceService.get_regulatory_metrics()
        
        # Alert if verification rate is below 90%
        if metrics['verification_rate'] < 90:
            alerts.append({
                'severity': 'warning',
                'category': 'Account Verification',
                'message': f"Account verification rate ({metrics['verification_rate']}%) is below 90% threshold",
                'value': metrics['verification_rate'],
                'threshold': 90
            })
        
        # Alert if too many frozen accounts (>10%)
        frozen_rate = (metrics['frozen_accounts'] / metrics['total_accounts'] * 100) if metrics['total_accounts'] > 0 else 0
        if frozen_rate > 10:
            alerts.append({
                'severity': 'high',
                'category': 'Frozen Accounts',
                'message': f"Frozen account rate ({frozen_rate:.1f}%) exceeds 10% threshold",
                'value': frozen_rate,
                'threshold': 10
            })
        
        # Alert if suspicious activities are high (>5% of transactions)
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM transactions')
        total_txns = cursor.fetchone()[0]
        conn.close()
        
        suspicious_rate = (metrics['suspicious_activities'] / total_txns * 100) if total_txns > 0 else 0
        if suspicious_rate > 5:
            alerts.append({
                'severity': 'critical',
                'category': 'Suspicious Activity',
                'message': f"Suspicious activity rate ({suspicious_rate:.1f}%) exceeds 5% threshold",
                'value': suspicious_rate,
                'threshold': 5
            })
        
        return alerts
    
    @staticmethod
    def get_audit_log(limit=50, user_id=None):
        """
        Get audit log entries
        
        Args:
            limit: Maximum number of entries to return
            user_id: Filter by specific user (optional)
        
        Returns:
            list of audit log entries
        """
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT log_id, user_id, action, entity_type, entity_id, details, timestamp
                FROM audit_log
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT log_id, user_id, action, entity_type, entity_id, details, timestamp
                FROM audit_log
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'log_id': row[0],
            'user_id': row[1],
            'action': row[2],
            'entity_type': row[3],
            'entity_id': row[4],
            'details': row[5],
            'timestamp': row[6]
        } for row in rows]
    
    @staticmethod
    def get_compliance_dashboard_stats():
        """Get statistics for compliance officer dashboard"""
        metrics = ComplianceService.get_regulatory_metrics()
        alerts = ComplianceService.get_threshold_alerts()
        
        return {
            'metrics': metrics,
            'alerts': alerts,
            'alert_count': len(alerts),
            'critical_alerts': len([a for a in alerts if a['severity'] == 'critical']),
            'compliance_score': ComplianceService.calculate_compliance_score(metrics, alerts)
        }
    
    @staticmethod
    def calculate_compliance_score(metrics, alerts):
        """
        Calculate overall compliance score (0-100)
        
        Higher score = better compliance
        """
        score = 100
        
        # Deduct for alerts
        for alert in alerts:
            if alert['severity'] == 'critical':
                score -= 20
            elif alert['severity'] == 'high':
                score -= 10
            elif alert['severity'] == 'warning':
                score -= 5
        
        # Deduct for low verification rate
        if metrics['verification_rate'] < 95:
            score -= (95 - metrics['verification_rate'])
        
        return max(0, min(100, score))
