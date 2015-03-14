from flask import Blueprint, render_template
from flask.ext.security import current_user
from app.modules.public.mod_authentication.user_registration.model import User
from app.modules.public.mod_apply_for_job.model import Job
from app.modules.public.mod_apply_for_training.model import Training
from bson import ObjectId

# Define the blueprint:
mod_profile = Blueprint('mod_profile', __name__)

# Set the route and accepted methods
@mod_profile.route('/profile')
def profile():
    jobs_applied = current_user['jobs_applied']
    show_jobs = []
    if jobs_applied:
        for job in jobs_applied:
            show_jobs.append(Job.objects.get(id=job))

    trainings = current_user['trainings']
    show_trainings = []
    if trainings:
        for training in trainings:
            show_trainings.append(Training.objects.get(id=training))
    return render_template('profile/index.html', current_user=current_user, show_jobs=show_jobs, show_trainings= show_trainings)


@mod_profile.route('/profile/<string:request_user>')
def get_user(request_user):

    return render_template('profile/profile.html', username=user)