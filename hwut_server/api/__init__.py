from hwut_server.api.execute import mod as mod_execute
from hwut_server.api.about import mod as mod_about

def register(app):
    """
    :param flask.Flask app: a Flask app
    """

    app.register_blueprint(mod_execute)
    app.register_blueprint(mod_about)
