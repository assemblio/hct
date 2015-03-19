from flask import Blueprint, render_template, request
from app.modules.public.mod_apply_for_training.model import Training
# Define the blueprint:
admin_trainings = Blueprint('admin_trainings', __name__)


# Set the route and accepted methods
@admin_trainings.route('/admin/trainings', methods=['GET'])
def index():
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    trainings = Training.objects.all()
    pagination = trainings.paginate(page=page, per_page=10)
    return render_template('admin/jobs/jobs.html', pagination=pagination)
