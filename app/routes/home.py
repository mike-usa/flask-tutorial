"""Home routes."""
from flask import Blueprint
bp = Blueprint('home', __name__)

from ..controllers.home import *
bp.route('/', methods=['GET'])(index)
bp.route('/home', methods=['GET'])(index)


