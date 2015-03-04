import os
import ConfigParser
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.pymongo import PyMongo

# Create MongoDB database object.
mongo = PyMongo()


def create_app():
    ''' Create the Flask app.
    '''
    # Create the Flask app.
    app = Flask(__name__)

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Import Admin modules
    from app.admin.mod_roles_permissions.views import mod_roles_permissions
    from app.admin.mod_users.views import mod_users

    # Import public interface modules
    from app.public.mod_applications.views import mod_applications
    from app.public.mod_apply_for_job.views import mod_apply_for_job
    from app.public.mod_apply_for_training.views import mod_apply_for_training
    from app.public.mod_cv.views import mod_cv
    from app.public.mod_home.views import mod_home
    from app.public.mod_register.views import mod_register
    from app.public.mod_jobs.views import mod_jobs
    from app.public.mod_profile.views import mod_profile

    # Register public interface blueprint(s)
    app.register_blueprint(mod_profile)
    app.register_blueprint(mod_jobs)
    app.register_blueprint(mod_applications)
    app.register_blueprint(mod_apply_for_job)
    app.register_blueprint(mod_apply_for_training)
    app.register_blueprint(mod_cv)
    app.register_blueprint(mod_home)
    app.register_blueprint(mod_register)

    # Register Admin interface blueprints(s)
    app.register_blueprint(mod_roles_permissions)
    app.register_blueprint(mod_users)

    # Init app for use with this PyMongo
    # http://flask-pymongo.readthedocs.org/en/latest/#flask_pymongo.PyMongo.init_app
    mongo.init_app(app, config_prefix='MONGO')

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''

    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    # FIXME: Use the "common pattern" described in "Configuring from Files": http://flask.pocoo.org/docs/config/
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    # Set up config properties
    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['BASE_PATH'] = config.get('Application', 'BASE_PATH')

    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()

    # Set the secret key, keep this really secret. We need this for session manager.
    # Check out sectopm "How to generate good secret keys" in http://flask.pocoo.org/docs/quickstart/
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

    # First log informs where we are logging to. Bit silly but serves  as a confirmation that logging works.
    # FIXME: Logging isn't working, figure out why.
    app.logger.info('Logging to: %s', log_path)

