"""User-Group relationship data model."""

# Standard library imports
# --- None ---

# Third party imports
# --- None ---

# Local application imports
from app import db
from .mixins.inspector import InspectorMixin
from .mixins.timestamp import TimestampMixin

app_schema = 'flaskapp'

class Members(TimestampMixin, db.Model, InspectorMixin):
  """Data model for the users-groups members associations."""

  __tablename__ = 'members'
  __table_args__ = { 'schema': app_schema }
  user_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.users.id'), primary_key=True)
  group_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.groups.id'), primary_key=True)


class Owners(TimestampMixin, db.Model, InspectorMixin):
  """Data model for the users-groups owners associations."""

  __table_args__ = { 'schema': app_schema }
  __tablename__ = 'owners'
  user_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.users.id'), primary_key=True)
  group_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.groups.id'), primary_key=True)


class Maintainers(TimestampMixin, db.Model, InspectorMixin):
  """Data model for the users-groups maintainers associations."""

  __table_args__ = { 'schema': app_schema }
  __tablename__ = 'maintainers'
  user_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.users.id'), primary_key=True)
  group_id = db.Column(db.Integer, db.ForeignKey(f'{app_schema}.groups.id'), primary_key=True)