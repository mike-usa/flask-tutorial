"""User data model."""
from app import db
from . user_group import Assignment

class User(db.Model):
    """Data model for user accounts."""
    __table_args__ = { 'schema': 'flaskapp'}
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    admin = db.Column(db.Boolean, nullable=False)
    groups = db.relationship('Group',
        secondary=Assignment.__table__,
        back_populates='members'
    )

    def __repr__(self):
        return "<User {}>".format(self.username)
