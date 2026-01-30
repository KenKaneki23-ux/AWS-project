"""
Financial Manager Dashboard Routes
Provides reporting, KPIs, and financial analytics
"""

from flask import Blueprint, render_template, request, jsonify, Response
from decorators.auth_decorators import login_required, role_required
from services.reporting_service import ReportingService
import json

financial_bp = Blueprint('financial', __name__, url_prefix='/financial')

@financial_bp.route('/dashboard')
@role_required('FINANCIAL_MANAGER')
def dashboard():
    """Financial manager dashboard"""
    kpis = ReportingService.get_kpi_summary()
    trends = ReportingService.get_transaction_trends(days=30)
    top_transactions = ReportingService.get_top_transactions(limit=5)
    
    return render_template('financial/dashboard.html',
                           kpis=kpis,
                           trends=trends,
                           top_transactions=top_transactions)

@financial_bp.route('/reports')
@role_required('FINANCIAL_MANAGER')
def reports():
    """Custom report builder"""
    return render_template('financial/reports.html')

@financial_bp.route('/reports/generate', methods=['POST'])
@role_required('FINANCIAL_MANAGER')
def generate_report():
    """Generate custom report based on filters"""
    filters = {
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date'),
        'transaction_type': request.form.get('transaction_type'),
        'min_amount': float(request.form.get('min_amount', 0)) if request.form.get('min_amount') else None,
        'max_amount': float(request.form.get('max_amount', 0)) if request.form.get('max_amount') else None
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v}
    
    report = ReportingService.generate_custom_report(filters)
    
    return render_template('financial/report_result.html', report=report, filters=filters)

@financial_bp.route('/metrics')
@role_required('FINANCIAL_MANAGER')
def metrics():
    """Get metrics (JSON)"""
    kpis = ReportingService.get_kpi_summary()
    
    return jsonify(kpis)

@financial_bp.route('/trends')
@role_required('FINANCIAL_MANAGER')
def trends():
    """Get transaction trends (JSON)"""
    days = int(request.args.get('days', 30))
    trends = ReportingService.get_transaction_trends(days=days)
    
    return jsonify({
        'trends': trends,
        'period_days': days
    })

@financial_bp.route('/transactions')
@role_required('FINANCIAL_MANAGER')
def transactions():
    """Transaction analytics view"""
    transaction_type = request.args.get('type', '')
    
    if transaction_type:
        top_transactions = ReportingService.get_top_transactions(limit=20, transaction_type=transaction_type)
    else:
        top_transactions = ReportingService.get_top_transactions(limit=20)
    
    kpis = ReportingService.get_kpi_summary()
    
    return render_template('financial/transactions.html',
                           transactions=top_transactions,
                           kpis=kpis,
                           selected_type=transaction_type)

@financial_bp.route('/export')
@role_required('FINANCIAL_MANAGER')
def export():
    """Export report as JSON"""
    kpis = ReportingService.get_kpi_summary()
    trends = ReportingService.get_transaction_trends(days=30)
    
    report_data = {
        'kpis': kpis,
        'trends': trends,
        'generated_at': str(request.args.get('timestamp', ''))
    }
    
    response = Response(
        json.dumps(report_data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition':'attachment; filename=financial_report.json'}
    )
    
    return response
