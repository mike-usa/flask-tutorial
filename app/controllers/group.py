from datetime import datetime as dt
import re

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.group import Group, db


def index():
  """Show all groups."""

  if {'group','groupname'} & set(request.args):
    groupname = get_groupname_from_querystring()
    group = get_group_from_querystring()
    if group:
      return redirect(url_for('group_blueprint.update',group=group.group))
    else:
      return create(group=groupname)

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
      return group.serializer()
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
    groupname = get_groupname_from_querystring()

  if not groupname:
    session['messages'].append({'error': 'Could not find group to create'})
    return redirect(url_for('home_blueprint.index'))

  # ensure no group exists
  existing_group = Group.query.filter(
      Group.groupname == groupname
  ).first()

  if existing_group:
    return redirect(url_for('group_blueprint.show',groupname=groupname))

  # Create an instance of the Group class of required fields
  new_group = Group(
    group=groupname,
    owner=request.args.get('owner'),
    created=dt.now(),
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
    exclude_fields = ['group', 'groupname', 'created', 'updated', 'modified']

    if column.lower() in exclude_fields and group.__dict__[column] != value:
      session['messages'].append(
          {'error': f'Cannot update protected table field ({arg}).'})
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
      members = User.query.filter(User.id.in_(values)).all()
      group.members.extend(members)  # extend() multiple, not append() single
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


########################################


def get_groupname_from_querystring():
  for key in ['group', 'groupname']:
    if key in request.args:
      groupname = request.args[key]  # request.args.get(key)

  return groupname if groupname else None


def get_group_from_querystring():
  groupname = get_groupname_from_querystring()

  return Group.query.filter(Group.group == groupname).first()
