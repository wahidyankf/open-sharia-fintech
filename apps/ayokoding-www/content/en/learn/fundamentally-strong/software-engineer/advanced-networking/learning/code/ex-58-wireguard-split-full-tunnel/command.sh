#!/bin/sh
# ex-58: AllowedIPs = 0.0.0.0/0 asks wg-quick to route EVERYTHING through the
# tunnel -- which requires extra fwmark + policy-routing rules so the
# WireGuard handshake/keepalive UDP packets THEMSELVES don't try to route
# through the very tunnel they are establishing (a routing loop) (co-25)
wg-quick up wg0 # [Interface]/[Peer] config has AllowedIPs = 0.0.0.0/0
ip route
ip rule show
