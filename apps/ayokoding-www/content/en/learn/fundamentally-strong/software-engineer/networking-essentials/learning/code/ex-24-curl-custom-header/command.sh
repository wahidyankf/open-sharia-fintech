#!/bin/sh
# ex-24: -H adds a header of your choosing, alongside curl's defaults
curl -H "X-Demo: 1" -v --http1.1 https://example.com 2>&1 1>/dev/null | grep "^>"
