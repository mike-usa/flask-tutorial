"""Home routes."""

# Standard library imports
# --- None ---

# Third party imports
from flask import Blueprint

# Local application imports
from ..controllers.home import *  # controller actions


bp = Blueprint('home', __name__)

bp.route('/', methods=['GET'])(index)
bp.route('/home', methods=['GET'])(index)


