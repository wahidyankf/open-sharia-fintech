#!/usr/bin/env bash
# Example 67: grep -E with the ^ start-of-line anchor
set -euo pipefail

printf 'ERROR: disk full\ninfo: ERROR count is 3\nERROR again\n' | grep -E '^ERROR'
# => ^ anchors the match to the START of the line, not to a substring anywhere within it
# => the middle line contains the substring ERROR too, but not at the start, so it is excluded
# => Output: "ERROR: disk full" then "ERROR again"
