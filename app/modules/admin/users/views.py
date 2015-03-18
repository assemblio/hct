from flask import render_template, Blueprint
from flask.ext.security import login_required, roles_required

# Define the blueprint:
admin_users = Blueprint('admin_users', __name__)


@admin_users.route('/admin/users')
@login_required
@roles_required('Admin')
def index():
    return render_template('admin/users/users.html')
