#!/usr/bin/env bash
# Example 1: Key-Value SET/GET.
# SET/GET a string key via redis-cli against Valkey/Redis (co-20) -- verify the
# value round-trips exactly, byte for byte, and that a missing key reads back nil.
# --no-raw forces the traditional typed formatting ((integer), (nil), quoted
# strings) even though this script runs non-interactively.
set -euo pipefail # => stop on the first failing command -- a broken round trip should fail loudly

redis-cli --no-raw SET session:42 "active" # => co-20: stores the string "active" under key session:42
redis-cli --no-raw GET session:42          # => co-20: reads the exact value just written
redis-cli --no-raw EXISTS session:42       # => co-20: a fast 1/0 membership check, cheaper than a full GET
redis-cli --no-raw GET session:99          # => session:99 was never SET
redis-cli --no-raw DEL session:42          # => co-20: removes the key and frees the memory it held
redis-cli --no-raw GET session:42          # => confirms the delete actually took effect
