#!/usr/bin/env bash
# Example 76: a genuine unquoted-variable bug that shellcheck catches (SC2086)
set -euo pipefail # => same strict-mode header as every other example in this primer

file="not a real file.txt" # => a path that CONTAINS a space, so the bug below has a visible effect
rm $file                   # => BUG: $file is unquoted, so it word-splits on the space at expansion time
# => shellcheck flags this exact line with SC2086 -- the fix would be `rm "$file"`, deliberately NOT applied here
