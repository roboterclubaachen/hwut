from hwut_server.api.about import mod as mod_about
from hwut_server.api.execute import mod as mod_execute
from hwut_server.api.runners import mod as mod_runners
from hwut_server.api.targets import mod as mod_targets


def register(app):
    """
    :param flask.Flask app: a Flask app
    """

    app.register_blueprint(mod_about)
    app.register_blueprint(mod_execute)
    app.register_blueprint(mod_runners)
    app.register_blueprint(mod_targets)
