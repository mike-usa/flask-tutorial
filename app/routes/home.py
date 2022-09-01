"""Application routes."""
from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    hide_container = True
    return render_template(
        'home.jinja2',
        title='Home',
        hide_container=hide_container,
        messages=g.messages
    )