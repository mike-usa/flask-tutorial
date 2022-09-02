# This file is special in that it imports (integrates) all
# the routes in the directory intended to be exposed through
# the application.  This import could be automated to not
# specify the files with some complex loading code
#
# The file also services as a pre-processor with `before_request`
# as well as a catch-all for bad routes


from flask import current_app as app
from flask import g, session, url_for, redirect

# load all routes
from . import home
from . import user
from . import group

# initialize global
g.messages = []

# applied to every route
@app.before_request
def set_messages():
    g.messages = session['messages'] if 'messages' in session else []
    session['messages'] = []  # clear after capturing for display
    g.active = True


@app.route('/<path:path>')
def catch_all(path):
    messages = [{'error': 'Route not found'}]
    session['messages'] = messages
    return redirect(url_for('home.index'))


# Registers Blueprint with App
# needed all to reference action in url_for (e.g., `url_for('home.index')`)
app.register_blueprint(home.bp)
app.register_blueprint(user.bp)
app.register_blueprint(group.bp)