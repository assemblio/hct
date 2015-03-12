import ConfigParser
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from hct_app.modules.public.mod_authentication.user_registration.model import User, Role

# Create the Flask app.
app = Flask(__name__)

# Create login_manager
login_manager = LoginManager()

# Init login manager
login_manager.init_app(app)

# Create the MongoDB instance
database = MongoEngine()

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(database, User, Role)
security_ = Security(app, user_datastore)


def create_app():
    # Create the MongoDB instance
    db = MongoEngine()

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Instantiate MongoEngine instance
    db.init_app(app)

    # Import Admin modules
    from hct_app.modules.admin.mod_roles_permissions.views\
        import mod_roles_permissions
    from hct_app.modules.admin.mod_users.views import mod_users

    # Import public interface modules
    from hct_app.modules.public.mod_applications.views import mod_applications
    from hct_app.modules.public.mod_apply_for_job.views import mod_apply_for_job
    from hct_app.modules.public.mod_apply_for_training.views \
        import mod_apply_for_training
    from hct_app.modules.public.mod_cv.views import mod_cv
    from hct_app.modules.public.mod_home.views import mod_home
    from hct_app.modules.public.mod_authentication.views\
        import mod_authentication
    from hct_app.modules.public.mod_jobs.views import mod_jobs
    from hct_app.modules.public.mod_profile.views import mod_profile

    # Register public interface blueprint(s)
    app.register_blueprint(mod_profile)
    app.register_blueprint(mod_jobs)
    app.register_blueprint(mod_applications)
    app.register_blueprint(mod_apply_for_job)
    app.register_blueprint(mod_apply_for_training)
    app.register_blueprint(mod_cv)
    app.register_blueprint(mod_home)
    app.register_blueprint(mod_authentication)

    # Register Admin interface blueprints(s)
    app.register_blueprint(mod_roles_permissions)
    app.register_blueprint(mod_users)

    return app


def load_config(app):
    ''' Reads the config file and loads configuration
    properties into the Flask app.
    :param app: The Flask app object.
    '''

    ''' Get the path to the application directory,
    that's where the config file resides.
    '''
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    ''' Read config file
    # FIXME: Use the "common pattern" described in "Configuring
    #from Files": http://flask.pocoo.org/docs/config/
    '''
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    # Set up config properties
    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['BASE_PATH'] = config.get('Application', 'BASE_PATH')
    app.config['SECURITY_PASSWORD_SALT'] = config.get(
        'Application',
        'SECURITY_PASSWORD_SALT'
    )
    app.config['SECURITY_REGISTERABLE'] = config.get(
        'Application',
        'SECURITY_REGISTERABLE'
    )

    # Config MONGODB
    app.config['MONGODB_SETTINGS'] = {
        'db': config.get('MONGODB_SETTINGS', 'MONGODB_DATABASE'),
        'host': config.get('MONGODB_SETTINGS', 'MONGODB_HOST'),
        'port': int(config.get('MONGODB_SETTINGS', 'MONGODB_PORT'))
    }

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path
    # with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()

    # Set the secret key, keep this really secret.
    # We need this for session manager.
    # Check out section "How to generate good secret keys"
    # in http://flask.pocoo.org/docs/quickstart/
    app.secret_key = config.get('Application', 'SECRET_KEY')


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    # FIXME: Logging isn't working, figure out why.
    app.logger.info('Logging to: %s', log_path)


def create_user_roles():
    # Create the roles using the flask-security plugin.

    # Create User role
    if not user_datastore.find_role('User'):
        # Create the user role
        user_datastore.create_role(
            name='user',
            description='User of the system.'
        )

    # Create Admin Role and admin user
    if not user_datastore.find_role('Admin'):
        # Create the admin role
        user_datastore.create_role(
            name='Admin',
            description='Admin of the system.'
        )
        # Create the admin user
        user_datastore.create_user(
            email="admin@admin.com",
            username="admin",
            password="admin"
        )
# Create roles
create_user_roles()
