#!/usr/bin/env bash
# Example 4: Redis List Basics.
# LPUSH/RPUSH/LRANGE model a FIFO work queue (co-20) -- items pushed to the
# right and popped from the left preserve first-in-first-out order.
set -euo pipefail # => stop on the first failing command

redis-cli --no-raw DEL queue:jobs                           # => resets state -- this example is fully self-contained
redis-cli --no-raw RPUSH queue:jobs "job-1" "job-2" "job-3" # => co-20: RPUSH appends to the RIGHT end, preserving arrival order
redis-cli --no-raw LRANGE queue:jobs 0 -1                   # => co-20: LRANGE 0 -1 reads the WHOLE list, index -1 means "the last element"
redis-cli --no-raw LPOP queue:jobs                          # => co-20: LPOP removes and returns the LEFT (oldest) element -- FIFO consumption
redis-cli --no-raw LRANGE queue:jobs 0 -1                   # => confirms job-1 is gone, job-2/job-3 remain in order
