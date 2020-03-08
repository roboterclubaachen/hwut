from functools import wraps
from flask import request, jsonify, Response
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.exceptions import abort

from hwut_server.models.users import Users


def check_authentication(username, password, superuser=False):
    """This function is called to check if a username /
    password combination is valid.
    :param password: Username
    :param username: Password
    :param superuser: additionally check if user is superuser
    """
    try:
        user = Users.query.filter_by(name=username).one()
        if superuser:
            return user.verify_password(password) and user.is_superuser()
        else:
            return user.verify_password(password)
    except MultipleResultsFound:
        abort(500, 'Multiple user with name \'' + username + '\' found.')
    except NoResultFound:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        jsonify({
            'status': 'Unauthorized',
            'error': 'Please authenticate using HTTP Basic Auth (realm=\'HWUT\')'
        }),
        401,
        {'WWW-Authenticate': 'Basic realm="HWUT"'}
    )


def requires_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authentication(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated_function


def requires_superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authentication(auth.username, auth.password, True):
            return authenticate()
        return f(*args, **kwargs)
    return decorated_function
