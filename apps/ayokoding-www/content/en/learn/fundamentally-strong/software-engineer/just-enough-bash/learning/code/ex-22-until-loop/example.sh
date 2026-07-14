#!/usr/bin/env bash
# Example 22: Until Loop
n=0                      # => n starts at 0
until [[ $n -eq 3 ]]; do # => until runs its body while the condition is FALSE, stopping once true
  echo "$n"              # => Output: 0, then 1, then 2 -- printed BEFORE the increment below
  n=$((n + 1))           # => n becomes 1, then 2, then 3
done                     # => loop exits once n equals 3
