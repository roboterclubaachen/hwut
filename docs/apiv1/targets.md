## Target API

### Board list
Get a list of all available boards.

    GET /targets/boards

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| extended | bool | Extended information. (optional, default: false) |

#### Example

    curl -X GET https://hwut.de/apiv1/targets/boards

#### Response
`200 OK`

```
[
	{
		"name": "nucleo-f303re",
		"microcontroller": "stm32f303re"
	},
	{...}
]
```

or if the extended parameter is set to true:

```
[
	{
		"name": "nucleo-f303re",
		"microcontroller": "stm32f303re",
		"manufacturer": "STMicroelectronics",
		"runners": [
			42,
			21
		]
	},
	{...}
]
```

### Board information
Information about the board.

    GET /targets/boards/{board}

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| extended | bool | Extended information. (optional, default: false) |

#### Example

    curl -X GET https://hwut.de/apiv1/targets/boards/nucleo-f303re

#### Response
`200 OK`

```
{
	"name": "nucleo-f303re",
	"microcontroller": "stm32f303re"
}
```

or if the extended parameter is set to true:

```
{
	"name": "nucleo-f303re",
	"microcontroller": "stm32f303re",
	"manufacturer": "STMicroelectronics",
	"runners": [
		42,
		21
	]
}
```

### Create a new board

    PUT /targets/boards/nucleo-f303re

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| microcontroller | string | The microcontroller embedded on the board. |
| manufacturer | string | Manufacturer of the board. (optional) |

#### Example

    curl -X PUT https://hwut.de/apiv1/targets/boards/nucleo-f303re?microcontroller=stm32f303re&manufacturer=STMicroelectronics

#### Response
`201 Created`

```
{
	"name": "nucleo-f303re",
	"microcontroller": "stm32f303re",
	"manufacturer": "STMicroelectronics",
	"runners": []
}
```


### Delete Board
Delete a board.

    DELETE /targets/boards/{board}

#### Example

    curl -X DELETE https://hwut.de/apiv1/targets/boards/nucleo-f303re

#### Response
`204 No Content`


### Microcontroller list
Get a list of all available microcontrollers.

    GET /targets/microcontrollers

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| extended | bool | Extended information. (optional, default: false) |

#### Example

    curl -X GET https://hwut.de/apiv1/targets/microcontrollers

#### Response
`200 OK`

```
[
	{
		"name": "nucleo-f303re"
	},
	{...}
]
```

or if the extended parameter is set to true:

```
[
	{
		"name": "stm32f303re",
		"manufacturer": "STMicroelectronics"
	},
	{...}
]
```

### Microcontroller information
Information about the microcontroller.

    GET /targets/microcontrollers/{microcontroller}

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| extended | bool | Extended information. (optional, default: false) |

#### Example

    curl -X GET https://hwut.de/apiv1/targets/microcontrollers/stm32f303re

#### Response
`200 OK`

```
{
	"name": "nucleo-f303re"
}
```

or if the extended parameter is set to true:

```
{
	"name": "stm32f303re",
	"manufacturer": "STMicroelectronics"
}
```

### Create a new microcontroller

    PUT /targets/microcontrollers/{microcontroller}

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| manufacturer | string | Manufacturer of the microcontroller. (optional) |

#### Example

    curl -X PUT https://hwut.de/apiv1/targets/microcontrollers/stm32f303re?manufacturer=STMicroelectronics

#### Response
`201 Created`

```
{
	"name": "stm32f303re",
	"manufacturer": "STMicroelectronics"
}
```


### Delete a microcontroller

    DELETE /targets/microcontrollers/{microcontroller}

#### Example

    curl -X DELETE https://hwut.de/apiv1/targets/microcontroller/stm32f303re

#### Response
`204 No Content`
