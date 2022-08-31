"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, g, request, session, url_for

from .models.user import User, db
from .models.group import Group, db

g.messages = []

@app.before_request
def set_messages():
    g.messages = session['messages'] if 'messages' in session else []
    session['messages'] = []  # clear after capturing for display
    g.active = True


@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    hide_container = True
    return render_template(
        'home.jinja2',
        title='Home',
        hide_container=hide_container,
        messages=g.messages
    )


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


@app.route("/groups", strict_slashes=False, methods=["GET"])
@app.route("/groups/<string:group>", strict_slashes=False, methods=["GET"])
def group_records(group=None):
    """Create a group via query string parameters."""
    group = request.args.get('group') if group==None else group
    description = request.args.get('description')
    is_security = bool(request.args.get('is_security')) if 'is_security' in request.args else False

    if group:
        existing_group = Group.query.filter(
            Group.group == group
        ).first()
        if existing_group:
            return render_template('groups.jinja2', groups=[existing_group], title=group, page_title=group, messages=g.messages)
        
        # Create an instance of the Group class
        new_group = Group(
            group=group,
            created=dt.now(),
            description=description,
            is_security=is_security,
        )
        
        # Adds new User record to database
        db.session.add(new_group)
        
        # Commits all changes
        db.session.commit()

        session['messages']=[{'success': 'Group successfully created'}]

        # Change url (drop querystring)
        return redirect(url_for("group_records"))

    return render_template("groups.jinja2", groups=Group.query.all(), title="Show Groups", messages=g.messages)


@app.route('/<path:path>')
def catch_all(path):
    messages = [{'error': 'Route not found'}]
    session['messages'] = messages
    return redirect(url_for('home_page'))