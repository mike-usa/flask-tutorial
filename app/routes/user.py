"""User routes."""

# Standard library imports
# --- None ---

# Third party imports
from flask import Blueprint
from flask_cors import CORS

# Local application imports
from ..controllers.user import *  # controller actions


bp = Blueprint('user_blueprint',
     __name__,
     url_prefix='/users'
)
CORS(bp) # enable CORS on the user_blueprint

bp.route('/', methods=['GET'])(index)
bp.route('/<string:username>', methods=['GET'])(show)
bp.route('/<string:username>/new', methods=['GET'])(new)
bp.route('/<string:username>/edit', methods=['GET'])(edit)
bp.route('/<string:username>', methods=['POST'])(update)
bp.route('/<string:username>', methods=['DELETE'])(delete)