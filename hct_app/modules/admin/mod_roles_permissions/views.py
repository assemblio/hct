from flask import Blueprint

# Define the blueprint:
mod_roles_permissions = Blueprint('mod_roles_permissions', __name__)

# Set the route and accepted methods
@mod_roles_permissions.route('/permissions', methods=['GET'])
def index():
    return ""