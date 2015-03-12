from flask import Blueprint, render_template, request, redirect
from flask.ext.security import roles_required, login_required
from .form import RegisterTraining
from .model import Training
from bson import ObjectId

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

@mod_apply_for_training.route('/create-training', methods=['GET', 'POST'])
@login_required
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




