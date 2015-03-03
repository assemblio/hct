from flask import Blueprint

# Define the blueprint:
mod_applications = Blueprint('mod_applications', __name__)

# Set the route and accepted methods
@mod_applications.route('/applications', methods=['GET'])
def index():
    return ""