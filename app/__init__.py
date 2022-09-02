"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False, static_folder='./assets', template_folder='./views')
    app.config.from_object("config.Config")
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    db.init_app(app)

    with app.app_context():
        from . import routes

        db.create_all()  # Create database tables for our data models

        return app
