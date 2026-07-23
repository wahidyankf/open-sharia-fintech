#!/usr/bin/env bash
# Example 60: pipefail catches a failing first stage
set -uo pipefail # => deliberately omits -e here, so the script can inspect $? after a failing pipeline

grep quux /dev/null | wc -l # => grep finds no "quux" in empty input, so grep itself exits 1 (no match)
# => wc -l still succeeds (exit 0), printing the line count "0"
echo "pipeline exit status: $?" # => with pipefail ON, $? is grep's FAILING status (1), not wc -l's success (0)
