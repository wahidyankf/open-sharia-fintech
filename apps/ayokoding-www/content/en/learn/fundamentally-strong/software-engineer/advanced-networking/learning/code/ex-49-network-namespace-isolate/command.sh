#!/bin/sh
# ex-49: ip netns add creates a new, isolated network-namespace stack; ip netns
# exec runs a command INSIDE that namespace instead of the host's default one
# -- its routing table starts genuinely empty, since nothing has configured
# any routes inside this brand-new namespace yet (co-21)
ip route
echo "--- create namespace 'demo' ---"
ip netns add demo
echo "--- namespace demo: routing table ---"
ip netns exec demo ip route
echo "--- namespace demo: loopback interface state ---"
ip netns exec demo ip link show dev lo
ip netns delete demo
