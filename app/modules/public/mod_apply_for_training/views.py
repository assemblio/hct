from flask import Blueprint,render_template

# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('/trainings', methods=['GET'])
def index():
    return  render_template('home/trainings.html')