#!/usr/bin/env bash
# Example 21: While Loop
n=0                      # => n starts at 0
while [[ $n -lt 3 ]]; do # => condition re-checked before every pass, including the first
  n=$((n + 1))           # => n becomes 1, then 2, then 3
  echo "$n"              # => Output: 1, then 2, then 3, each on its own line
done                     # => loop exits once n reaches 3
