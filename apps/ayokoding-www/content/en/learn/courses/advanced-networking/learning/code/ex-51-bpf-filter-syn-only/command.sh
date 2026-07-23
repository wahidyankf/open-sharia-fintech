#!/bin/sh
# ex-51: tcp[tcpflags] reads the TCP header's flags byte directly; & tcp-syn
# masks out everything except the SYN bit; != 0 keeps only packets where that
# bit is actually set -- isolating handshake-OPENING packets specifically,
# not SYN-ACKs replies from the other side of a DIFFERENT connection (co-22)
tcpdump -i eth0 -n 'tcp[tcpflags] & tcp-syn != 0' -c 2
