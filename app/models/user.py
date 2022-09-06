"""User data model."""
from app import db
from . user_group import Assignment, Owners, Maintainers
from .mixins.timestamp import TimestampMixin
from .mixins.inspector import InspectorMixin

import json
from datetime import date, datetime

def default(object):
  # format dates
  if isinstance(object, (date, datetime)):
    return object.strftime('%Y-%m-%d %H:%m')

  if object.__class__.__name__ == 'Group':
    return object.serializer()
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
    secondary=Assignment.__table__,
    back_populates='members'
  )

  # Displays
  def serializer(self):
    columns = self.keys()

    excludes = []
    columns = list(set(columns) - set(excludes))

    response = {}
    for column in columns:
      response[column] = getattr(self, column)

    return json.loads(json.dumps(response, default=default))



  def __repr__(self):
    return "<User {}>".format(self.username)
