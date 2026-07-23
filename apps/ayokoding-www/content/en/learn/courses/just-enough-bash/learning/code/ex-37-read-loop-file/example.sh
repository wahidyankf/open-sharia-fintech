#!/usr/bin/env bash
# Example 37: reading a file line by line
set -euo pipefail

# names.txt (colocated in this directory) holds three names, one per line: alice, bob, carol
while IFS= read -r line; do # => IFS= keeps leading/trailing whitespace intact; -r keeps backslashes literal
  echo "line: $line"        # => prints each line exactly as it appears in the file
done <names.txt             # => redirects names.txt as the loop's stdin, one read per iteration
# => Output: "line: alice", "line: bob", "line: carol"
