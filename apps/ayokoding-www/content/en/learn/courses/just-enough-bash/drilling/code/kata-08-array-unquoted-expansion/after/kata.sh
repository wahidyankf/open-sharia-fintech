#!/usr/bin/env bash
set -uo pipefail
# Kata 8 (FIXED): "${files[@]}" quoted preserves each array element as
# ONE word regardless of embedded spaces, matching the array's real length.
files=("report one.txt" "report-two.txt")
count=0
for f in "${files[@]}"; do
  count=$((count + 1))
  echo "element $count: '$f'"
done
echo "total elements seen: $count (array actually holds ${#files[@]})"
