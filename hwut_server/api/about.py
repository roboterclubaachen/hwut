from flask import Blueprint, jsonify

from hwut_server.__about__ import git_hash, git_branch, __version__

mod = Blueprint('about', __name__)


@mod.route('/version', methods=['GET'])
def version():
    """
    Show version information
    """
    version_info = {
        'version': __version__,
        'git_hash': git_hash,
        'git_branch': git_branch,
    }
    return jsonify(version_info)
