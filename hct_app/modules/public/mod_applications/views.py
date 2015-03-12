from flask import Blueprint, render_template

# Define the blueprint:
mod_applications = Blueprint('mod_applications', __name__)

# Set the route and accepted methods
@mod_applications.route('/applications/applicants-sidebar')
def applicants_listing():
    return render_template('applications/candidates-sidebar.html')

@mod_applications.route('/applications/applicants')
def applicants_tab():
    return render_template('applications/candidates.html')

