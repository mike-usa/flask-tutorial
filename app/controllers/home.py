"""Home Controller"""

# Standard library imports
# --- None ---

# Third party imports
from flask import render_template, g

# Local application imports
# --- None ---


# Controller Actions

def index():
  """Display the homepage."""

  return render_template(
      'home.jinja2',
      title='Home',
      hide_container=True,
      messages=g.messages
  )
