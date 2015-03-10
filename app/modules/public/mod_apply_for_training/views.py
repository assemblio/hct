from flask import Blueprint, render_template, request
from flask.ext.security import roles_required, login_required
from .form import RegisterTraining
from .model import Training
from app.modules.public.mod_authentication.decorators import role_required
# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('/trainings')
def index():
    trainings = Training.objects()
    return  render_template('applications/trainings.html', trainings=trainings)

@mod_apply_for_training.route('/create-training', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create():
    form = RegisterTraining(request.form)
    training = Training(
        title=form.title.data,
        startDate = form.startDate.data,
        endDate = form.endDate.data,
        space = form.space.data,
        instructorName = form.instructorName.data,
        instructorSurname = form.instructorSurname.data,
        agenda = form.agenda.data,
        description = form.description.data,
        requirements = form.requirements.data
    )
    if training:
        training.save()
    #user_datastore.add_role_to_user(user, "User")

    return render_template('applications/createTrainings.html', form=form)
<<<<<<< HEAD
'''
@mod_apply_for_training.route('/display-training', methods=['GET'])
def display():
        json = db.training.find()
        resp = Response(
        response=json_util.dumps(json),
        mimetype='application/json')
    return render_template('applications/createTrainings.html', form=form)
'''
=======

>>>>>>> bbb3a7bb4359497dee68665484ab8b878d121d6b



