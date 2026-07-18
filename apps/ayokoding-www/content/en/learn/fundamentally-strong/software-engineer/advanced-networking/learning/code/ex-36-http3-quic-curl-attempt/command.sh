#!/bin/sh
# ex-36: --http3 forces QUIC and requires curl to have been built against an
# HTTP/3-capable backend (ngtcp2+nghttp3 against a QUIC-capable TLS library,
# or quiche) -- neither is compiled into this sandbox's curl 8.7.1 build
# (macOS system curl, linked against LibreSSL via SecureTransport), so this
# attempt genuinely fails at option-parsing time rather than negotiating
# HTTP/3 (co-16). See the prose below for what a successful negotiation
# would print on a curl build that DOES have HTTP/3 support.
curl --http3 -v https://example.com
