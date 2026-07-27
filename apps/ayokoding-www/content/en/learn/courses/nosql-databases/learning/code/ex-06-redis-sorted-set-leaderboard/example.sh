#!/usr/bin/env bash
# Example 6: Redis Sorted Set Leaderboard.
# ZADD/ZRANGE build a score leaderboard (co-20) -- a sorted set keeps every
# member ordered by its numeric score, so range reads come back pre-sorted.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw DEL leaderboard:weekly                                   # => resets state -- this example is fully self-contained
redis-cli --no-raw ZADD leaderboard:weekly 120 "alice" 95 "bob" 150 "carol" # => co-20: ZADD scores 3 members
redis-cli --no-raw ZRANGE leaderboard:weekly 0 -1 WITHSCORES                # => co-20: ZRANGE returns members LOW-to-HIGH score by default
redis-cli --no-raw ZREVRANGE leaderboard:weekly 0 0 WITHSCORES              # => co-20: ZREVRANGE 0 0 asks for just the TOP entry
redis-cli --no-raw ZSCORE leaderboard:weekly "alice"                        # => co-20: ZSCORE reads one member's score directly, O(1)
