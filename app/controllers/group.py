from datetime import datetime as dt

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.group import Group, db


def index():
  """Show all groups."""
  return render_template(
    "groups.jinja2",
    groups=Group.query.order_by(Group.group).all(),
    title="Show Groups",
    messages=g.messages
  )


def show(groupname=None):
  """Create a user via query string parameters."""
  group = Group.query.filter(Group.group==groupname).first_or_404(description='No "{}" group found'.format(groupname))

  # if args:
  #   updates['description] = args.description if 'description' in args else None
  #   description = args.description if 'description' in args else None

  #sqlalchemy.sql.schema.Column
  # col=Group.__table__.columns[0]
  # print(Group.__table__.columns)
  # print(col.c)

  return render_template(
    "groups.jinja2",
    groups=[group],
    title="Show Group",
    page_title=group.group,
    messages=g.messages,
    columns=Group.__table__.columns
  )

def new():
  pass

def create():
  # email = request.args.get("email")
  # admin = bool(request.args.get("admin")) if 'admin' in request.args else False

  # existing_user = User.query.filter(
  #     User.username == id
  # ).first()

  # if existing_user:
  #   return render_template('users.jinja2', users=[existing_user], title=username, page_title=username, messages=g.messages)

  # # Create an instance of the User class
  # new_user = User(
  #     username=id,
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
