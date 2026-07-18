#!/bin/sh
# ex-01: --http1.1 forces the classic HTTP/1.1 request/response line format so the
# stage boundaries (DNS resolve, TCP connect, TLS handshake, HTTP request/response)
# are easy to point at one by one when mapping them to OSI/TCP-IP layers (co-01)
curl -s -v --http1.1 https://example.com
