#!/usr/bin/env bash
# Example 64: trap ... INT handles SIGINT instead of dying silently
set -euo pipefail # => same strict-mode header as every other example in this primer

trap 'echo "interrupted"; exit 0' INT # => runs when the process receives SIGINT, then exits cleanly (status 0)
# => a trap set here, before any interruptible work begins, is what makes SIGINT catchable at all
echo "waiting..."              # => printed immediately, so a caller knows the trap is installed
sleep 2                        # => a real window for an external `kill -INT` to land during this sleep
echo "finished-without-signal" # => reached only if no SIGINT arrives during the sleep above
