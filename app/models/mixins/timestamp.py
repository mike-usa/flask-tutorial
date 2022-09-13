# from datetime import datetime, timezone
from app import db
from sqlalchemy.sql import func

class TimestampMixin(object):
  created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now()) #default=datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()) #onupdate=datetime.now(timezone.utc))
  created_by = db.Column(db.String)
  updated_by = db.Column(db.String)
