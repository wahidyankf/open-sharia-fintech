#!/bin/sh
# ex-66: -connect for the TCP target, -servername for TLS SNI
openssl s_client -connect example.com:443 -servername example.com </dev/null
