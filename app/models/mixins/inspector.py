from sqlalchemy.inspection import inspect

class InspectorMixin(object):
  """Provide dict-like interface to db.Model subclasses."""

  def __getitem__(self, key):
    """Expose object attributes like dict values."""
    return getattr(self, key)

  def keys(self):
    """Identify what db columns we have."""
    return inspect(self).attrs.keys()
