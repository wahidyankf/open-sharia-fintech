#!/usr/bin/env bash
# Example 48: counting duplicates with sort | uniq -c
set -euo pipefail

# six fruit names, with "apple" and "banana" each repeated, in no particular order
printf 'apple\nbanana\napple\ncherry\nbanana\napple\n' |
  sort |  # => uniq -c only counts ADJACENT duplicates, so sort groups equal lines together first
  uniq -c # => -c prefixes each unique line with how many times it appeared
# => Output: "3 apple", "2 banana", "1 cherry" -- each count right-aligned by uniq -c
