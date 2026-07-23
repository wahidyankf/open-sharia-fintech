#!/bin/sh
# ex-52: --compressed asks for a compressed reply AND transparently decompresses it
curl -v --compressed --http1.1 https://example.com 2>&1 1>/dev/null | grep -iE "accept-encoding|content-encoding"
