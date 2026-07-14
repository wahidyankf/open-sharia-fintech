#!/usr/bin/env bash
set -uo pipefail
# Kata 8 (BUGGY): unquoted ${files[@]} word-splits each element on
# whitespace, so "report one.txt" becomes TWO loop iterations instead
# of one.
files=("report one.txt" "report-two.txt")
count=0
# Intentionally unquoted: this IS the kata's bug under test.
# shellcheck disable=SC2068
for f in ${files[@]}; do
  count=$((count + 1))
  echo "element $count: '$f'"
done
echo "total elements seen: $count (array actually holds ${#files[@]})"
