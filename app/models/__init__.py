"""Initialize and customize `db` object"""

# Standard library imports
# --- None ---

# Third party imports
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from flask_migrate import Migrate

# Local application imports
# --- None ---



class ExtendedBase(BaseQuery):
  '''Extends BaseQuery for all models'''
  def get_or(self, ident, default=None):
    """
      Retrieve model by primary key or return none

      Examples: 
      User.query.get_or(user_id, anonymous_user)
      User.query.get_or(3)
      User.query.get_or({'id': 3})
    """
    return self.get(ident) or default


db = SQLAlchemy(query_class=ExtendedBase)
migrate = Migrate()
