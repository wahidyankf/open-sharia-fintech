#!/usr/bin/env bash
set -euo pipefail
# Kata 3 (FIXED): -le (less-than-or-equal) makes the loop run exactly
# max_attempts times, attempts 1 through 3 inclusive.
max_attempts=3
attempt=1
while [ "$attempt" -le "$max_attempts" ]; do
  echo "attempt $attempt of $max_attempts"
  attempt=$((attempt + 1))
done
echo "loop ran $((attempt - 1)) time(s), expected $max_attempts"
