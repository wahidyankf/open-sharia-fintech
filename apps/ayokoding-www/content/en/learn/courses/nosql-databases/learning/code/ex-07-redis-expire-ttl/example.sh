#!/usr/bin/env bash
# Example 7: Redis EXPIRE and TTL.
# EXPIRE + TTL on a session key (co-24) -- verify the countdown, then the
# eventual miss once the key actually expires.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw SET session:auth "token-abc" # => creates the key with no expiry yet
redis-cli --no-raw EXPIRE session:auth 5        # => co-24: schedules the key to expire in 5 seconds
redis-cli --no-raw TTL session:auth             # => co-24: TTL reports seconds remaining until expiry
sleep 6                                         # => wait past the 5-second expiry
redis-cli --no-raw GET session:auth             # => the key should now be gone
redis-cli --no-raw TTL session:auth             # => co-24: TTL on a NEVER-EXISTED or EXPIRED key returns -2
