from flask import render_template, Blueprint
from flask.ext.security import login_required, roles_required
from app.modules.public.mod_apply_for_job.model import Job

# Define the blueprint:
admin_reports = Blueprint('admin_reports', __name__)


@admin_reports.route('/admin/reports')
@login_required
@roles_required('Admin')
def index():
    job =Job.objects.all()
    return render_template('admin/reports/reports.html')
