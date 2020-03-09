from flask_script import Shell as BaseShell

from flask import current_app
from hwut_server import models, database


def make_context():
    return dict(app=current_app, model=models, db=database.db)


class Shell(BaseShell):
    def __init__(self, *args, **kw):
        super(Shell, self).__init__(make_context=make_context, *args, **kw)
