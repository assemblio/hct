from flask import render_template, Blueprint
from flask.ext.security import login_required, roles_required

# Define the blueprint:
admin_home = Blueprint('admin_home', __name__)


@admin_home.route('/admin')
@login_required
@roles_required('Admin')
def index():
    return render_template('admin/index.html')
