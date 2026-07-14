#!/bin/sh
# ex-47: -H sets Content-Type explicitly; -d supplies the raw JSON body
# without -H, the server would have no reliable way to tell this body apart from form data
curl -s -H "Content-Type: application/json" -d '{"x":1}' https://postman-echo.com/post
