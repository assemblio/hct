from flask import Blueprint,render_template
from flask.ext.security import roles_required, login_required
# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('/trainings')
def index():
    return  render_template('applications/trainings.html')

@mod_apply_for_training.route('/createTrainings', methods=['GET'])
@login_required
def create():
    return  render_template('applications/createTrainings.html')