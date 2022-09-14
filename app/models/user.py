"""User data model."""

# Standard library imports
import json
from datetime import date, datetime

# Third party imports
from app import db
from sqlalchemy import event

# Local application imports
from .user_group import Members, Owners, Maintainers
from .mixins.inspector import InspectorMixin
from .mixins.timestamp import TimestampMixin


def json_format(object):
  # format dates
  if isinstance(object, (date, datetime)):
    return object.strftime('%Y-%m-%d %H:%M %z')

  # Call 'Group' to serialize itself
  if object.__class__.__name__ == 'Group':
    return object.serialize()

  # instance display
  return f'<{object.__class__.__name__} id={object.id}>'


class User(TimestampMixin, db.Model, InspectorMixin):
  """Data model for user accounts."""
  
  app_schema = 'flaskapp'
  __table_args__ = { 'schema': app_schema }
  __tablename__ = "users"

  # Attriubutes
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True, nullable=False)
  email = db.Column(db.String(80), index=True, unique=True, nullable=False)
  bio = db.Column(db.Text, nullable=True)
  admin = db.Column(db.Boolean, nullable=False)
  
  # Relationships
  owns = db.relationship('Group',
    secondary=Owners.__table__,
    back_populates='owners'
  )
  maintains = db.relationship('Group',
    secondary=Maintainers.__table__,
    back_populates='maintainers'
  )
  groups = db.relationship('Group',
    secondary=Members.__table__,
    back_populates='members'
  )

  # Displays
  def serialize(self):
    """Display the model as a string or JSON string."""
    columns = self.keys()

    excludes = []
    columns = list(set(columns) - set(excludes))

    response = {}
    for column in columns:
      response[column] = getattr(self, column)

    return json.loads(json.dumps(response, default=json_format))


  def __repr__(self):
    return "<User {}>".format(self.username)
