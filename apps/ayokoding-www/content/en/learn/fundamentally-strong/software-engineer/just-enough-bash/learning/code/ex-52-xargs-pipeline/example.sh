#!/usr/bin/env bash
# Example 52: piping find results into xargs grep
set -euo pipefail

mkdir -p project                         # => builds a small real project directory to search
printf 'TODO: fix this\n' >project/a.txt # => a.txt contains a TODO marker
printf 'nothing here\n' >project/b.txt   # => b.txt has no TODO marker
printf 'TODO: refactor\n' >project/c.txt # => c.txt also contains a TODO marker

find project -name '*.txt' | sort | xargs grep -l TODO # => xargs turns the file list into grep's file arguments
# => -l prints only the NAMES of files containing a match
