#!/usr/bin/env bash
# Example 35: consuming arguments with shift
set -euo pipefail

set -- alpha beta gamma # => three simulated arguments to consume one at a time

while [ "$#" -gt 0 ]; do # => loops while at least one positional parameter remains
  echo "processing: $1"  # => $1 always refers to the CURRENT first remaining argument
  shift                  # => drops $1 and renumbers the rest down by one ($2 becomes $1)
done                     # => closes the while-loop

echo "remaining: $#" # => all arguments have been shifted away, so $# is 0
# => Output: three "processing: ..." lines (alpha, beta, gamma), then "remaining: 0"
