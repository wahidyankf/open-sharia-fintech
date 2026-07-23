#!/bin/sh
# ex-48a: PUT -- typically means "replace this resource with this body"
# -X overrides curl's default method choice, which would otherwise be GET here
curl -s -X PUT https://postman-echo.com/put -d "a=1"

# ex-48b: DELETE -- typically means "remove this resource"
# no -d is supplied here -- DELETE conventionally identifies a resource by URL alone
curl -s -X DELETE https://postman-echo.com/delete
