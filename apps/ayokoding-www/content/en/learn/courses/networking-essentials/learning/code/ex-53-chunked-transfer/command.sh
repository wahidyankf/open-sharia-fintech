#!/bin/sh
# ex-53: example.com's CDN streams its response chunked -- no Content-Length at all
curl -v --http1.1 https://example.com 2>&1 1>/dev/null | grep -i "transfer-encoding\|content-length"
