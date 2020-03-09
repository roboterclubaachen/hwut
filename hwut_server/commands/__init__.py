import sys

from flask_script import Manager

from .shell import Shell
from .server import Server

from .database import manager as database_manager


from hwut_server.app import create_app
from config import to_envvar


def _create_app(config):
    if not to_envvar(config):
        print('Config file "{}" not found.'.format(config))
        sys.exit(1)

    return create_app()


manager = Manager(_create_app)

manager.add_option('-c', '--config', dest='config', required=False)

manager.add_command("shell", Shell())
manager.add_command("runserver", Server())
manager.add_command("db", database_manager)
