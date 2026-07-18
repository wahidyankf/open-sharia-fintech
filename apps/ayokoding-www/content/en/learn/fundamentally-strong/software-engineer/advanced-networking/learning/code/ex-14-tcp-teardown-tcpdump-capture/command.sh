#!/bin/sh
# ex-14: this reuses Example 13's EXACT capture -- same command, same trace --
# examining the LAST few lines instead of the first three (co-07). The
# "-H 'Connection: close'" header is what makes the server close its side
# promptly, so a real FIN/ACK teardown appears in a single short capture
# instead of the connection sitting idle in ESTAB indefinitely.
tcpdump -i eth0 -n 'tcp and port 443' -c 20 &
sleep 1
curl -s -o /dev/null --http1.1 -H 'Connection: close' https://example.com
sleep 2
