"""Group data model."""
from app import db
from . user_group import Assignment

class Group(db.Model):
    """Data model for groups."""
    __table_args__ = { 'schema': 'flaskapp'}
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(64), index=True, unique=True, nullable=False)
    owner = db.Column(db.String(64))        # reference User model
    description = db.Column(db.String(200))
    created = db.Column(db.DateTime, nullable=False)
    is_security = db.Column(db.Boolean, nullable=False)
    members = db.relationship('User',
        secondary=Assignment.__table__,
        back_populates='groups'
    )


    def __repr__(self):
        return "<Group {}>".format(self.group)