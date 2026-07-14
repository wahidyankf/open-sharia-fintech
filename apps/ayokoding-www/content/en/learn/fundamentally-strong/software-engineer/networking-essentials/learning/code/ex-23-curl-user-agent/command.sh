#!/bin/sh
# ex-23: -A overrides the default "curl/<version>" User-Agent header
curl -A "myagent" -v --http1.1 https://example.com 2>&1 1>/dev/null | grep "^>"
