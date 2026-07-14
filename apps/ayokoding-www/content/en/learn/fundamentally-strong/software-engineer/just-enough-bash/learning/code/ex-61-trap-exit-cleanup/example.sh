#!/usr/bin/env bash
# Example 61: trap ... EXIT for cleanup
set -euo pipefail # => the strict-mode baseline every example in this primer builds on

tmp="./work.tmp"         # => a plain scratch file this script creates and must clean up
trap 'rm -f "$tmp"' EXIT # => registers a cleanup command that fires on ANY exit path, success or failure
# => registering trap right after naming tmp means even an early failure below still cleans up

echo "work" >"$tmp" # => simulates doing some work that leaves a scratch file behind
echo "exists during run: $([[ -e "$tmp" ]] && echo yes || echo no)"
# => Output: exists during run: yes
# => once this script exits -- success or failure -- the EXIT trap fires and removes $tmp automatically
