#!/usr/bin/env bash
# Example 17: If File Test
if [[ -f data.txt ]]; then # => -f tests that a path exists and is a regular file
  echo "exists"            # => taken because data.txt is colocated with this script
fi                         # => Output: exists
