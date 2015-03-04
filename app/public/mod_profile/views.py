from flask import Blueprint, render_template

# Define the blueprint:
mod_profile = Blueprint('mod_profile', __name__)

# Set the route and accepted methods
@mod_profile.route('/profile')
def profile():
    return render_template('profile/profile.html')
