from werkzeug.exceptions import abort

from hwut_server.decorators import check_authentication

FILE_STORAGE = './file_storage'


def extended_and_authorized(request):
    if request.args.get('extended') == '1':
        auth = request.authorization
        if not auth:
            return abort(401)
        if check_authentication(auth.username, auth.password):
            return True
        else:
            return abort(403)
    else:
        return False
