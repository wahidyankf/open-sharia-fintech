#!/bin/sh
# ex-22: request a path that deliberately does not exist on this real host
curl -o /dev/null -s -w "%{http_code}\n" https://example.com/this-path-does-not-exist-xyz123
