import os
import ConfigParser
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.pymongo import PyMongo

from flask.ext.bcrypt import Bcrypt

from utils.utils import Utils

# Create MongoDB database object.
mongo = PyMongo()
utils = Utils()
# Flask BCrypt hashing object will be used to salt the user password
flask_bcrypt = Bcrypt()


def create_app():
    ''' Create the Flask app.
    '''
    # Create the Flask app.
    app = Flask(__name__)

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

     # Import a module / component using its blueprint handler variable
    from app.mod_landing_page.views import mod_landing_page
    from app.mod_auth.views import mod_auth
    from app.mod_patient_directory.views import mod_patient_directory
    from app.mod_malignant_disease.views import mod_malignant_disease
    from app.mod_ekografia.views import mod_ekografia
    from app.mod_mamografia.views import mod_mamografia
    from app.mod_doc_profile.views import mod_doc_profile

    # Register blueprint(s)
    app.register_blueprint(mod_landing_page)
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_patient_directory)
    app.register_blueprint(mod_malignant_disease)
    app.register_blueprint(mod_ekografia)
    app.register_blueprint(mod_mamografia)
    app.register_blueprint(mod_doc_profile)

    # Register URL rules.
    register_url_rules(app)

    # Init app for use with this PyMongo
    # http://flask-pymongo.readthedocs.org/en/latest/#flask_pymongo.PyMongo.init_app
    mongo.init_app(app, config_prefix='MONGO')

    return app