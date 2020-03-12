#!/usr/bin/env python3

import argparse
import datetime
import os
import requests
import sys
import secrets
import serial
import subprocess
import time

FILE_STORAGE = './file_storage'


class HwutRunnerStm32:
    def run_test(self):
        # Get test from server
        r = requests.get(self.runner_base_url + '/get', auth=self.auth)
        if r.status_code == 404:
            # Currently no job available -> try again in 10 seconds
            time.sleep(10)
            return True
        if r.status_code != 200:
            print('Error: unable to get job')
            return False
        json = r.json()
        if not ('id' in json and
                'executable_location' in json and
                'log_location' in json and
                'other_location' in json and
                'time_limit' in json and
                'baudrate' in json):
            print('Error: unable to get job. Response is incorrect: ', r.text)
            return False
        job_id = int(json['id'])
        executable_location = json['executable_location']
        log_location = json['log_location']
        other_location = json['other_location']
        baudrate = json['baudrate']
        time_limit = datetime.timedelta(seconds=int(json['time_limit']))

        # download executable file
        r = requests.get(executable_location, auth=self.auth)
        if r.status_code != 200:
            print('Error: unable to get executable')
            return False
        executable_filename = secrets.token_urlsafe(32)
        with open(os.path.join(FILE_STORAGE, executable_filename), 'wb') as f:
            f.write(r.content)

        print('starting job {}'.format(job_id))

        # confirm start
        r = requests.post(self.runner_base_url + '/start', auth=self.auth)
        if r.status_code != 204:
            # Report error
            print('Error: ', r.text, ', ', r.content)
            return False

        start_time = datetime.datetime.now()

        # Start serial output log capture
        self.serial_port.baudrate = baudrate
        self.serial_port.open()
        if not self.serial_port.is_open():
            # FIXME: abort test, report error to server
            print('Error: unable to open serial device')
            return False
        self.serial_port.reset_input_buffer()

        # Flash microcontroller
        # e.g. `openocd -f interface/stlink-v2-1.cfg -c "hla_serial 066BFF323637414257071840" -f target/stm32f4x.cfg \
        # -c "program nucleo-f411re.elf verify" -c "reset run" -c "shutdown"`
        openocd_stdout = subprocess.check_output([
            'openocd',
            '-f',
            'interface/{}.cfg'.format(self.programmer_type),
            '-c',
            '"hla_serial {}'.format(self.programmer_id),
            '-f',
            'target/{}.cfg'.format(self.openocd_target),
            '-c',
            'program {} verify'.format(executable_filename),
            '-c',
            'reset run',
            '-c',
            'shutdown',
        ])
        # FIXME: Output? Check return value? ...

        # Wait for timer to finish while reading serial data
        serial_data = ''
        while (datetime.datetime.now() - start_time) < time_limit:
            serial_data += self.serial_port.read_all()  # FIXME: There must be a better way...

        # Upload logfile
        r = requests.put(log_location, data=serial_data, auth=self.auth)
        if r.status_code != 204:
            # Report error
            print('Error: ', r.text, ', ', r.content)
            return False

        # mark job as finished
        r = requests.post(self.runner_base_url + '/stop', auth=self.auth)
        if r.status_code != 204:
            # Report error
            print('Error: ', r.text, ', ', r.content)
            return False

        # remove executable file
        os.remove(os.path.join(FILE_STORAGE, executable_filename))

        return True

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--id', '-i', type=int, help='Id of the runner.', required=True)
        parser.add_argument('--token', '-t', type=str, help='Token of the runner.', required=True)
        parser.add_argument('--serial-device', '-s', type=str, help='Path of serial device.', required=True)
        parser.add_argument('--programmer-type', '-pt', type=str, help='Type of the programmer.', required=True)
        parser.add_argument('--programmer-id', '-pi', type=str, help='Unique id (serial number) of the programmer.',
                            required=True)
        parser.add_argument('--openocd-target', '-ot', type=str, help='OpenOCD target for the microcontroller.',
                            required=True)
        parser.add_argument('--base-url', '-b', type=str, help='Base URL of the HWUT server.',
                            default='https://hwut.de/apiv1/')
        args = parser.parse_args()
        self.runner_id = str(args.id)
        self.runner_token = args.token
        self.runner_base_url = args.base_url
        self.serial_device_path = args.serial_device
        # FIXME: Get programmer type from server?!?
        self.programmer_type = args.programmer_type
        self.programmer_id = args.programmer_id
        # FIXME: Get microcontroller from server ?!?
        self.openocd_target = args.openocd_target

        self.serial_port = serial.Serial()
        self.serial_port.port = self.serial_device_path

        self.auth = (self.runner_id, self.runner_token)

    def main(self):
        while True:
            try:
                self.run_test()
            except:
                print('Error running test')
                print("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    runner = HwutRunnerStm32()
    exit(runner.main())
