import os
from secrets import token_urlsafe

from flask import Blueprint, jsonify, request, abort
from sqlalchemy import and_, or_
from sqlalchemy.orm.exc import NoResultFound

from hwut_server.database import db
from hwut_server.decorators import requires_runner_authentication
from hwut_server.models import Jobs, JobStatus, Runners
from hwut_server.utils import FILE_STORAGE

mod = Blueprint('runner_jobs', __name__)


@mod.route('/get', methods=['GET'])
@requires_runner_authentication
def job_get():
    """
    Get a new job
    """
    runner = Runners.query.filter(id=request.authorization.username).one()

    # check if a job is already queued for the runner
    try:
        job = Jobs.query.filter(and_(Jobs.runner == runner.id, Jobs.status == JobStatus.QUEUED)).one()
    # Else queue a new job
    except NoResultFound:
        try:
            filters = list()
            filters.append(Jobs.status == JobStatus.WAITING)
            filters.append(Jobs.microcontroller == runner.microcontroller)
            filters.append(or_(Jobs.board == runner.board, Jobs.board == ''))
            job = Jobs.query.filter(and_(*filters)).order_by(Jobs.created.desc()).first()
        except NoResultFound:
            return '', 404
        except:
            return abort(500)

        runner.acquire()

        job.status = JobStatus.QUEUED
        job.runner = runner.id

    runner.ping()
    db.session.commit()

    return jsonify({
        'id': job.id,
        'executable_location': request.url_root + 'executable',
        'log_location': request.url_root + 'log',
        'other_location': request.url_root + 'other',
        'time_limit': job.duration_limit_seconds,
        'baudrate': 115200,  # FIXME
    })


@mod.route('/executable', methods=['GET'])
@requires_runner_authentication
def job_get_executable():
    runner_id = request.authorization.username
    try:
        job = Jobs.query.filter(and_(Jobs.runner == runner_id, Jobs.status == JobStatus.RUNNING)).one()
    except NoResultFound:
        return abort(400)

    if not job.filename_executable:
        return abort(409, 'executable file already exists')


@mod.route('/start', methods=['POST'])
@requires_runner_authentication
def job_start():
    """
    Runner confirms job has stopped
    """
    runner_id = request.authorization.username
    try:
        job = Jobs.query.filter(and_(Jobs.runner == runner_id, Jobs.status == JobStatus.RUNNING)).one()
        job.status = JobStatus.RUNNING
        db.session.commit()
        return '', 204
    except NoResultFound:
        return abort(404)


@mod.route('/stop', methods=['POST'])
@requires_runner_authentication
def job_stop():
    """
    Runner confirms job is about to start
    """
    runner = Runners.query.filter(id=request.authorization.username).one()
    try:
        job = Jobs.query.filter(and_(Jobs.runner == runner.id, Jobs.status == JobStatus.QUEUED)).one()
        if request.args.get('error') and request.args.get('error') == '1':
            job.status = JobStatus.ERROR
        else:
            job.status = JobStatus.FINISHED
        runner.release()
        db.session.commit()
        return '', 204
    except NoResultFound:
        return abort(404)


@mod.route('/log', methods=['PUT'])
@requires_runner_authentication
def job_upload_log():
    runner_id = request.authorization.username
    try:
        job = Jobs.query.filter(and_(Jobs.runner == runner_id, Jobs.status == JobStatus.RUNNING)).one()
    except NoResultFound:
        return abort(400)

    if job.filename_log:
        return abort(409, 'log file already exists')

    job.filename_log = token_urlsafe(32)
    size = request.content_length
    if size is None:
        return abort(400, 'log file is missing')
    if size is not None and size > 5000000:  # Size limit 5MB
        return abort(413, 'maximum log file size is 5MB')
    with open(os.path.join(FILE_STORAGE, job.filename_log), 'wb') as f:
        f.write(request.stream.read())

    db.session.commit()
    return '', 204


@mod.route('/other', methods=['PUT'])
@requires_runner_authentication
def job_upload_other():
    return abort(501)
