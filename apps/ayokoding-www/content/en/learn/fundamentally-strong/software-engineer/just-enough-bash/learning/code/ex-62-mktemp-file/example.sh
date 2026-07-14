#!/usr/bin/env bash
# Example 62: mktemp creates a unique temp file, trap cleans it up
set -euo pipefail # => same strict-mode header as every other example in this primer

tmp="$(mktemp)"          # => mktemp creates a unique, empty file and prints its path
trap 'rm -f "$tmp"' EXIT # => cleans up tmp on any exit path, so a failure never leaks scratch files
# => trap runs whether the rest of this script succeeds or fails -- cleanup is unconditional

echo "created: $([[ -f "$tmp" ]] && echo yes || echo no)"
# => the $() combines a test and its yes/no rendering into one line
# => Output: created: yes
if [[ "$(basename "$tmp")" =~ ^tmp\.[[:alnum:]]+$ ]]; then
  # => this pattern matches mktemp's default template on both macOS and Linux
  echo "basename matches mktemp's default tmp.XXXXXXXXXX template"
  # => Output: basename matches mktemp's default tmp.XXXXXXXXXX template
fi # => closes the if
