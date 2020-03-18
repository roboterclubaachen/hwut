## Info API

### Version
Retrieve version information.

    GET /version

#### Example

    curl -X GET https://hwut.de/apiv1/version


#### Response
`200 OK`

```
{
  "git_branch": "develop",
  "git_hash": "4242424",
  "version": "0.0.1"
}
```

### Authentication test

    GET /auth_test

#### Example

    curl -X GET https://hwut.de/apiv1/auth_test


#### Response
`200 OK`

```
You're authenticated if you can read this.
```
