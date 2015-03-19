from flask import render_template, Blueprint, request
from flask.ext.security import login_required, roles_required
from app.modules.public.mod_authentication.user_registration.model import User
# Define the blueprint:
admin_users = Blueprint('admin_users', __name__)


@admin_users.route('/admin/users', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def index():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    useri = User.objects.all()
    pagination = useri.paginate(page=page, per_page=10)
    return render_template('admin/users/users.html', pagination=pagination)
