from flask import Blueprint, render_template

# Define the blueprint:
admin_jobs = Blueprint('admin_jobs', __name__)


# Set the route and accepted methods
@admin_jobs.route('/admin/jobs', methods=['GET'])
def index():
    return render_template('admin/jobs/jobs.html')
