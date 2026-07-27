#!/usr/bin/env bash
# Example 5: Redis Set Basics.
# SADD/SMEMBERS model a tag set (co-20) -- a set stores unique members with no
# ordering guarantee, and adding a duplicate is silently a no-op.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw DEL post:88:tags                           # => resets state -- this example is fully self-contained
redis-cli --no-raw SADD post:88:tags "python" "nosql" "redis" # => co-20: SADD adds 3 distinct members
redis-cli --no-raw SADD post:88:tags "python"                 # => co-20: re-adding an EXISTING member changes nothing
redis-cli --no-raw SMEMBERS post:88:tags                      # => co-20: SMEMBERS returns every member, order not guaranteed
redis-cli --no-raw SCARD post:88:tags                         # => co-20: SCARD is the set's cardinality (member count), O(1)
