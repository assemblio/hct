from flask import Blueprint, render_template, flash, request, url_for, redirect
from user_registration.form import LoginForm, RegisterForm
from flask.ext.security import MongoEngineUserDatastore, login_user, login_required, logout_user
from app.modules.public.mod_authentication.user_registration.model import User, Role
from mongoengine import DoesNotExist
from app import db
from .utils import Utils

# Create Utils instance
utils = Utils()
# Define the blueprint:
mod_authentication = Blueprint('mod_authentication', __name__, url_prefix="/auth")

# Set the route and accepted methods
@mod_authentication.route('/register', methods=['GET', 'POST'])
def index():
    form = RegisterForm(request.form)
    user = User(
        username=form.username.data,
        email=form.email.data,
        password=form.password.data,
        name=form.name.data,
        surname=form.surname.data,
        address1=form.address1.data,
        address2=form.address2.data,
        #date_of_birth=form.date_of_birth.data,
        phone_mobile=form.phone_mobile.data,
        phone_work=form.phone_work.data,
        expected_salary=form.expected_salary.data
    )
    print "before validation"
    print form.email.data
    try:
        form.email.data == User.objects.get(email=form.email.data)
        print "email exists in the database"
        flash('Email already exists.', 'success')
    except DoesNotExist:
        user.save()
        user_datastore = MongoEngineUserDatastore(db, User, Role)
        user_datastore.add_role_to_user(user, "User")
        login_user(user)
        return render_template('home/welcome.html', form=form)

    return render_template('home/register.html', form=form)

@mod_authentication.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.objects.get(email=form.email.data, password=form.password.data)
        if user['email'] == form.email.data and user['password'] == form.password.data:
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('mod_home.index'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('home/login.html', form=form)
    return render_template('home/login.html', form=form)

@mod_authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('mod_public_user.login'))

@mod_authentication.route('/loginheader', methods=['POST','GET'])
def login_header():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.objects.get(email=form.email.data)
        login_user(user)
        if user['email'] == form.email.data and user['password'] == form.password.data:
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('mod_home.index'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('home/login.html')

    return render_template('home/login.html', form=form, next=next)