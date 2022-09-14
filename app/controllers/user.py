"""User Controller"""

# Standard library imports
from datetime import datetime, timezone
import re

# Third party imports
from flask import redirect, render_template, g, request, session, url_for
from sqlalchemy import or_

# Local application imports
from app.models.user import User, db


# Controller Actions

def index():
  """Show all users."""

  if {'user','username'} & set(request.args):
    username = __get_username_from_querystring()
    user = __get_user_from_querystring()
    if user:
      return redirect(url_for('user_blueprint.update',username=user.username))
    else:
      return create(username=username)

  return render_template(
    "users.jinja2",
    users=User.query.order_by(User.username).all(),
    title="Show Users",
    messages=g.messages
  )


def show(username=None,user=None):
  """Show a specific user."""

  if not user:
    user = User.query.filter(User.username==username).first_or_404(description='No "{}" user was found.'.format(username))

  if request.args:
    if 'response' in request.args and request.args['response'] == 'json':
      return user.serialize()
    else:
      return update(username=username, user=user)

  return render_template(
    "users.jinja2",
    users=[user], # shares a view with the index
    title="Show User",
    page_title=user.username,
    messages=g.messages
  )


def new():
  pass


def create(username=None):
  """Create a new user"""

  if not username:
    username = __get_username_from_querystring()

  if not username:
    session['messages'].append({'error': 'Could not find a user to create'})
    return redirect(url_for('home_blueprint.index'))

  # ensure no user exists
  existing_user = User.query.filter(
      User.username == username
  ).first()

  if existing_user:
    return redirect(url_for('user_blueprint.show', username=username))

  # Create an instance of the User class of required fields
  new_user = User(
    username=username,
    email=request.args.get('email'),
    created_at=datetime.now(timezone.utc),
    admin=bool(
        request.args.get("admin")
      ) if 'admin' in request.args else False
  )

  try:
    # Adds new User record to database
    db.session.add(new_user)
    # Commits all changes
    db.session.commit()
    session['messages'] = [{'success': 'User successfully created'}]
    return redirect(url_for('user_blueprint.show', username=username))
  except Exception as e:
    db.session.rollback()
    db.session.flush()
    session['messages'].append({'error': f'Could not create user {username}'})
    session['messages'].append({'error': f'{e}'})
    return redirect(url_for('user_blueprint.index'))


def edit():
  pass


def update(username=None, user=None):
  tainted = False
  def redirect_home():
    return redirect(url_for('user_blueprint.show', username=username)) # user.username

  if not user:
    user = User.query.filter(User.username == username).first_or_404(
          description=f'No "{username}" user was found.'
    )
    if not user:
      session['messages'].append({'error': 'Could not find user to update'})
      redirect_home()

  # convert 'user' key to 'username'
  table_columns = set(user.__table__.columns.keys())
  relationships = user.__mapper__.relationships.keys()
  aliases = { 'user': 'username' }
  rel_aliases = { 
    'belongsto': 'groups',
    'member': 'groups',
    'memberof': 'groups',
    'group': 'groups',
    'owner': 'owns',
    'own': 'owns',
    'maintainer': 'maintains',
    'maintain': 'maintains',
  }

  column_args = []
  relationship_args = []
  unrecognized_args = []
  for key in request.args:
    if key in table_columns or key in aliases:
      column_args.append(key)
    elif key in relationships or key in rel_aliases:
      relationship_args.append(key)
    else:
      unrecognized_args.append(key)


  # Update db fields
  for arg in column_args:
    column = aliases[arg] if arg in aliases else arg
    value = request.args.get(arg)

    # Don't process protected fields
    exclude_fields = ['user', 'username', 'created_at','created_by', 'updated_at','updated_by', 'modified']

    if column.lower() in exclude_fields and user.__dict__[column] != value:
      session['messages'].append({'error': f'Cannot update protected table field ({arg}).'})
      return redirect_home()

    type = user.__table__.columns[column].type.__class__.__name__
    if type == 'Boolean':
      value = value.lower() in ['true','1','yes']
    setattr(user, column, value)
    tainted = True

  # Update joined fields
  for arg in relationship_args:
    value = request.args.get(arg)
    values = list(filter(None,re.split('\s*,\s*', value)))
    relationship = rel_aliases[arg] if arg in rel_aliases else arg

    if relationship in ['groups','owns','maintains']:
      from app.models.group import Group
      # must pass object (can't pass id's)
      if values and value not in ['[]','None']:
        vals = {
          'add': {
            'strings': [],
            'integers': []
          },
          'remove': {
            'strings': [],
            'integers': []
          }
        }
        for v in values:
          if v.lstrip('-').isdigit():
            v = int(v)
            if v >= 0:
              vals['add']['integers'].append(v)
            else:
              vals['remove']['integers'].append(abs(v))
          elif isinstance(v, str):
            if v[0] != '-':
              vals['add']['strings'].append(v)
            else:
              vals['remove']['strings'].append(v.lstrip('-'))

        # Adds
        add_groups = Group.query.filter(
          or_(
            Group.id.in_(vals['add']['integers']),
            Group.group.in_(vals['add']['strings'])
          )
        ).all()
        # NOTE; extend() == multiple; append() == single
        getattr(user, relationship).extend(add_groups)

        # Removes
        rem_groups = Group.query.filter(
          or_(
            Group.id.in_(vals['remove']['integers']),
            Group.group.in_(vals['remove']['strings'])
          )
        ).all()
        for group in rem_groups:
          getattr(user, relationship).remove(group)

        tainted = True
      else:
        # groups = Group.query.where(None).all()
        setattr(user, relationship, [])
        tainted = True
    else:
      setattr(user, relationship, value)
      tainted  = True

  if tainted:
    try:
      value = db.session.commit()
      # session['messages'].append({'info': f'Commit value: {value}'})
      session['messages'].append({'success': f'Successfully updated user {username}'})
    except Exception as e:
      db.session.rollback()
      db.session.flush()
      session['messages'].append({'error': f'Error encountered updating {username}; {e}'})
  else:
    session['messages'].append({'info': 'No changes made to user record.'})

  # Clear query string
  return redirect(url_for('user_blueprint.show',username=username))


def delete():
  pass


# Private Functions

def __get_username_from_querystring():
  for key in ['user','username']:
    if key in request.args:
      username = request.args[key] #request.args.get(key)

  return username if username else None


def __get_user_from_querystring():
  username = __get_username_from_querystring()

  return User.query.filter(User.username == username).first()
