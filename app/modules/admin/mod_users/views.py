# Import flask dependencies
from flask import Blueprint, render_template, session, request, url_for, redirect

# Define the blueprint:
mod_users = Blueprint('mod_users', __name__)

# Set the route and accepted methods
@mod_users.route('/users', methods=['GET'])
def index():
    #doc_id = session.get('docId')
    #Retrieve logged-in doctor document, to populate his profile page
    #doctor_doc = mongo.db.users.find_one({'_id': doc_id})
    '''
    return render_template('doc_profile/doc_profile.html', doctor_doc=doctor_doc)
    '''