#!/bin/sh
# ex-04: reuse Example 2's exact command, grep the ONE line that matters here
curl -v --http1.1 https://example.com 2>&1 1>/dev/null | grep "^< HTTP"
