from flask import Blueprint, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from hwut_server.models import Boards, Microcontrollers
from hwut_server.decorators import requires_authentication, requires_superuser
from hwut_server.utils import extended_and_authorized
from hwut_server.database import db

mod = Blueprint('targets', __name__, url_prefix='/targets')


@mod.route('/boards', methods=['GET'])
def targets_boards():
    extended = extended_and_authorized(request)
    return jsonify([b.to_dict(extended=extended) for b in Boards.query.all()])


@mod.route('/boards/<string:board_name>', methods=['GET'])
def targets_boards_get(board_name):
    extended = extended_and_authorized(request)
    try:
        return jsonify(Boards.query.filter(Boards.name == board_name).one().to_dict(extended=extended))
    except:
        abort(404)


@mod.route('/boards/<string:board_name>', methods=['PUT'])
@requires_authentication
def targets_boards_create(board_name):
    microcontroller = request.args.get('microcontroller')
    if Microcontrollers.query.filter(Microcontrollers.name == microcontroller).count() != 1:
        return abort(400, 'Microcontroller not found. Please create the microcontroller first.')
    manufacturer = request.args.get('manufacturer')
    board = Boards(board_name, microcontroller)
    if manufacturer:
        board.manufacturer = manufacturer
    try:
        db.session.add(board)
        db.session.commit()
    except:
        return redirect(request.path, 303)
    return targets_boards_get(board_name), 201


@mod.route('/boards/<string:board_name>', methods=['DELETE'])
@requires_superuser
def targets_boards_delete(board_name):
    try:
        board = Boards.query.filter(Boards.name == board_name).one()
        db.session.delete(board)
        db.session.commit()
        return '', 204
    except MultipleResultsFound:
        abort(500, 'board exists multiple time in database')
    except NoResultFound:
        abort(410, 'board does not exist')


@mod.route('/microcontrollers', methods=['GET'])
def targets_microcontrollers():
    extended = extended_and_authorized(request)
    return jsonify([m.to_dict(extended=extended) for m in Microcontrollers.query.all()])


@mod.route('/microcontrollers/<string:microcontroller_name>', methods=['GET'])
def targets_microcontrollers_get(microcontroller_name):
    try:
        return jsonify(
            Microcontrollers.query.filter(Microcontrollers.name == microcontroller_name).one().to_dict(extended=True))
    except:
        abort(404)


@mod.route('/microcontrollers/<string:microcontroller_name>', methods=['PUT'])
@requires_authentication
def targets_microcontrollers_create(microcontroller_name):
    microcontroller = Microcontrollers(microcontroller_name)
    manufacturer = request.args.get('manufacturer')
    if manufacturer:
        microcontroller.manufacturer = manufacturer
    try:
        db.session.add(microcontroller)
        db.session.commit()
    except:
        return redirect(request.path, 303)
    return targets_microcontrollers_get(microcontroller_name), 201


@mod.route('/microcontrollers/<string:microcontroller_name>', methods=['DELETE'])
@requires_superuser
def targets_microcontrollers_delete(microcontroller_name):
    try:
        microcontroller = Microcontrollers.query.filter(Microcontrollers.name == microcontroller_name).one()
        db.session.delete(microcontroller)
        db.session.commit()
        return '', 204
    except MultipleResultsFound:
        abort(500, 'microcontroller exists multiple time in database')
    except NoResultFound:
        abort(410, 'microcontroller does not exist')
