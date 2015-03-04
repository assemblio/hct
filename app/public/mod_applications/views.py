from flask import Blueprint, render_template

# Define the blueprint:
mod_applications = Blueprint('mod_applications', __name__)

# Set the route and accepted methods
@mod_applications.route('/applications/applicants-listing')
def applicants_listing():
    return render_template('applications/applicants-listing.html')

@mod_applications.route('/applications/applicants-tab')
def applicants_tab():
    return render_template('applications/applicants-tab.html')

@mod_applications.route('/applications/applicants-listing-no-sidebar')
def applicants_listing_no_sidebar():
    return render_template('applications/applicants-listing-no-sidebar.html')