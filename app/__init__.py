"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False, static_folder='./assets', template_folder='./views')
    app.config.from_object("config.Config")
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    db.init_app(app)
    migrate.init_app(app,db)

    with app.app_context():
        from . import routes

        # Create database tables for our data models
        # bind=None targets only default database connection and not other binds
        #   if it's not supplied it'll attempt to create on all databases bound
        #   to flask app (e.g., boardstaff, bankstaff, etc)
        # db.create_all(bind=None)

        return app
