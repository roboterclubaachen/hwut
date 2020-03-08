import os

from flask import Flask

from hwut_server.api import register as register_api
from hwut_server.runner_api import register as register_runner_api


class HwutServer(Flask):
    def __init__(self, name='hwut_server', config_file=None, *args, **kw):
        # Create Flask instance
        super(HwutServer, self).__init__(name, *args, **kw)

        # Load default settings and from environment variable
        #self.config.from_pyfile(config.DEFAULT_CONF_PATH)
        #
        #if 'HWUT_CONFIG' in os.environ:
        #    self.config.from_pyfile(os.environ['HWUT_CONFIG'])
        #
        if config_file:
            self.config.from_pyfile(config_file)

        register_api(self)
        register_runner_api(self)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from hwut_server.database import db
        db.init_app(self)


def create_app(*args, **kw):
    app = HwutServer(*args, **kw)
    app.add_sqlalchemy()
    return app
