"""Group routes."""
# from app.models.group import Group, db

from flask import Blueprint
bp = Blueprint('group_blueprint',
     __name__,
     url_prefix='/groups'
)

from ..controllers.group import *
bp.route('/', methods=['GET'])(index)
bp.route('/<string:groupname>', methods=['GET'])(show)
bp.route('/<string:groupname>/new', methods=['GET'])(new)
bp.route('/<string:groupname>/edit', methods=['GET'])(edit)
bp.route('/<string:groupname>', methods=['POST'])(update)
bp.route('/<string:groupname>', methods=['DELETE'])(delete)