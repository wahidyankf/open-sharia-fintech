#!/usr/bin/env bash
# Example 41: piping printf into grep
set -euo pipefail

# printf writes four fruit lines; grep '^a' keeps only the lines that START with "a"
printf 'apple\nbanana\navocado\ncherry\n' | grep '^a' # => grep '^a' matches "apple" and "avocado", not "banana"/"cherry"
# => Output: apple, then avocado
