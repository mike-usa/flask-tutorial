"""User-Group relationship data model."""
from app import db

class Assignment(db.Model):
    """Data model for the users-groups associations."""
    __table_args__ = { 'schema': 'flaskapp' }
    __tablename__ = 'users_groups'
    user_id = db.Column(db.Integer, db.ForeignKey('flaskapp.users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('flaskapp.groups.id'), primary_key=True)