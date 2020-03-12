import os

from flask import Flask

from hwut_server.api import register as register_api
from hwut_server.runner_api import register as register_runner_api
from hwut_server.errorhandler import register as register_errorhandler

class HwutServer(Flask):
    def __init__(self, name='hwut_server', config_file=None, *args, **kw):
        # Create Flask instance
        super(HwutServer, self).__init__(name, *args, **kw)

        if config_file:
            print('Loading config from file: config_file = {}'.format(config_file))
            self.config.from_pyfile(config_file)
        elif 'HWUT_CONFIG' in os.environ:
            print('Loading config from env: HWUT_CONFIG = {}'.format(os.environ['HWUT_CONFIG']))
            self.config.from_pyfile(os.environ['HWUT_CONFIG'])
        else:
            print('No config found. Exit.')
            exit(1)

        register_api(self)
        register_runner_api(self)
        register_errorhandler(self)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from hwut_server.database import db
        db.init_app(self)


def create_app(*args, **kw):
    app = HwutServer(*args, **kw)
    app.add_sqlalchemy()
    return app
