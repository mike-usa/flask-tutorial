"""Group Controller"""

# Standard library imports
from datetime import datetime as dt
import re

# Third party imports
from flask import redirect, render_template, g, request, session, url_for
from sqlalchemy import or_

# Local application imports
from app.models.group import Group, db


# Controller Actions

def index():
  """Show all groups."""

  if {'group','groupname'} & set(request.args):
    groupname = __get_groupname_from_querystring()
    group = __get_group_from_querystring()
    if group:
      return redirect(url_for('group_blueprint.update',group=group.group))
    else:
      return create(groupname=groupname)

  return render_template(
    "groups.jinja2",
    groups=Group.query.order_by(Group.group).all(),
    title="Show Groups",
    messages=g.messages
  )


def show(groupname=None,group=None):
  """Show a specific group."""
  if not group:
    group = Group.query.filter(Group.group==groupname).first_or_404(description='No "{}" group found'.format(groupname))
  # print(f'group {group.group}: [owner]={group.owner.username}')
  if request.args:
    if 'response' in request.args and request.args['response'] == 'json':
      return group.serialize()
    else:
      return update(groupname=groupname, group=group)

  return render_template(
    "groups.jinja2",
    groups=[group], # shares a view with the index
    title="Show Group",
    page_title=group.group,
    messages=g.messages
  )


def new():
  pass


def create(groupname=None):
  """Create a new group."""
  if not groupname:
    groupname = __get_groupname_from_querystring()

  if not groupname:
    session['messages'].append({'error': 'Could not find group to create'})
    return redirect(url_for('home_blueprint.index'))

  # ensure no group exists
  existing_group = Group.query.filter(
      Group.group == groupname
  ).first()

  if existing_group:
    return redirect(url_for('group_blueprint.show',groupname=groupname))

  # Create an instance of the Group class of required fields
  new_group = Group(
    group=groupname,
    created_at=dt.now(),
    is_security=bool(
      request.args.get('is_security')
    ) if 'is_security' in request.args else False
  )

  try:
    db.session.add(new_group)
    db.session.commit()
    session['messages'] = [{'success': 'Group successfully created'}]
    return redirect(url_for('group_blueprint.show'), groupname=groupname)
  except Exception as e:
    db.session.rollback()
    db.session.flush()
    session['messages'].append({'error': f'Could not create group {groupname}'})
    session['messages'].append({'error': f'{e}'})
    return redirect(url_for('group_blueprint.index'))


def edit():
  pass


def update(groupname=None, group=None):
  tainted = False
  def redirect_home():
    return redirect(url_for('group_blueprint.show', groupname=groupname))

  if not group:
    group = Group.query.filter(Group.group == groupname).first_or_404(
        description=f'No "{groupname}" group was found.'
    )
    if not group:
      session['messages'].append({'error': 'Could not find group to update'})
      redirect_home()

  # convert 'groupname' key to 'group'
  table_columns = set(Group.__table__.columns.keys())
  relationships = Group.__mapper__.relationships.keys()
  aliases = { 'groupname': 'group' }
  rel_aliases = {
    'users': 'members',
    'user': 'members',
    'member': 'members',
    'owner': 'owners',
    'owned_by': 'owners',
    'maintainer': 'maintainers',
    'maintained_by': 'maintainers',
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
    exclude_fields = ['group', 'groupname', 'created_at','created_by', 'updated_at','updated_by', 'modified']

    if column.lower() in exclude_fields and group.__dict__[column] != value:
      session['messages'].append(
        {'error': f'Cannot update protected table field ({arg}).'}
      )
      return redirect_home()

    type = group.__table__.columns[column].type.__class__.__name__
    if type == 'Boolean':
      value = value.lower() in ['true', '1', 'yes']
    setattr(group, column, value)
    tainted = True

  # Update joined fields
  for arg in relationship_args:
    value = request.args.get(arg)
    values = re.split('\s*,\s*', value)
    relationship = rel_aliases[arg] if arg in rel_aliases else arg

    if relationship in ['members', 'owners', 'maintainers']:
      from app.models.user import User
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
        add_members = User.query.filter(
          or_(
            User.id.in_(vals['add']['integers']),
            User.username.in_(vals['add']['strings'])
          )
        ).all()
        # NOTE: extend() == multiple; append() == single
        getattr(group, relationship).extend(add_members)

        # Removes
        rem_members = User.query.filter(
          or_(
            User.id.in_(vals['remove']['integers']),
            User.username.in_(vals['remove']['strings'])
          )
        ).all()
        for member in rem_members:
          getattr(group, relationship).remove(member)

        tainted = True
      else:
        # members = User.query.where(None).all()
        setattr(group, relationship, [])
        tainted = True
    else:
      setattr(group, relationship, value)
      tainted = True

  if tainted:
    try:
      value = db.session.commit()
      # session['messages'].append({'info': f'Commit value: {value}'})
      session['messages'].append({'success': f'Successfully updated group {groupname}'})
    except Exception as e:
      db.session.rollback()
      db.session.flush()
      session['messages'].append({'error': f'Error encountered updating {groupname}; {e}'})
  else:
    session['messages'].append({'info': 'No changes made to group record.'})

  # Clear query string
  return redirect(url_for('group_blueprint.show', groupname=groupname))


def delete():
  pass


# Private Functions


def __get_groupname_from_querystring():
  for key in ['group', 'groupname']:
    if key in request.args:
      groupname = request.args[key]  # request.args.get(key)

  return groupname if groupname else None


def __get_group_from_querystring():
  groupname = __get_groupname_from_querystring()

  return Group.query.filter(Group.group == groupname).first()
