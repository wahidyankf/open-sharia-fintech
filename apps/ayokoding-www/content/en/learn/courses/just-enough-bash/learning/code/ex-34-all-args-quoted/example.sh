#!/usr/bin/env bash
# Example 34: looping over all arguments with "$@"
set -euo pipefail

set -- "alpha beta" gamma # => two arguments: one contains a space, one does not

for arg in "$@"; do # => "$@" expands to each argument as its OWN word, spaces intact
  echo "$arg"       # => prints the argument exactly as it was passed
done                # => closes the for-loop
# => Output: "alpha beta" (kept as ONE line, space intact), then "gamma"
