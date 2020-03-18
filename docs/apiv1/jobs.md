## Jobs API

### Submit job

    PUT /jobs/submit

Executable (`*.bin`, `*.hex` or `*.elf` file) is the request body.

#### Parameters
| Name  | Type    | Description |
|-------|---------|-------------|
| duration_limit_seconds | int | Time limit for the job execution |
| board | string | Board to run the test on |
| comment | string | The comment can be used to assign a title or description to the job. (**optional**) |

#### Example

    curl -T example.elf -X PUT "https://hwut.de/apiv1/jobs/submit?board=nucleo-f303re&duration_limit_seconds=5"

#### Response
`201 Created`

Header `Location: /jobs/42`

Status and more information about the created job can be retrieved
from the url in the Location header field.

### Job information
Get number of tracks

    GET /job/{id}

#### Example

    curl -X GET "https://hwut.de/apiv1/jobs/42"

#### Response

`200 OK`

```
{
	"id": 42,
	"created": "2020-01-01 00:00:00.000000",
	"status": "RUNNING",
	"owner": "user"
}
```

or if the user is the owner of the job:

```
{
	"id": 42,
	"created": "2020-01-01 00:00:00.000000",
	"status": "RUNNING",
	"owner": "user",
	"comment": "Bla blubb comment",
	"duration_limit_seconds": 120,
	"filename_executable": "xs4IsRBCGs_RWCRUXgOZfs0e20aWFJLWecndiFBJG34",
	"filename_log": null,
	"filename_other": null,
	"board": "nucleo-f303re"
}
```

### Job information
Cancel a job

    DELETE /job/{id}

#### Example

    curl -X DELETE "https://hwut.de/apiv1/jobs/42"

#### Response

`204 No Content`

or

`400 Bad request - 'Unable to cancel job. Current job status: FINISHED'`
if the job cannot be cancel.


### Job status shortcut
Check if a job has finished

    GET /job/{id}/is_finished

#### Example

    curl -X GET "https://hwut.de/apiv1/jobs/42/is_finished"

#### Response

`204 No Content` if the job has finished

or

`404 Not found` if the job has not yet finished.


### Job list
Get list of jobs

    GET /jobs

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| limit | int | Number of jobs to include in the response (optional, default 50) |
| offset | int | Offset from the first job to include in the response (optional, default 0) |

Note: Parameters are not implemented yet.

#### Example

    curl -X GET "https://hwut.de/apiv1/jobs"

#### Response

`200 OK`

```
[
	{
		"id": 42,
		"created": "2020-01-01 00:00:00.000000",
		"status": "RUNNING",
		"owner": "user"
	},
	{...}
]
```

### Retrieve job logfile

    GET /job/{id}/log

#### Example

    curl -X GET "https://hwut.de/apiv1/jobs/42/log"

#### Response

`200 OK`
and the log file (MIME type 'text/plain') as response body.

`404 Not found` if the log is not available, e.g. is the job is not finished.

### COPY!!!!!!!!!!!!!!!!!!
Get number of tracks

    GET /track/num

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| user_track | array of ints | Description (optional) |


#### Example

    curl -X GET "https://hwut.de/apiv1/jobs/42"

#### Response

Status `200 OK`
