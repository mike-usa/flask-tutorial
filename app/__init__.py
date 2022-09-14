"""Initialize Flask app."""

# Standard library imports
import os

# Third party imports
from flask import Flask
from werkzeug.utils import import_string

# Local application imports
from .models import db, migrate

env = os.environ['FLASK_ENV'] if 'FLASK_ENV' in os.environ else 'development'

def create_app():
  """Construct the core application."""

  app = Flask(__name__, instance_relative_config=False, static_folder='./assets', template_folder='./views')
  # create object in order to use `@property` and load into app
  cfg = import_string(f'config.{env.title()}Config')()
  app.config.from_object(cfg)
  app.jinja_env.add_extension('jinja2.ext.loopcontrols')

  db.init_app(app)
  migrate.init_app(app,db)

  with app.app_context():
    from . import routes

    # NOTE: below is commented-out in favor of using `flask db migrate`
    #
    # Create database tables for our data models
    # bind=None targets only default database connection and not other binds
    #   if it's not supplied it'll attempt to create on all databases bound
    #   to flask app (e.g., boardstaff, bankstaff, etc)
    # db.create_all(bind=None)

    return app
