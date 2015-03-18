from flask import Blueprint, render_template

# Define the blueprint:
admin_applicants = Blueprint('admin_applicants', __name__)


# Set the route and accepted methods
@admin_applicants.route('/admin/applicants', methods=['GET'])
def index():
    return render_template('admin/applicants/applicants.html')
