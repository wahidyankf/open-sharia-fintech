#!/usr/bin/env bash
set -euo pipefail
scratch_dir="$(mktemp -d)"
cd "$scratch_dir"
# Kata 6 (FIXED): [[ -e "$f" ]] || continue skips the loop body when the
# glob matched nothing and bash left it as the literal, unexpanded pattern.
for f in *.txt; do
  [[ -e "$f" ]] || continue
  echo "processing: $f"
  wc -l "$f"
done
echo "no .txt files found -- loop body never ran, no error"
cd /
rm -rf "$scratch_dir"
