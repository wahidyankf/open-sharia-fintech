#!/bin/sh
# ex-39: forcing HTTP/1.1 is REQUIRED here -- WebSockets' Upgrade mechanism is an
# HTTP/1.1-only feature (HTTP/2 and HTTP/3 use different, header/frame-based
# mechanisms for the same purpose). Sec-WebSocket-Key is a base64 client nonce;
# the server's Sec-WebSocket-Accept in the response proves it understood this
# was specifically a WebSocket upgrade request, not a generic Upgrade (co-17)
curl -s -v -i -N --http1.1 --max-time 5 \
	-H "Connection: Upgrade" \
	-H "Upgrade: websocket" \
	-H "Sec-WebSocket-Version: 13" \
	-H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
	https://echo.websocket.org/
