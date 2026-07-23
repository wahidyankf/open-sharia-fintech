#!/usr/bin/env bash
set -euo pipefail
scratch_dir="$(mktemp -d)"
cd "$scratch_dir"
# Kata 6 (BUGGY): no .txt files exist in this empty scratch dir, but
# without a no-match guard the loop still "processes" the literal,
# unexpanded glob pattern itself as if it were a real filename.
for f in *.txt; do
  echo "processing: $f"
  wc -l "$f"
done
cd /
rm -rf "$scratch_dir"
