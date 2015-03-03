from flask import Blueprint

# Define the blueprint:
mod_register = Blueprint('mod_register', __name__)

# Set the route and accepted methods
@mod_register.route('', methods=['GET'])
def index():
    return ""