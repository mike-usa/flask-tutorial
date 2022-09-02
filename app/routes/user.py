"""User routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import redirect, render_template, g, request, session, url_for

from app.models.user import User, db

from flask import Blueprint
bp = Blueprint('user_blueprint',
     __name__,
     url_prefix='/users'
)

from ..controllers.user import *
bp.route('/', methods=['GET'])(index)
bp.route('/<string:username>', methods=['GET'])(show)
bp.route('/<string:username>/new', methods=['GET'])(new)
bp.route('/<string:username>/edit', methods=['GET'])(edit)
bp.route('/<string:username>', methods=['POST'])(update)
bp.route('/<string:username>', methods=['DELETE'])(delete)