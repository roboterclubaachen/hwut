import os
from flask import Flask

app = Flask(__name__)

# import and register execute class
from .execute import mod as execute_mod

app.register_blueprint(execute_mod)
