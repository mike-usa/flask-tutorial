"""User-Group relationship data model."""
from app import db
from .mixins.timestamp import TimestampMixin


class Assignment(TimestampMixin, db.Model):
    """Data model for the users-groups members associations."""
    __table_args__ = { 'schema': 'flaskapp' }
    __tablename__ = 'users_groups'
    user_id = db.Column(db.Integer, db.ForeignKey('flaskapp.users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('flaskapp.groups.id'), primary_key=True)


class Owners(TimestampMixin, db.Model):
    """Data model for the users-groups ownrs associations."""
    __table_args__ = { 'schema': 'flaskapp' }
    __tablename__ = 'owners'
    user_id = db.Column(db.Integer, db.ForeignKey('flaskapp.users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('flaskapp.groups.id'), primary_key=True)


class Maintainers(TimestampMixin, db.Model):
    """Data model for the users-groups maintainers associations."""
    __table_args__ = { 'schema': 'flaskapp' }
    __tablename__ = 'maintainers'
    user_id = db.Column(db.Integer, db.ForeignKey('flaskapp.users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('flaskapp.groups.id'), primary_key=True)