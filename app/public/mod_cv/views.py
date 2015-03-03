from flask import Blueprint

# Define the blueprint:
mod_cv = Blueprint('mod_cv', __name__)

# Set the route and accepted methods
@mod_cv.route('', methods=['GET'])
def index():
    return ""