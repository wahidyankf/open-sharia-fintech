#!/usr/bin/env bash
# Example 40: here-string matching with grep
set -euo pipefail

text="the quick foo fox" # => the string to search, held in a variable

if grep -q foo <<<"$text"; then # => <<< feeds $text to grep's stdin as a single line, no temp file needed
  echo "matched"                # => runs because grep found "foo" inside $text
else                            # => runs only if grep found no match
  echo "no match"               # => not reached in this run
fi                              # => closes the if/else
# => Output: matched
