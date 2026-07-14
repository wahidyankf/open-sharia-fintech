#!/usr/bin/env bash
# Example 71: iterating over a Bash array
set -euo pipefail # => same strict-mode header as every other example in this primer

arr=(a b c) # => a three-element indexed array, indices 0, 1, 2
for item in "${arr[@]}"; do
  # => "${arr[@]}" expands each element as its own separate, correctly-quoted word
  # => without the quotes, an element containing spaces would incorrectly split into multiple words
  echo "$item" # => prints one element per line
done           # => closes the for-loop
# => Output: a, b, c -- each on its own line
