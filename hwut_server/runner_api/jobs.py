from flask import Blueprint, jsonify, request

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from werkzeug.exceptions import abort
from hwut_server.database import db
from hwut_server.decorators import requires_authentication


mod = Blueprint('jobs', __name__)


@mod.route('/get', methods=['GET'])
@requires_authentication
def job_get():
    """
    Get a new job
    """
    # TODO ...
    return jsonify(None)
