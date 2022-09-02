from datetime import datetime as dt

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.user import User, db


def index():
  """Show all users."""
  return render_template(
    "users.jinja2",
    users=User.query.order_by(User.username).all(),
    title="Show Users",
    messages=g.messages
  )


def show(username=None):
  """Show a specific user."""
  user = User.query.filter(User.username==username).first_or_404(description='No "{}" user was found.'.format(username))
  return render_template(
    "users.jinja2",
    users=[user], # shares a view with the index
    title="Show User",
    page_title=user.username,
    messages=g.messages
  )


def new():
  pass

def create():
  # username = request.args.get("user") if 'user' in request.args else ''
  # email = request.args.get("email")
  # admin = bool(request.args.get("admin")) if 'admin' in request.args else False

  # if username:
  #     existing_user = User.query.filter(
  #         User.username == username
  #     ).first()

  #     if existing_user:
  #         return render_template('users.jinja2', users=[existing_user], title=username, page_title=username, messages=g.messages)

  #     # Create an instance of the User class
  #     new_user = User(
  #         username=username,
  #         email=email,
  #         created=dt.now(),
  #         admin=admin,
  #     )

  #     # Adds new User record to database
  #     db.session.add(new_user)

  #     # Commits all changes
  #     db.session.commit()

  #     session['messages'] = [{'success': 'User successfully created'}]

  #     # Change url (drop querystring)
  #     return redirect(url_for("user_records"))
  # email = request.args.get("email")
  # admin = bool(request.args.get("admin")) if 'admin' in request.args else False

  # existing_user = User.query.filter(
  #     User.username == username
  # ).first()

  # if existing_user:
  #   return render_template('users.jinja2', users=[existing_user], title=username, page_title=username, messages=g.messages)

  # # Create an instance of the User class
  # new_user = User(
  #     username=username,
  #     email=email,
  #     created=dt.now(),
  #     admin=admin,
  # )

  # # Adds new User record to database
  # db.session.add(new_user)

  # # Commits all changes
  # db.session.commit()

  # session['messages'] = [{'success': 'User successfully created'}]

  # # Change url (drop querystring)
  # return redirect(url_for("user_records"))
  pass

def edit():
  pass

def update():
  pass

def delete():
  pass
