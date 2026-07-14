#!/usr/bin/env bash
# Example 32: checking a function's return status
set -euo pipefail

is_even() {               # => defines a function that reports even/odd via exit status
  local n="$1"            # => n is the number to check, scoped to this call
  if ((n % 2 == 0)); then # => arithmetic test: true when n has no remainder mod 2
    return 0              # => return 0 means "success" (n is even)
  else                    # => otherwise n is odd
    return 1              # => return 1 means "failure" (n is odd)
  fi                      # => closes the if/else
}                         # => closes the function

if is_even 3; then # => calling is_even inside `if` checks its return status directly
  echo "3 is even" # => this branch runs only if is_even returned 0
else               # => is_even returned non-zero (1), so the failure branch runs
  echo "3 is odd"  # => branch body confirming the failure path was taken
fi                 # => closes the if/else
# => Output: 3 is odd
