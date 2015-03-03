from flask import request, g, url_for, render_template
from flask import Blueprint

# Define the blueprint:
mod_home = Blueprint('mod_home', __name__)

# Set the route and accepted methods
@mod_home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if username in g.users:
            # Authenticate and log in!
            if g.users[username].authenticate(request.form['password']):
                return '''
                        <a href="">View users</a><br/>
                        <a href="">Create users</a><br/>
                        <a href="">Logout</a>
                        '''
        return 'Failure :('
    return render_template('home/index.html')
