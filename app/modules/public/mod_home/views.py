from flask import request, render_template
from flask import Blueprint

# Define the blueprint:
mod_home = Blueprint('mod_home', __name__)

# Set the route and accepted methods
@mod_home.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')

@mod_home.route('/about-us')
def about_us():
    return render_template('home/about-us.html')

@mod_home.route('/contacts')
def contacts():
    return render_template('home/contacts.html')

@mod_home.route('/terms-and-conditions')
def terms_conditions():
    return render_template('home/terms-and-conditions.html')
