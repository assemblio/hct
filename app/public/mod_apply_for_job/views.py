from flask import Blueprint

# Define the blueprint:
mod_apply_for_job = Blueprint('mod_apply_for_job', __name__)

# Set the route and accepted methods
@mod_apply_for_job.route('', methods=['GET'])
def index():
    return ""