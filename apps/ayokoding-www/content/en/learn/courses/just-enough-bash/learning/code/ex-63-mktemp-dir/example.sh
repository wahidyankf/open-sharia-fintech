#!/usr/bin/env bash
# Example 63: mktemp -d creates a scratch directory, trap cleans it up
set -euo pipefail # => same strict-mode header as every other example in this primer

dir="$(mktemp -d)"        # => mktemp -d creates a unique, empty DIRECTORY and prints its path
trap 'rm -rf "$dir"' EXIT # => -rf is required here (not -f) since dir is a directory, not a plain file
# => registering trap immediately after mktemp -d means even an early failure below still cleans up

echo "created: $([[ -d "$dir" ]] && echo yes || echo no)"
# => Output: created: yes
echo "note" >"$dir/note.txt" # => writes a real file inside the scratch directory, to prove it is usable
echo "usable: $([[ -f "$dir/note.txt" ]] && echo yes || echo no)"
# => Output: usable: yes
# => on exit, trap -rf removes the WHOLE directory -- note.txt included -- in a single operation
