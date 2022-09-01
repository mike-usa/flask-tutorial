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
    return redirect(url_for('home_page'))