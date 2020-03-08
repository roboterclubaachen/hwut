# HWUT daemon

Webservice that executes STM32 Executables on real hardware (e.g. development boards) and returns the serial output.

## Status

Work in progress.

### Demo

First start the daemon: `./server/run.py`

Then you can submit a file to be executed: `curl -v -F 'executable=@/home/user/modm/build/stm32f4_discovery/blink/release/blink.elf' http://localhost:5000/apiv1/execute/stm32f407`

## HTTP API (v1)

`POST /apiv1/execute/{target}`
*{target}* ist the target MCU, e.g. *STM32F429ZIT*.

`GET /apiv1/targets`
List of supported targets.

## Daemon configuration

The configuration is stored in the SQL database and can be edited from the web interface: `/admin/configuration`.

## Concepts

### Target

A target is a microcontroller on a specific board that is available to run tests on.
Any target can be identified by the board name and microcontroller.
Boards may be available with different microcontrollers.

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
