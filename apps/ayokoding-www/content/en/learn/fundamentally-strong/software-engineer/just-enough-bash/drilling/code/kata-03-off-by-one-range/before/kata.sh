#!/usr/bin/env bash
set -euo pipefail
# Kata 3 (BUGGY): meant to attempt a task up to 3 times (attempts 1, 2, 3),
# but the loop guard uses -lt instead of -le, so it only runs twice.
max_attempts=3
attempt=1
while [ "$attempt" -lt "$max_attempts" ]; do
  echo "attempt $attempt of $max_attempts"
  attempt=$((attempt + 1))
done
echo "loop ran $((attempt - 1)) time(s), expected $max_attempts"
