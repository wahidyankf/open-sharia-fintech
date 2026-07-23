#!/bin/sh
# ex-10: traceroute sends probes with increasing TTL, one hop farther each
# round -- each router along the path replies once its TTL hits zero,
# producing a numbered hop list with a per-hop round-trip time (co-05)
traceroute -m 5 -w 1 example.com
