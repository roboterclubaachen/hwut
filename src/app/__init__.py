import os
from flask import Flask, jsonify

app = Flask(__name__)

# import and register execute class
from .execute import mod as execute_mod

# TODO: central error handlers
@app.errorhandler(400)
def not_found(error):
    return jsonify({
        'status': 'Bad Request',
        'error': error.description
    }), 400


@app.errorhandler(401)
def not_found(error):
    return jsonify({
        'status': 'Unauthorized',
        'error': error.description
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'Not found',
        'error': error.description
    }), 404


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'status': 'Method Not Allowed',
        'error': error.description
    }), 405


@app.errorhandler(409)
def not_found(error):
    return jsonify({
        'status': 'Conflict',
        'error': error.description
    }), 409


@app.errorhandler(500)
def not_found(error):
    return jsonify({
        'status': 'Internal error',
        'error': error.description
    }), 500


app.register_blueprint(execute_mod)
