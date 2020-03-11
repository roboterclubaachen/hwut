import os
from secrets import token_urlsafe
from flask import Blueprint, jsonify, request, redirect, abort
from datetime import datetime

from hwut_server.decorators import requires_authentication, check_authentication
from hwut_server.models.jobs import Jobs, JobStatus
from hwut_server.models.targets import Microcontrollers, Boards
from hwut_server.database import db
from hwut_server.utils import FILE_STORAGE

mod = Blueprint('jobs', __name__, url_prefix='/jobs')


@mod.route('/submit', methods=['PUT'])
@requires_authentication
def submit():
    user = request.authorization.username

    duration_limit_seconds = 60
    if request.args.get('duration_limit_seconds'):
        duration_limit_seconds = request.args.get('duration_limit_seconds')
    if duration_limit_seconds > 300:
        return abort(413, 'maximum execution time is 300 seconds')

    # board argument is optional
    board = request.args.get('board')
    if board:
        try:
            Boards.query.filter(Boards.name == board).one()
        except:
            return abort(400, 'board in unknown')

    microcontroller = request.args.get('microcontroller')
    if microcontroller is None:
        return abort(400, 'microcontroller must be specified')
    else:
        try:
            Microcontrollers.query.filter(Microcontrollers.name == microcontroller).one()
        except:
            return abort(400, 'microcontroller in unknown')

    filename_executable = token_urlsafe(32)
    size = request.content_length
    if size is None or size < 500:  # minimum size 0.5kB
        return abort(400, 'executable file is missing or empty')
    if size is not None and size > 5000000:  # Size limit 5MB
        return abort(413, 'maximum executable file size is 5MB')
    with open(os.path.join(FILE_STORAGE, filename_executable), 'wb') as f:
        f.write(request.stream.read())

    try:
        job = Jobs(
            datetime.now(),
            JobStatus.WAITING,
            duration_limit_seconds,
            filename_executable,
            user,
            board,
            microcontroller,
        )
        if request.args.get('comment'):
            job.comment = request.args.get('comment')
        db.session.add(job)
        db.session.commit()
    except:
        return abort(500, 'unable to create runner')
    return redirect(mod.url_prefix + '/' + str(job.id), 201)


@mod.route('/<int:id>', methods=['GET'])
def get(id):
    job = Jobs.query.filter(Jobs.id == id).one()
    auth = request.authorization
    extended = (auth and ((check_authentication(auth.username, auth.password, superuser=True)) or (
                check_authentication(auth.username, auth.password) and auth.username == job.owner)))
    return jsonify(job.to_dict(extended))


@mod.route('/<int:id>', methods=['DELETE'])
@requires_authentication
def cancel(id):
    job = Jobs.query.filter(Jobs.id == id).one()
    auth = request.authorization
    if auth and (
            (check_authentication(auth.username, auth.password, superuser=True))
            or (check_authentication(auth.username, auth.password) and auth.username == job.owner)):
        if job.status == JobStatus.WAITING:
            job.status = JobStatus.CANCELED
            db.session.commit()
            return jsonify(job.to_dict(True)), 204
        else:
            return abort(400, 'Unable to cancel job. Current job status: {}'.format(job.status.name))
    else:
        return abort(401)


@mod.route('', methods=['GET'])
@requires_authentication
def list_jobs():
    auth = request.authorization
    if check_authentication(auth.username, auth.password, superuser=True):
        job_list = Jobs.query.all()
    else:
        job_list = Jobs.query.filter(Jobs.owner == auth.username).all()
    extended = False
    if request.args.get('extended') and request.args.get('extended') == '1':
        extended = True
    return jsonify([job.to_dict(extended) for job in job_list])
