#!/bin/sh
# ex-50: host+port together narrow the capture to ONLY packets both to/from
# the named IP AND on port 443 -- everything else on the interface (other
# hosts, other ports) is filtered out at capture time, not just hidden from
# the printed output (co-22)
tcpdump -i eth0 -n 'host 172.66.147.243 and port 443' -c 4
