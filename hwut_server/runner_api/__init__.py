from hwut_server.runner_api.jobs import mod as mod_jobs


def register(app):
    """
    :param flask.Flask app: a Flask app
    """

    app.register_blueprint(mod_jobs)
