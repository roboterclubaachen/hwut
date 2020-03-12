from functools import wraps

from flask import request
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.exceptions import abort

from hwut_server.models import Runners, Users


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


def requires_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return abort(401)
        if not check_authentication(auth.username, auth.password):
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


def requires_superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return abort(401)
        if not check_authentication(auth.username, auth.password, superuser=True):
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


def check_runner_authentication(username, password):
    try:
        runner = Runners.query.filter_by(id=username).one()
        if runner.token == password and runner.enabled:
            return True
        else:
            return False
    except NoResultFound:
        return False


def requires_runner_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_runner_authentication(auth.username, auth.password):
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function
