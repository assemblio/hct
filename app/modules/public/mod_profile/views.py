from flask import Blueprint, render_template, request, url_for, redirect
from flask.ext.security import current_user
from app.modules.public.mod_authentication.user_registration.model\
    import User
from app.modules.public.mod_apply_for_job.model import Job
from app.modules.public.mod_apply_for_training.model import Training
from app.modules.public.mod_authentication.user_registration.form import\
    RegisterForm
from flask.ext.security import login_required
from bson import ObjectId

# Define the blueprint:
mod_profile = Blueprint('mod_profile', __name__)


# Set the route and accepted methods
@mod_profile.route('/profile')
@login_required
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
    return render_template(
        'profile/index.html',
        current_user=current_user,
        show_jobs=show_jobs,
        show_trainings=show_trainings
    )


@mod_profile.route('/profile/<string:request_user>')
def get_user(request_user):
    user = User.objects.get(id=ObjectId(request_user))
    return render_template('profile/profile.html', username=user)


@mod_profile.route('/personal-info', methods=['POST', 'GET'])
@login_required
def update_personal_info():
    user_doc = User.objects.get(email=current_user.email)
    user_form = RegisterForm()

    if request.method == "GET":
        if current_user.is_authenticated():
            user_form.first_name.data = user_doc['first_name']
            user_form.last_name.data = user_doc['last_name']
            user_form.email.data = user_doc['email']
            user_form.phone_mobile.data = user_doc['phone_mobile']
            user_form.phone_work.data = user_doc['phone_work']
            user_form.fax.data = user_doc['fax']
            user_form.address1.data = user_doc['address1']
            user_form.address2.data = user_doc['address2']
            user_form.expected_salary.data = user_doc['expected_salary']
            return render_template(
                'home/personal_info.html',
                form=user_form,
                action=url_for('mod_profile.update_personal_info'),
                display_pass_field=True
            )
        else:
            return render_template('home/index.html')
    elif request.method == "POST":
        user_doc.update(
            set__email=user_form.email.data,
            set__first_name=user_form.first_name.data,
            set__last_name=user_form.last_name.data,
            set__password=user_form.first_name.data,
            set__phone_mobile=user_form.phone_mobile.data,
            set__phone_work=user_form.phone_work.data,
            set__fax=user_form.fax.data,
            set__address1=user_form.address1.data,
            set__address2=user_form.address2.data,
            set__expected_salary=user_form.expected_salary.data
        )
        return redirect(url_for('mod_profile.update_personal_info'))


@mod_profile.route('/update-education', methods=['POST', 'GET'])
@login_required
def update_education():
    user_doc = User.objects.get(email=current_user.email)
    user_form = RegisterForm()

    if request.method == 'GET':
        if current_user.is_authenticated():
            user_form.school.data = user_doc['school']
            user_form.fieldOfStudy.data = user_doc['fieldOfStudy']
            user_form.schoolDegree.data = user_doc['schoolDegree']
            user_form.startDateSchool.data = user_doc['startDateSchool']
            user_form.endDateSchool.data = user_doc['endDateSchool']
            user_form.schoolDescription.data = user_doc['schoolDescription']

            return render_template(
                'home/update_education.html',
                form=user_form,
                action=url_for('mod_profile.update_education')
            )
        else:
            return render_template('home/index.html')
    elif request.method == 'POST':
        if user_form.validate_on_submit():
            user_doc.update(
                set__school=user_form.school.data,
                set__fieldOfStudy=user_form.fieldOfStudy.data,
                set__schoolDegree=user_form.schoolDegree.data,
                set__startDateSchool=user_form.startDateSchool.data,
                set__endDateSchool=user_form.endDateSchool.data,
                set__schoolDescription=user_form.schoolDescription.data
            )

        return render_template('home/update_education.html', form=user_form)


@mod_profile.route('/update-experience', methods=['POST', 'GET'])
@login_required
def update_experience():
    form = RegisterForm(request.form)
    return render_template('home/update_experience.html', form=form)


@mod_profile.route('/update-summary', methods=['POST', 'GET'])
@login_required
def update_summary():
    form = RegisterForm(request.form)
    return render_template('home/update_summary.html', form=form)
