#!/bin/sh
# ex-17: -v prints each captured packet's options list in full -- filtering
# to SYN packets only (tcp-syn flag set) isolates the two handshake segments
# that actually carry window-scale negotiation, so "wscale" is easy to find
# alongside "mss" and "sackOK" in the exact documented options order (co-08)
tcpdump -i eth0 -n -v 'tcp and port 443 and tcp[tcpflags] & (tcp-syn) != 0' -c 2 &
sleep 1
curl -s -o /dev/null --http1.1 https://example.com
sleep 1
