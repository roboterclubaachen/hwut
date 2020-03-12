#!/usr/bin/env python3

import argparse
import subprocess
import time


class HwutRunnerStm32:
    def run_test(self):
        # Get test from server and confirm start
        # TODO
        executable_filename = 'nucleo-f411re.elf'
        time_limit_seconds = 60

        # Start timer
        # TODO

        # Start serial output log capture
        # TODO

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

        # Wait for timer to finish
        time.sleep(time_limit_seconds)

        # Upload logfile and mark job as finished
        # TODO

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--id', '-i', type=int, help='Id of the runner.', required=True)
        parser.add_argument('--token', '-t', type=str, help='Token of the runner.', required=True)
        parser.add_argument('--serial-device', '-s', type=str, help='Path of serial device.', required=True)
        parser.add_argument('--programmer-type', '-pt', type=str, help='Type of the programmer.', required=True)
        parser.add_argument('--programmer-id', '-pi', type=str, help='Unique id (serial number) of the programmer.', required=True)
        parser.add_argument('--openocd-target', '-ot', type=str, help='OpenOCD target for the microcontroller.', required=True)
        parser.add_argument('--base-url', '-b', type=str, help='Base URL of the HWUT server.', default='https://hwut.de/apiv1/')
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

    def main(self):
        while True:
            self.run_test()


if __name__ == "__main__":
    runner = HwutRunnerStm32()
    exit(runner.main())
