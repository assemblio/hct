from flask import \
    Blueprint, render_template, flash, request, url_for, redirect, current_app
from user_registration.form import LoginForm, RegisterForm
from flask.ext.security import login_user, login_required, logout_user
from app.modules.public.mod_authentication.user_registration.model import User
from mongoengine import DoesNotExist
from app import user_datastore, bcrypt

# Define the blueprint:
mod_authentication = Blueprint(
    'mod_authentication',
    __name__,
    url_prefix="/auth"
)


# Set the route and accepted methods
@mod_authentication.route('/register', methods=['GET', 'POST'])
def register():
    '''
     Register user.
    '''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    previous_url = request.form['previous_url']

    #form = RegisterForm(request.form)

    if request.method == 'POST':
        try:
            User.objects.get(email=email)
            redirect(url_for(previous_url))
        except DoesNotExist:
            user = User(
                email=email,
                password=bcrypt.generate_password_hash(password, rounds=12),
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            default_role = user_datastore.find_role('User')
            user_datastore.add_role_to_user(user, default_role)
            login_user(user)
            return render_template('home/welcome.html')
    else:
        return redirect(url_for(previous_url))


@mod_authentication.route('/login', methods=['GET', 'POST'])
def login():
    '''
     Login request.
    '''
    form = LoginForm(request.form)

    email = request.form['email']
    password = request.form['password']
    previous_url = request.form['previous_url']
    if request.method == 'POST':
        user = User.objects.get(email=email)
        if user['email'] == email and bcrypt.check_password_hash(user['password'], password):
            login_user(user)
            current_app.logger.info("User '%s' logged in." % email)
            return redirect(url_for(previous_url))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('home/login.html', form=form)
    elif request.method == "GET":
        return redirect(url_for(previous_url))


@mod_authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mod_authentication.login'))
