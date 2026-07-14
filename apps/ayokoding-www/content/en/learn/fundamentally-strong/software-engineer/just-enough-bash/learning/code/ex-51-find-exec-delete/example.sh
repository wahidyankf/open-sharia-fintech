#!/usr/bin/env bash
# Example 51: deleting files found by find
set -euo pipefail

mkdir -p tmp-dir                                         # => builds a small real directory to clean up
touch tmp-dir/keep.txt tmp-dir/old.tmp tmp-dir/cache.tmp # => one file to keep, two .tmp files to remove

find tmp-dir -name '*.tmp' -delete # => -delete removes every file find matches, in place

find tmp-dir -type f | sort # => lists what remains, to prove only the .tmp files are gone
# => Output: tmp-dir/keep.txt -- both old.tmp and cache.tmp were deleted
