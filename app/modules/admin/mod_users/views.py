import datetime

# Import flask dependencies

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, session
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from app.modules.models.models import User
#from app.modules.models.email import send_email
from app.modules.models.decorators import check_confirmed
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from .token import confirm_token, generate_confirmation_token
from app import db

import app
# Define the blueprint:
mod_users = Blueprint('users', __name__, url_prefix="/users", static_folder='static',template_folder='templates')


@mod_users.route('/')
@login_required
def home():
    return render_template('main/index.html')

@mod_users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            confirmed=True
        ).save()
        '''
        app.session.add(user)
        app.session.commit()
        '''
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("users.confirmed"))

    return render_template('user/register.html', form=form)

@mod_users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.objects.get(email=form.email.data, password=form.password.data)
        print user
        if user['email'] == form.email.data and user['password'] == form.password.data:
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('users.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@mod_users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@mod_users.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ChangePasswordForm(request.form)
    print current_user.email
    if form.validate_on_submit():
        user = User.objects(email=current_user.email)
        if user:
            user.password =form.password.data
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)


@mod_users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.objects(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('users.home'))


@mod_users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('users.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@mod_users.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))