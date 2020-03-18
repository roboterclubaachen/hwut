# HWUT daemon

Webservice that executes STM32 Executables on real hardware (e.g. development boards) and returns the serial output.

## Status

The service on https://hwut.de/ is online.

Some functions may be missing or unstable, a lot of work is currently being done on this project.

### Demo

Then you can submit a file to be executed: `curl -T example.elf -X PUT "https://hwut.de/apiv1/jobs/submit?board=nucleo-f303re&duration_limit_seconds=5"`

## HTTP API (v1)

See [API documentation](docs/API.md)

## Concepts

### Board

A microcontroller is mounted on a board.
Additionally the board brings the programmer, an UART logger and optional a logic analyser.

A board may have extra peripherals connected via SPI, TWI, or similar.

## Architecture

HWUT consists of three components.

### HWUT Server
HWUT Server is the central component. It manages all test requests, configuration, permissions, payment, etc.

### HWUT Runner
HWUT Runner is responsible for executing the tests on the embedded hardware. An instance will run for every microcontroller and gets the test from the *HWUT server* via network.

### HWUT Client
A CLI client to communicate with the server. Not available yet, use `curl` instead.
