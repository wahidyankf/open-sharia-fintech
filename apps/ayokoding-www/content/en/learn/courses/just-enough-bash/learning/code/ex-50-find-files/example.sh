#!/usr/bin/env bash
# Example 50: finding files by name
set -euo pipefail

mkdir -p sample-dir/sub                                      # => builds a small real directory tree to search
touch sample-dir/a.txt sample-dir/b.txt sample-dir/sub/c.txt # => three .txt files at two nesting depths
touch sample-dir/notes.md                                    # => one non-matching file, to prove find filters it out

find sample-dir -name '*.txt' | sort # => -name '*.txt' matches only .txt files, at any depth
# => sort makes the listing order deterministic
