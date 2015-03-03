from flask import Blueprint, g
from flaskext.auth import Auth, AuthUser, logout, Permission, Role, \
    permission_required
from app import mongo, flask_bcrypt
import app

mod_roles_permissions = Blueprint()

auth = Auth(app, login_url_name='index')

user_create = Permission('user', 'create')
user_view = Permission('user', 'view')

roles = {
    'admin': Role('admin', [user_create, user_view]),
    'userview': Role('userview', [user_view]),
}

def load_role(role_name):
    """
    Function that has to be defined to be able to retrieve the actual role
    object from the user.role attribute. In this simple case, we could
    actually assign the role object directly to user.role, in which this
    function would simply be the identity function (lambda x: x). This extra
    step becomes needed however in case the role object is more complex
    and it can't be simply pickled anymore.
    """
    return roles.get(role_name)

auth.load_role = load_role

@app.before_request
def init_users():
    """
    Initializing users by hardcoding password. Another use case is to read
    usernames from an external file (like /etc/passwd).
    """
    user = AuthUser(username='user')
    # Setting and encrypting the hardcoded password.
    user.set_and_encrypt_password('password', salt='123')
    # Setting role of the user.
    user.role = 'userview'

    # Doing the same for the admin
    admin = AuthUser(username='admin')
    admin.set_and_encrypt_password('admin')
    admin.role = 'admin'

    # Persisting users for this request.
    g.users = {'user': user, 'admin': admin, }

@permission_required(resource='user', action='view')
def user_view():
    return 'Users are: {0}.'.format(g.users)

@permission_required(resource='user', action='create')
def user_create():
    return 'I can create users!'


def logout_view():
    user_data = logout()
    if user_data is None:
        return 'No user to log out.'
    return 'Logged out user {0}.'.format(user_data['username'])