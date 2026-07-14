#!/bin/sh
# ex-05: same -v output, this time grepping the line curl SENT (the ">" prefix)
curl -v --http1.1 https://example.com 2>&1 1>/dev/null | grep "^> GET"
