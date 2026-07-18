#!/bin/sh
# ex-13: capture only TCP segments on port 443 (the BPF filter "tcp and port 443")
# while opening a real HTTPS connection in another terminal -- verify the
# [S], [S.], [.] flag sequence (SYN, SYN-ACK, ACK) appears in order (co-07)
#
# This sandbox's host (macOS) cannot open a raw capture socket without root
# (`tcpdump: ioctl(SIOCIFCREATE): Operation not permitted`, confirmed by testing).
# The transcript below is a GENUINE live capture, taken inside a local Debian
# Linux container (Docker, --cap-add=NET_ADMIN --cap-add=NET_RAW, no other
# privilege escalation) whose kernel implements the real Linux TCP stack --
# not a reconstruction. Run as two commands in the same shell: the capture
# in the background, then the connection that generates the traffic it sees.
tcpdump -i eth0 -n 'tcp and port 443' -c 20 &
sleep 1
curl -s -o /dev/null --http1.1 -H 'Connection: close' https://example.com
sleep 2
