from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import roles_required, login_required, current_user
from .form import RegisterTraining
from .model import Training
from app.modules.public.mod_authentication.user_registration.model import User
from bson import ObjectId
from flask.ext.mongoengine import DoesNotExist

# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('/trainings')
def index():
    trainings = Training.objects()
    return  render_template('applications/trainings.html', trainings=trainings)

@mod_apply_for_training.route('/training/<string:training_id>')
def training(training_id):
    training = Training.objects.get(id=ObjectId(training_id))
    return render_template('applications/training.html', training=training)

@mod_apply_for_training.route('/training/apply/<string:training_id>')
@login_required
def apply_for_training(training_id):
    try:
        training = Training.objects.get(id=ObjectId(training_id))
        Training.objects.get(participants=ObjectId(current_user.id))
    except DoesNotExist:
        if training['space'] != 0:
            Training.objects.get(id=ObjectId(training_id)).update(push__participants=current_user.id, dec__space=1)
            User.objects.get(id=ObjectId(current_user.id)).update(push__trainings=ObjectId(training_id))
            return "Succesfully applied"
    return "You already applied for this training"

@mod_apply_for_training.route('/create-training', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def create():
    form = RegisterTraining(request.form)
    training = Training(
        title=form.title.data,
        startDate=form.startDate.data,
        endDate=form.endDate.data,
        space=form.space.data,
        instructorName=form.instructorName.data,
        instructorSurname=form.instructorSurname.data,
        agenda=form.agenda.data,
        description=form.description.data,
        requirements=form.requirements.data
    )
    if form.validate_on_submit():
        training.save()
        return redirect('/trainings')
    return render_template('applications/createTrainings.html', form=form)




