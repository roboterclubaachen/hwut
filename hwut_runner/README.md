# HWUT runner

## Status

- [x] Runner for STM chips on ST-Link V2 Nucleo boards
- [ ] Runner for STM chips on other boards
- [ ] Runner for AVR chips
- [ ] Runner for LPC chips
- [ ] Startup script to start multiple runners

## Setup

### Programmer
#### ST-Link

For ST-Link V2 you discover the serial number using the following command:

```bash
$ lsusb -d 0483:374b -v 2>/dev/null | grep iSerial | egrep -o "[A-Z0-9]{24}"
0671FF303435554157122749
```

Put the serial number and the ST-Link version (e.g. `stlink-v2-1`) into the config file.


### Serial CDC device path

Connect a single board to your computer and detect the path of the serial device.
Usually you want a unique and persistent path like `/dev/serial/by-id/...`, but e.g. `/dev/ttyACM0` is also possible.

Example for *STMicroelectronics Nucleo* boards with integrated *STLinkV2.1* programmer:
```bash
$ lsusb -d 0483:374b -v 2>/dev/null | grep iSerial | egrep -o "[A-Z0-9]{24}" | xargs -I{} find /dev/serial/by-id/ -name "*{}*"
/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066CFF525254667867204032-if02
```

Put the path into the config file.

### Create runner

Create a runner on your server with the appropriate configuration.

```bash
$ curl -X PUT "https://hwut.de/apiv1/runners/add?board=nucleo-f303re&microcontroller=stm32f303re" --user user:password
Runner created. See /runners/42
$ # Get information about your newly created runner
$ curl -X GET "https://hwut.de/apiv1/runners/42" --user user:password
{
  "busy": false, 
  "created": "Thu, 12 Mar 2020 04:01:54 GMT", 
  "enabled": true, 
  "id": 15, 
  "job_counter": 0, 
  "last_seen": null, 
  "ping_counter": 0, 
  "token": "CTB2qbV6bspVOlfrCXUyNeAEopPCVJmv0R1yDdFz0vQ"
}
```

Notice the *id* (which is used as username) and *token*.
Put both into the config file.
Keep the token secret.
