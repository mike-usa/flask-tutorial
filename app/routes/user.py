"""User routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.user import User, db


@app.route("/users", strict_slashes=False, methods=["GET"])
@app.route("/users/<string:username>", strict_slashes=False, methods=["GET"])
def user_records(username=None):
    """Create a user via query string parameters."""
    username = request.args.get("user") if username == None else username
    email = request.args.get("email")
    admin = bool(request.args.get("admin")) if 'admin' in request.args else False
    if username:
        existing_user = User.query.filter(
            User.username == username
        ).first()

        if existing_user:
            return render_template('users.jinja2', users=[existing_user], title=username, page_title=username, messages=g.messages)
        
        # Create an instance of the User class
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            admin=admin,
        )
        
        # Adds new User record to database
        db.session.add(new_user)
        
        # Commits all changes
        db.session.commit()

        session['messages']=[{'success': 'User successfully created'}]
        
        # Change url (drop querystring)
        return redirect(url_for("user_records"))

    return render_template("users.jinja2", users=User.query.all(), title="Show Users", messages=g.messages)
