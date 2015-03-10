from functools import wraps
from flask.ext.login import current_user
import app

def role_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return app.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                return app.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper