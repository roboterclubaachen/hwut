# HWUT daemon

Webservice that executes STM32 Executables on real hardware (Nucleo Boards) and returns the serial output.

## Status

Work in progress.

## HTTP URLs (Endpoints)

`POST /execute/{target}`
*{target}* ist the target MCU, e.g. *STM32F429ZIT*.

`GET /targets`
List of supported targets.

## Daemon configuration

Configuration file:
```
# target,{Stlink hla_serial},{/dev/ttyXXXX}
```
