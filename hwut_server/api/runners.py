from flask import Blueprint, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from hwut_server.models import Boards, Microcontrollers, Runners
from hwut_server.decorators import requires_authentication, requires_superuser, check_authentication
from hwut_server.database import db
from hwut_server.utils import extended_and_authorized

mod = Blueprint('runners', __name__, url_prefix='/runners')


@mod.route('/*', methods=['GET'], defaults={'filter_type': 'any', 'filter1': None, 'filter2': None})
@mod.route('/<string:filter_type>/<string:filter1>', methods=['GET'], defaults={'filter2': None})
@mod.route('/<string:filter_type>/<string:filter1>/<string:filter2>', methods=['GET'])
def runners_list(filter_type, filter1, filter2):
    runner_list = list()
    if filter_type == 'any':
        runner_list = Runners.query.all()
    elif (filter_type == 'by_board') and (filter1 is not None) and (filter2 is None):
        runner_list = Runners.query.filter(Runners.target_board == filter1).all()
    elif (filter_type == 'by_microcontroller') and (filter1 is not None) and (filter2 is None):
        runner_list = Runners.query.filter(Runners.target_microcontroller == filter1).all()
    elif (filter_type == 'by_board_and_microcontroller') and (filter1 is not None) and (filter2 is not None):
        runner_list = Runners.query.filter(Runners.target_microcontroller == filter1) \
            .filter(Runners.target_board == filter1).all()
    else:
        abort(400)

    extended = extended_and_authorized(request)
    return jsonify([r.to_dict(extended=extended) for r in runner_list])


@mod.route('/<int:id>', methods=['GET'])
def targets_boards_get(id):
    try:
        runner = Runners.query.filter(Runners.id == id).one()
        auth = request.authorization
        if auth and (
                (check_authentication(auth.username, auth.password, superuser=True))
                or (check_authentication(auth.username, auth.password) and auth.username == runner.owner)):
            return jsonify(runner.to_dict(extended=True))
        else:
            return jsonify(runner.to_dict())
    except:
        abort(404)


@mod.route('/add', methods=['PUT'])
@requires_authentication
def runner_create():
    if (request.args.get('board') is None) or (request.args.get('microcontroller') is None):
        abort(400)

    user = request.authorization.username
    try:
        board = Boards.query.filter(Boards.name == request.args.get('board')).one()
    except NoResultFound:
        abort(410, 'board "{}" does not exist'.format(request.args.get('board')))
        return
    try:
        microcontroller = Microcontrollers.query\
            .filter(Microcontrollers.name == request.args.get('microcontroller')).one()
    except NoResultFound:
        abort(410, 'microcontroller does not exist')
        return
    try:
        runner = Runners(user, board.name, microcontroller.name)
        db.session.add(runner)
        db.session.commit()
    except:
        abort(500, 'unable to create runner')
        return
    return redirect(mod.url_prefix + '/' + str(runner.id), 201)


@mod.route('/<int:id>', methods=['DELETE'])
@requires_superuser
def runner_delete(id):
    try:
        runner = Runners.query.filter(Runners.id == id).one()
        db.session.delete(runner)
        db.session.commit()
        return '', 204
    except MultipleResultsFound:
        abort(500, 'runner exists multiple time in database')
    except NoResultFound:
        abort(410, 'runner does not exist')