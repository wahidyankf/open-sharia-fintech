#!/usr/bin/env bash
set -euo pipefail
file="my notes.txt"
touch "$file"
if [ -f $file ]; then
  echo "found: $file"
else
  echo "not found (word-split bug)"
fi
rm -f "$file"
