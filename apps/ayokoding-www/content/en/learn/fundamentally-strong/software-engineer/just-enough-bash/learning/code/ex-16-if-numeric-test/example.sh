#!/usr/bin/env bash
# Example 16: If Numeric Test
n=20                     # => n holds the number 20
if [[ $n -gt 10 ]]; then # => -gt is the numeric "greater than" test inside [[ ]]
  echo "big"             # => taken because 20 is greater than 10
fi                       # => Output: big
