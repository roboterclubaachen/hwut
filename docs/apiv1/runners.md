## Runner API

### Runner list
Retrieve version information.

    GET /runners/*
    GET /runners/by_board/{board}

#### Example

    curl -X GET https://hwut.de/apiv1/runners/by_board/nucleo-f303re

#### Response
`200 OK`

```
[
	{
		"id": 42,
		"enabled": true,
		"board": "nucleo-f303re"
	},
	{...}
]
```

or if the user owns the runner:

```
[
	{
		"id": 42,
		"token": "cI3lkAFM5KyREj1M78eeSbBeslAje-gRz2fWbe34a6U",
		"created": "2020-01-01 00:00:00.000000",
		"enabled": true,
		"last_seen": "2020-03-01 00:00:00.000000",
		"ping_counter": 421337,
		"job_counter": 1337,
		"busy": false,
		"board": "nucleo-f303re"
	},
	{...}
]
```

or an empty list if no runner is found.


### Runner information
Get information about the specified runner.

    GET /runners/{id}

#### Example

    curl -X GET https://hwut.de/apiv1/runners/42

#### Response
`200 OK`

```
{
	"id": 42,
	"enabled": true,
	"board": "nucleo-f303re"
}
```

or if the user owns the runner:

```
{
	"id": 42,
	"token": "cI3lkAFM5KyREj1M78eeSbBeslAje-gRz2fWbe34a6U",
	"created": "2020-01-01 00:00:00.000000",
	"enabled": true,
	"last_seen": "2020-03-01 00:00:00.000000",
	"ping_counter": 421337,
	"job_counter": 1337,
	"busy": false,
	"board": "nucleo-f303re"
}
```


### Create a new runner

    PUT /runners/add

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| board | string  | Board the runner is using |

#### Example

    curl -X PUT https://hwut.de/apiv1/runners/add?board=nucleo-f303re

#### Response
`200 Created`

Header: `Location: /runners/42`


### Delete a runner

    DELETE /runners/{id}

#### Example

    curl -X DELETE https://hwut.de/apiv1/runner/42

#### Response
`204 No Content`
