#!/bin/sh
# ex-08a: http:// with no port -- curl defaults to 80
curl -v --http1.1 http://example.com 2>&1 1>/dev/null | grep -E "Trying|Connected"

# ex-08b: https:// with no port -- curl defaults to 443
curl -v --http1.1 https://example.com 2>&1 1>/dev/null | grep -E "Trying|Connected"
