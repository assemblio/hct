from flask import Blueprint, render_template, flash, request, url_for, redirect
from user_registration.form import LoginForm, RegisterForm
from flask.ext.security import login_user, login_required, logout_user
from app.modules.public.mod_authentication.user_registration.model import User, Role
from mongoengine import DoesNotExist
from app import user_datastore

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
    if form.validate_on_submit():
        try:
            form.email.data == User.objects.get(email=form.email.data)
        except DoesNotExist:
            user.save()
            default_role = user_datastore.find_role('User')
            user_datastore.add_role_to_user(user, default_role)
            login_user(user)
            return render_template('home/welcome.html', form=form)

    return render_template('home/register.html', form=form)

@mod_authentication.route('/registerheader', methods=['GET', 'POST'])
def register_header():
    form = RegisterForm(request.form)
    next_url = request.form['next-on-register'].data
    user = User(
        name=form['name'].data,
        username=form['username'].data,
        email=form['email'].data,
        password=form['password'].data
    )
    if request.method == "POST":
        try:
            form['email'].data == User.objects.get(email=form['email'].data)
        except DoesNotExist:
            user.save()
            default_role = user_datastore.find_role('User')
            user_datastore.add_role_to_user(user, default_role)
            login_user(user)
            return redirect(url_for(next_url))

    return render_template('home/register.html', form=form)

@mod_authentication.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    next_url = request.form['next-on-login'].data
    print next_url
    if form.validate_on_submit():
        user = User.objects.get(email=form.email.data, password=form.password.data)
        if user['email'] == form.email.data and user['password'] == form.password.data:
            login_user(user)
            return redirect(url_for(next_url))
        else:
            return render_template('home/login.html', form=form)
    return render_template('home/login.html', form=form)

@mod_authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mod_public_user.login'))

@mod_authentication.route('/loginheader', methods=['POST','GET'])
def login_header():
    form = LoginForm(request.form)
    next_url = request.form['next-on-login']
    if request.method == 'POST':
        user = User.objects.get(email=form.email.data)
        if user['email'] == form.email.data and user['password'] == form.password.data:
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for(next_url))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('home/login.html')

    return render_template('home/login.html', form=form)