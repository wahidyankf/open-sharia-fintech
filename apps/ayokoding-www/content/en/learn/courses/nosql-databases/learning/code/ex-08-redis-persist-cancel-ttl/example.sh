#!/usr/bin/env bash
# Example 8: Redis PERSIST Cancels TTL.
# PERSIST removes a key's expiry (co-24) -- verify TTL returns -1 (exists, no
# expiry) afterward, not -2 (does not exist) and not the original countdown.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw SET session:persist "token-xyz" EX 30 # => co-24: SET ... EX 30 sets the value AND a 30s expiry in one call
redis-cli --no-raw TTL session:persist                   # => confirms the expiry is active
redis-cli --no-raw PERSIST session:persist               # => co-24: PERSIST strips the expiry, the key becomes permanent again
redis-cli --no-raw TTL session:persist                   # => co-24: TTL on a key that exists with NO expiry returns exactly -1
redis-cli --no-raw GET session:persist                   # => the value itself is untouched by PERSIST -- only the expiry changed
