from flask import Blueprint, jsonify, request
import subprocess
import tempfile
import os

mod = Blueprint('execute', __name__, url_prefix='/execute')


@mod.route('/<string:target>', methods=['POST'])
def execute(target):
    # Flash microcontroller
    tempdir = tempfile.mkdtemp()
    filename = os.path.join(tempdir, next(tempfile._get_candidate_names()))
    file = request.files['executable']
    file.save(filename)
    openocd_stdout = subprocess.check_output(
        ['openocd', '-f', 'data/openocd_stm32f4_discovery.cfg', '-c', 'modm_program ' + filename]).decode("utf-8")
    os.remove(filename)

    # Read serial output
    # TODO

    return jsonify({
        'target': target,
        'version': 0,
        'data': str(request.files),
        'openocd_stdout': openocd_stdout,
        'filename': filename,
        'serial_output': "",
    })
