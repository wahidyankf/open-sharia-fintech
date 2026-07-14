#!/bin/sh
# ex-46: -d implies POST and application/x-www-form-urlencoded encoding
# postman-echo.com is a public echo API -- its JSON reply proves what the server actually saw
curl -s -d "a=1&b=2" https://postman-echo.com/post
