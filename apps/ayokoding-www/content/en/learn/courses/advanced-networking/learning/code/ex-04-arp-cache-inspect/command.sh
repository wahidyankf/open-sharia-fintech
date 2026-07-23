#!/bin/sh
# ex-04: ip neigh show prints the kernel's ARP cache -- one IP-to-MAC entry
# per local host this machine has already resolved via ARP (co-02). Ping
# the default gateway first so it has a fresh entry to show.
ping -c 1 "$(ip route | awk '/default/ {print $3; exit}')" >/dev/null
ip neigh show
