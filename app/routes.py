"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models.user import User, db
from .models.group import Group, db


@app.route("/", methods=["GET"])
def home_page():
    return render_template('home.jinja2', title='Home', hide_container=True)


@app.route("/users", methods=["GET"])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get("user")
    email = request.args.get("email")
    admin = bool(request.args.get("admin")) if 'admin' in request.args else False
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(f"{username} ({email}) already created!")
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=admin,
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for("user_records"))
    return render_template("users.jinja2", users=User.query.all(), title="Show Users")


@app.route("/groups", methods=["GET"])
def group_records():
    """Create a group via query string parameters."""
    group = request.args.get('group')
    description = request.args.get('description')
    is_security = bool(request.args.get('is_security')) if 'is_security' in request.args else False

    if group:
        existing_group = Group.query.filter(
            Group.group == group
        ).first()
        if existing_group:
            return make_response(f"{group} already created!")
        new_group = Group(
            group=group,
            created=dt.now(),
            description=description,
            is_security=is_security,
        )  # Create an instance of the Group class
        db.session.add(new_group)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for("group_records"))
    return render_template("groups.jinja2", groups=Group.query.all(), title="Show Groups")
