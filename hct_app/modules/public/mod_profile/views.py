from flask import Blueprint, render_template
from flask.ext.security import current_user
from hct_app.modules.public.mod_authentication.user_registration.model import User

# Define the blueprint:
mod_profile = Blueprint('mod_profile', __name__)

# Set the route and accepted methods
@mod_profile.route('/profile')
def profile():
    print current_user
    return render_template('profile/index.html', current_user=current_user)


@mod_profile.route('/profile/<string:request_user>')
def get_user(request_user):
    user = User.objects.get(username=request_user)
    return render_template('profile/profile.html', username=user)