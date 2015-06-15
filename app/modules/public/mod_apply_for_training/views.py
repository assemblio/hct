from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import roles_required, login_required, current_user
from .form import RegisterTraining
from .model import Training
from app.modules.public.mod_authentication.user_registration.model import User
from bson import ObjectId
from flask.ext.mongoengine import DoesNotExist
import datetime

# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('/trainings')
def index():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    trainings = Training.objects.all()
    pagination = trainings.paginate(page=page, per_page=10)
    return  render_template('applications/trainings.html', pagination=pagination)

@mod_apply_for_training.route('/training/<string:training_id>')
def training(training_id):
    training = Training.objects.get(id=ObjectId(training_id))
    return render_template('applications/training.html', training=training)

@mod_apply_for_training.route('/training/<string:action>/<string:training_id>')
@login_required
def apply_for_training(action, training_id):
    if action == 'apply':
        training = Training.objects.get(id=ObjectId(training_id))
        if not training['participants']:
            training['participants'] = []
        if not ObjectId(current_user.id) in training['participants']:
            if training['space'] != 0:
                Training.objects.get(id=ObjectId(training_id)).update(push__participants=ObjectId(current_user.id), dec__space=1)
                User.objects.get(id=ObjectId(current_user.id)).update(push__trainings=ObjectId(training_id))
                return redirect('/trainings')
    elif action == 'unapply':
        training = Training.objects.get(id=ObjectId(training_id))
        if ObjectId(current_user.id) in training['participants']:
            Training.objects.get(id=ObjectId(training_id)).update(pull__participants=ObjectId(current_user.id), inc__space=1)
            User.objects.get(id=ObjectId(current_user.id)).update(pull__trainings=ObjectId(training_id))
            return redirect('/trainings')
    elif action == 'delete' and current_user.has_role('Admin'):
        Training.objects.get(id=ObjectId(training_id)).delete()
        User.objects.get(id=ObjectId(current_user.id)).update(pull__trainings=ObjectId(training_id))
        return redirect('/trainings')

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

@mod_apply_for_training.route('/training/edit/<string:training_id>', methods=['GET','POST'])
@login_required
@roles_required('Admin')
def edit_training(training_id):
    if request.method == "GET":
        training_form = RegisterTraining()
        training_doc = Training.objects.get(id=ObjectId(training_id))
        if current_user.is_authenticated():
            training_form.title.data = training_doc['title']
            training_form.startDate.data = training_doc['startDate']
            training_form.endDate.data = training_doc['endDate']
            training_form.space.data = training_doc['space']
            training_form.instructorName.data = training_doc['instructorName']
            training_form.instructorSurname.data = training_doc['instructorSurname']
            training_form.agenda.data = training_doc['agenda']
            training_form.short_description.data = training_doc['short_description']
            training_form.description.data = training_doc['description']
            training_form.requirements.data = training_doc['requirements']
            training_form.target_group.data = training_doc['target_group']
            return render_template(
                'applications/editTraining.html',
                form=training_form,
                display_pass_field=True
            )
        else:
            return render_template('home/trainings.html')
    elif request.method == "POST":
        training_form = RegisterTraining()
        training_doc = Training.objects.get(id=ObjectId(training_id))
        training_doc.update(
            set__title=training_form.title.data,
            set__startDate=training_form.startDate.data,
            set__endDate=training_form.endDate.data,
            set__space=training_form.space.data,
            set__instructorName=training_form.instructorName.data,
            set__instructorSurname=training_form.instructorSurname.data,
            set__agenda=training_form.agenda.data,
            set__short_description=training_form.short_description.data,
            set__description=training_form.description.data,
            set__requirements=training_form.requirements.data,
            set__target_group=training_form.target_group.data
        )
        return redirect(url_for("mod_apply_for_training.training",training_id=training_id))









