from flask import Blueprint, jsonify

from hwut_server.decorators import requires_authentication

mod = Blueprint('runner_jobs', __name__)


@mod.route('/get', methods=['GET'])
@requires_authentication
def job_get():
    """
    Get a new job
    """
    # TODO ...
    return jsonify(None)
