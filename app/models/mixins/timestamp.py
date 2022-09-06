from datetime import datetime, timezone
from app import db

class TimestampMixin(object):
  created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
  updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
