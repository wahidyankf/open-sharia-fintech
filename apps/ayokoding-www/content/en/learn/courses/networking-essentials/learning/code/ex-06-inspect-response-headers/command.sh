#!/bin/sh
# ex-06: info.cern.ch returns a fixed Content-Length instead of chunked transfer
curl -v --http1.1 https://info.cern.ch 2>&1 1>/dev/null | grep -iE "^< content-type|^< content-length"
