from flask import Blueprint, render_template, request
from app.modules.public.mod_apply_for_job.model import Job

# Define the blueprint:
admin_jobs = Blueprint('admin_jobs', __name__)


# Set the route and accepted methods
@admin_jobs.route('/admin/jobs', methods=['GET'])
def index():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    jobs = Job.objects.all()
    #page = request.get('page')
    pagination = jobs.paginate(page=page, per_page=10)
    return render_template('admin/jobs/jobs.html', pagination=pagination)
