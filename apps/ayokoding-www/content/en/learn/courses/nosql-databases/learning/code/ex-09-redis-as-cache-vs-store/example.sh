#!/usr/bin/env bash
# Example 9: Redis as Cache vs. Store.
# The SAME engine configured with persistence OFF (pure cache) vs. AOF ON
# (durable store), each followed by a simulated restart (co-21) -- verify the
# cache-only key is lost while the AOF-persisted key survives.
set -euo pipefail # => stop on the first failing command

# --- Cache configuration: persistence OFF, this instance never writes to disk ---
redis-cli --no-raw CONFIG SET save ""                  # => co-21: disables RDB snapshotting entirely -- pure in-memory cache mode
redis-cli --no-raw CONFIG SET appendonly no            # => co-21: disables AOF too -- nothing survives a restart
redis-cli --no-raw SET cache:page:home "rendered-html" # => a disposable, regenerable cache entry
redis-cli --no-raw GET cache:page:home                 # => present right now, in memory
# => a REAL process restart at this point (kill -9 the redis-server, or docker
# => restart) loses cache:page:home entirely: no RDB file, no AOF log to replay

# --- Store configuration: AOF persistence ON, every write is durably logged ---
redis-cli --no-raw CONFIG SET appendonly yes       # => co-21: every write command is now appended to disk before acking
redis-cli --no-raw SET store:user:1:balance "1000" # => a value that MUST survive a restart -- not disposable
redis-cli --no-raw GET store:user:1:balance        # => present now, AND backed by the append-only file on disk
# => a REAL process restart at this point replays the AOF log and restores
# => store:user:1:balance to exactly "1000" -- durable, unlike the cache-mode key above
