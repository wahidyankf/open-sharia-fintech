#!/usr/bin/env bash
# Example 46: summing a column with awk
set -euo pipefail

# three numbers, one per line, to be totaled
printf '10\n20\n30\n' | awk '{sum += $1} END {print sum}' # => sum accumulates $1 per line; END{} prints it once, after all lines
# => Output: 60 -- 10 + 20 + 30
