#!/usr/bin/env bash
# Example 59: branching on a command's exit status
set -euo pipefail

printf 'apple\nbanana\ncherry\n' >fruits.txt # => builds a small real data file to search

if grep -q banana fruits.txt; then # => -q runs grep silently; `if` checks its exit status directly
  echo "found banana"              # => runs because grep found a match (exit status 0)
else                               # => runs only if grep found no match (exit status 1)
  echo "banana missing"            # => not reached in this run
fi                                 # => closes the if/else
# => Output: found banana
