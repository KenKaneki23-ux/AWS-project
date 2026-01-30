"""
Transaction management routes
Handles deposits, withdrawals, transfers, and history
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from decorators.auth_decorators import login_required
from models.transaction import Transaction
from models.account import Account
import csv
from io import StringIO

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Transaction creation page"""
    user_accounts = Account.get_by_user(current_user.user_id)
    all_accounts = Account.get_all()  # For transfers
    
    if request.method == 'POST':
        transaction_type = request.form.get('type')
        account_id = request.form.get('account_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', '')
        
        try:
            if transaction_type == 'deposit':
                Transaction.create_deposit(account_id, amount, description)
                flash(f'Deposit of ${amount:,.2f} successful!', 'success')
            
            elif transaction_type == 'withdrawal':
                Transaction.create_withdrawal(account_id, amount, description)
                flash(f'Withdrawal of ${amount:,.2f} successful!', 'success')
            
            elif transaction_type == 'transfer':
                target_account_id = request.form.get('target_account_id')
                Transaction.create_transfer(account_id, target_account_id, amount, description)
                flash(f'Transfer of ${amount:,.2f} successful!', 'success')
            
            return redirect(url_for('transactions.history'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('transactions/create.html', accounts=user_accounts, all_accounts=all_accounts)

@transactions_bp.route('/history')
@login_required
def history():
    """Transaction history page with filtering"""
    # Get user's accounts
    user_accounts = Account.get_by_user(current_user.user_id)
    account_ids = {acc.account_id for acc in user_accounts}
    
    # Get filter parameters
    page = int(request.args.get('page', 1))
    per_page = 20
    transaction_type = request.args.get('type', '')
    search = request.args.get('search', '')
    
    # Get all transactions for user's accounts
    all_user_transactions = []
    for account in user_accounts:
        transactions = Transaction.get_by_account(account.account_id, limit=200)
        all_user_transactions.extend(transactions)
    
    # Sort by timestamp
    all_user_transactions.sort(key=lambda x: x.timestamp if x.timestamp else '', reverse=True)
    
    # Apply filters
    filtered = all_user_transactions
    if transaction_type:
        filtered = [t for t in filtered if t.transaction_type == transaction_type]
    if search:
        filtered = [t for t in filtered if search.lower() in t.transaction_id.lower() or 
                   (t.description and search.lower() in t.description.lower())]
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]
    
    total_pages = (len(filtered) + per_page - 1) // per_page
    
    return render_template('transactions/history.html', 
                           transactions=paginated,
                           page=page,
                           total_pages=total_pages,
                           transaction_type=transaction_type,
                           search=search)

@transactions_bp.route('/<transaction_id>')
@login_required
def detail(transaction_id):
    """Transaction detail page"""
    transaction = Transaction.get_by_id(transaction_id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('transactions.history'))
    
    # Verify user owns the account
    user_accounts = Account.get_by_user(current_user.user_id)
    account_ids = {acc.account_id for acc in user_accounts}
    
    if transaction.account_id not in account_ids:
        flash('You do not have permission to view this transaction.', 'danger')
        return redirect(url_for('transactions.history'))
    
    # Get account info
    account = Account.get_by_id(transaction.account_id)
    target_account = None
    if transaction.target_account_id:
        target_account = Account.get_by_id(transaction.target_account_id)
    
    return render_template('transactions/detail.html', 
                           transaction=transaction,
                           account=account,
                           target_account=target_account)

@transactions_bp.route('/export')
@login_required
def export():
    """Export transactions to CSV"""
    user_accounts = Account.get_by_user(current_user.user_id)
    
    all_transactions = []
    for account in user_accounts:
        transactions = Transaction.get_by_account(account.account_id, limit=500)
        all_transactions.extend(transactions)
    
    # Sort by timestamp
    all_transactions.sort(key=lambda x: x.timestamp if x.timestamp else '', reverse=True)
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Transaction ID', 'Account ID', 'Type', 'Amount', 'Timestamp', 'Status', 'Description'])
    
    for txn in all_transactions:
        writer.writerow([
            txn.transaction_id,
            txn.account_id,
            txn.transaction_type,
            f'${txn.amount:,.2f}',
            txn.timestamp,
            txn.status,
            txn.description or ''
        ])
    
    response = output.getvalue()
    
    from flask import Response
    return Response(
        response,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=transactions.csv'}
    )
