#!/bin/sh
# ex-27: the SAME query, issued twice a few seconds apart -- the ANSWER
# section's TTL column must be strictly lower on the second query, proving
# the resolver served the second answer from its own cache instead of
# re-asking example.com's authoritative servers (co-12)
dig example.com A
sleep 2
dig example.com A
