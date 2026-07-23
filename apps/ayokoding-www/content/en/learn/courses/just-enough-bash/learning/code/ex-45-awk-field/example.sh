#!/usr/bin/env bash
# Example 45: extracting a field with awk
set -euo pipefail

# two space-separated records: name, age, role
printf 'alice 30 engineer\nbob 25 designer\n' | awk '{print $2}' # => $2 is the 2nd whitespace-separated field on each line
# => Output: 30, then 25 -- the age field from each record
