#!/usr/bin/env bash
# Example 70: a safe glob loop that skips cleanly when nothing matches
set -euo pipefail # => same strict-mode header as every other example in this primer

count=0              # => tracks how many real files the loop actually processed
for f in ./*.txt; do # => if NO .txt file exists, the glob expands to the literal string ./*.txt unchanged
  [[ -e "$f" ]] || continue
  # => this guard is essential: without it, "$f" would be treated as a real (nonexistent) filename
  # => "$f" here is either a genuine path, OR the literal, un-expanded glob pattern itself
  count=$((count + 1)) # => only reached for entries that genuinely exist on disk
  echo "found: $f"     # => announces each real match
done                   # => closes the for-loop
echo "total: $count"   # => 0 when no .txt files exist in this directory; N when they do
