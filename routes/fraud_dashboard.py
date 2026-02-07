"""
Fraud Analyst Dashboard Routes
Provides fraud monitoring, alerts, and risk analysis
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from decorators.auth_decorators import login_required, role_required
from services.fraud_service import FraudService
from models.transaction import Transaction
from models.account import Account

fraud_bp = Blueprint('fraud', __name__, url_prefix='/fraud')

@fraud_bp.route('/dashboard')
@role_required('FRAUD_ANALYST')
def dashboard():
    """Fraud analyst dashboard"""
    stats = FraudService.get_dashboard_stats()
    suspicious = FraudService.get_suspicious_transactions(limit=10)
    recent_alerts = FraudService.get_recent_alerts(hours=24, limit=5)
    
    return render_template('fraud/dashboard.html',
                           stats=stats,
                           suspicious=suspicious,
                           recent_alerts=recent_alerts)

@fraud_bp.route('/transactions')
@role_required('FRAUD_ANALYST')
def transactions():
    """View all transactions with fraud filters"""
    page = int(request.args.get('page', 1))
    show_flagged_only = request.args.get('flagged_only', 'false') == 'true'
    
    per_page = 20
    
    if show_flagged_only:
        all_transactions = FraudService.get_suspicious_transactions(limit=200)
    else:
        all_transactions = Transaction.get_all(limit=200)
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_transactions[start:end]
    
    total_pages = (len(all_transactions) + per_page - 1) // per_page
    
    return render_template('fraud/transactions.html',
                           transactions=paginated,
                           page=page,
                           total_pages=total_pages,
                           flagged_only=show_flagged_only)

@fraud_bp.route('/transaction/<transaction_id>')
@role_required('FRAUD_ANALYST')
def transaction_detail(transaction_id):
    """View transaction details"""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('fraud.dashboard'))
    
    account = Account.get_by_id(transaction.account_id)
    risk_score = FraudService.get_account_risk_score(transaction.account_id)
    
    return render_template('fraud/transaction_detail.html',
                           transaction=transaction,
                           account=account,
                           risk_score=risk_score)

@fraud_bp.route('/transaction/<transaction_id>/flag', methods=['POST'])
@role_required('FRAUD_ANALYST')
def flag_transaction(transaction_id):
    """Flag a transaction as fraudulent"""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('fraud.dashboard'))
    
    transaction.flag_fraud()
    flash(f'Transaction {transaction_id[:8]}... has been flagged as fraudulent.', 'warning')
    return redirect(url_for('fraud.transaction_detail', transaction_id=transaction_id))

@fraud_bp.route('/transaction/<transaction_id>/unflag', methods=['POST'])
@role_required('FRAUD_ANALYST')
def unflag_transaction(transaction_id):
    """Remove fraud flag from a transaction"""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('fraud.dashboard'))
    
    transaction.unflag_fraud()
    flash(f'Fraud flag removed from transaction {transaction_id[:8]}...', 'success')
    return redirect(url_for('fraud.transaction_detail', transaction_id=transaction_id))

@fraud_bp.route('/account/<account_id>/risk')
@role_required('FRAUD_ANALYST')
def account_risk(account_id):
    """View account risk analysis"""
    account = Account.get_by_id(account_id)
    
    if not account:
        flash('Account not found.', 'danger')
        return redirect(url_for('fraud.dashboard'))
    
    risk_score = FraudService.get_account_risk_score(account_id)
    transactions = Transaction.get_by_account(account_id, limit=50)
    
    return render_template('fraud/account_risk.html',
                           account=account,
                           risk_score=risk_score,
                           transactions=transactions)

@fraud_bp.route('/action', methods=['POST'])
@role_required('FRAUD_ANALYST')
def action():
    """Perform fraud prevention action (freeze/flag)"""
    action_type = request.form.get('action')
    entity_type = request.form.get('entity_type')
    entity_id = request.form.get('entity_id')
    
    if action_type == 'freeze_account' and entity_type == 'account':
        account = Account.get_by_id(entity_id)
        if account:
            account.freeze()
            flash(f'Account {entity_id[:8]}... has been frozen.', 'warning')
    
    elif action_type == 'flag_transaction' and entity_type == 'transaction':
        transaction = Transaction.get_by_id(entity_id)
        if transaction:
            transaction.flag_fraud()
            flash(f'Transaction {entity_id[:8]}... has been flagged as fraudulent.', 'warning')
    
    return redirect(request.referrer or url_for('fraud.dashboard'))

@fraud_bp.route('/alerts')
@role_required('FRAUD_ANALYST')
def alerts():
    """Get real-time alerts (JSON)"""
    alerts = FraudService.get_recent_alerts(hours=24, limit=20)
    
    return jsonify({
        'alerts': [txn.to_dict() for txn in alerts],
        'count': len(alerts)
    })
