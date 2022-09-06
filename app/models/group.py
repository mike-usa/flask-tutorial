"""Group data model."""
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

  # if object.__class__.__name__ == 'User':
  #   return object.serializer()

  return f'<{object.__class__.__name__} id={object.id}>'


class Group(TimestampMixin, db.Model, InspectorMixin):
  """Data model for groups."""
  app_schema = 'flaskapp'
  __table_args__ = { 'schema': app_schema }
  __tablename__ = "groups"

  # Attributes
  id = db.Column(db.Integer, primary_key=True)
  group = db.Column(db.String(64), index=True, unique=True, nullable=False)
  description = db.Column(db.String(200))
  is_security = db.Column(db.Boolean, nullable=False)

  # Relationships
  owners = db.relationship('User',
    secondary=Owners.__table__,
    back_populates="owns"
  )
  maintainers = db.relationship('User',
    secondary=Maintainers.__table__,
    back_populates='maintains'
  )
  members = db.relationship('User',
    secondary=Assignment.__table__,
    back_populates='groups'
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
      return "<Group {}>".format(self.group)
