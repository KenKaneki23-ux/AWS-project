"""
Compliance Officer Dashboard Routes
Provides compliance monitoring, audit logs, and regulatory metrics
"""

from flask import Blueprint, render_template, request, jsonify
from decorators.auth_decorators import login_required, role_required
from services.compliance_service import ComplianceService

compliance_bp = Blueprint('compliance', __name__, url_prefix='/compliance')

@compliance_bp.route('/dashboard')
@role_required('COMPLIANCE_OFFICER')
def dashboard():
    """Compliance officer dashboard"""
    dashboard_stats = ComplianceService.get_compliance_dashboard_stats()
    
    return render_template('compliance/dashboard.html',
                           stats=dashboard_stats)

@compliance_bp.route('/metrics')
@role_required('COMPLIANCE_OFFICER')
def metrics():
    """Get regulatory metrics (JSON)"""
    metrics = ComplianceService.get_regulatory_metrics()
    
    return jsonify(metrics)

@compliance_bp.route('/alerts')
@role_required('COMPLIANCE_OFFICER')
def alerts():
    """Get threshold alerts (JSON)"""
    alerts = ComplianceService.get_threshold_alerts()
    
    return jsonify({
        'alerts': alerts,
        'count': len(alerts)
    })

@compliance_bp.route('/audit')
@role_required('COMPLIANCE_OFFICER')
def audit():
    """View audit log"""
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Get audit logs
    offset = (page - 1) * per_page
    # For now, get all and paginate (in production, would do this in the query)
    all_audits = ComplianceService.get_audit_log(limit=200)
    
    paginated = all_audits[offset:offset + per_page]
    total_pages = (len(all_audits) + per_page - 1) // per_page
    
    return render_template('compliance/audit.html',
                           audits=paginated,
                           page=page,
                           total_pages=total_pages)

@compliance_bp.route('/transactions')
@role_required('COMPLIANCE_OFFICER')
def transactions():
    """Transaction compliance monitoring"""
    metrics = ComplianceService.get_regulatory_metrics()
    
    return render_template('compliance/transactions.html',
                           metrics=metrics)

@compliance_bp.route('/drill-down')
@role_required('COMPLIANCE_OFFICER')
def drill_down():
    """Root cause analysis tool"""
    metric = request.args.get('metric', '')
    
    metrics = ComplianceService.get_regulatory_metrics()
    alerts = ComplianceService.get_threshold_alerts()
    
    return render_template('compliance/drill_down.html',
                           metric=metric,
                           metrics=metrics,
                           alerts=alerts)
