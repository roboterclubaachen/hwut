from flask import jsonify, Response


def register(app):
    """
    Register error handlers on the given app
    :type app: flask.Flask
    """

    @app.errorhandler(400)
    def error_400(error):
        return jsonify({
            'status': 'Bad Request',
            'message': str(error),
        }), 400

    @app.errorhandler(401)
    def error_401(error):
        """Sends a 401 response that enables basic auth"""
        return Response(
            jsonify({
                'status': 'Unauthorized',
                'info': 'Please authenticate using HTTP Basic Auth (realm=\'HWUT\')',
                'message': str(error),
            }),
            401,
            {'WWW-Authenticate': 'Basic realm="HWUT"'}
        )

    @app.errorhandler(403)
    def error_403(error):
        return jsonify({
            'status': 'Forbidden',
            'message': str(error),
        }), 403

    @app.errorhandler(404)
    def error_404(error):
        return jsonify({
            'status': 'Not found',
            'message': str(error),
        }), 404

    @app.errorhandler(405)
    def error_405(error):
        return jsonify({
            'status': 'Method Not Allowed',
            'message': str(error),
        }), 405

    @app.errorhandler(409)
    def not_found(error):
        return jsonify({
            'status': 'Conflict',
            'message': str(error),
        }), 409

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 'Internal Server Error',
            'message': str(error),
        }), 500

    @app.errorhandler(501)
    def not_implemented(error):
        return jsonify({
            'status': 'Not Implemented',
            'message': str(error),
        }), 501

    @app.errorhandler(TypeError)
    @app.errorhandler(ValueError)
    def raise_type_value_error(error):
        return jsonify({
            'status': 'Not Implemented',
            'message': str(error),
        }), 400

    @app.errorhandler(LookupError)
    def raise_lookup_error(error):
        return jsonify({
            'status': 'Not Implemented',
            'message': str(error),
        }), 404
