from flask import render_template, g

def index():
  """Create a homepage."""
  return render_template(
      'home.jinja2',
      title='Home',
      hide_container=True,
      messages=g.messages
  )
