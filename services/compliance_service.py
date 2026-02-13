"""
Compliance monitoring service
Tracks regulatory metrics and audit logs
"""

from datetime import datetime, timedelta
from services.database_adapter import get_database_adapter

class ComplianceService:
    """Service for compliance monitoring and regulatory tracking"""
    
    @staticmethod
    def get_regulatory_metrics():
        """
        Get key regulatory compliance metrics
        
        Returns:
            dict with compliance metrics
        """
        db = get_database_adapter()
        
        # Get all data
        all_transactions = db.get_all_transactions(limit=2000)
        all_accounts = db.get_all_accounts()
        
        # Large transaction reporting (>$10,000)
        large_transactions = sum(1 for txn in all_transactions 
                                if txn.get('amount', 0) > 10000 and txn.get('status') == 'completed')
        
        # Suspicious activity reports (flagged transactions)
        suspicious_activities = sum(1 for txn in all_transactions if txn.get('fraud_flag'))
        
        # Account verification rate (active vs total)
        verified_accounts = sum(1 for acc in all_accounts if acc.get('status') == 'active')
        total_accounts = len(all_accounts)
        
        verification_rate = (verified_accounts / total_accounts * 100) if total_accounts > 0 else 0
        
        # Recent audit log entries (placeholder - would need audit log table)
        recent_audits = 0
        
        # Frozen accounts (risk mitigation)
        frozen_accounts = sum(1 for acc in all_accounts if acc.get('status') == 'frozen')
        
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
        db = get_database_adapter()
        all_transactions = db.get_all_transactions(limit=2000)
        total_txns = len(all_transactions)
        
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
        # Placeholder - would need audit log implementation in DynamoDB
        # For now, return empty list
        return []
    
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
