#!/bin/sh
# ex-33: --http2 forces curl's HTTP/2 code path even on a host it would
# otherwise negotiate down from -- the [HTTP/2] stream-negotiation lines
# and the space-suffixed "HTTP/2 200" status line are curl's own frame
# -level indicators that the exchange really ran over HTTP/2 (co-15)
curl -s -v --http2 https://example.com
