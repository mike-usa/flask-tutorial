"""Flask configuration variables."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
  """Set Flask configuration from .env file."""

  # General Config
  SECRET_KEY = environ.get("SECRET_KEY")
  FLASK_APP = environ.get("FLASK_APP")
  FLASK_ENV = environ.get("FLASK_ENV")
  TESTING = False

  # Database
  # SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  db_dialect = 'postgresql'
  db_driver = 'psycopg2'
  db_user = 'pythonapp'
  db_pass = ''
  db_host = 'localhost'
  db_port = '5432'
  db_name = 'dev_db'

  @property
  def SQLALCHEMY_DATABASE_URI(self):
    db_uri = environ.get("SQLALCHEMY_DATABASE_URI")

    if not db_uri:
      db_uri = f'{self.db_dialect}+{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    return db_uri


class ProductionConfig(Config):
  db_name = 'prod_db'
  db_host = 'production'


class TestConfig(Config):
  db_name = 'test_db'
  TESTING = True


class DevelopmentConfig(Config):
  db_name = 'dev_db'
  pass