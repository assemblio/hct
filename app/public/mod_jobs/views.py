from flask import Blueprint, render_template

# Define the blueprint:
mod_jobs = Blueprint('mod_jobs', __name__)

# Set the route and accepted methods
@mod_jobs.route('/job')
def job():
    return render_template('applications/job.html')

@mod_jobs.route('/jobs')
def jobs():
    return render_template('applications/jobs.html')