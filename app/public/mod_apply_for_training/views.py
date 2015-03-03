from flask import Blueprint

# Define the blueprint:
mod_apply_for_training = Blueprint('mod_apply_for_training', __name__)

# Set the route and accepted methods
@mod_apply_for_training.route('', methods=['GET'])
def index():
    return ""