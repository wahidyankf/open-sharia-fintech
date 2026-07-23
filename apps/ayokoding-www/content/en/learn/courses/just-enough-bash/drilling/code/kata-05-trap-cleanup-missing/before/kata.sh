#!/usr/bin/env bash
set -euo pipefail
# Kata 5 (BUGGY): creates a scratch file but never registers a trap to
# clean it up, so a mid-script failure leaves it behind forever.
scratch="$(mktemp /tmp/kata5-scratch.XXXXXX)"
echo "working in $scratch"
echo "partial output" >"$scratch"

# Simulate a real failure partway through the script.
false
echo "this line never runs"
