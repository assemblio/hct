from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.security import roles_required, login_required, current_user
from flask.ext.mongoengine import DoesNotExist
from .form import CreateJob
from .model import Job
from app.modules.public.mod_authentication.user_registration.model import User
from bson import ObjectId
# Define the blueprint:
mod_apply_for_job = Blueprint('mod_apply_for_job', __name__)

# Set the route and accepted methods

@mod_apply_for_job.route('/jobs')
def index():
    jobs = Job.objects()
    return render_template('applications/jobs.html', jobs=jobs)


@mod_apply_for_job.route('/job/<string:job_id>')
def job(job_id):
    jobs = Job.objects.get(id=ObjectId(job_id))
    return render_template('applications/jobs-single.html', jobs=jobs)

@mod_apply_for_job.route('/job/apply/<string:job_id>')
@login_required
def apply_for_job(job_id):
    job = Job.objects.get(id=ObjectId(job_id))
    if not job['applicants']:
        job['applicants'] = []
    if not ObjectId(current_user.id) in job['applicants']:
        Job.objects.get(id=ObjectId(job_id)).update(push__applicants=current_user.id)
        User.objects.get(id=ObjectId(current_user.id)).update(push__jobs_applied=ObjectId(job_id))
        return redirect('/jobs')

@mod_apply_for_job.route('/create-job', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateJob(request.form)
    job = Job(
        title=form.title.data,
        date=form.date.data,
        location=form.location.data,
        description=form.description.data,
        requirements=form.requirements.data,
        target_group=form.target_group.data,
        industry=form.industry.data

    )
    if form.validate_on_submit():
        job.save()
    # user_datastore.add_role_to_user(user, "User")
        return redirect('/jobs')
    return render_template('applications/createJob.html', form=form)

@mod_apply_for_job.route('/edit-job/<string:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    if request.method == "GET":
        job_form = CreateJob()
        job_doc = Job.objects.get(id=ObjectId(job_id))
        if current_user.is_authenticated():
            job_form.title.data = job_doc['title']
            job_form.date.data = job_doc['date']
            job_form.location.data = job_doc['location']
            job_form.short_description.data = job_doc['short_description']
            job_form.description.data = job_doc['description']
            job_form.requirements.data = job_doc['requirements']
            job_form.target_group.data = job_doc['target_group']
            job_form.industry.data = job_doc['industry']
            return render_template(
                'applications/editJob.html',
                form=job_form,
                #action=url_for('mod_apply_for_job.edit_job'),
                display_pass_field=True
            )
        else:
            return render_template('home/jobs.html')
    elif request.method == "POST":
        job_form = CreateJob()
        job_doc = Job.objects.get(id=ObjectId(job_id))
        job_doc.update(
            set__title=job_form.title.data,
            set__date=job_form.date.data,
            set__location=job_form.location.data,
            set__short_description=job_form.short_description.data,
            set__description=job_form.description.data,
            set__requirements=job_form.requirements.data,
            set__target_group=job_form.target_group.data,
            set__industry=job_form.industry.data
        )
        return redirect('/job/'+job_id)