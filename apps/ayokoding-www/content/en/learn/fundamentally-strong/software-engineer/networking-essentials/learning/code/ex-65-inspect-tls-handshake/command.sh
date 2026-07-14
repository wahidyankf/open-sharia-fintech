#!/bin/sh
# ex-65: grep just the TLS handshake lines out of curl's full verbose trace
curl -v https://example.com 2>&1 1>/dev/null | grep -iE "SSL connection|ALPN|subject:|issuer:"
