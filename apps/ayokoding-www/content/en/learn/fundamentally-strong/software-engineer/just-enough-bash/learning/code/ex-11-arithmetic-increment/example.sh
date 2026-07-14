#!/usr/bin/env bash
# Example 11: Arithmetic Increment
i=0                 # => i starts at 0
while ((i < 3)); do # => (( )) is an arithmetic-context conditional testing i < 3
  i=$((i + 1))      # => recomputes i as i + 1 using arithmetic expansion
done                # => loop exits once i reaches 3
echo "$i"           # => Output: 3
