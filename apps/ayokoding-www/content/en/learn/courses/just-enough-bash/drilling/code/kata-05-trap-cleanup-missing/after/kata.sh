#!/usr/bin/env bash
set -euo pipefail
# Kata 5 (FIXED): trap 'rm -f "$scratch"' EXIT runs on ANY exit path --
# normal completion, explicit exit, or an uncaught failure -- so the
# scratch file is guaranteed to be cleaned up.
scratch="$(mktemp /tmp/kata5-scratch.XXXXXX)"
trap 'rm -f "$scratch"' EXIT
echo "working in $scratch"
echo "partial output" >"$scratch"

# Simulate the same real failure partway through the script.
false
echo "this line never runs"
