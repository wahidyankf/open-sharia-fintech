#!/usr/bin/env bash
# Example 3: Redis Hash Basics.
# HSET/HGETALL model a user record as a hash (co-20) -- a hash groups several
# named fields under one key, cheaper than one string key per field.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw DEL user:7                                             # => resets state -- this example is fully self-contained
redis-cli --no-raw HSET user:7 name "Grace" role "engineer" active "true" # => co-20: HSET writes 3 fields in one call
redis-cli --no-raw HGETALL user:7                                         # => co-20: HGETALL returns every field/value pair on the hash
redis-cli --no-raw HGET user:7 role                                       # => co-20: HGET reads a single named field, cheaper than HGETALL for one value
redis-cli --no-raw HDEL user:7 active                                     # => co-20: HDEL removes one field, leaving the rest of the hash intact
redis-cli --no-raw HGETALL user:7                                         # => confirms only the deleted field is gone
