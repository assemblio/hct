from flask import Blueprint, render_template, request
from flask.ext.security import roles_required, login_required
from .form import CreateJob
from .model import Job
# Define the blueprint:
mod_apply_for_job = Blueprint('mod_apply_for_job', __name__)

# Set the route and accepted methods

@mod_apply_for_job.route('/jobs')
def index():
    jobs = Job.objects()
    return render_template('applications/jobs.html', jobs=jobs)


@mod_apply_for_job.route('/create-job', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateJob(request.form)
    job = Job(
        title=form.title.data,
        #date=form.date.data,
        location=form.location.data,
        description=form.description.data,
        requirements=form.requirements.data
    )
    if form.validate_on_submit():
        job.save()
    # user_datastore.add_role_to_user(user, "User")

    return render_template('applications/createJob.html', form=form)

