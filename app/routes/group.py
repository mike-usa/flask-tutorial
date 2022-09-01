"""Group routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.group import Group, db


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
